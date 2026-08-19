import streamlit as st
import pandas as pd
from datetime import time

# Configuration de la page
st.set_page_config(
    page_title="ENGITAS - Système de Présence",
    page_icon="🛡️",
    layout="wide",
)

# Injection du CSS personnalisé inspiré de votre site web
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
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #1e3a8a; border-radius: 16px;
        padding: 20px; text-align: center; height: 170px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4); margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .service-card:hover { border-color: #0284c7; transform: translateY(-3px); }
    .partner-badge {
        background-color: #ffffff; color: #111827; border-radius: 8px; padding: 10px 12px;
        text-align: center; font-weight: bold; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        margin-bottom: 12px; display: flex; align-items: center; justify-content: center;
        font-size: 13px; border: 1px solid #e5e7eb;
    }
    .location-card {
        background-color: #111827; border: 1px solid #1e3a8a; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
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
        {"ID": 3, "Nom": "Jean Dupont", "Utilisateur": "jdupont", "Poste": "Technicien Réseau", "Rôle": "Employé", "Statut": "Actif"}
    ])

# --- LOGIQUE D'AFFICHAGE ---
if not st.session_state.connecte:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown("---")
        st.write("Navigation rapide :")
        if st.button("🔑 Connexion / Espace Admin"): st.session_state.page_active = "Connexion"; st.rerun()

    # Barre de menu horizontale principale identique au site
    col_logo, col_menu, col_btn = st.columns([1, 4, 1])
    with col_logo: st.markdown("### 🌐 ENGITAS")
    with col_menu:
        m1, m2, m3, m4, m5 = st.columns(5)
        if m1.button("Accueil"): st.session_state.page_active = "Accueil"; st.rerun()
        if m2.button("Services"): st.session_state.page_active = "Services"; st.rerun()
        if m3.button("Écosystème"): st.session_state.page_active = "Ecosysteme"; st.rerun()
        if m4.button("Présence géo"): st.session_state.page_active = "PresenceGeo"; st.rerun()
        if m5.button("Contact"): st.session_state.page_active = "Contact"; st.rerun()
    with col_btn:
        if st.button("Demander un devis"): st.session_state.page_active = "Contact"; st.rerun()

    st.markdown("---")

    # --- PAGES PUBLIQUES ---
    if st.session_state.page_active == "Accueil" or st.session_state.page_active == "Connexion":
        st.markdown("<h1 style='text-align: center;'>Des solutions IT complètes et intégrées</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>De l'audit stratégique à la cybersécurité, nous couvrons l'ensemble de vos besoins informatiques avec des solutions sur mesure.</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown("### 🔐 Espace de Connexion")
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter au système"):
                st.session_state.connecte = True
                st.session_state.username = username
                st.session_state.role = "admin" if username == "admin" else "employe"
                st.rerun()
        with col_c2:
            st.info("💡 **Astuce de connexion :**\n\n- Entrez `admin` pour accéder au panneau de configuration.\n- Entrez tout autre identifiant pour l'espace collaborateur.")

    elif st.session_state.page_active == "Services":
        st.markdown("<h2 style='text-align: center;'>Nos Domaines d'Expertise</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 30px;'>Découvrez l'ensemble de nos services professionnels intégrés.</p>", unsafe_allow_html=True)
        
        # Grille des 8 services de votre capture d'écran
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
        with r1_c1: st.markdown('<div class="service-card"><h4>01</h4><p><b>Audit & Conseil IT</b></p></div>', unsafe_allow_html=True)
        with r1_c2: st.markdown('<div class="service-card"><h4>02</h4><p><b>Infrastructure & Réseau</b></p></div>', unsafe_allow_html=True)
        with r1_c3: st.markdown('<div class="service-card"><h4>03</h4><p><b>Cybersécurité</b></p></div>', unsafe_allow_html=True)
        with r1_c4: st.markdown('<div class="service-card"><h4>04</h4><p><b>Cloud Computing</b></p></div>', unsafe_allow_html=True)

        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        with r2_c1: st.markdown('<div class="service-card"><h4>05</h4><p><b>Services Managés</b></p></div>', unsafe_allow_html=True)
        with r2_c2: st.markdown('<div class="service-card"><h4>06</h4><p><b>Environnement Utilisateur</b></p></div>', unsafe_allow_html=True)
        with r2_c3: st.markdown('<div class="service-card"><h4>07</h4><p><b>Solutions Logicielles & Data</b></p></div>', unsafe_allow_html=True)
        with r2_c4: st.markdown('<div class="service-card"><h4>08</h4><p><b>Formation & Certifications</b></p></div>', unsafe_allow_html=True)

    elif st.session_state.page_active == "Ecosysteme":
        st.markdown("<h2 style='text-align: center;'>Nos partenaires technologiques</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 30px;'>Nous nous appuyons sur les meilleurs éditeurs et constructeurs pour vous offrir des solutions fiables.</p>", unsafe_allow_html=True)
        
        # Affichage des badges partenaires similaires à votre capture
        p_cols = st.columns(6)
        partners = ["Microsoft", "IBM", "Proxmox", "Lenovo", "Dell EMC", "Oracle", "VMware", "Fortinet", "Veeam", "NetApp", "Huawei", "Cisco"]
        for i, partner in enumerate(partners):
            with p_cols[i % 6]:
                st.markdown(f'<div class="partner-badge">🛡️ {partner}</div>', unsafe_allow_html=True)

        st.markdown("<br><h3 style='text-align: center;'>Ils nous font confiance</h3>", unsafe_allow_html=True)
        c_cols = st.columns(6)
        clients = ["COBAC", "Orange", "CFAO Mobility", "BICEC", "CORIS Bank", "BEAC"]
        for i, client in enumerate(clients):
            with c_cols[i % 6]:
                st.markdown(f'<div class="partner-badge" style="background:#1f2937; color:#ffffff;">🏢 {client}</div>', unsafe_allow_html=True)

    elif st.session_state.page_active == "PresenceGeo":
        st.markdown("<h2 style='text-align: center;'>PRÉSENCE GÉOGRAPHIQUE</h2>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0284c7;'>Nous trouver</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col_map, col_info = st.columns([1.2, 1])
        with col_map:
            st.markdown('<div class="location-card"><h4>📍 Chapelle Essos, Yaoundé</h4><p style="color:#9ca3af;">VGFP+6RW, Unnamed Rd, Yaoundé, Cameroun</p></div>', unsafe_allow_html=True)
            # Intégration d'une carte géographique fictive ou centrée sur le Cameroun
            st.map(pd.DataFrame({'lat': [3.8480, 4.0511], 'lon': [11.5021, 9.7679]}))
        with col_info:
            st.markdown("""
            <div class="location-card">
                <h3>📍 Yaoundé</h3>
                <p><b>Lieu-dit :</b> Chapelle ESSOS<br><b>B.P. :</b> 13820, Yaoundé</p>
            </div>
            <div class="location-card">
                <h3>📍 Douala</h3>
                <p><b>Lieu-dit :</b> Bali, en face station MRS<br><b>B.P. :</b> 13820, Yaoundé</p>
            </div>
            <p style="color:#9ca3af;">📞 +237 699 580 265 / +237 699 361 756<br>✉️ contact@engitas.com</p>
            """, unsafe_allow_html=True)

    elif st.session_state.page_active == "Contact":
        st.markdown("<h2 style='text-align: center;'>Contactez-nous / Demande de devis</h2>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.text_input("Nom complet")
            st.text_input("Adresse Email")
        with col_f2:
            st.text_input("Téléphone")
            st.text_input("Objet de la demande")
        st.text_area("Votre Message ou expression de besoin")
        st.button("Envoyer ma demande")

else:
    # --- ESPACE CONNECTÉ (ADMIN / EMPLOYÉ) ---
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.username}**")
        st.markdown("---")
        if st.session_state.role == "admin":
            options_menu = ["Tableau de bord", "Gestion des employés", "Admin", "Déconnexion"]
        else:
            options_menu = ["Signer ma présence", "Déconnexion"]
        
        menu_option = st.radio("Navigation interne", options_menu)
        if menu_option == "Déconnexion":
            st.session_state.connecte = False; st.rerun()

    if menu_option == "Admin":
        st.markdown("### ⚙️ Panneau de Configuration Système")
        tab1, tab2, tab3, tab4 = st.tabs(["🕒 Paramètres", "📍 Zones GPS", "📜 Logs Audit", "📥 Rapports"])

        with tab1:
            st.markdown("#### Configuration des heures")
            heure_limite = st.time_input("Heure limite d'arrivée", value=time(9, 0))
            if st.button("Sauvegarder les horaires"): st.success(f"Heure limite mise à jour : {heure_limite}")

        with tab2:
            st.markdown("#### Gestion des sites")
            nom_site = st.text_input("Nom du site")
            lat = st.number_input("Latitude", format="%.6f")
            lon = st.number_input("Longitude", format="%.6f")
            if st.button("Ajouter Site"): st.info(f"Site {nom_site} enregistré avec succès.")

        with tab3:
            st.markdown("#### 📜 Journaux d'activité")
            logs = pd.DataFrame({
                "Date": ["2026-08-19 08:45", "2026-08-19 09:12"],
                "Action": ["Connexion Admin", "Tentative d'accès hors délai"]
            })
            st.table(logs)

        with tab4:
            st.markdown("#### 📥 Exportation des rapports de présence")
            csv = st.session_state.employes_df.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger le rapport CSV", data=csv, file_name='rapport_engitas.csv', mime='text/csv')

    elif menu_option == "Gestion des employés":
        st.markdown("### 👥 Gestion des Collaborateurs")
        st.session_state.employes_df = st.data_editor(st.session_state.employes_df, num_rows="dynamic")
    
    else:
        st.markdown(f"### Espace Collaborateur : {menu_option}")
        st.success("Vous êtes connecté au système de pointage ENGITAS.")

st.markdown('<div class="footer">Design by <b>ARNOLD OMAM</b> | ENGITAS 2026</div>', unsafe_allow_html=True)