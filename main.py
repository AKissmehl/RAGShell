from view.cli_view import CLIView
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import ROUNDED
import sys

class Controller:
    """Controller: Responsible for state management."""

    def __init__(self):
        self.view = CLIView()
        self.current_state = "main_menu"
        self.rag_setup_password = "admin123"
        self.first_time_main_menu = True
        self.system_prompt = "You are a helpful lab assistant. Provide concise, technical answers to laboratory questions."
        self.vector_db_loaded = False
        self.documents_loaded = 0

    def run(self):
        """Main loop of the program."""
        while True:
            if self.current_state == "main_menu":
                self._handle_main_menu()
            elif self.current_state == "rag_interaction":
                self._handle_rag_interaction()
            elif self.current_state == "rag_setup":
                self._handle_rag_setup()

    def _handle_main_menu(self):
        """Processes the main menu."""
        show_welcome = self.first_time_main_menu
        if self.first_time_main_menu:
            self.first_time_main_menu = False
        
        choice = self.view.show_main_menu(show_welcome=show_welcome)
        if choice == "1":
            self.current_state = "rag_interaction"
        elif choice == "2":
            self.current_state = "rag_setup"
        elif choice.lower() == "q":
            self.view.show_success("Chatbot exited.")
            sys.exit(0)

    def _handle_rag_interaction(self):
        """Processes the RAG interaction (currently: dummy)."""
        while True:
            question = self.view.show_rag_interaction()
            if question.lower() == "back":
                self.current_state = "main_menu"
                break
            elif question.lower() == "help":
                self.view.show_success("Tips: Formulate your question precisely, e.g., 'How do you calibrate a pH meter?'")
            else:
                # Dummy answer (can be replaced later by RAG component)
                dummy_answer = (
                    f"Here would be the answer to your question: '{question}'.\n"
                    "Currently, the RAG component is not yet implemented.\n"
                    "This view is already ready for integration!"
                )
                self.view.show_answer(dummy_answer)

    def _handle_rag_setup(self):
        """Processes the RAG setup menu."""
        choice = self.view.show_rag_setup_menu()
        if choice == "4":
            self.current_state = "main_menu"
        elif choice == "1":
            # Configure System Prompt
            self._configure_system_prompt()
        elif choice == "2":
            # Load Documents to Vector DB
            self._load_documents_to_vector_db()
        elif choice == "3":
            # View Current Configuration
            self._view_current_configuration()

    def _configure_system_prompt(self):
        """Configure the system prompt for RAG."""
        self.view._clear_screen()
        title = Text("System Prompt Configuration", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))
        
        current_prompt = self.system_prompt
        self.view.console.print("Current system prompt:")
        self.view.console.print(Panel(current_prompt, border_style="yellow"))
        
        new_prompt = Prompt.ask("\n[bold blue]Enter new system prompt[/bold blue] (or press Enter to keep current)")
        
        if new_prompt.strip():
            self.system_prompt = new_prompt
            self.view.show_success("System prompt updated successfully!")
        else:
            self.view.show_success("System prompt unchanged.")

    def _load_documents_to_vector_db(self):
        """Simulate loading documents to vector database."""
        self.view._clear_screen()
        title = Text("Load Documents to Vector DB", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))
        
        # Simulate document loading
        self.view.console.print("[italic]Simulating document loading...[/italic]")
        
        # This would be replaced with actual document loading logic
        # For now, we'll simulate loading some documents
        self.documents_loaded = 5  # Simulate loading 5 documents
        self.vector_db_loaded = True
        
        self.view.show_success(f"Successfully loaded {self.documents_loaded} documents to vector database!")
        self.view.show_success("Vector DB is now ready for RAG operations.")

    def _view_current_configuration(self):
        """View current RAG configuration."""
        self.view._clear_screen()
        title = Text("Current RAG Configuration", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))
        
        config_info = f"""
System Prompt:
{self.system_prompt}

Vector DB Status: {'Loaded' if self.vector_db_loaded else 'Not loaded'}
Documents Loaded: {self.documents_loaded}
        """
        self.view.console.print(Panel(config_info, title="[bold]Configuration Details[/bold]", border_style="green"))
        
        # Wait for user to press Enter
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    controller = Controller()
    controller.run()
