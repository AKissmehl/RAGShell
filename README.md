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


## Lab Task

1. **Test the Chatbot**
   
   1. There is a new program to fly to the Moon, where the first human flight started a couple of days ago. Start the chatbot and pose a question about the **Artemis program**, then record the answer you receive and your question.
   2. Now, check the menu options. You can set up the vector database there. Do that, then open the chat again and ask your question again.

2. **Analyze the Response**

   2. Take some quick notes on how the responses differ and whether they are accurate. You can use Wikipedia to verify the responses. Specifically, include a short reflection on how the vector database makes a difference compared to raw LLM.

3. **Set a New System Prompt**

   2. You can find two system prompts in the folder `data/system_prompts`. In the settings, you can set a new system prompt. Go ahead and test both prompts with the prompt below, then record the answers.

4. **Reflect on the Output**

   Reflect on the different outputs and describe how they differ. Keep in mind that we deliberately chose to use a small model that can run on local hardware. Use the following headings to guide your reflection:
   - **Opportunities and Risks**: What are the opportunities and risks of pedagogical agents that are not tailored to a subject domain?
   - **Role of RAG**: How does RAG help, and what are its limitations?
   - **Behavior and Challenges**: From your perspective, what behavior needs to be implemented by a pedagogical agent to be useful, and what are the challenges?