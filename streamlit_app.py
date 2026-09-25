import streamlit as st
from src.chatbot import SecurityChatbot
from pathlib import Path
import torch
from sentence_transformers import util

import base64
from pathlib import Path

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="Cybersecurity Awareness Chatbot",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)
# Load background image as base64
bg_image = get_base64_image("dark theme.jpg")

st.markdown(f"""
    <style>
    /* Full background image */
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Remove top header bar */
    header[data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    /* Remove bottom footer bar */
    footer[data-testid="stfooter"] {{
        background: rgba(0,0,0,0);
    }}

    /* Remove extra padding */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Make chat messages readable */
    .stChatMessage {{
        background-color: rgba(14, 17, 23, 0.80) !important;
        border-radius: 12px;
        padding: 12px;
    }}

    /* Hide Streamlit footer */
    footer {{
        visibility: hidden;
    }}

    

    /* Optional: make sidebar slightly transparent */
    section[data-testid="stSidebar"] {{
        background-color: rgba(14, 17, 23, 0.85);
    }}
    </style>
""", unsafe_allow_html=True)
# --------------------------
# Load Chatbot
# --------------------------
@st.cache_resource
def load_chatbot():
    knowledge_path = Path("data") / "knowledge_base.json"
    return SecurityChatbot(str(knowledge_path))

bot = load_chatbot()

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.title("🛡️ About this Project")
    st.markdown("""
    **Cybersecurity Awareness Chatbot**
    
    This is an advanced NLP-powered chatbot designed to answer common cybersecurity questions.
    
    **Features:**
    - Semantic understanding (Sentence Transformers)
    - Real-time responses
    - Focused on security awareness topics
    
    **Topics Covered:**
    - Phishing
    - Malware & Ransomware
    - Passwords & MFA
    - Incident Response
    - SOC
    - Social Engineering
    - Zero-day
    
    ---
    Built as a hands-on cybersecurity learning project.
    """)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --------------------------
# Main Chat Interface
# --------------------------
st.title("🛡️ Cybersecurity Awareness Chatbot")
st.markdown("### Welcome to the world of Cybersecurity!")
st.caption("From phishing scams to ransomware attacks - ask me anything about the world of cybersecurity.")
# Example Questions
st.markdown("#### Example Questions:")
col1, col2, col3 = st.columns(3)

example_questions = [
    "What is phishing?",
    "How to detect phishing?",
    "What is ransomware?",
    "What is MFA?",
    "Explain incident response",
    "What does a SOC do?"
]

def ask_example(question):
    st.session_state.example_question = question

with col1:
    if st.button(example_questions[0]):
        ask_example(example_questions[0])
    if st.button(example_questions[3]):
        ask_example(example_questions[3])

with col2:
    if st.button(example_questions[1]):
        ask_example(example_questions[1])
    if st.button(example_questions[4]):
        ask_example(example_questions[4])

with col3:
    if st.button(example_questions[2]):
        ask_example(example_questions[2])
    if st.button(example_questions[5]):
        ask_example(example_questions[5])

st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the world of Cybersecurity! 👋\n\nI'm your security awareness assistant. Ask me anything about phishing, malware, passwords, MFA, incident response, or SOC."}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle example question click
if "example_question" in st.session_state:
    prompt = st.session_state.example_question
    del st.session_state.example_question
else:
    prompt = st.chat_input("Type your security question here...")

# Process user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response + confidence
    # We need to modify slightly to also return confidence
    user_embedding = bot.model.encode(prompt, convert_to_tensor=True)
    similarities = util.cos_sim(user_embedding, bot.pattern_embeddings)[0]
    best_score = torch.max(similarities).item()
    best_idx = torch.argmax(similarities).item()

    if best_score > 0.45:
        tag = bot.tags[best_idx]
        response = bot.knowledge[tag]["responses"][0]
        confidence = best_score
    else:
        response = bot.knowledge["default"]["responses"][0]
        confidence = best_score

    full_response = f"{response}\n\n**Confidence:** {confidence:.2f}"

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    with st.chat_message("assistant"):
        st.markdown(full_response)