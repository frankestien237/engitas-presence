import json
import os
import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🏢", layout="wide"
)

# Style CSS personnalisé
st.markdown(
    """
    <style>
    .hero-container {
        padding: 2rem 0;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .hero-highlight {
        color: #00b4d8;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-bottom: 2rem;
    }
    .card-grid {
        display: flex;
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .info-card {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        padding: 1.5rem;
        border-radius: 8px;
        flex: 1;
        text-align: center;
    }
    .info-card h3 {
        color: #00b4d8;
        margin-bottom: 0.5rem;
    }
    .info-card p {
        color: #cccccc;
        margin: 0;
        font-size: 0.9rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Fonction sécurisée pour charger les utilisateurs (Ligne 27 corrigée)
def charger_utilisateurs():
    nom_fichier = "utilisateurs.json"
    if not os.path.exists(nom_fichier) or os.path.getsize(nom_fichier) == 0:
        return {
            "admin": {"password": "adminpassword", "role": "Administrateur"}
        }
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            if not contenu:
                return {
                    "admin": {
                        "password": "adminpassword",
                        "role": "Administrateur",
                    }
                }
            return json.loads(contenu)
    except Exception:
        return {
            "admin": {"password": "adminpassword", "role": "Administrateur"}
        }


# Initialisation sécurisée des utilisateurs dans la session
if "utilisateurs" not in st.session_state:
    st.session_state.utilisateurs = charger_utilisateurs()

# --- BARRE LATÉRALE ---
st.sidebar.markdown(
    "<h2 style='color: #00b4d8; text-align: center;'>ENGITAS</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #a0a0a0; font-size: 14px;'>Système de Présence</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

if "user_connecte" in st.session_state:
    st.sidebar.markdown(f"👤 Connecté : **{st.session_state.user_connecte}**")
    role_actuel = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]

    options_menu = ["Signer ma présence", "Pointer mon départ"]
    if role_actuel == "Administrateur":
        options_menu.append("Tableau de bord Admin")

    options_menu.append("Déconnexion")
    menu = st.sidebar.radio("Navigation", options_menu)

    if menu == "Déconnexion":
        del st.session_state.user_connecte
        st.rerun()
else:
    menu = st.sidebar.radio("Navigation", ["Connexion", "S'inscrire"])

# --- 1. CONNEXION ---
if menu == "Connexion":
    st.markdown(
        """
        <div class="hero-container">
            <div style="font-size: 12px; color: #00b4d8; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">
                CLOUD & VIRTUALISATION • SÉCURITÉ
            </div>
            <div class="hero-title">
                Solutions innovantes de <span class="hero-highlight">cloud & virtualisation</span>
            </div>
            <div class="hero-subtitle">
                Accompagner les entreprises au Cameroun et en Afrique dans leur transformation numérique avec des solutions IT sur mesure — audit, cybersécurité, cloud et services managés.
            </div>
            
            <div class="card-grid">
                <div class="info-card">
                    <h3>360°</h3>
                    <p>Cybersécurité & Protection</p>
                </div>
                <div class="info-card">
                    <h3>24/7</h3>
                    <p>Infrastructure IT</p>
                </div>
                <div class="info-card">
                    <h3>25+</h3>
                    <p>Années d'expertise</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Connexion à votre compte")
    with st.form("form_connexion"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit_connexion = st.form_submit_button("Se connecter")

        if submit_connexion:
            if (
                username in st.session_state.utilisateurs
                and st.session_state.utilisateurs[username]["password"]
                == password
            ):
                st.session_state.user_connecte = username
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error(
                    "Nom d'utilisateur ou mot de passe incorrect.", icon="⚠️"
                )

# --- 2. S'INSCRIRE ---
elif menu == "S'inscrire":
    st.markdown("### Créer un compte employé")
    with st.form("form_inscription"):
        new_user = st.text_input("Choisissez un nom d'utilisateur")
        new_pass = st.text_input("Choisissez un mot de passe", type="password")
        submit_inscription = st.form_submit_button("S'inscrire")

        if submit_inscription:
            if new_user in st.session_state.utilisateurs:
                st.warning("Ce nom d'utilisateur existe déjà.")
            elif new_user == "" or new_pass == "":
                st.error("Veuillez remplir tous les champs.")
            else:
                st.session_state.utilisateurs[new_user] = {
                    "password": new_pass,
                    "role": "Employé",
                }
                st.success("Compte créé avec succès ! Vous pouvez vous connecter.")