# Recipe Agent

A conversational cooking assistant agent built with **LangChain**, **LangGraph**, **Ollama (`llama3.2`)**, and **TheMealDB API**. Includes both a **CLI interface** and a **Web UI (Streamlit)**.

---

## Architecture & Stack

- **LLM**: Ollama `llama3.2` with `temperature=0.4` via `langchain-ollama`
- **Framework**: LangGraph `create_react_agent` (prebuilt ReAct loop with `MemorySaver` for conversational state)
- **Tool**: `search_recipe` (queries TheMealDB API, free & keyless)
- **Interfaces**:
  - 🖥️ **CLI**: `agent.py`
  - 🌐 **Web App**: `app.py` (built with Streamlit)

---

## Project Structure

```text
recipe_agent/
├── .venv/              # Virtual environment
├── requirements.txt    # Project dependencies
├── tools.py            # Recipe search tool (TheMealDB)
├── agent.py            # ReAct agent definition & interactive CLI
├── app.py              # Modern Streamlit web application
└── README.md           # Documentation & instructions
```

---

## Quick Start: Running in Website / Browser

### 1. Ensure Ollama is running
```bash
ollama serve
ollama pull llama3.2
```

### 2. Launch the Streamlit Web Application
In your terminal, run:
```bash
streamlit run app.py
```

This will automatically open your default web browser at:
👉 **`http://localhost:8501`**

### Web UI Features:
- 💬 **Interactive Chat Interface**: Familiar ChatGPT-style chat with `🧑` and `👨‍🍳` avatars.
- ⚡ **Quick-Prompt Buttons**: One-click shortcuts for recipes like Chicken Biryani, Pasta Carbonara, or Pancakes.
- ⚙️ **Sidebar Controls**: Adjust temperature, select model, or clear conversation memory.
- 🔄 **Conversation Memory**: Maintains context across multiple questions during your session.

---

## Alternative: Running via Command Line (CLI)

```bash
python agent.py
```
Exit the CLI anytime by typing `quit`, `exit`, or `q`.
