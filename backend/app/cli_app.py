import os
import sys
from .app import TodoApp
from ..models import Task

class CliApp:
    def __init__(self, todo_file: str = "todo_data.json"):
        """Initialize the application"""
        self.config = TodoApp(todo_file)
        self.running = True

# ======== menu methods ========    

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
        print("7️⃣  List completed tasks")
        print("8️⃣  List sections")
        print("9️⃣  Manage sections")
        print("0️⃣  Exit")
        print("=" * 50)
        
    def get_user_choice(self) -> str:
        """Get user's menu choice"""
        return input("Select option number: ").strip()
    
    def get_user_input(self, prompt: str, sec_prompt: str) -> str:
        """Get user's input"""
        user_input = ""
        while not user_input.strip():
            self.clear_screen()
            print(prompt)
            print("=" * 30)
            user_input = input(sec_prompt).strip()
        return user_input
    
    def pause(self):
        """Pause for user input"""
        input("\n📝 Press Enter to continue...")

    def list_sections(self):
        """Print all sections"""
        self.clear_screen()
        print("📂 Sections:")
        for section in self.config.model.sections:
            print(f"- {section.name} ({len(section.tasks)} tasks)")
        self.pause()

    def list_tasks(self):
        """List all tasks"""
        self.clear_screen()
        print("📋 All Tasks:")
        tasks = self.config.get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                status = "✅ Completed" if task.completed else "❌ Pending"
                print(f"- {task.title} ({status})")
        self.pause()
    
    def select_section(self) -> str:
        """Select a section by name"""
        self.clear_screen()
        print("📂 Select Section: ")
        for i, section in enumerate(self.config.model.sections, start=1):
            print(f"{i}. {section.name}")
            
        section_choice = input("Enter section number (or 'n' for new section | default: General): ").strip()

        if section_choice.lower() == 'n':
            section_name = self.get_user_input("➕ Create New Section", "Enter a name for the new section:")
            self.config.create_section(section_name)
            return section_name
        elif section_choice.isdigit() and 1 <= int(section_choice) <= len(self.config.model.sections):
            return self.config.model.sections[int(section_choice) - 1].name
        else:
            return "General"
        
    def list_tasks_by_section(self):
        """List tasks by section"""
        self.clear_screen()
        section_name = self.select_section()
        section = self.config.get_section_by_name(section_name)
        
        if not section:
            print(f"No tasks found in section '{section_name}'.")
            self.pause()
            return
        
        print(f"📂 Tasks in Section: {section.name}")
        for task in section.tasks:
            status = "✅ Completed" if task.completed else "❌ Pending"
            print(f"- {task.title} ({status})")
        self.pause()
            
    def list_completed_tasks(self):
        """List completed tasks"""
        self.clear_screen()
        print("✅ Completed Tasks:")
        tasks = self.config.get_completed_tasks()
        if not tasks:
            print("No completed tasks found.")
        else:
            for task in tasks:
                print(f"- {task.title}")
        self.pause()
    
        
# ======== main application methods ========

    def run(self):
        """Run the main application loop"""
        while self.running:
            self.clear_screen()
            self.show_menu()
            
            choice = self.get_user_choice()
            
            match choice:
                case '1':
                    self.add_task_to_section()
                case '2':
                    self.list_tasks()
                case '3':
                    self.list_tasks_by_section()
                case '4':
                    self.mark_task_complete()
                case '5':
                    self.mark_task_incomplete()
                case '6':
                    self.delete_task()
                case '7':
                    self.list_completed_tasks()
                case '8':
                    self.list_sections()
                case '9':
                    self.manage_sections()
                case '0':
                    self.running = False
    
    def add_task_to_section(self):
        """Add a new task to a section"""
        section_name = self.select_section()
        
        title = self.get_user_input("➕ Create New Task", "Enter task title:")
        description = input("Enter task description (optional): ").strip()

        task = Task(title=title, description=description)
        self.config.add_task_to_section(task, section_name)
        print(f"Task '{task.title}' added successfully!")
        self.pause()
    
    def mark_task_complete(self):
        """Mark a task as complete"""
        task_id = input("Enter task ID to mark as complete: ").strip()
        task = self.config.get_task(task_id)
        
        if not task:
            print(f"Task with ID {task_id} not found.")
            self.pause()
            return
        
        task.complete()
        self.config.save_to_file()
        print(f"Task '{task.title}' marked as complete.")
        self.pause()
        
    def mark_task_incomplete(self):
        """Mark a task as incomplete"""
        task_id = input("Enter task ID to mark as complete: ").strip()
        task = self.config.get_task(task_id)
        
        if not task:
            print(f"Task with ID {task_id} not found.")
            self.pause()
            return
        
        task.incomplete()
        self.config.save_to_file()
        print(f"Task '{task.title}' marked as complete.")
        self.pause()
        
    def delete_task(self):
        """Delete a task by ID"""
        self.list_tasks()
        self.select_section
        task_id = input("Enter task ID to delete: ").strip()
        
        if not self.config.remove_task_by_id(task_id):
            print(f"Task with ID {task_id} not found.")
        else:
            print(f"Task with ID {task_id} deleted successfully.")
        self.pause()

    def manage_sections(self):
        """Manage sections"""
        self.clear_screen()
        print("📁 Manage Sections")
        print("=" * 20)
        print("1️⃣  Add new section")
        print("2️⃣  Delete section")
        print("0️⃣  Exit")
        print("=" * 20)
        
        choice = input("Select option: ").strip()
        self.list_sections()
        
        if choice == '1':
            section_name = self.get_user_input("➕ Create New Section", "Enter a name for the new section:")
            self.config.create_section(section_name)
            
        elif choice == '2':
            section_name = self.get_user_input("❌ Delete Section", "Enter the name of the section to delete:")
            self.config.remove_section_by_name(section_name)
            
        
        self.pause()
    
if __name__ == "__main__":
    app = CliApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting application...")
        sys.exit(0)