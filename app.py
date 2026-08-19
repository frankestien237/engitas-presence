import streamlit as st

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
    .login-container { background-color: #0b0f19; border: 2px solid #1e3a8a; border-radius: 16px; padding: 40px; box-shadow: 0 0 25px rgba(30, 58, 138, 0.4); max-width: 700px; margin: auto; }
    .stButton>button { background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%); color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem; font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4); }
    h1, h2, h3 { color: #ffffff; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #111827; color: #9ca3af; text-align: center; padding: 10px; font-size: 13px; border-top: 1px solid #1f2937; z-index: 100; }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialisation de la session
if "connecte" not in st.session_state: st.session_state.connecte = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = ""

# Initialisation de la liste des employés en session
if "employes_list" not in st.session_state:
    st.session_state.employes_list = [
        {"nom": "Jean Dupont", "username": "jdupont", "poste": "Non attribué"},
        {"nom": "Marie Curie", "username": "mcurie", "poste": "Non attribué"},
    ]

# --- SI L'UTILISATEUR N'EST PAS CONNECTÉ ---
if not st.session_state.connecte:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        auth_mode = st.radio("Mode", ["Connexion", "S'inscrire"], label_visibility="collapsed")
    
    if auth_mode == "Connexion":
        st.markdown("<h2 style='text-align: center;'>Connexion ENGITAS</h2>", unsafe_allow_html=True)
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            if username.lower() == "admin" and password == "adminpassword":
                st.session_state.connecte = True
                st.session_state.username = username
                st.session_state.role = "admin"
                st.rerun()
            elif username:
                st.session_state.connecte = True
                st.session_state.username = username
                st.session_state.role = "employe"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif auth_mode == "S'inscrire":
        st.markdown("<h2 style='text-align: center;'>Inscription Employé - ENGITAS</h2>", unsafe_allow_html=True)
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        nom_complet = st.text_input("Nom complet")
        new_username = st.text_input("Nom d'utilisateur souhaité")
        new_password = st.text_input("Mot de passe", type="password")
        
        if st.button("Créer mon compte"):
            if nom_complet and new_username and new_password:
                # Ajout du nouvel employé dans la liste globale
                st.session_state.employes_list.append({
                    "nom": nom_complet, 
                    "username": new_username, 
                    "poste": "Non attribué"
                })
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            else:
                st.error("Veuillez remplir tous les champs.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- SI L'UTILISATEUR EST CONNECTÉ ---
else:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown(f"👤 **Connecté :** <span style='color: #38bdf8;'>{st.session_state.username}</span>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.session_state.role == "admin":
            options_menu = ["Tableau de bord", "Gestion des employés", "Admin", "Déconnexion"]
        else:
            options_menu = ["Signer ma présence", "Départ Pause (12h)", "Retour Pause (13h)", "Pointer mon départ", "Déconnexion"]
        
        menu_option = st.radio("Navigation", options_menu)

        if menu_option == "Déconnexion":
            st.session_state.connecte = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

    # --- LOGIQUE D'AFFICHAGE DES PAGES ---
    st.markdown(f"## {menu_option}")
    
    if menu_option == "Signer ma présence":
        st.error("⏳ POINTAGE FERMÉ : Il est plus de 09h00.")
        
    elif menu_option == "Départ Pause (12h)":
        if st.button("Confirmer départ en pause"):
            st.success("Départ en pause enregistré.")
            
    elif menu_option == "Retour Pause (13h)":
        if st.button("Confirmer retour de pause"):
            st.success("Retour de pause enregistré.")
            
    elif menu_option == "Pointer mon départ":
        if st.button("Confirmer mon départ"):
            st.success("Départ enregistré. Bonne soirée !")
            
    elif menu_option == "Tableau de bord":
        st.write("📊 Vue d'ensemble des présences (Réservé Admin).")
        
    elif menu_option == "Gestion des employés":
        st.markdown("### 👥 Gestion des employés & Attribution des postes")

        # Affichage et modification interactive pour chaque employé inscrit
        for i, emp in enumerate(st.session_state.employes_list):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"**Nom:** {emp['nom']} ({emp['username']})")
            with col2:
                liste_postes = ["Non attribué", "Développeur", "Comptable", "Commercial", "RH"]
                try:
                    current_index = liste_postes.index(emp["poste"])
                except ValueError:
                    current_index = 0

                nouveau_poste = st.selectbox(
                    f"Poste pour {emp['username']}",
                    liste_postes,
                    index=current_index,
                    key=f"poste_{i}",
                )
            with col3:
                if st.button("Enregistrer", key=f"btn_{i}"):
                    st.session_state.employes_list[i]["poste"] = nouveau_poste
                    st.success(f"Poste mis à jour pour {emp['nom']} !")
        
    elif menu_option == "Admin":
        st.write("⚙️ Paramètres système.")

# --- PIED DE PAGE ---
st.markdown('<div class="footer">Design & Développement by <b>ARNOLD OMAM</b> | ENGITAS 2026</div>', unsafe_allow_html=True)