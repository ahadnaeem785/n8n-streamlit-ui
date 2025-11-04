import streamlit as st
import requests
import uuid
import time
import random

# -------------------------------
# 🏨 App Configuration
# -------------------------------
st.set_page_config(page_title="Chez Jules Concierge", page_icon="🛎️")

st.title("🛎️ Chez Jules – Your Digital Concierge")
st.write("Ask me anything about Hotel Hafen Flensburg — I’m here to help!")

# -------------------------------
# 🧠 Session Management
# -------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []  # store messages as list of dicts

# -------------------------------
# 💬 Display Chat History
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# 🗣️ Chat Input
# -------------------------------
if prompt := st.chat_input("Your message to Jules..."):
    # Save and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 🔗 Your n8n Webhook endpoint
        N8N_URL = "https://muhammadahad764.app.n8n.cloud/webhook/hotel/chat"

        payload = {
            "message": prompt,
            "sessionId": st.session_state.session_id
        }


        # Assistant chat bubble
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            with st.spinner("thinking..."):
                response = requests.post(N8N_URL, json=payload, timeout=90)

            # Handle response
            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "Hmm... I didn’t quite catch that.")
            else:
                reply = f"Error {response.status_code}: {response.text}"

            # -------------------------------
            # ✨ STREAMING EFFECT (Human-like typing)
            # -------------------------------
            streamed_text = ""
            for char in reply:
                streamed_text += char
                message_placeholder.markdown(streamed_text + "▌")
                # slower after punctuation, faster otherwise
                if char in [".", ",", "!", "?"]:
                    time.sleep(random.uniform(0.08, 0.15))
                else:
                    time.sleep(random.uniform(0.015, 0.03))
            message_placeholder.markdown(streamed_text)  # clean up cursor

        # ✅ Save assistant reply (after rendering)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Connection error: {e}")
