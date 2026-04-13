import os
import sys

from rich.box import ROUNDED
from rich.panel import Panel
from rich.text import Text

from rag.config import RAGConfig
from rag.document_processor import DocumentProcessor
from rag.llm_integration import LLMIntegration
from rag.rag_pipeline import RAGPipeline
from rag.vector_db import VectorDB
from view.cli_view import CLIView


class Controller:
    """Controller: Responsible for state management."""

    def __init__(self):
        self.view = CLIView()
        self.current_state = "main_menu"
        self.rag_setup_password = "admin123"
        self.first_time_main_menu = True
        self.system_prompt = "You are a helpful lab assistant. Provide answers to questions."
        self.vector_db_loaded = False
        self.documents_loaded = 0

        # Initialize RAG components
        self.config = RAGConfig()
        self.llm = None
        self.vector_db = None
        self.document_processor = None
        self.rag_pipeline = None
        self._initialize_rag_components()

    def _initialize_rag_components(self):
        """Initialize RAG components from configuration."""
        try:
            # Load configuration
            config = self.config.load_config()
            llm_config = config.get("llm", {})
            rag_config = config.get("rag", {})

            # Initialize LLM with proper error handling
            provider = llm_config.get("provider")
            model_path = llm_config.get("model_path", "")
            context_window = llm_config.get("context_window")
            
            # Get generation parameters from config
            generation_params = llm_config.get("generation_params", {})

            try:
                self.llm = LLMIntegration.create_llm(provider, model_path, context_window, generation_params)
                # Update configuration to reflect the actual provider being used
                llm_config['provider'] = provider
                self.config.update_config({"llm": llm_config})
                self.config.save_config(self.config.config)

            except ImportError as e:
                if "llama-cpp-python" in str(e):
                    self.view.show_error(f"Missing dependency: {str(e)}")
                    self.view.show_success("Attempting to install llama-cpp-python...")
                    try:
                        import subprocess
                        import sys
                        # Install llama-cpp-python
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", "llama-cpp-python"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        self.view.show_success("✓ llama-cpp-python installed successfully!")
                        # Try to create LLM again
                        self.llm = LLMIntegration.create_llm(provider, model_path, context_window, generation_params)
                    except Exception as install_error:
                        self.view.show_error(f"Failed to install llama-cpp-python: {str(install_error)}")
                        self.view.show_error("Please install llama-cpp-python manually and restart.")
                        raise
                else:
                    raise e

            except (FileNotFoundError, RuntimeError) as e:
                error_str = str(e).lower()
                if "tinyllama" in error_str or "gguf" in error_str or "ggml" in error_str or "model" in error_str:
                    self.view.show_error(f"Model file not found: {str(e)}")
                    self.view.show_success("Attempting to download the TinyLlama model...")
                    # Use our built-in download function
                    if self._download_model():
                        # Try to create LLM again after successful download
                        try:
                            self.llm = LLMIntegration.create_llm(provider, model_path, context_window, generation_params)
                        except Exception as retry_error:
                            self.view.show_error(f"Failed to load model after download: {str(retry_error)}")
                            self.view.show_error("Please check the model file and restart the application.")
                            raise
                    else:
                        self.view.show_error("❌ Model download failed")
                        self.view.show_error("Please check your internet connection and try again.")
                        raise
                else:
                    raise e

            except Exception as e:
                self.view.show_error(f"Failed to initialize LLM: {str(e)}")
                self.view.show_error("Please check your configuration and try again.")
                raise

            # Initialize document processor
            chunk_size = rag_config.get("chunk_size")
            chunk_overlap = rag_config.get("chunk_overlap")
            self.document_processor = DocumentProcessor(chunk_size, chunk_overlap)

            # Initialize vector database (but don't connect yet)
            persist_dir = rag_config.get("persist_directory")
            self.vector_db = VectorDB(persist_directory=persist_dir)

            # Initialize RAG pipeline (will be updated when vector DB is loaded)
            if self.llm and self.vector_db:
                self.rag_pipeline = RAGPipeline(self.vector_db, self.llm, self.system_prompt)

        except Exception as e:
            self.view.show_error(f"Failed to initialize RAG components: {str(e)}")

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
        """Processes the RAG interaction using the actual RAG pipeline."""
        if not self.rag_pipeline:
            self.view.show_error("RAG pipeline is not initialized. Please check configuration.")
            self.current_state = "main_menu"
            return

        while True:
            question = self.view.show_rag_interaction()
            if question.lower() == "back":
                self.current_state = "main_menu"
                break
            elif question.lower() == "help":
                self.view.show_success("Tips: Formulate your question precisely, e.g., 'How do you calibrate a pH meter?'")
            else:
                try:
                    # Use the actual RAG pipeline
                    answer = self.rag_pipeline.answer_question(question)
                    self.view.show_answer(answer)
                except Exception as e:
                    self.view.show_error(f"Failed to generate answer: {str(e)}")

    def _handle_rag_setup(self):
        """Processes the RAG setup menu."""
        choice = self.view.show_rag_setup_menu()
        if choice == "5":
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
        elif choice == "4":
            # Quick LLM Provider Switch
            self._switch_llm_provider()

    def _configure_system_prompt(self):
        """Configure the system prompt for RAG."""
        self.view._clear_screen()
        title = Text("System Prompt Configuration", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))

        current_prompt = self.system_prompt
        self.view.console.print("Current system prompt:")
        self.view.console.print(Panel(current_prompt, border_style="yellow"))

        # Use console.input instead of Prompt.ask to support multi-line input
        self.view.console.print("\n[bold blue]Enter new system prompt[/bold blue] (or press Enter to keep current)")
        self.view.console.print("(Press Enter twice on an empty line to finish)")
        
        # Read multiple lines until two consecutive empty lines
        lines = []
        while True:
            try:
                line = input(">> ")  # Use plain input for multi-line support
                if line == "":
                    # Check if this is the second consecutive empty line
                    if len(lines) > 0 and lines[-1] == "":
                        break
                lines.append(line)
            except KeyboardInterrupt:
                self.view.show_success("System prompt configuration cancelled.")
                return
        
        # Join lines and clean up
        new_prompt = "\n".join(lines).strip()

        if new_prompt:
            self.system_prompt = new_prompt
            self.view.show_success("System prompt updated successfully!")
        else:
            self.view.show_success("System prompt unchanged.")

    def _load_documents_to_vector_db(self):
        """Load documents to vector database."""
        self.view._clear_screen()
        title = Text("Load Documents to Vector DB", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))

        try:
            # Get folder selection from user
            default_path = self.config.get_rag_config().get("data_path")
            selected_folder = self.view.show_folder_selection_dialog(default_path)

            # Get all markdown files from the selected folder
            import os
            import glob

            if not os.path.exists(selected_folder):
                self.view.show_error(f"Folder does not exist: {selected_folder}")
                return

            # Find all markdown files in the folder
            file_paths = glob.glob(os.path.join(selected_folder, "*.md"))

            if not file_paths:
                self.view.show_error(f"No markdown files found in: {selected_folder}")
                return

            self.view.console.print(f"[italic]Found {len(file_paths)} markdown files in {selected_folder}[/italic]")

            # Process documents
            self.view.console.print("[italic]Processing documents...[/italic]")

            if not self.document_processor:
                self.document_processor = DocumentProcessor(
                    chunk_size=self.config.get_rag_config().get("chunk_size"),
                    chunk_overlap=self.config.get_rag_config().get("chunk_overlap")
                )

            # Process all documents
            processed_docs = self.document_processor.process_multiple_documents(file_paths)

            # Add to vector database
            if not self.vector_db:
                persist_dir = self.config.get_rag_config().get("persist_directory")
                self.vector_db = VectorDB(persist_directory=persist_dir)
                self.vector_db.connect()

            self.vector_db.add_documents(
                documents=processed_docs["documents"],
                metadatas=processed_docs["metadatas"],
                ids=processed_docs["ids"]
            )

            self.documents_loaded = len(processed_docs["documents"])
            self.vector_db_loaded = True

            # Update RAG pipeline with the loaded vector DB
            if self.llm and self.vector_db:
                self.rag_pipeline = RAGPipeline(self.vector_db, self.llm, self.system_prompt)

            self.view.show_success(f"Successfully loaded {self.documents_loaded} document chunks from {len(file_paths)} files to vector database!")
            self.view.show_success("Vector DB is now ready for RAG operations.")

        except Exception as e:
            self.view.show_error(f"Failed to load documents: {str(e)}")

    def _switch_llm_provider(self):
        """Download model if missing."""
        self.view._clear_screen()
        title = Text("Llama.cpp Model Setup", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))

        # Simply call the download function
        self.view.show_success("Starting model download...")
        download_success = self._download_model()

        if download_success:
            self.view.show_success("✅ Model downloaded successfully!")
            self.view.show_success("Please restart the application to use the model.")
        else:
            self.view.show_error("❌ Model download failed")
            self.view.show_error("Please check your internet connection and try again.")

    def _view_current_configuration(self):
        """View current RAG configuration."""
        self.view._clear_screen()
        title = Text("Current RAG Configuration", style="bold blue", justify="center")
        self.view.console.print(Panel(title, box=ROUNDED, border_style="blue"))

        # Load current configuration
        llm_config = self.config.get_llm_config()
        rag_config = self.config.get_rag_config()

        # Escape newlines in system prompt for proper display
        escaped_prompt = self.system_prompt.replace('\n', ' \\n ')
        config_info = f"""
System Prompt:
{escaped_prompt}

LLM Configuration:
  Provider: {llm_config.get('provider', 'not configured')}
  Model Path: {llm_config.get('model_path', 'not configured')}
  Context Window: {llm_config.get('context_window', 'not configured')}

RAG Configuration:
  Embedding Model: {rag_config.get('embedding_model', 'not configured')}
  Chunk Size: {rag_config.get('chunk_size', 'not configured')}
  Chunk Overlap: {rag_config.get('chunk_overlap', 'not configured')}
  Persist Directory: {rag_config.get('persist_directory', 'not configured')}
  Data Path: {rag_config.get('data_path', 'not configured')}

Runtime Status:
  Vector DB Status: {'Loaded' if self.vector_db_loaded else 'Not loaded'}
  Documents Loaded: {self.documents_loaded}
  LLM Status: {'Loaded' if self.llm else 'Not loaded'}
  RAG Pipeline Status: {'Ready' if self.rag_pipeline else 'Not ready'}
        """

        self.view.console.print(Panel(config_info, title="[bold]Configuration Details[/bold]", border_style="green"))

        # Wait for user to press Enter
        input("\nPress Enter to continue...")

    def _download_model(self) -> bool:
        """Download LLM model from Hugging Face."""
        try:
            self.view.console.print("[italic]Downloading TinyLlama model from Hugging Face...[/italic]")
            
            # Import required libraries
            try:
                from huggingface_hub import hf_hub_download
            except ImportError:
                self.view.show_error("huggingface_hub not installed. Installing...")
                import subprocess
                import sys
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "huggingface-hub"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                from huggingface_hub import hf_hub_download
            
            # Get download config
            download_config = self.config.get_download_config()
            
            # Create models directory if it doesn't exist
            local_dir = download_config.get("local_dir", "models")
            os.makedirs(local_dir, exist_ok=True)
            
            # Download the model
            model_path = hf_hub_download(
                repo_id=download_config.get("repo_id"),
                filename=download_config.get("filename"),
                local_dir=local_dir,
                repo_type="model"
            )
            # Rename the file to our expected name
            expected_path = download_config.get("expected_path")
            if model_path != expected_path:
                os.rename(model_path, expected_path)
                model_path = expected_path
            
            self.view.show_success(f"✅ Model downloaded successfully to: {model_path}")
            return True
            
        except Exception as e:
            self.view.show_error(f"Model download failed: {str(e)}")
            self.view.show_error("Please check your internet connection and try again.")
            return False

if __name__ == "__main__":
    controller = Controller()
    controller.run()