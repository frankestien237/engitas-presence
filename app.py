import streamlit as st
import pandas as pd
from datetime import time

# Configuration de la page
st.set_page_config(
    page_title="ENGITAS - Système de Présence",
    page_icon="🛡️",
    layout="wide",
)

# Injection du CSS personnalisé
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1f2937; }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem;
        font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }
    .service-card {
        background-color: #111827; border: 1px solid #1f2937; border-radius: 16px;
        padding: 25px; text-align: center; height: 200px;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%; background-color: #111827;
        color: #9ca3af; text-align: center; padding: 10px; font-size: 13px;
        border-top: 1px solid #1f2937; z-index: 100;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialisation de la session
if "connecte" not in st.session_state: st.session_state.connecte = False
if "page_active" not in st.session_state: st.session_state.page_active = "Connexion"
if "employes_df" not in st.session_state:
    st.session_state.employes_df = pd.DataFrame([
        {"ID": 1, "Nom": "Arnold Omam", "Utilisateur": "aomam", "Poste": "Développeur", "Rôle": "Employé"}
    ])

# --- LOGIQUE D'AFFICHAGE ---
if not st.session_state.connecte:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.radio("Menu", ["Connexion", "S'inscrire"], label_visibility="collapsed")

    # Barre de menu horizontale
    col_logo, col_menu, col_btn = st.columns([1, 4, 1])
    with col_logo: st.markdown("### 🌐 ENGITAS")
    with col_menu:
        m1, m2, m3, m4, m5 = st.columns(5)
        if m1.button("Accueil"): st.session_state.page_active = "Connexion"; st.rerun()
        if m2.button("Services"): st.session_state.page_active = "Services"; st.rerun()
        if m3.button("Écosystème"): st.session_state.page_active = "Ecosysteme"; st.rerun()
        if m4.button("Présence géo"): st.session_state.page_active = "PresenceGeo"; st.rerun()
        if m5.button("Contact"): st.session_state.page_active = "Contact"; st.rerun()
    with col_btn:
        if st.button("Demander un devis"): st.session_state.page_active = "Contact"; st.rerun()

    # --- CONTENU DES PAGES ---
    if st.session_state.page_active == "Connexion":
        st.markdown("<h2 style='text-align: center;'>Connexion</h2>", unsafe_allow_html=True)
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            st.session_state.connecte = True
            st.session_state.username = username
            st.session_state.role = "admin" if username == "admin" else "employe"
            st.rerun()

    elif st.session_state.page_active == "Services":
        st.markdown("## Nos Services")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="service-card"><h3>🛡️ Sécurité</h3><p>Gestion des accès et surveillance.</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="service-card"><h3>📍 Géolocalisation</h3><p>Suivi en temps réel.</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="service-card"><h3>📊 Analytics</h3><p>Rapports détaillés.</p></div>', unsafe_allow_html=True)

    elif st.session_state.page_active == "Ecosysteme":
        st.markdown("## Notre Écosystème")
        st.write("Bienvenue dans l'écosystème ENGITAS. Nous connectons vos équipes.")

    elif st.session_state.page_active == "PresenceGeo":
        st.markdown("## Présence Géolocalisée")
        st.info("Visualisez la position de vos sites en temps réel.")

    elif st.session_state.page_active == "Contact":
        st.markdown("## Contact")
        st.text_input("Email")
        st.text_area("Message")
        st.button("Envoyer")

else:
    # --- SI CONNECTÉ (Votre logique admin/employé reste inchangée) ---
    with st.sidebar:
        st.write(f"Connecté en tant que: **{st.session_state.username}**")
        if st.button("Déconnexion"): st.session_state.connecte = False; st.rerun()
    
    st.write("Tableau de bord utilisateur ici.")

st.markdown('<div class="footer">Design by <b>ARNOLD OMAM</b> | ENGITAS 2026</div>', unsafe_allow_html=True)