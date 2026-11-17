import sys
from typing import Any, Optional, Union
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import search_recipe

SYSTEM_PROMPT = """You are a friendly and passionate chef assistant.
When a user asks for a recipe or cooking help, use the search_recipe tool to find it.
Present the ingredients clearly, explain the steps in simple language, and add
helpful cooking tips — substitutions, serving suggestions, or difficulty notes.
Make cooking feel approachable and fun for everyone."""

_default_agent = None


def build_agent(
    model: str = "llama3.2",
    temperature: float = 0.4,
    checkpointer: Optional[Any] = None,
):
    """
    Build and return a prebuilt LangGraph ReAct agent using Ollama and the search_recipe tool.
    """
    llm = ChatOllama(model=model, temperature=temperature)
    tools = [search_recipe]
    if checkpointer is None:
        checkpointer = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent


def ask(
    agent_or_query: Union[Any, str],
    query: Optional[str] = None,
    thread_id: str = "recipe_session",
) -> str:
    """
    Send a user message to the agent and return the response.

    Supports both invocation styles:
      - ask(agent, "How do I make biryani?")
      - ask("How do I make biryani?")  # uses lazily built default agent
    """
    global _default_agent

    if query is None and isinstance(agent_or_query, str):
        if _default_agent is None:
            _default_agent = build_agent()
        agent = _default_agent
        user_message = agent_or_query
    else:
        agent = agent_or_query
        user_message = query or ""

    if not user_message.strip():
        return "Please ask a recipe or cooking question!"

    config = {}
    if getattr(agent, "checkpointer", None) is not None:
        config["configurable"] = {"thread_id": thread_id}

    try:
        response = agent.invoke({"messages": [("user", user_message)]}, config=config if config else None)
        messages = response.get("messages", [])
        if not messages:
            return "No response received from agent."

        last_message = messages[-1]
        content = getattr(last_message, "content", "")
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # If content is a list of parts/dictionaries
            parts = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    parts.append(part["text"])
                else:
                    parts.append(str(part))
            return "".join(parts)
        return str(content)
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "connect" in error_msg.lower():
            return (
                f"Error: Unable to connect to Ollama ({error_msg}).\n"
                "Please make sure Ollama is running (`ollama serve`) and llama3.2 is downloaded (`ollama pull llama3.2`)."
            )
        raise e


def main():
    """Interactive while-loop CLI chat for the Recipe Agent."""
    print("=" * 60)
    print("          Recipe Agent — Friendly Chef Assistant          ")
    print("=" * 60)
    print("Ask me for any recipe, cooking help, or culinary tips!")
    print("Type 'quit', 'exit', or 'q' to exit.\n")

    agent = build_agent()
    thread_id = "chef_cli_session"

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("\nChef: Happy cooking! Goodbye! 👋\n")
                break

            response = ask(agent, user_input, thread_id=thread_id)
            print(f"\nChef:\n{response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nChef: Session ended. Happy cooking! Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
