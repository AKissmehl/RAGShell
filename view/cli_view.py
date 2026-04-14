import sys
import termios
import tty

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text


class CLIView:
    """View: Responsible for user interaction and output."""

    def __init__(self):
        self.console = Console()
        self.FIRST = True

    def _clear_screen(self):
        self.console.clear()

    def _get_key(self):
        """Get a single key press from terminal."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Handle arrow keys
            if ch == '\x1b':
                ch = ch + sys.stdin.read(2)
                if ch == '\x1b[A':
                    return 'UP'
                if ch == '\x1b[B':
                    return 'DOWN'
            elif ch == '\r' or ch == '\n':
                return 'ENTER'
            elif ch == 'q':
                return 'q'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _arrow_menu(self, options, title):
        """Show an interactive menu with arrow key navigation."""
        selected = 0
        while True:
            self._clear_screen()
            
            # Show title
            title_text = Text(title, style="bold cyan", justify="center")
            self.console.print(Panel(title_text, box=ROUNDED, border_style="cyan"))
            
            # Show options with selection indicator
            menu_items = []
            for i, option in enumerate(options):
                if i == selected:
                    menu_items.append(f"> [green]{option}[/green]")
                else:
                    menu_items.append(f"  {option}")
            
            menu_text = "\n".join(menu_items)
            self.console.print(Panel(menu_text, title="[bold]Main Menu[/bold]", border_style="green"))
            
            # Show instructions
            self.console.print("[italic]Use arrow keys to navigate, Enter to select, q to exit[/italic]")
            
            # Get key
            key = self._get_key()
            
            # Handle navigation
            if key == 'UP':
                selected = selected - 1 if selected > 0 else len(options) - 1
            elif key == 'DOWN':
                selected = selected + 1 if selected < len(options) - 1 else 0
            elif key == 'ENTER':  # Enter
                return str(selected + 1)  # Return 1-based index
            elif key == 'q':  # Exit
                return 'q'
            elif key in ['1', '2', '3']:  # Direct number input
                return key

    def show_main_menu(self, show_welcome: bool = True) -> str:
        """Shows the main menu and returns the selection."""
        # Check if we can use arrow navigation (interactive terminal)
        if sys.stdin.isatty():
            try:
                if show_welcome:
                    self.show_success("Welcome to the Lab Chatbot!")
                
                options = ["Ask experiment questions", "RAG Setup", "Exit"]
                choice = self._arrow_menu(options, "RAGShell")
                
                # Map choice to our values
                if choice == "3":  # Exit
                    return "q"
                else:
                    return choice
            except Exception:
                # Fallback to prompt if arrow navigation fails
                pass
        
        # Fallback to original prompt
        self._clear_screen()
        if show_welcome:
            self.show_success("Welcome to the Lab Chatbot!")
            
        title = Text("Lab Chatbot v1.0", style="bold cyan", justify="center")
        self.console.print(Panel(title, box=ROUNDED, border_style="cyan"))
        
        menu_items = """
        [green]1.[/green] Ask experiment questions
        [green]2.[/green] RAG Setup
        [red]q.[/red] Exit
        """
        self.console.print(Panel(menu_items, title="[bold]Main Menu[/bold]", border_style="green"))
        return Prompt.ask("\n[bold]Please select an option[/bold]", default="1")

    def show_rag_interaction(self) -> str:
        """Shows the RAG interaction and returns the question."""
        if self.FIRST:
            self._clear_screen()
            title = Text("Experiment Questions", style="bold cyan", justify="center")
            self.console.print(Panel(title, box=ROUNDED, border_style="cyan"))

            instructions = "Ask your question (or 'back' for main menu, 'help' for tips)"
            self.console.print(Panel(instructions, title="[bold]Ask a Question[/bold]", border_style="blue"))
            self.FIRST = False
        
        # Show input box at bottom
        self.console.print("\n" + "="*80)
        return Prompt.ask("[bold blue]>>[/bold blue] ")

    def show_answer(self, answer: str):
        """Shows the answer (currently: dummy implementation)."""
        answer_panel = Panel(answer, 
                          title="[bold green]Answer[/bold green]", 
                          border_style="green",
                          expand=False)
        self.console.print(answer_panel)

    def show_rag_setup_menu(self) -> str:
        """Shows the RAG setup menu and returns the selection."""
        self._clear_screen()
        title = Text("RAG Setup Menu", style="bold blue", justify="center")
        self.console.print(Panel(title, box=ROUNDED, border_style="blue"))
        
        menu_items = """
        1. Configure System Prompt
        2. Load Documents to Vector DB
        3. View Current Configuration
        4. Quick LLM Download
        5. Back to main menu
        """
        self.console.print(Panel(menu_items, title="[bold blue]RAG Configuration[/bold blue]", border_style="blue"))
        return Prompt.ask("\n[bold blue]Select an option[/bold blue]", default="5")

    def show_llm_provider_menu(self) -> str:
        """Shows LLM provider selection menu and returns the choice."""
        # This method is no longer used - download happens automatically in _switch_llm_provider
        return "1"

    def show_folder_selection_dialog(self, default_path: str) -> str:
        """Shows folder selection dialog and returns the selected path."""
        self._clear_screen()
        title = Text("Select Document Folder", style="bold blue", justify="center")
        self.console.print(Panel(title, box=ROUNDED, border_style="blue"))

        menu_items = f"""
        1. Use default folder: {default_path}
        2. Choose custom folder
        """
        self.console.print(Panel(menu_items, title="[bold blue]Folder Selection[/bold blue]", border_style="blue"))
        choice = Prompt.ask("\n[bold blue]Select an option[/bold blue]", default="1")

        if choice == "1":
            return default_path
        elif choice == "2":
            custom_path = Prompt.ask("[bold blue]Enter custom folder path[/bold blue]")
            return custom_path.strip()
        else:
            return default_path

    def show_error(self, message: str):
        """Shows an error message."""
        error_panel = Panel(f"Oh no. {message}",
                            title="[bold red]Error[/bold red]",
                            border_style="red",
                            style="red")
        self.console.print(error_panel)

    def show_success(self, message: str):
        """Shows a success message."""
        success_panel = Panel(f"✓ {message}",
                              title="[bold green]Success[/bold green]",
                              border_style="green",
                              style="green")
        self.console.print(success_panel)

    def get_password(self, prompt: str) -> str:
        self._clear_screen()
        title = Text("Authentication Required", style="bold red", justify="center")
        self.console.print(Panel(title, box=ROUNDED, border_style="red"))
        return Prompt.ask(prompt, password=True)
