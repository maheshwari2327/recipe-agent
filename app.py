import uuid
import streamlit as st
from agent import build_agent, ask

# Page configuration
st.set_page_config(
    page_title="Recipe Agent — Chef Assistant",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .stChatMessage {
        border-radius: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("🍳 Recipe Agent")
    st.markdown("Your AI-powered culinary companion powered by **LangGraph**, **Ollama (`llama3.2`)**, and **TheMealDB**.")
    st.markdown("---")

    st.subheader("⚙️ Settings")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.4, step=0.05,
                            help="0.4 is optimal for friendly tone and accurate recipes.")
    model_name = st.selectbox("Ollama Model", ["llama3.2"], index=0)

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.agent = build_agent(model=model_name, temperature=temperature)
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown(
        "- Ask for full recipes (e.g., *'Chicken Biryani'*)\n"
        "- Inquire about ingredient substitutions\n"
        "- Ask for serving recommendations or pairings"
    )

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello there! I'm your chef assistant. Tell me what you'd like to cook, "
                "or ask for recipe ideas, substitutions, and cooking tips!"
            ),
        }
    ]

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state.agent = build_agent(model=model_name, temperature=temperature)

# Header
st.markdown('<div class="main-title">👨‍🍳 Chef Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Search delicious recipes from TheMealDB with friendly instructions & tips.</div>',
    unsafe_allow_html=True,
)

# Quick suggestion chips when only the greeting is present
if len(st.session_state.messages) == 1:
    st.write("**Need some inspiration? Try asking:**")
    col1, col2, col3 = st.columns(3)
    preset_query = None
    with col1:
        if st.button("🍛 Chicken Biryani", use_container_width=True):
            preset_query = "How do I make Chicken Biryani?"
    with col2:
        if st.button("🍝 Pasta Carbonara", use_container_width=True):
            preset_query = "Can you give me a recipe for Carbonara?"
    with col3:
        if st.button("🥞 Fluffy Pancakes", use_container_width=True):
            preset_query = "How to make classic pancakes?"

    if preset_query:
        st.session_state.messages.append({"role": "user", "content": preset_query})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(preset_query)
        with st.chat_message("assistant", avatar="👨‍🍳"):
            with st.spinner("Cooking up your recipe..."):
                response = ask(st.session_state.agent, preset_query, thread_id=st.session_state.thread_id)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Display chat messages
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "👨‍🍳"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask for a recipe or cooking advice..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant", avatar="👨‍🍳"):
        with st.spinner("👨‍🍳 Chef is checking ingredients and recipe notes..."):
            response = ask(st.session_state.agent, prompt, thread_id=st.session_state.thread_id)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
