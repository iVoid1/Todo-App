import os
import sys
from typing import Sequence
from rich import print as rprint
import builtins

# Global Hijack
builtins.print = rprint

from todo.todo import Todo
from todo.todo import TaskModel

class CliApp:
    def __init__(self, todo_file: str = "todo_data.json"):
        self.todo = Todo(todo_file)
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self, title: str):
        self.clear_screen()
        print("=" * 50)
        print(f"✨ {title.center(46)} ✨")
        print("=" * 50)

    def pause(self):
        input("\n📝 Press [Enter] to continue...")

    def display_tasks(self, tasks: Sequence[TaskModel], title="Tasks", indent=0):
        if indent == 0:
            self.header(title)
            if title in ["All Tasks", "Delete Task", "Mark as Complete", "Mark as Incomplete", "Select Parent Task"]:
                tasks = self.todo.get_root_tasks

        if not tasks and indent == 0:
            print("📭 Nothing to show here.")
            return

        for task in tasks:
            status = "✅" if task.completed else "❌"
            spacing = "    " * indent
            prefix = "📝" if indent == 0 else "└──"
            short_id = f"[cyan]{task.title}[/cyan]"
            
            print(f"{spacing}{prefix} {short_id} {status}")
            
            if task.description:
                desc_pfx = "     " + ("    " * indent)
                print(f"{desc_pfx}[dim]└─ {task.description}[/dim]")

            if indent == 0 and task.subtasks:
                self.display_tasks(task.subtasks, title=title, indent=indent + 1)
        
    def list_tasks_by_section_flow(self):
        section_name = self.select_section_flow()
        section = self.todo.get_section(section_name)
        if section:
            self.display_tasks(section.tasks, title=f"Section: {section.name}")
        else:
            print(f"[red]⚠️ Section '{section_name}' not found![/red]")
        self.pause()

    def add_task_flow(self):
        self.header("Add New Task")
        section_name = self.select_section_flow()
        title = input("Task Title: ").strip()
        desc = input("Description (optional): ").strip()
        if title:
            self.todo.create_task(title, section_name, desc)
            print(f"\n[green]✅ Added to '{section_name}'![/green]")
        self.pause()

    def add_subtask_flow(self):
        self.header("Add Subtask")
        self.display_tasks(self.todo.get_root_tasks, "Select Parent Task")
        parent_id = input("\nEnter Parent Task ID (first 4 chars): ").strip()
        parent_task = self.todo.get_task(parent_id)
        
        if not parent_task:
            print("[red]❌ Parent Task not found.[/red]")
            self.pause()
            return

        print(f"\nAdding subtask to: [bold]{parent_task.title}[/bold]")
        title = input("Subtask Title: ").strip()
        desc = input("Description (optional): ").strip()

        if title:
            self.todo.create_subtask(parent_id, title, desc)
            print("\n[green]✅ Subtask added successfully![/green]")
        self.pause()

    def select_section_flow(self) -> str:
        sections = self.todo.model.sections
        print("\nAvailable Sections:")
        for i, sec in enumerate(sections, 1):
            print(f"{i}. {sec.name}")
        
        choice = input("\nSelect number (or type new name): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            return sections[idx].name if 0 <= idx < len(sections) else "General"
        return choice if choice else "General"

    def mark_task_flow(self, complete=True):
        state = "Complete" if complete else "Incomplete"
        self.display_tasks(self.todo.get_root_tasks, f"Mark as {state}")
        tid = input(f"\nEnter Task ID to mark {state}: ").strip()
        task = self.todo.get_task(tid)
        if task:
            task.mark_task(complete)
            self.todo.save_to_file()
            print("[green]✅ Done![/green]")
        else:
            print("[red]❌ Task not found.[/red]")
        self.pause()

    def delete_task_flow(self):
        self.display_tasks(self.todo.get_root_tasks, "Delete Task")
        tid = input("\nEnter task title to delete: ").strip()
        if self.todo.remove_task_by_title(tid):
            print("[yellow]🗑️ Deleted.[/yellow]")
        else:
            print("[red]❌ Not found.[/red]")
        self.pause()

    def manage_sections_flow(self):
        self.header("Manage Sections")
        print("1. Add Section\n2. List Sections\n3. Delete Section\n0. Back")
        choice = input("\nChoice: ").strip()

        if choice == '1':
            name = input("New Section Name: ").strip()
            if name: self.todo.create_section(name)

        elif choice == '2':
            sections = self.todo.model.sections
            print("\nAvailable Sections:")
            for i, sec in enumerate(sections, 1):
                print(f"{i}. {sec.name}")

        elif choice == '3':
            name = input("Section Name to Delete: ").strip()
            self.todo.remove_section_by_name(name)
            
        self.pause()

    def run(self):
        menu_options = {
            '1': self.add_task_flow,
            '2': lambda: self.display_tasks(self.todo.get_root_tasks, "All Tasks") or self.pause(),
            '3': self.list_tasks_by_section_flow,
            '4': lambda: self.mark_task_flow(True),
            '5': lambda: self.mark_task_flow(False),
            '6': self.delete_task_flow,
            '7': lambda: self.display_tasks(self.todo.get_completed_tasks, "Completed") or self.pause(),
            '8': self.manage_sections_flow,
            '9': self.add_subtask_flow,
            '0': sys.exit
        }

        while self.running:
            self.header("TODO MANAGEMENT SYSTEM")
            print("1. Add Task          2. List All          3. Filter by Section")
            print("4. Mark Done         5. Mark Undone       6. Delete Task")
            print("7. View Completed    8. Manage Sections   9. Add Subtask")
            print("0. Exit")
            print("=" * 50)
            choice = input("Option: ").strip()
            if choice in menu_options:
                menu_options[choice]()

if __name__ == "__main__":
    app = CliApp()
    app.run()