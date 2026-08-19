import streamlit as st
import pandas as pd
from datetime import time, datetime

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
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    .login-container {
        background-color: #0b0f19;
        border: 2px solid #1e3a8a;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 0 25px rgba(30, 58, 138, 0.4);
        max-width: 700px;
        margin: auto;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0369a1 100%, #075985 100%);
    }
    .stTextInput>div>div>input {
        background-color: #111827;
        color: white;
        border: 1px solid #374151;
        border-radius: 8px;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .location-card {
        background-color: #111827;
        border: 1px solid #1e3a8a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .location-card h4 {
        color: #38bdf8;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .location-card p {
        color: #9ca3af;
        margin: 0;
        font-size: 14px;
    }
    .partner-badge {
        background-color: #ffffff;
        color: #111827;
        border-radius: 10px;
        padding: 12px 15px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-size: 14px;
        border: 1px solid #e5e7eb;
    }
    .service-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111827;
        color: #9ca3af;
        text-align: center;
        padding: 10px;
        font-size: 13px;
        border-top: 1px solid #1f2937;
        z-index: 100;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SYNCHRONISATION AVEC LES PARAMÈTRES URL (Anti-déconnexion au rafraîchissement) ---
params = st.query_params

if "connecte" not in st.session_state:
    st.session_state.connecte = params.get("connecte", "False") == "True"
if "username" not in st.session_state:
    st.session_state.username = params.get("username", "")
if "role" not in st.session_state:
    st.session_state.role = params.get("role", "")

if "page_active" not in st.session_state:
    st.session_state.page_active = "Connexion"

# Paramètres globaux de configuration (Admin)
if "config_admin" not in st.session_state:
    st.session_state.config_admin = {
        "heure_limite": time(9, 0),
        "rayon_gps": 50,
        "mode_maintenance": False,
        "alerte_retard": True
    }

# Initialisation de la base de données des employés en session
if "employes_df" not in st.session_state:
    st.session_state.employes_df = pd.DataFrame([
        {"ID": 1, "Nom": "Arnold Omam", "Utilisateur": "aomam", "Poste": "Développeur Senior", "Rôle": "Employé", "Statut": "Actif"},
        {"ID": 2, "Nom": "Valere Feugwang", "Utilisateur": "vfeugwang", "Poste": "Directeur Général", "Rôle": "Admin", "Statut": "Actif"},
        {"ID": 3, "Nom": "Jean Dupont", "Utilisateur": "jdupont", "Poste": "Technicien Réseau", "Rôle": "Employé", "Statut": "Actif"}
    ])

# Initialisation de l'historique des pointages
if "pointages_df" not in st.session_state:
    st.session_state.pointages_df = pd.DataFrame([
        {"Date": "2026-08-19", "Employé": "Arnold Omam", "Arrivée": "08:45", "Pause Début": "12:02", "Pause Fin": "13:00", "Départ": "17:05", "Statut": "À l'heure"},
        {"Date": "2026-08-19", "Employé": "Jean Dupont", "Arrivée": "09:15", "Pause Début": "12:10", "Pause Fin": "13:05", "Départ": "17:00", "Statut": "En retard"},
    ])

# --- SI L'UTILISATEUR N'EST PAS CONNECTÉ ---
if not st.session_state.connecte:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown("<p style='color: #9ca3af; font-size: 14px;'>Sécurité & Pointage GPS</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Navigation**")
        auth_mode = st.radio("", ["Connexion", "S'inscrire"], label_visibility="collapsed")

    col_logo, col_menu, col_btn = st.columns([1, 4, 1])
    with col_logo:
        st.markdown("### 🌐 ENGITAS")
    with col_menu:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            if st.button("Accueil"):
                st.session_state.page_active = "Connexion"
                st.rerun()
        with m2:
            if st.button("Services"):
                st.session_state.page_active = "Services"
                st.rerun()
        with m3:
            if st.button("Écosystème"):
                st.session_state.page_active = "Ecosysteme"
                st.rerun()
        with m4:
            if st.button("Présence géo"):
                st.session_state.page_active = "PresenceGeo"
                st.rerun()
        with m5:
            if st.button("Contact"):
                st.session_state.page_active = "Contact"
                st.rerun()
    with col_btn:
        st.button("Demander un devis")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.page_active == "PresenceGeo":
        st.markdown("<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>PRÉSENCE GÉOGRAPHIQUE</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Nous trouver</h1>", unsafe_allow_html=True)

        geo_col1, geo_col2 = st.columns([1.3, 1])
        with geo_col1:
            st.markdown(
                """
                <div style="border-radius: 12px; overflow: hidden; border: 1px solid #1e3a8a; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3980.772591691515!2d11.5305!3d3.8667!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zQsOhbnF1ZSBvdSBDaGFwZWxsZSBFc3NvcywgWWFvdW5kw6ksIENhbWVyb3Vu!5e0!3m2!1sfr!2sfr!4v1620000000000!5m2!1sfr!2sfr" width="100%" height="380" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with geo_col2:
            st.markdown(
                """
                <div class="location-card">
                    <h4>📍 Yaoundé</h4>
                    <p><b>Lieu-dit :</b> Chapelle ESSOS</p>
                    <p><b>B.P. :</b> 13820, Yaoundé</p>
                </div>
                <div class="location-card">
                    <h4>📍 Douala</h4>
                    <p><b>Lieu-dit :</b> Bali, en face station MRS</p>
                    <p><b>B.P. :</b> 13820, Yaoundé</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif st.session_state.page_active == "Contact":
        st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>📞 Contacts en cas de problème</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="login-container" style="text-align: center;">
                <p style="font-size: 18px; margin-bottom: 20px;">Besoin d'assistance ? Contactez les responsables ci-dessous :</p>
                <div style="background-color: #111827; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #374151;">
                    <h3 style="color: #38bdf8; margin-bottom: 5px;">ARNOLD OMAM</h3>
                    <p style="color: #9ca3af; margin: 0;">Développeur (DEV)</p>
                    <p style="font-size: 20px; font-weight: bold; color: #ffffff; margin-top: 10px;">📞 698 27 81 63</p>
                </div>
                <div style="background-color: #111827; padding: 20px; border-radius: 10px; border: 1px solid #374151;">
                    <h3 style="color: #38bdf8; margin-bottom: 5px;">Mr Valere FEUGWANG</h3>
                    <p style="color: #9ca3af; margin: 0;">Directeur Général (DG)</p>
                    <p style="font-size: 20px; font-weight: bold; color: #ffffff; margin-top: 10px;">📞 699 58 02 65</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif st.session_state.page_active == "Ecosysteme":
        st.markdown("<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>ÉCOSYSTÈME</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Partenaires technologiques</h1>", unsafe_allow_html=True)
        p1, p2, p3, p4, p5, p6, p7, p8 = st.columns(8)
        with p1: st.markdown('<div class="partner-badge">🪟 Microsoft</div>', unsafe_allow_html=True)
        with p2: st.markdown('<div class="partner-badge">🔵 IBM</div>', unsafe_allow_html=True)
        with p3: st.markdown('<div class="partner-badge">🟧 Proxmox</div>', unsafe_allow_html=True)
        with p4: st.markdown('<div class="partner-badge">🟥 Lenovo</div>', unsafe_allow_html=True)
        with p5: st.markdown('<div class="partner-badge">🌐 Dell EMC</div>', unsafe_allow_html=True)
        with p6: st.markdown('<div class="partner-badge">🔴 Oracle</div>', unsafe_allow_html=True)
        with p7: st.markdown('<div class="partner-badge">🔷 VMware</div>', unsafe_allow_html=True)
        with p8: st.markdown('<div class="partner-badge">🔴 Fortinet</div>', unsafe_allow_html=True)

    elif st.session_state.page_active == "Services":
        st.markdown("<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>NOS SERVICES</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Des solutions IT complètes et intégrées</h1>", unsafe_allow_html=True)
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        with row1_col1: st.markdown('<div class="service-card"><h3>🔍</h3><p><b>Audit & Conseil IT</b></p></div>', unsafe_allow_html=True)
        with row1_col2: st.markdown('<div class="service-card"><h3>🌐</h3><p><b>Infrastructure & Réseau</b></p></div>', unsafe_allow_html=True)
        with row1_col3: st.markdown('<div class="service-card"><h3>🛡️</h3><p><b>Cybersécurité</b></p></div>', unsafe_allow_html=True)
        with row1_col4: st.markdown('<div class="service-card"><h3>☁️</h3><p><b>Cloud Computing</b></p></div>', unsafe_allow_html=True)

    else:
        if auth_mode == "Connexion":
            st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Connexion à votre compte ENGITAS</h2>", unsafe_allow_html=True)
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            username_input = st.text_input("Nom d'utilisateur", placeholder="Nom d'utilisateur")
            password_input = st.text_input("Mot de passe", type="password", placeholder="Mot de passe")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Se connecter"):
                if username_input and password_input:
                    if username_input.strip().lower() == "admin" and password_input == "adminpassword":
                        st.session_state.connecte = True
                        st.session_state.username = "admin"
                        st.session_state.role = "admin"
                    else:
                        st.session_state.connecte = True
                        st.session_state.username = username_input
                        st.session_state.role = "employe"
                    
                    # Sauvegarde dans l'URL pour empêcher la déconnexion lors du rechargement
                    st.query_params["connecte"] = "True"
                    st.query_params["username"] = st.session_state.username
                    st.query_params["role"] = st.session_state.role
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Inscription - ENGITAS</h2>", unsafe_allow_html=True)
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            nom_inscrit = st.text_input("Nom complet", placeholder="Votre nom")
            user_inscrit = st.text_input("Nouvel utilisateur", placeholder="Nom d'utilisateur")
            pwd_inscrit = st.text_input("Nouveau mot de passe", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("S'inscrire"):
                if nom_inscrit and user_inscrit and pwd_inscrit:
                    if user_inscrit in st.session_state.employes_df["Utilisateur"].values:
                        st.warning("Cet utilisateur existe déjà !")
                    else:
                        nouvel_id = int(st.session_state.employes_df["ID"].max()) + 1
                        nouvel_employe = {
                            "ID": nouvel_id,
                            "Nom": nom_inscrit,
                            "Utilisateur": user_inscrit,
                            "Poste": "Employé",
                            "Rôle": "Employé",
                            "Statut": "Actif"
                        }
                        st.session_state.employes_df = pd.concat([st.session_state.employes_df, pd.DataFrame([nouvel_employe])], ignore_index=True)
                        st.success("Compte créé avec succès ! Il est instantanément visible dans l'espace admin.")
                else:
                    st.warning("Veuillez remplir tous les champs.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- SI L'UTILISATEUR EST CONNECTÉ ---
else:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown("<p style='color: #9ca3af; font-size: 14px;'>Sécurité & Pointage GPS</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"👤 **Connecté :**\n<span style='color: #38bdf8;'>{st.session_state.username}</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Navigation**")

        if st.session_state.role == "admin":
            options_menu = [
                "Tableau de bord",
                "Gestion des employés",
                "Admin",
                "Déconnexion",
            ]
        else:
            options_menu = [
                "Signer ma présence",
                "Départ Pause (12h)",
                "Retour Pause (13h)",
                "Pointer mon départ",
                "Déconnexion",
            ]

        menu_option = st.radio("", options_menu, label_visibility="collapsed")

        if menu_option == "Déconnexion":
            st.session_state.connecte = False
            st.session_state.username = ""
            st.session_state.role = ""
            # Nettoyage des paramètres URL à la déconnexion
            st.query_params.clear()
            st.rerun()

    col_logo, col_menu, col_btn = st.columns([1, 3, 1])
    with col_logo:
        st.markdown("### 🌐 ENGITAS")
    with col_btn:
        st.button("Demander un devis")

    st.markdown("<br>", unsafe_allow_html=True)

    if menu_option == "Signer ma présence":
        st.markdown("### 📝 Pointer mon Arrivée (Géolocalisation GPS Sécurisée & Limite 9h00)")
        st.error("⏳ POINTAGE FERMÉ : Il est plus de 09h00. Le pointage des arrivées n'est plus autorisé pour aujourd'hui.")
        
    elif menu_option == "Tableau de bord":
        st.markdown("### 📊 Tableau de bord de présence")
        st.markdown("<p style='color: #9ca3af;'>Suivi en temps réel des pointages et de l'assiduité des collaborateurs.</p>", unsafe_allow_html=True)
        
        df_affichage = st.session_state.pointages_df

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric(label="Total Collaborateurs", value=len(st.session_state.employes_df))
        with kpi2:
            st.metric(label="Présents aujourd'hui", value=2, delta="100%")
        with kpi3:
            st.metric(label="Arrivées à l'heure", value="75%", delta="-5%")
        with kpi4:
            st.metric(label="Retards enregistrés", value=1, delta="+1", delta_color="inverse")
            
        st.markdown("---")
        
        col_f1, col_f2 = st.columns([2, 2])
        with col_f1:
            recherche_employe = st.text_input("🔍 Rechercher un employé", placeholder="Nom...")
        with col_f2:
            filtre_statut = st.selectbox("Filtrer par statut", ["Tous", "À l'heure", "En retard"])
            
        if recherche_employe:
            df_affichage = df_affichage[df_affichage["Employé"].str.contains(recherche_employe, case=False, na=False)]
        if filtre_statut != "Tous":
            df_affichage = df_affichage[df_affichage["Statut"] == filtre_statut]

        st.markdown("#### Historique détaillé des pointages")
        st.dataframe(df_affichage, use_container_width=True, hide_index=True)

    elif menu_option == "Départ Pause (12h)":
        st.markdown("### ☕ Validation - Départ en Pause (12h)")
        if st.button("Valider mon départ en pause"):
            heure_actuelle = datetime.now().strftime("%H:%M")
            date_du_jour = datetime.now().strftime("%Y-%m-%d")
            nouvelle_ligne = {"Date": date_du_jour, "Employé": st.session_state.username.capitalize(), "Arrivée": "08:30", "Pause Début": heure_actuelle, "Pause Fin": "--:--", "Départ": "--:--", "Statut": "À l'heure"}
            st.session_state.pointages_df = pd.concat([pd.DataFrame([nouvelle_ligne]), st.session_state.pointages_df], ignore_index=True)
            st.success(f"✅ Départ en pause validé avec succès à {heure_actuelle} !")

    elif menu_option == "Retour Pause (13h)":
        st.markdown("### 💻 Validation - Retour de Pause (13h)")
        if st.button("Valider mon retour de pause"):
            heure_actuelle = datetime.now().strftime("%H:%M")
            st.success(f"✅ Retour de pause validé avec succès à {heure_actuelle} !")

    elif menu_option == "Pointer mon départ":
        st.markdown("### 🚪 Validation - Départ de la Journée")
        if st.button("Valider mon départ"):
            heure_actuelle = datetime.now().strftime("%H:%M")
            st.success(f"✅ Départ de la journée enregistré à {heure_actuelle}.")

    elif menu_option == "Gestion des employés":
        st.markdown("### 👥 Gestion des employés inscrits (Admin)")
        st.markdown("<p style='color: #9ca3af;'>Liste complète de tous les employés et inscrits de la plateforme :</p>", unsafe_allow_html=True)
        edited_df = st.data_editor(
            st.session_state.employes_df,
            num_rows="dynamic",
            use_container_width=True,
            key="employee_editor"
        )
        st.session_state.employes_df = edited_df
        
        if st.button("💾 Enregistrer les modifications"):
            st.success("La base des employés a été mise à jour avec succès !")

    elif menu_option == "Admin":
        st.markdown("### ⚙️ Liste des employés inscrits & Paramètres de l'application (Admin)")
        
        st.markdown("#### 📋 Répertoire des noms inscrits")
        st.dataframe(st.session_state.employes_df[["ID", "Nom", "Utilisateur", "Rôle", "Statut"]], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("#### 🛠️ Configuration générale")
        with st.form("form_admin_params"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                new_heure_limite = st.time_input("Heure limite d'arrivée", value=st.session_state.config_admin["heure_limite"])
                new_rayon_gps = st.slider("Rayon GPS (mètres)", 10, 500, value=st.session_state.config_admin["rayon_gps"])
            with col_p2:
                new_mode_maintenance = st.toggle("Mode maintenance", value=st.session_state.config_admin["mode_maintenance"])
                new_alerte_retard = st.toggle("Notifications de retard", value=st.session_state.config_admin["alerte_retard"])
            
            if st.form_submit_button("💾 Sauvegarder les paramètres"):
                st.session_state.config_admin["heure_limite"] = new_heure_limite
                st.session_state.config_admin["rayon_gps"] = new_rayon_gps
                st.success("Paramètres mis à jour avec succès !")

# --- PIED DE PAGE ---
st.markdown(
    """
    <div class="footer">
        Design & Développement by <b>ARNOLD OMAM</b> | ENGITAS 2026
    </div>
    """,
    unsafe_allow_html=True,
)