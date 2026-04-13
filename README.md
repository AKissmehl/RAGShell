# RAGShell

Welcome to the first lab in the course **DM2731 AI for Learning**. This lab introduces you to 
**Retrieval-Augmented Generation (RAG)** systems with local LLM support. The goal is to help you understand how 
RAG works and explore its applications, with a focus on using it as a pedagogical agent to provide information about 
the Artemis program.

## Quick Start

### 1. Install Git (if not already installed)
- **macOS**: Open a terminal and run `brew install git` or download from [git-scm.com](https://git-scm.com/).
- **Linux**: Open a terminal and run `sudo apt install git` (or use your package manager).
- **Windows**: Download from [git-scm.com](https://git-scm.com/) and install.

### 2. Clone the Repository
Open a terminal and run:
```bash
git clone https://github.com/AKissmehl/RAGShell.git
cd RAGShell
```

### 3. Set Up a Python Virtual Environment
To avoid conflicts with other Python projects, create a virtual environment:

- **macOS/Linux**:
  Open a terminal and run:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  Open Command Prompt and run:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. Install Dependencies
This project is Python-based. Ensure you have Python and pip installed:

- **Install Python and pip (if not already installed)**:
  - On macOS/Linux: Open a terminal and run `brew install python` or use your package manager.
  - On Windows: Download Python from [python.org](https://www.python.org/downloads/) (includes pip).

- **Install required packages**:
  Open a terminal and run:
  ```bash
  pip install -r requirements.txt
  ```


## Lab Task: Creating and a testing Pedagogical Chatbot

1. **Test the Chatbot**
   
   1. Start the chatbot and ask a question about the Artemis program.
   2. Record your question and the response.
2. Set Up the Vector Database
   1. Return to the main menu. 
   2. Select "RAG Setup" and load the provided documents into the vector database. 
   3. Return to the chat and ask the same question again. 
   4. Record the new response.
3. **Analyze the Response**
   1. Compare the two responses for accuracy and detail. 
   2. Use Wikipedia or official sources to verify the information. 
   3. Reflect on how the vector database improved or altered the response.
4. **Write and Test Your Own System Prompts**
   - **General Prompt:** Create a prompt for a chatbot with no specific domain focus. 
   Example: "You are a helpful assistant. Answer questions to the best of your ability, using clear and concise language."
   - **Subject-Specific Prompt:** Create a prompt tailored to the Artemis program or space exploration.
Example: "You are an expert on space exploration. Provide detailed, accurate, and technically precise answers about the Artemis program, lunar missions, and related topics."
5. **Reflect on the Output**
    - Write a short report (500 words +/- 10%) addressing the following:
      - **Opportunities and Risks** What are the opportunities and risks of using pedagogical agents not tailored to a specific subject domain? 
      - **Role of RAG** How does RAG improve the chatbot’s responses? What are its limitations? 
      - **Behavior and Challenges** What behaviors should a pedagogical agent implement to be useful? What challenges might arise?