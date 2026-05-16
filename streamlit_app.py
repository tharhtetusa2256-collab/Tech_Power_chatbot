import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Tech Power AI Business Assistant",
    page_icon="⚡",
    layout="centered",
)

SYSTEM_PROMPT = """
You are Tech Power AI Business Assistant.
Your job is to help small businesses understand AI automation opportunities.
Be practical, friendly, and business-focused.
When useful, ask for the client's business type, current workflow, pain points, and contact details.
Never claim a feature is already integrated unless the code actually supports it.
"""

BUSINESS_MODES = {
    "General AI Consultant": "Help the user discover practical automation opportunities for their business.",
    "Customer Support FAQ": "Answer customer support style questions clearly and politely.",
    "Lead Capture": "Guide the conversation toward collecting name, business type, problem, budget, and contact method.",
    "Content Ideas": "Generate practical social media and marketing content ideas for small businesses.",
}

st.title("⚡ Tech Power AI Business Assistant")
st.write(
    "A practical AI assistant demo for Tech Power Co.,Ltd. "
    "Use it to show clients how AI can support customer service, lead capture, content creation, and workflow automation."
)

with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    model = st.text_input("Model", value="gpt-4o-mini")
    mode = st.selectbox("Assistant Mode", list(BUSINESS_MODES.keys()))

    st.divider()
    st.subheader("Tech Power Offer")
    st.markdown(
        """
        - AI chatbot setup
        - Lead capture automation
        - Customer support workflow
        - AI content system
        - Business process automation
        """
    )

if not openai_api_key:
    st.info("Add your OpenAI API key in the sidebar to start the demo.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "မင်္ဂလာပါ 👋 I am Tech Power AI Business Assistant. "
                "Tell me what kind of business you run, and I can suggest useful AI automation ideas."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about AI automation for your business...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\nCurrent mode: " + BUSINESS_MODES[mode]},
        *[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    ]

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
