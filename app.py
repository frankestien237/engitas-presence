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
    .login-container {
        background-color: #0b0f19; border: 2px solid #1e3a8a; border-radius: 16px;
        padding: 40px; box-shadow: 0 0 25px rgba(30, 58, 138, 0.4);
        max-width: 700px; margin: auto;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem;
        font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }
    .stTextInput>div>div>input { background-color: #111827; color: white; border: 1px solid #374151; border-radius: 8px; }
    .location-card {
        background-color: #111827; border: 1px solid #1e3a8a; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .partner-badge {
        background-color: #ffffff; color: #111827; border-radius: 10px; padding: 12px 15px;
        text-align: center; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 15px; display: flex; align-items: center; justify-content: center;
        gap: 10px; font-size: 14px; border: 1px solid #e5e7eb;
    }
    .service-card {
        background-color: #111827; border: 1px solid #1f2937; border-radius: 16px;
        padding: 25px; text-align: center; height: 180px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
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
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = ""
if "page_active" not in st.session_state: st.session_state.page_active = "Connexion"
if "employes_df" not in st.session_state:
    st.session_state.employes_df = pd.DataFrame([
        {"ID": 1, "Nom": "Arnold Omam", "Utilisateur": "aomam", "Poste": "Développeur Senior", "Rôle": "Employé", "Statut": "Actif"},
        {"ID": 2, "Nom": "Valere Feugwang", "Utilisateur": "vfeugwang", "Poste": "Directeur Général", "Rôle": "Admin", "Statut": "Actif"},
        {"ID": 3, "Nom": "Jean Dupont", "Utilisateur": "jdupont", "Poste": "Technicien Réseau", "Rôle": "Employé", "Statut": "Actif"},
        {"ID": 4, "Nom": "Marie Claire", "Utilisateur": "mclaire", "Poste": "Support Client", "Rôle": "Employé", "Statut": "Inactif"}
    ])

# --- LOGIQUE D'AFFICHAGE ---
if not st.session_state.connecte:
    # [Code de navigation non connecté inchangé...]
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        auth_mode = st.radio("", ["Connexion", "S'inscrire"], label_visibility="collapsed")

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

    # Logique des pages publiques (PresenceGeo, Services, etc.)
    if st.session_state.page_active == "PresenceGeo":
        st.markdown("<h1 style='text-align: center;'>Nous trouver</h1>", unsafe_allow_html=True)
        # ... (le reste de vos colonnes)
    elif st.session_state.page_active == "Connexion":
        st.markdown("<h2 style='text-align: center;'>Connexion</h2>", unsafe_allow_html=True)
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            st.session_state.connecte = True
            st.session_state.username = username
            st.session_state.role = "admin" if username == "admin" else "employe"
            st.rerun()

else:
    # --- SI CONNECTÉ ---
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.username}**")
        if st.session_state.role == "admin":
            options_menu = ["Tableau de bord", "Gestion des employés", "Admin", "Déconnexion"]
        else:
            options_menu = ["Signer ma présence", "Déconnexion"]
        
        menu_option = st.radio("Navigation", options_menu)
        if menu_option == "Déconnexion":
            st.session_state.connecte = False; st.rerun()

    if menu_option == "Admin":
        st.markdown("### ⚙️ Panneau de Configuration Système")
        tab1, tab2, tab3, tab4 = st.tabs(["🕒 Paramètres", "📍 Zones GPS", "📜 Logs Audit", "📥 Rapports"])

        with tab1:
            st.markdown("#### Configuration des heures")
            heure_limite = st.time_input("Heure limite d'arrivée", value=time(9, 0))
            if st.button("Sauvegarder les horaires"): st.success(f"Heure limite : {heure_limite}")

        with tab2:
            st.markdown("#### Gestion des sites")
            nom_site = st.text_input("Nom du site")
            lat = st.number_input("Latitude", format="%.6f")
            lon = st.number_input("Longitude", format="%.6f")
            if st.button("Ajouter Site"): st.info(f"Site {nom_site} enregistré.")

        with tab3:
            st.markdown("#### 📜 Journaux d'activité")
            logs = pd.DataFrame({
                "Date": ["2026-08-19 08:45", "2026-08-19 09:12"],
                "Action": ["Connexion", "Tentative hors délai"]
            })
            st.table(logs)

        with tab4:
            st.markdown("#### 📥 Exportation")
            csv = st.session_state.employes_df.to_csv(index=False).encode('utf-8')
            st.download_button("Exporter en CSV", data=csv, file_name='rapport_engitas.csv')

    elif menu_option == "Gestion des employés":
        st.session_state.employes_df = st.data_editor(st.session_state.employes_df, num_rows="dynamic")
    
    else:
        st.write(f"Section : {menu_option}")

st.markdown('<div class="footer">Design by <b>ARNOLD OMAM</b> | ENGITAS 2026</div>', unsafe_allow_html=True)