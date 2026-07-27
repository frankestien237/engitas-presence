from datetime import datetime
import json
import os
import random
from geopy.distance import geodesic
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🛡️", layout="wide"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .stButton>button {
        background-color: #00b4d8;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0096c7;
        color: #ffffff;
    }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .hero-container {
        background: linear-gradient(135deg, rgba(14, 17, 23, 0.95) 0%, rgba(22, 27, 34, 0.95) 100%), 
                    url('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #30363d;
        color: white;
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
    }
    .hero-highlight {
        color: #00b4d8;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #a0a0a0;
        margin-top: 10px;
        margin-bottom: 20px;
        max-width: 700px;
    }
    .card-grid {
        display: flex;
        gap: 15px;
        margin-top: 15px;
    }
    .info-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        flex: 1;
        text-align: center;
    }
    .info-card h3 {
        color: #00b4d8;
        margin: 0;
        font-size: 20px;
    }
    .info-card p {
        color: #c9d1d9;
        font-size: 13px;
        margin: 5px 0 0 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- COORDONNÉES DE RÉFÉRENCE ---
CENTRE_LAT = 4.0511
CENTRE_LON = 9.7679
RAYON_AUTORISE_KM = 1.0

FICHIER_UTILISATEURS = "utilisateurs.json"
FICHIER_PRESENCES = "presences.json"


def charger_utilisateurs():
    if os.path.exists(FICHIER_UTILISATEURS):
        with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        users_defaut = {
            "admin": {
                "mdp": "1234",
                "role": "Administrateur",
            },
            "employe1": {
                "mdp": "abcd",
                "role": "Employé",
            },
        }
        sauvegarder_utilisateurs(users_defaut)
        return users_defaut


def sauvegarder_utilisateurs(users):
    with open(FICHIER_UTILISATEURS, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def charger_presences():
    if os.path.exists(FICHIER_PRESENCES):
        with open(FICHIER_PRESENCES, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []


def sauvegarder_presences(presences):
    with open(FICHIER_PRESENCES, "w", encoding="utf-8") as f:
        json.dump(presences, f, indent=4, ensure_ascii=False)


if "utilisateurs" not in st.session_state:
    st.session_state.utilisateurs = charger_utilisateurs()

if "presences" not in st.session_state:
    st.session_state.presences = charger_presences()

# --- BARRE LATÉRALE ---
if os.path.exists("logo_engitas.png"):
    st.sidebar.image("logo_engitas.png", width="stretch")
else:
    st.sidebar.markdown(
        "<h2 style='color: #00b4d8;'>ENGITAS</h2>", unsafe_allow_html=True
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
    # Affichage de la bannière style ENGITAS sur la page d'accueil/connexion
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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h3 style='text-align: center; color: #ffffff;'>🔐 Espace de Connexion</h3>",
            unsafe_allow_html=True,
        )

        with st.form("form_connexion"):
            identifiant = st.text_input("Nom d'utilisateur")
            mdp = st.text_input("Mot de passe", type="password")
            valider = st.form_submit_button("Se connecter", use_container_width=True)

            if valider:
                if identifiant in st.session_state.utilisateurs:
                    if (
                        st.session_state.utilisateurs[identifiant].get("mdp")
                        == mdp
                    ):
                        st.session_state.user_connecte = identifiant
                        st.success("Connexion réussie !")
                        st.rerun()
                    else:
                        st.error("Mot de passe incorrect.")
                else:
                    st.error("Utilisateur introuvable.")

# --- 2. INSCRIPTION ---
elif menu == "S'inscrire":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: #00b4d8;'>ENGITAS</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #ffffff;'>📝 Inscription Employé</h3>",
            unsafe_allow_html=True,
        )
        with st.form("form_inscription"):
            nouveau_nom = st.text_input("Nom d'utilisateur")
            nouveau_mdp = st.text_input("Mot de passe", type="password")
            valider_insc = st.form_submit_button("S'inscrire", use_container_width=True)

            if valider_insc:
                if nouveau_nom and nouveau_mdp:
                    if nouveau_nom in st.session_state.utilisateurs:
                        st.error("Ce nom d'utilisateur existe déjà.")
                    else:
                        st.session_state.utilisateurs[nouveau_nom] = {
                            "mdp": nouveau_mdp,
                            "role": "Employé",
                        }
                        sauvegarder_utilisateurs(st.session_state.utilisateurs)
                        st.success(
                            "Compte créé avec succès ! Vous pouvez vous connecter."
                        )
                else:
                    st.warning("Veuillez remplir tous les champs.")

# --- 3. SIGNER LA PRÉSENCE (ARRIVÉE) ---
elif menu == "Signer ma présence":
    st.markdown(
        "<h1 style='color: #00b4d8;'>ENGITAS - Validation de présence (Arrivée)</h1>",
        unsafe_allow_html=True,
    )

    components.html(
        """
        <div id="clock" style="color: #00b4d8; font-family: monospace; font-size: 16px; margin-bottom: 10px;"></div>
        <script>
            function updateTime() {
                const now = new Date();
                const yyyy = now.getFullYear();
                const mm = String(now.getMonth() + 1).padStart(2, '0');
                const dd = String(now.getDate()).padStart(2, '0');
                const hh = String(now.getHours()).padStart(2, '0');
                const min = String(now.getMinutes()).padStart(2, '0');
                const ss = String(now.getSeconds()).padStart(2, '0');
                const timeStr = `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
                document.getElementById('clock').innerText = "🕒 Heure synchronisée de votre appareil : " + timeStr;
            }
            updateTime();
            setInterval(updateTime, 1000);
        </script>
        """,
        height=40,
    )

    role_user = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]
    maintenant = datetime.now()
    acces_autorise = True

    if role_user == "Employé":
        st.info(
            "🕒 **Horaires d'ouverture ENGITAS :** Du lundi au vendredi, de 08h00 à 17h00."
        )
        jour_semaine = maintenant.weekday()
        heure_actuelle_time = maintenant.time()

        heure_ouverture = datetime.strptime("08:00:00", "%H:%M:%S").time()
        heure_fermeture = datetime.strptime("17:00:00", "%H:%M:%S").time()

        est_un_jour_ouvrable = 0 <= jour_semaine <= 4
        est_dans_la_plage_horaire = (
            heure_ouverture <= heure_actuelle_time <= heure_fermeture
        )

        if not est_un_jour_ouvrable or not est_dans_la_plage_horaire:
            acces_autorise = False
            st.error(
                "❌ Le système de pointage ENGITAS est actuellement fermé pour les employés."
            )
    else:
        st.info(
            "ℹ️ Compte Administrateur ENGITAS : Accès permanent sans restriction."
        )

    if acces_autorise:
        st.markdown(
            "### Position GPS (Calcul automatique de la distance au site)"
        )

        mode_gps = st.radio(
            "Mode de géolocalisation",
            [
                "Simulation Automatique (Bureau ENGITAS)",
                "Saisie manuelle des coordonnées",
            ],
        )

        if mode_gps == "Simulation Automatique (Bureau ENGITAS)":
            lat_user = CENTRE_LAT
            lon_user = CENTRE_LON
            st.success(
                "📍 Position détectée automatiquement sur le site ENGITAS."
            )
        else:
            col1, col2 = st.columns(2)
            with col1:
                lat_user = st.number_input("Latitude", format="%.6f", value=0.0)
            with col2:
                lon_user = st.number_input("Longitude", format="%.6f", value=0.0)

        choix_synchro = st.text_input(
            "Confirmez l'heure affichée sur votre téléphone (Format AAAA-MM-JJ HH:MM:SS)",
            value=maintenant.strftime("%Y-%m-%d %H:%M:%S")
        )

        if st.button("Valider mon arrivée", type="primary"):
            if lat_user == 0.0 or lon_user == 0.0:
                st.warning("Veuillez renseigner des coordonnées valides.")
            else:
                point_reference = (CENTRE_LAT, CENTRE_LON)
                point_utilisateur = (lat_user, lon_user)
                distance = geodesic(point_reference, point_utilisateur).km

                try:
                    dt_final = datetime.strptime(choix_synchro.strip(), "%Y-%m-%d %H:%M:%S")
                except:
                    dt_final = maintenant

                date_du_jour = dt_final.strftime("%Y-%m-%d")
                heure_str = dt_final.strftime("%H:%M:%S")

                deja_pointe = any(
                    p["Nom"] == st.session_state.user_connecte
                    and p["Date"] == date_du_jour
                    for p in st.session_state.presences
                )

                if deja_pointe:
                    st.warning("Vous avez déjà enregistré une présence aujourd'hui.")
                elif distance <= RAYON_AUTORISE_KM:
                    presence_data = {
                        "Nom": st.session_state.user_connecte,
                        "Date": date_du_jour,
                        "Heure_Arrivee": heure_str,
                        "Heure_Depart": None,
                        "Temps_Travail": None,
                        "Distance (km)": round(distance, 3),
                        "Statut": "Présent(e)",
                    }
                    st.session_state.presences.append(presence_data)
                    sauvegarder_presences(st.session_state.presences)
                    st.success(f"✅ Arrivée validée avec succès à {heure_str} !")
                else:
                    st.error(
                        f"❌ Trop loin du site ({round(distance, 2)} km)."
                    )

# --- 3. BIS - POINTER LE DÉPART ---
elif menu == "Pointer mon départ":
    st.markdown(
        "<h1 style='color: #00b4d8;'>ENGITAS - Validation de Départ</h1>",
        unsafe_allow_html=True,
    )
    
    maintenant = datetime.now()
    
    choix_synchro_depart = st.text_input(
        "Confirmez l'heure de départ de votre téléphone (Format AAAA-MM-JJ HH:MM:SS)",
        value=maintenant.strftime("%Y-%m-%d %H:%M:%S")
    )

    date_du_jour = maintenant.strftime("%Y-%m-%d")

    enregistrement_actif = None
    for p in st.session_state.presences:
        if (
            p["Nom"] == st.session_state.user_connecte
            and p["Date"] == date_du_jour
            and (p.get("Heure_Depart") is None or p.get("Heure_Depart") == "")
        ):
            enregistrement_actif = p
            break

    if enregistrement_actif:
        st.info(f"Arrivée enregistrée aujourd'hui à : **{enregistrement_actif['Heure_Arrivee']}**")
        if st.button("Valider mon départ", type="primary"):
            try:
                dt_depart = datetime.strptime(choix_synchro_depart.strip(), "%Y-%m-%d %H:%M:%S")
            except:
                dt_depart = maintenant

            heure_str = dt_depart.strftime("%H:%M:%S")
            enregistrement_actif["Heure_Depart"] = heure_str
            
            fmt = "%H:%M:%S"
            t_arrivee = datetime.strptime(enregistrement_actif["Heure_Arrivee"], fmt)
            t_depart = datetime.strptime(heure_str, fmt)
            delta = t_depart - t_arrivee
            
            if delta.seconds < 0:
                heures, minutes = 0, 0
            else:
                heures = int(delta.seconds // 3600)
                minutes = int((delta.seconds % 3600) // 60)
                
            enregistrement_actif["Temps_Travail"] = f"{heures}h {minutes}min"
            
            sauvegarder_presences(st.session_state.presences)
            st.success(f"✅ Départ validé à {heure_str} ! Temps de travail total : {heures}h {minutes}min.")
    else:
        st.warning("Aucun pointage d'arrivée actif trouvé pour aujourd'hui, ou vous avez déjà pointé votre départ.")

# --- 4. TABLEAU DE BORD ADMIN ---
elif menu == "Tableau de bord Admin":
    st.markdown(
        "<h1 style='color: #00b4d8;'>ENGITAS - Tableau de Bord Administrateur</h1>",
        unsafe_allow_html=True,
    )

    date_auj = datetime.now().strftime("%Y-%m-%d")
    employes_inscrits = [
        nom
        for nom, info in st.session_state.utilisateurs.items()
        if info["role"] == "Employé"
    ]
    total_employes = len(employes_inscrits)

    df_global = (
        pd.DataFrame(st.session_state.presences)
        if len(st.session_state.presences) > 0
        else pd.DataFrame(columns=["Nom", "Date", "Heure_Arrivee", "Heure_Depart", "Temps_Travail", "Distance (km)", "Statut"])
    )

    if not df_global.empty and "Heure_Arrivee" in df_global.columns:
        df_global["Heure_dt"] = pd.to_datetime(df_global["Heure_Arrivee"], format="%H:%M:%S", errors="coerce")
        
        presents_08h = (
            df_global[
                (df_global["Date"] == date_auj)
                & (df_global["Nom"].isin(employes_inscrits))
                & (df_global["Heure_dt"].dt.hour < 12)
            ]["Nom"]
            .unique()
            .tolist()
        )
        
        presents_16h = (
            df_global[
                (df_global["Date"] == date_auj)
                & (df_global["Nom"].isin(employes_inscrits))
                & (df_global["Heure_dt"].dt.hour >= 12)
            ]["Nom"]
            .unique()
            .tolist()
        )
    else:
        presents_08h = []
        presents_16h = []

    nb_presents_08h = len(presents_08h)
    nb_presents_16h = len(presents_16h)

    absents_08h = [e for e in employes_inscrits if e not in presents_08h]
    absents_16h = [e for e in employes_inscrits if e not in presents_16h]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employés", total_employes)
    with col2:
        st.metric("Présents 08H", nb_presents_08h)
    with col3:
        st.metric("Présents 16H", nb_presents_16h)
    with col4:
        st.metric("Total Pointages", len(df_global))

    st.markdown("---")
    onglet_presents, onglet_absents = st.tabs(
        ["✅ Historique des Présents", "❌ Absents du jour"]
    )

    with onglet_presents:
        st.markdown("### Historique complet des présences et temps de travail")
        if not df_global.empty:
            tous_noms = list(st.session_state.utilisateurs.keys())
            employe_selectionne = st.selectbox(
                "Filtrer par utilisateur", ["Tous"] + tous_noms
            )
            df_affiche = (
                df_global
                if employe_selectionne == "Tous"
                else df_global[df_global["Nom"] == employe_selectionne]
            )

            df_affiche_clean = df_affiche.drop(columns=["Heure_dt"], errors="ignore")
            st.dataframe(df_affiche_clean, use_container_width=True)
            
            csv_data = df_affiche_clean.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger le rapport (CSV)",
                data=csv_data,
                file_name="rapport_presences_engitas.csv",
                mime="text/csv",
            )
        else:
            st.info("Aucune présence enregistrée.")

    with onglet_absents:
        st.markdown(f"### Suivi des absents du {date_auj}")
        col_abs1, col_abs2 = st.columns(2)
        
        with col_abs1:
            st.markdown("#### Session 08H")
            if absents_08h:
                df_abs_08 = pd.DataFrame(
                    {"Nom": absents_08h, "Date": date_auj, "Session": "08H", "Statut": "Absent(e)"}
                )
                st.dataframe(df_abs_08, use_container_width=True)
            else:
                st.success("🎉 Aucun absent à 08H !")

        with col_abs2:
            st.markdown("#### Session 16H")
            if absents_16h:
                df_abs_16 = pd.DataFrame(
                    {"Nom": absents_16h, "Date": date_auj, "Session": "16H", "Statut": "Absent(e)"}
                )
                st.dataframe(df_abs_16, use_container_width=True)
            else:
                st.success("🎉 Aucun absent à 16H !")