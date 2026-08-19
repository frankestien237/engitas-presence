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
    /* Style des cartes de localisation géographique */
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
    /* Style des badges de partenaires et cartes de confiance */
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
    .trust-card {
        background-color: #ffffff;
        color: #111827;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .trust-card h4 {
        color: #111827;
        margin: 0 0 5px 0;
        font-size: 16px;
    }
    .trust-card p {
        color: #6b7280;
        margin: 0;
        font-size: 13px;
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
    /* Style du pied de page */
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

# Initialisation de la session
if "connecte" not in st.session_state:
    st.session_state.connecte = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "page_active" not in st.session_state:
    st.session_state.page_active = "Connexion"

# --- SI L'UTILISATEUR N'EST PAS CONNECTÉ ---
if not st.session_state.connecte:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown(
            "<p style='color: #9ca3af; font-size: 14px;'>Sécurité & Pointage GPS</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown("**Navigation**")
        auth_mode = st.radio(
            "", ["Connexion", "S'inscrire"], label_visibility="collapsed"
        )

    # En-tête supérieur avec menu complet (Accueil, Services, Écosystème, Contact, Présence géographique)
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

    # Affichage selon la page active
    if st.session_state.page_active == "PresenceGeo":
        st.markdown(
            "<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>PRÉSENCE GÉOGRAPHIQUE</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 40px;'>Nous trouver</h1>",
            unsafe_allow_html=True,
        )

        geo_col1, geo_col2 = st.columns([1.3, 1])

        with geo_col1:
            # Intégration de la carte interactive Google Maps (Chapelle Essos, Yaoundé)
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
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div class="location-card">
                    <h4>📍 Douala</h4>
                    <p><b>Lieu-dit :</b> Bali, en face station MRS</p>
                    <p><b>B.P. :</b> 13820, Yaoundé</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        inf_col1, inf_col2 = st.columns(2)
        with inf_col1:
            st.markdown(
                """
                <div style="background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937;">
                    <p style="margin: 0; color: #38bdf8; font-weight: bold;">📞 Téléphones :</p>
                    <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 14px;">
                        +237 699 580 265 / +237 699 361 756<br>
                        +237 691 797 770 / +237 699 683 833<br>
                        +237 222 226 190
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with inf_col2:
            st.markdown(
                """
                <div style="background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937;">
                    <p style="margin: 0; color: #38bdf8; font-weight: bold;">✉️ Emails & Web :</p>
                    <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 14px;">
                        contact@engitas.com<br>
                        support@engitas.com<br>
                        www.engitas.com
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif st.session_state.page_active == "Contact":
        st.markdown(
            "<h2 style='text-align: center; margin-bottom: 20px;'>📞 Contacts en cas de problème</h2>",
            unsafe_allow_html=True,
        )
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
        st.markdown(
            "<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>ÉCOSYSTÈME</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 10px;'>Partenaires technologiques</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: #9ca3af; margin-bottom: 30px;'>Les meilleurs éditeurs et constructeurs pour des solutions fiables et éprouvées.</p>",
            unsafe_allow_html=True,
        )

        p1, p2, p3, p4, p5, p6, p7, p8 = st.columns(8)
        with p1:
            st.markdown(
                '<div class="partner-badge">🪟 Microsoft</div>',
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                '<div class="partner-badge">🔵 IBM</div>',
                unsafe_allow_html=True,
            )
        with p3:
            st.markdown(
                '<div class="partner-badge">🟧 Proxmox</div>',
                unsafe_allow_html=True,
            )
        with p4:
            st.markdown(
                '<div class="partner-badge">🟥 Lenovo</div>',
                unsafe_allow_html=True,
            )
        with p5:
            st.markdown(
                '<div class="partner-badge">🌐 Dell EMC</div>',
                unsafe_allow_html=True,
            )
        with p6:
            st.markdown(
                '<div class="partner-badge">🔴 Oracle</div>',
                unsafe_allow_html=True,
            )
        with p7:
            st.markdown(
                '<div class="partner-badge">🔷 VMware</div>',
                unsafe_allow_html=True,
            )
        with p8:
            st.markdown(
                '<div class="partner-badge">🔴 Fortinet</div>',
                unsafe_allow_html=True,
            )

        q1, q2, q3, q4, q5, q6, q7 = st.columns(7)
        with q1:
            st.markdown(
                '<div class="partner-badge">🟩 Veeam</div>',
                unsafe_allow_html=True,
            )
        with q2:
            st.markdown(
                '<div class="partner-badge">🟣 SentinelOne</div>',
                unsafe_allow_html=True,
            )
        with q3:
            st.markdown(
                '<div class="partner-badge">⬛ NetApp</div>',
                unsafe_allow_html=True,
            )
        with q4:
            st.markdown(
                '<div class="partner-badge">📈 ManageEngine</div>',
                unsafe_allow_html=True,
            )
        with q5:
            st.markdown(
                '<div class="partner-badge">🩷 Check Point</div>',
                unsafe_allow_html=True,
            )
        with q6:
            st.markdown(
                '<div class="partner-badge">🔴 Trend Micro</div>',
                unsafe_allow_html=True,
            )
        with q7:
            st.markdown(
                '<div class="partner-badge">🟢 Kaspersky</div>',
                unsafe_allow_html=True,
            )

        r1, r2, r3, r4, r5, r6, r7, r8 = st.columns(8)
        with r1:
            st.markdown(
                '<div class="partner-badge">🔴 Symantec</div>',
                unsafe_allow_html=True,
            )
        with r2:
            st.markdown(
                '<div class="partner-badge">🔴 Broadcom</div>',
                unsafe_allow_html=True,
            )
        with r3:
            st.markdown(
                '<div class="partner-badge"> Hewlett Packard Enterprise</div>',
                unsafe_allow_html=True,
            )
        with r4:
            st.markdown(
                '<div class="partner-badge">🟧 Wallix</div>',
                unsafe_allow_html=True,
            )
        with r5:
            st.markdown(
                '<div class="partner-badge">⬛ CyberArk</div>',
                unsafe_allow_html=True,
            )
        with r6:
            st.markdown(
                '<div class="partner-badge">🟥 Huawei</div>',
                unsafe_allow_html=True,
            )
        with r7:
            st.markdown(
                '<div class="partner-badge">🔴 Ricoh</div>',
                unsafe_allow_html=True,
            )
        with r8:
            st.markdown(
                '<div class="partner-badge">🟦 Cisco</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>CONFIANCE</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h2 style='text-align: center; margin-bottom: 40px;'>Ils nous font confiance</h2>",
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<div class="trust-card"><h4>COBAC</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>CORIS Bank</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>CCEI Bank</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>La Regionale</h4><p>Assurance</p></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                '<div class="trust-card"><h4>Orange</h4><p>Télécommunications</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>Attijariwafa Bank</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>Vision Finance</h4><p>Microfinance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>OAPI</h4><p>Institution Publique</p></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                '<div class="trust-card"><h4>CFAO Mobility</h4><p>Automobile</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>BANGE Bank</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>GroupeSNEF</h4><p>Industrie</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>BHT</h4><p>Hôtellerie & Tourisme</p></div>',
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                '<div class="trust-card"><h4>BICEC</h4><p>Banque & Finance</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>BEAC</h4><p>Institution Financière</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="trust-card"><h4>BC-PME SA</h4><p>Institution Financière</p></div>',
                unsafe_allow_html=True,
            )

    elif st.session_state.page_active == "Services":
        st.markdown(
            "<p style='text-align: center; color: #38bdf8; font-weight: bold; letter-spacing: 2px;'>NOS SERVICES</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 10px;'>Des solutions IT complètes et intégrées</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: #9ca3af; margin-bottom: 40px;'>De l'audit stratégique à la cybersécurité, nous couvrons l'ensemble de vos besoins informatiques avec des solutions sur mesure.</p>",
            unsafe_allow_html=True,
        )

        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        with row1_col1:
            st.markdown(
                '<div class="service-card"><h3>🔍</h3><p><b>Audit & Conseil IT</b></p></div>',
                unsafe_allow_html=True,
            )
        with row1_col2:
            st.markdown(
                '<div class="service-card"><h3>🌐</h3><p><b>Infrastructure & Réseau</b></p></div>',
                unsafe_allow_html=True,
            )
        with row1_col3:
            st.markdown(
                '<div class="service-card"><h3>🛡️</h3><p><b>Cybersécurité</b></p></div>',
                unsafe_allow_html=True,
            )
        with row1_col4:
            st.markdown(
                '<div class="service-card"><h3>☁️</h3><p><b>Cloud Computing</b></p></div>',
                unsafe_allow_html=True,
            )

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        with row2_col1:
            st.markdown(
                '<div class="service-card"><h3>💻</h3><p><b>Services Managés</b></p></div>',
                unsafe_allow_html=True,
            )
        with row2_col2:
            st.markdown(
                '<div class="service-card"><h3>👥</h3><p><b>Environnement Utilisateur</b></p></div>',
                unsafe_allow_html=True,
            )
        with row2_col3:
            st.markdown(
                '<div class="service-card"><h3>⚡</h3><p><b>Solutions Logicielles & Data</b></p></div>',
                unsafe_allow_html=True,
            )
        with row2_col4:
            st.markdown(
                '<div class="service-card"><h3>🎓</h3><p><b>Formation & Certifications</b></p></div>',
                unsafe_allow_html=True,
            )

    else:
        if auth_mode == "Connexion":
            st.markdown(
                "<h2 style='text-align: center; margin-bottom: 30px;'>Connexion à votre compte ENGITAS</h2>",
                unsafe_allow_html=True,
            )
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            username = st.text_input(
                "Nom d'utilisateur", placeholder="Nom d'utilisateur"
            )
            password = st.text_input(
                "Mot de passe", type="password", placeholder="Mot de passe"
            )
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Se connecter"):
                if username and password:
                    if (
                        username.lower() == "admin"
                        and password == "adminpassword"
                    ):
                        st.session_state.connecte = True
                        st.session_state.username = username
                        st.session_state.role = "admin"
                        st.rerun()
                    else:
                        st.session_state.connecte = True
                        st.session_state.username = username
                        st.session_state.role = "employe"
                        st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<h2 style='text-align: center; margin-bottom: 30px;'>Inscription - ENGITAS</h2>",
                unsafe_allow_html=True,
            )
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.text_input("Nom complet", placeholder="Votre nom")
            st.text_input("Nouvel utilisateur", placeholder="Nom d'utilisateur")
            st.text_input("Nouveau mot de passe", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("S'inscrire"):
                st.success(
                    "Compte créé avec succès ! Vous pouvez vous connecter."
                )
            st.markdown("</div>", unsafe_allow_html=True)

# --- SI L'UTILISATEUR EST CONNECTÉ ---
else:
    with st.sidebar:
        st.markdown("### **ENGITAS**")
        st.markdown(
            "<p style='color: #9ca3af; font-size: 14px;'>Sécurité & Pointage GPS</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(
            f"👤 **Connecté :**\n<span style='color: #38bdf8;'>{st.session_state.username}</span>",
            unsafe_allow_html=True,
        )
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

        menu_option = st.radio(
            "", options_menu, label_visibility="collapsed"
        )

        if menu_option == "Déconnexion":
            st.session_state.connecte = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

    col_logo, col_menu, col_btn = st.columns([1, 3, 1])
    with col_logo:
        st.markdown("### 🌐 ENGITAS")
    with col_btn:
        st.button("Demander un devis")

    st.markdown("<br>", unsafe_allow_html=True)

    if menu_option == "Signer ma présence":
        st.markdown(
            "### 📝 Pointer mon Arrivée (Géolocalisation GPS Sécurisée & Limite 9h00)"
        )
        st.error(
            "⏳ POINTAGE FERMÉ : Il est plus de 09h00. Le pointage des arrivées n'est plus autorisé pour aujourd'hui."
        )
    elif menu_option == "Tableau de bord":
        st.markdown("### 📊 Tableau de bord de présence")
        st.info("Ici s'affiche l'historique de vos pointages.")
    elif menu_option == "Gestion des employés":
        st.markdown("### 👥 Gestion des employés (Admin)")
        st.info("Interface d'administration des comptes employés.")
    else:
        st.markdown(f"### Section : {menu_option}")
        st.info(
            "Cette section est prête à intégrer vos fonctionnalités de pointage."
        )

# --- PIED DE PAGE FIXE EN BAS ---
st.markdown(
    """
    <div class="footer">
        Design & Développement by <b>ARNOLD OMAM</b> | ENGITAS 2026
    </div>
    """,
    unsafe_allow_html=True,
)