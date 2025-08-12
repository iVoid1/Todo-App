#!/usr/bin/env python3
"""
Interactive TODO CLI Application
"""

import os
import sys
from typing import Optional
from data.config import Config
from classes import Task, Section


class TodoApp:
    def __init__(self, config_file: str = "todo_data.json"):
        """Initialize the application"""
        self.config = Config(config_file)
        self.running = True
    
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_menu(self):
        """Display the main menu"""
        print("=" * 50)
        print("🗒️  TODO Task Management System")
        print("=" * 50)
        print("1️⃣  Add new task")
        print("2️⃣  List all tasks")
        print("3️⃣  List tasks by section")
        print("4️⃣  Mark task as complete")
        print("5️⃣  Mark task as incomplete")
        print("6️⃣  Delete task")
        print("7️⃣  Add subtask")
        print("8️⃣  Search tasks")
        print("9️⃣  Show statistics")
        print("🔟 Manage sections")
        print("0️⃣  Exit")
        print("=" * 50)
    
    def get_user_choice(self) -> str:
        """Get user's menu choice"""
        return input("Select option number: ").strip()
    
    def pause(self):
        """Pause for user input"""
        input("\n📝 Press Enter to continue...")
    
    def run(self):
        """Run the main application loop"""
        while self.running:
            self.clear_screen()
            self.show_menu()
            
            choice = self.get_user_choice()
            
            if choice == '1':
                self.add_task_interactive()
            elif choice == '2':
                self.list_all_tasks()
            elif choice == '3':
                self.list_section_tasks()
            elif choice == '4':
                self.complete_task_interactive()
            elif choice == '5':
                self.incomplete_task_interactive()
            elif choice == '6':
                self.delete_task_interactive()
            elif choice == '7':
                self.add_subtask_interactive()
            elif choice == '8':
                self.search_tasks_interactive()
            elif choice == '9':
                self.show_status()
            elif choice == '10':
                self.manage_sections()
            elif choice == '0':
                self.exit_app()
            else:
                print("❌ Invalid choice!")
                self.pause()
    
    def add_task_interactive(self):
        """Add a new task interactively"""
        self.clear_screen()
        print("➕ Add New Task")
        print("=" * 30)
        
        title = input("📝 Task title: ").strip()
        if not title:
            print("❌ Task title is required!")
            self.pause()
            return
        
        description = input("📄 Task description (optional): ").strip()
        
        # Show existing sections
        sections = self.config.get_all_sections()
        if sections:
            print("\n📁 Available sections:")
            for i, section in enumerate(sections, 1):
                print(f"   {i}. {section.name}")
            print(f"   {len(sections) + 1}. Create new section")
        
        section_name = input("📂 Section name (default: General Tasks): ").strip()
        if not section_name:
            section_name = "General Tasks"
        
        # Add the task
        task = self.config.create_task(title, description)
        success = self.config.add_task_to_section(task, section_name)
        
        if success:
            print(f"\n✅ Task '{title}' added successfully!")
            print(f"   ID: {task.id}")
            print(f"   Section: {section_name}")
        else:
            print(f"\n❌ Failed to add task!")
        
        self.pause()
    
    def list_all_tasks(self):
        """List all tasks"""
        self.clear_screen()
        print("📋 All Tasks")
        print("=" * 30)
        
        tasks = self.config.get_all_tasks()
        
        if not tasks:
            print("📭 No tasks available")
            self.pause()
            return
        
        # Group tasks by sections
        sections = self.config.get_all_sections()
        
        for section in sections:
            print(f"\n📁 Section: {section.name}")
            print("-" * 25)
            for task in section.tasks:
                self.print_task_details(task)
        
        self.pause()
    
    def list_section_tasks(self):
        """List tasks from a specific section"""
        self.clear_screen()
        print("📂 List Section Tasks")
        print("=" * 30)
        
        sections = self.config.get_all_sections()
        
        if not sections:
            print("📭 No sections available")
            self.pause()
            return
        
        print("📁 Available sections:")
        for i, section in enumerate(sections, 1):
            task_count = len(section.tasks)
            completed_count = len(section.get_completed_tasks())
            print(f"   {i}. {section.name} ({completed_count}/{task_count})")
        
        try:
            choice = int(input("\nSelect section number: "))
            if 1 <= choice <= len(sections):
                selected_section = sections[choice - 1]
                
                print(f"\n📋 Tasks in section: {selected_section.name}")
                print("-" * 30)
                
                if not selected_section.tasks:
                    print("📭 No tasks in this section")
                else:
                    for task in selected_section.tasks:
                        self.print_task_details(task)
            else:
                print("❌ Invalid section number!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        self.pause()
    
    def _task_validation(self, task):
        return Task.model_validate(task)
    
    def print_task_details(self, task, indent: int = 0):
        """Print task details with formatting"""
        task = self._task_validation(task)
        prefix = "  " * indent
        status = "✅" if task.completed else "⏳"
        progress = f" ({task.progress()}%)" if task.subtasks else ""
        
        print(f"{prefix}{status} [{task.id}] {task.title}{progress}")
        
        if task.description:
            print(f"{prefix}   📝 {task.description}")
        
        if task.subtasks:
            for subtask in task.subtasks:
                self.print_task_details(subtask, indent + 1)
    
    def complete_task_interactive(self):
        """Mark task as complete interactively"""
        self.clear_screen()
        print("✅ Complete Task")
        print("=" * 20)
        
        # Show pending tasks
        pending_tasks = [t for t in self.config.get_all_tasks() if not t.completed]
        
        if not pending_tasks:
            print("🎉 All tasks are complete!")
            self.pause()
            return
        
        print("⏳ Pending tasks:")
        for i, task in enumerate(pending_tasks, 1):
            print(f"   {i}. [{task.id}] {task.title}")
        
        try:
            choice = int(input("\nSelect task number to complete: "))
            if 1 <= choice <= len(pending_tasks):
                selected_task = pending_tasks[choice - 1]
                selected_task.complete()
                self.config.save_to_file()
                print(f"\n✅ Task completed: {selected_task.title}")
            else:
                print("❌ Invalid task number!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        self.pause()
    
    def incomplete_task_interactive(self):
        """Mark task as incomplete interactively"""
        self.clear_screen()
        print("↩️ Mark Task as Incomplete")
        print("=" * 30)
        
        # Show completed tasks
        completed_tasks = [t for t in self.config.get_all_tasks() if t.completed]
        
        if not completed_tasks:
            print("📭 No completed tasks!")
            self.pause()
            return
        
        print("✅ Completed tasks:")
        for i, task in enumerate(completed_tasks, 1):
            print(f"   {i}. [{task.id}] {task.title}")
        
        try:
            choice = int(input("\nSelect task number to mark as incomplete: "))
            if 1 <= choice <= len(completed_tasks):
                selected_task = completed_tasks[choice - 1]
                selected_task.incomplete()
                self.config.save_to_file()
                print(f"\n⏳ Task marked as incomplete: {selected_task.title}")
            else:
                print("❌ Invalid task number!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        self.pause()
    
    def delete_task_interactive(self):
        """Delete task interactively"""
        self.clear_screen()
        print("🗑️ Delete Task")
        print("=" * 15)
        
        all_tasks = self.config.get_all_tasks()
        
        if not all_tasks:
            print("📭 No tasks to delete!")
            self.pause()
            return
        
        print("📋 All tasks:")
        for i, task in enumerate(all_tasks, 1):
            status = "✅" if task.completed else "⏳"
            print(f"   {i}. {status} [{task.id}] {task.title}")
        
        try:
            choice = int(input("\nSelect task number to delete: "))
            if 1 <= choice <= len(all_tasks):
                selected_task = all_tasks[choice - 1]
                
                confirm = input(f"⚠️ Are you sure you want to delete '{selected_task.title}'? (yes/no): ")
                if confirm.lower() in ['yes', 'y']:
                    # Find section and remove task
                    for section in self.config.get_all_sections():
                        if selected_task in section.tasks:
                            self.config.remove_task_by_id(selected_task.id)
                            
                            print(f"\n🗑️ Task deleted: {selected_task.title}")
                            break
                else:
                    print("❌ Deletion cancelled")
            else:
                print("❌ Invalid task number!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        self.pause()
    
    def add_subtask_interactive(self):
        """Add subtask interactively"""
        self.clear_screen()
        print("➕ Add Subtask")
        print("=" * 25)
        
        all_tasks = self.config.get_all_tasks()
        
        if not all_tasks:
            print("📭 No tasks available to add subtasks to!")
            self.pause()
            return
        
        print("📋 Available tasks:")
        for i, task in enumerate(all_tasks, 1):
            status = "✅" if task.completed else "⏳"
            subtask_count = len(task.subtasks)
            print(f"   {i}. {status} [{task.id}] {task.title} ({subtask_count} subtasks)")
        
        try:
            choice = int(input("\nSelect parent task number: "))
            if 1 <= choice <= len(all_tasks):
                parent_task = all_tasks[choice - 1]
                
                title = input("📝 Subtask title: ").strip()
                if not title:
                    print("❌ Subtask title is required!")
                    self.pause()
                    return
                
                description = input("📄 Subtask description (optional): ").strip()
                
                subtask = self.config.create_task(title, description)
                parent_task.add_subtask(subtask)
                self.config.save_to_file()
                
                print(f"\n✅ Subtask '{title}' added to '{parent_task.title}'")
                print(f"   ID: {subtask.id}")
            else:
                print("❌ Invalid task number!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        self.pause()
    
    def search_tasks_interactive(self):
        """Search tasks interactively"""
        self.clear_screen()
        print("🔍 Search Tasks")
        print("=" * 25)
        
        search_term = input("Search term: ").strip()
        
        if not search_term:
            print("❌ Please enter a search term!")
            self.pause()
            return
        
        all_tasks = self.config.get_all_tasks()
        results = []
        
        for task in all_tasks:
            if (search_term.lower() in task.title.lower() or 
                search_term.lower() in task.description.lower()):
                results.append(task)
        
        if not results:
            print(f"🔍 No tasks found containing '{search_term}'")
        else:
            print(f"\n🔍 Search results ({len(results)} tasks):")
            print("-" * 30)
            for task in results:
                self.print_task_details(task)
        
        self.pause()
    
    def show_status(self):
        """Show task statistics"""
        self.clear_screen()
        print("📊 Task Statistics")
        print("=" * 25)
        
        all_tasks = self.config.get_all_tasks()
        completed_tasks = self.config.get_completed_tasks()
        sections = self.config.get_all_sections()
        
        total = len(all_tasks)
        completed = len(completed_tasks)
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        print(f"📈 Overall Statistics:")
        print(f"   Total tasks: {total}")
        print(f"   Completed tasks: {completed}")
        print(f"   Pending tasks: {pending}")
        print(f"   Completion rate: {completion_rate:.1f}%")
        print(f"   Number of sections: {len(sections)}")
        
        if sections:
            print(f"\n📁 Section Details:")
            for section in sections:
                section_completed = len(section.get_completed_tasks())
                section_total = len(section.tasks)
                section_rate = (section_completed / section_total * 100) if section_total > 0 else 0
                print(f"   • {section.name}: {section_completed}/{section_total} ({section_rate:.1f}%)")
        
        self.pause()
    
    def manage_sections(self):
        """Manage sections"""
        self.clear_screen()
        print("📁 Manage Sections")
        print("=" * 20)
        
        sections = self.config.get_all_sections()
        
        print("📂 Current sections:")
        if not sections:
            print("   📭 No sections available")
        else:
            for i, section in enumerate(sections, 1):
                task_count = len(section.tasks)
                print(f"   {i}. {section.name} ({task_count} tasks)")
        
        print("\n1. Create new section")
        print("2. Delete section")
        print("0. Exit")
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            section_name = input("📝 New section name: ").strip()
            if section_name:
                if section_name not in [s.name for s in sections]:
                    new_section = self.config.create_section(section_name)
                    print(f"✅ Section '{section_name}' created successfully!")
                else:
                    print(f"❌ Section '{section_name}' already exists!")
            else:
                print("❌ Section name is required!")
            
            self.pause()
        
        elif choice == '2':
            if not sections:
                print("📭 No sections available to delete")
                self.pause()
                return
            
            section_name = input("📝 Section name to delete: ").strip()
            if section_name in [s.name for s in sections]:
                confirm = input(f"⚠️ Are you sure you want to delete section '{section_name}'? (yes/no): ")
                if confirm.lower() in ['yes', 'y']:
                    section_to_delete = next(s for s in sections if s.name == section_name)
                    self.config.remove_section_by_name(section_to_delete.name)
                    print(f"✅ Section '{section_name}' deleted successfully!")
                else:
                    print("❌ Deletion cancelled")
            else:
                print(f"❌ Section '{section_name}' does not exist!")
            
            self.pause()
            
    def exit_app(self):
        """Exit the application"""
        self.clear_screen()
        print("👋 Thank you for using TODO Task Manager!")
        print("🎯 All your data has been saved successfully")
        self.running = False


def main():
    """Application entry point"""
    try:
        app = TodoApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()