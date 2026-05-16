import streamlit as st
import time
import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# importer le dataset
from data import data


# =========================
# Configuration page
# =========================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)


# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# Sidebar
# =========================
def show_sidebar():

    st.sidebar.title("Informations")

    st.sidebar.write("Version : 3.0 ML")
    st.sidebar.write("Réunion : mercredi")
    st.sidebar.write("Contact : ai.club@ipsas.tn")


# =========================
# Chat input
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
# Nettoyage texte
# =========================
def clean_text(text):

    text = text.lower()

    # supprimer ponctuation
    text = re.sub(r"[^\w\sàâéèêëîïôùûüç]", " ", text)

    # supprimer espaces multiples
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# Préparation X et y
# =========================
def prepare_xy(dataframe):

    X = dataframe["clean_message"]

    y = dataframe["intent"]

    return X, y


# =========================
# TF-IDF
# =========================
def create_vectorizer():

    vectorizer = TfidfVectorizer()

    return vectorizer


# =========================
# Entraînement modèle
# =========================
def train_model(X_train, y_train):

    model = MultinomialNB()

    model.fit(X_train, y_train)

    return model


# =========================
# Prediction intention
# =========================
def predict_intent(user_input, vectorizer, model):

    cleaned = clean_text(user_input)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)

    return prediction[0]


# =========================
# Réponses chatbot
# =========================
RESPONSES = {

    "salutation":
        "Bonjour 👋 Bienvenue dans AI Club Assistant.",

    "planning":
        "Les réunions ont lieu chaque mercredi à 13h30.",

    "contact":
        "Contact : ai.club@ipsas.tn",

    "activites":
        "Le club propose des ateliers en IA, Python, NLP et développement de chatbots.",

    "lieu":
        "Les séances se déroulent à l'IPSAS selon le planning affiché."
}


# =========================
# Génération réponse
# =========================
def generate_response_v3(user_input, vectorizer, model):

    intent = predict_intent(
        user_input,
        vectorizer,
        model
    )

    return RESPONSES.get(
        intent,
        "Je ne comprends pas. Peux-tu reformuler ?"
    )


#######################################################
# MACHINE LEARNING
#######################################################

# =========================
# Création dataframe
# =========================
df = pd.DataFrame(
    data,
    columns=["message", "intent"]
)

# nettoyage dataset
df["clean_message"] = df["message"].apply(clean_text)

# préparation X et y
X, y = prepare_xy(df)

# =========================
# Vectorisation
# =========================
vectorizer = create_vectorizer()

X_vector = vectorizer.fit_transform(X)

# =========================
# Entraînement modèle
# =========================
model = train_model(X_vector, y)


#######################################################
# MAIN
#######################################################
def main():

    st.title("🤖 AI Chatbot ML")

    st.write("Posez votre question au chatbot.")

    show_sidebar()

    # afficher historique
    show_conversation()

    # message utilisateur
    user_message = generate_message()

    if user_message:

        # sauvegarder user
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        # afficher user
        with st.chat_message("user"):

            st.markdown(user_message)

        # génération réponse
        with st.spinner("Le bot réfléchit..."):

            time.sleep(1)

            bot_response = generate_response_v3(
                user_message,
                vectorizer,
                model
            )

        # sauvegarder bot
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })

        # afficher bot
        with st.chat_message("assistant"):

            st.markdown(bot_response)


# =========================
# Exécution
# =========================
main()