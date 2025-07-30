<h1 align="center">WhatsApp Chat Analyzer 📊💬</h1>

<p align="center">
  A powerful and interactive tool to analyze WhatsApp group or individual chat exports using Python and Streamlit.
</p>

---

## 🚀 Live Demo

👉 [Click here to try the app on Streamlit](https://wapp-analyzer.streamlit.app/)

---

## 🔍 Features

- 📄 Upload `.txt` WhatsApp chat file (without media)
- 📊 Overall statistics: total messages, words, media shared, links
- 🕒 Daily & monthly message timelines
- 🔝 Most active users in group chats
- 💬 Most common words (with stopword removal)
- 😂 Emoji usage frequency
- 📅 Weekly and monthly heatmap activity

---

## 📁 How to Export WhatsApp Chat

1. Open the chat in WhatsApp.
2. Tap the three-dot menu → More → **Export Chat**
3. Choose **Without Media**
4. Transfer the `.txt` file to your computer and upload it in the app.

---

## 🛠 Tech Stack

- Python 3.10.8
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Emoji

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/karanbisht45/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
