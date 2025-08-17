from app import CliApp, TodoApp

if __name__ == "__main__":    
    app = CliApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting application...")