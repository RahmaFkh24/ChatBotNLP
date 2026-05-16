import streamlit as st
import time

# =========================
# Configuration de la page
# =========================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# =========================
# Initialisation session
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Sidebar
# =========================
def show_sidebar():
    st.sidebar.title("Informations")
    st.sidebar.write("Version : 1.0")
    st.sidebar.write("Réunion : samedi")
    st.sidebar.write("Contact : ai.chatbot@example.com")


# =========================
# Génération du message
# =========================
def generate_message():
    return st.chat_input("Entrez votre message")


# =========================
# Réponse du bot
# =========================
def generate_response(user_input):

    user_input = user_input.lower().strip()

    if "bonjour" in user_input:
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

    elif "ça va" in user_input:
        return "Je vais très bien 😊"

    elif "merci" in user_input:
        return "Avec plaisir !"

    else:
        return "Je ne comprends pas encore cette question."


# =========================
# Affichage conversation
# =========================
def show_conversation():

    # Afficher tous les messages sauvegardés
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# =========================
# Main
# =========================
def main():

    st.title("🤖 AI Chatbot")
    st.write("Posez votre question au bot.")

    show_sidebar()

    # Afficher historique
    show_conversation()

    # Entrée utilisateur
    user_message = generate_message()

    if user_message:

        # Sauvegarder message utilisateur
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        # Afficher utilisateur
        with st.chat_message("user"):
            st.markdown(user_message)

        # Générer réponse
        with st.spinner("Le bot réfléchit..."):
            time.sleep(1)
            bot_response = generate_response(user_message)

        # Sauvegarder réponse bot
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })

        # Afficher réponse bot
        with st.chat_message("assistant"):
            st.markdown(bot_response)


# =========================
# Exécution
# =========================
main()