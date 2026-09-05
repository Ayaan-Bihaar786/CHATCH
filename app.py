import os
import streamlit as st
from google import genai

# पेज की सेटिंग्स
st.set_page_config(page_title="Ayaan AI Chatbot", page_icon="🤖")

st.title("🤖 Ayaan AI Chatbot")
st.write("नमस्ते! मैं एक एआई चैटबॉट हूँ जिसे **'अयान' (Ayaan)** ने बनाया है।")

# Hugging Face के Secrets से अपने आप API Key ले लेगा (आपको यहाँ कुछ नहीं बदलना है)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("त्रुटि: Hugging Face के Secrets में 'GEMINI_API_KEY' सेट नहीं है!")
else:
    try:
        # क्लाइंट इनिशियलाइज करें
        client = genai.Client(api_key=api_key)

        # चैट हिस्ट्री को याद रखने के लिए सेशन स्टेट
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = client.chats.create(
                model="gemini-2.5-flash",
                config=genai.types.ChatConfig(
                    system_instruction="आपका नाम एक मददगार AI है। यदि कोई पूछे कि आपको किसने बनाया है, तो कहें कि आपको 'अयान' (Ayaan) ने बनाया है."
                )
            )

        # पुरानी चैट दिखाने के लिए
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # यूजर इनपुट
        if user_input := st.chat_input("यहाँ अपना सवाल लिखें..."):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Gemini से जवाब मंगाना
            with st.chat_message("assistant"):
                with st.spinner("सोच रहा हूँ..."):
                    response = st.session_state.chat_session.send_message(user_input)
                    bot_reply = response.text
                    st.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"एक एरर आ गई है: {e}")

