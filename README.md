# Cybersecurity Awareness Chatbot

An advanced NLP-powered chatbot designed to answer cybersecurity-related questions using semantic search.

Built as a hands-on project to practice modern NLP techniques and create a practical security awareness tool.

---

## Features

- Semantic understanding using **Sentence Transformers**
- Answers questions related to:
  - Phishing, Malware, Ransomware
  - Passwords & MFA
  - Incident Response & SOC
  - CIA Triad, Encryption, Hashing
  - Zero-day & Social Engineering
- Confidence score with every response
- Clean web interface built with **Streamlit**
- Example question buttons
- Chat history support

---

## Tech Stack

- Python
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Streamlit
- PyTorch
- JSON Knowledge Base

---

## Project Structure
security-chatbot/
├── data/
│   └── knowledge_base.json
├── src/
│   └── chatbot.py
├── streamlit_app.py
├── app.py
├── requirements.txt
└── README.md


---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/security-awareness-chatbot.git
cd security-awareness-chatbot

2. Create virtual environment & install dependenciesbash

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3. Run the Web Appbash

streamlit run streamlit_app.py

Future ImprovementsAdd conversation memory across sessions
Implement RAG (Retrieval-Augmented Generation)
Expand knowledge base with MITRE ATT&CK
Deploy online

AuthorMuhammad Junaid
Cybersecurity & IT Support  LinkedIn • GitHub
