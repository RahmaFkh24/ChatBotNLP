import streamlit as st
import time
import re

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
# Affichage conversation
# =========================
def show_conversation():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


#######################################################
# NLP
#######################################################

# =========================
# 1. Nettoyage du texte
# =========================
def clean_text(text):

    text = text.lower()

    # supprimer ponctuation
    text = re.sub(r"[^\w\sàâéèêëîïôùûüç]", " ", text)

    # supprimer espaces multiples
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# 2. Tokenisation
# =========================
def decouper_en_mots(text):
    return text.split()


# =========================
# 3. Stopwords
# =========================
STOPWORDS = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et",
    "est", "a", "au", "aux", "je", "tu", "il", "elle", "on",
    "nous", "vous", "ils", "elles", "mon", "ma", "mes",
    "ton", "ta", "tes", "son", "sa", "ses", "ce", "cet",
    "cette", "ces", "dans", "sur", "pour", "par", "avec",
    "en", "que", "qui", "quoi", "où", "quand", "comment",
    "bonjour", "me"
}

def supprimer_stopwords(text):

    mots = decouper_en_mots(text)

    mots_sans_stopwords = [
        mot for mot in mots
        if mot not in STOPWORDS
    ]

    return mots_sans_stopwords


# =========================
# Pipeline NLP
# =========================
def preprocess_text(text):

    text = clean_text(text)

    mots = supprimer_stopwords(text)

    return mots


# =========================
# Intentions
# =========================
INTENTS = {

    "salutation": [
        "salut", "hello", "bonsoir", "salam"
    ],

    "planning": [
        "planning", "horaire", "reunion",
        "réunion", "seance", "séance"
    ],

    "contact": [
        "contact", "email", "mail",
        "gmail", "telephone", "téléphone"
    ],

    "activites": [
        "activité", "activites", "activités",
        "atelier", "formation", "club", "ieee"
    ],

    "lieu": [
        "lieu", "salle", "classe",
        "endroit", "localisation",
        "ou", "où", "séance"
    ]
}


# =========================
# Détection intention
# =========================
def detect_intent(user_input):

    dict_score = {}

    mots_utiles = preprocess_text(user_input)

    for intent, keywords in INTENTS.items():

        score = sum(
            1 for word in keywords
            if word in mots_utiles
        )

        dict_score[intent] = score

    max_score = max(dict_score.values())

    if max_score == 0:
        return "fallback"

    for intent, score in dict_score.items():

        if score == max_score:
            return intent


# =========================
# Réponses
# =========================
RESPONSES = {

    "salutation":
        "Bonjour ! Bienvenue dans AI Club Assistant.",

    "planning":
        "Les réunions ont lieu les mercredis à 13h30.",

    "contact":
        "Contact : ai.club@ipsas.tn",

    "activites":
        "Le club propose des ateliers en IA, Python, NLP et développement de chatbots.",

    "lieu":
        "Les séances se déroulent dans la salle de conférence.",

    "fallback":
        "Je n’ai pas compris. Peux-tu reformuler ta question ?"
}


# =========================
# Génération réponse
# =========================
def generate_response_v2(user_input):

    intention = detect_intent(user_input)

    response = RESPONSES[intention]

    return response


# =========================
# Main
# =========================
def main():

    st.title("🤖 AI Chatbot")
    st.write("Posez votre question au bot.")

    show_sidebar()

    # historique
    show_conversation()

    # input user
    user_message = generate_message()

    if user_message:

        # sauvegarde user
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.markdown(user_message)

        # génération réponse
        with st.spinner("Le bot réfléchit..."):
            time.sleep(1)

            bot_response = generate_response_v2(user_message)

        # sauvegarde bot
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })

        with st.chat_message("assistant"):
            st.markdown(bot_response)


# =========================
# Exécution
# =========================
main()