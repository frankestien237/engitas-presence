from datetime import datetime
import json
import os
from geopy.distance import geodesic
import pandas as pd
import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🛡️", layout="wide"
)

# --- STYLE CSS PERSONNALISÉ (Thème Engitas) ---
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
            "admin": {"mdp": "1234", "role": "Administrateur"},
            "employe1": {"mdp": "abcd", "role": "Employé"},
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

    options_menu = ["Signer ma présence"]
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: #00b4d8;'>ENGITAS</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #ffffff;'>🔐 Connexion au Système de Présence</h3>",
            unsafe_allow_html=True,
        )
        with st.form("form_connexion"):
            nom = st.text_input("Nom d'utilisateur")
            mdp = st.text_input("Mot de passe", type="password")
            valider = st.form_submit_button("Se connecter", width="stretch")

            if valider:
                if (
                    nom in st.session_state.utilisateurs
                    and st.session_state.utilisateurs[nom]["mdp"] == mdp
                ):
                    st.session_state.user_connecte = nom
                    st.success(f"Bienvenue chez ENGITAS, {nom} !")
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")

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
            valider_insc = st.form_submit_button("S'inscrire", width="stretch")

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

# --- 3. SIGNER LA PRÉSENCE ---
elif menu == "Signer ma présence":
    st.markdown(
        "<h1 style='color: #00b4d8;'>ENGITAS - Validation de présence</h1>",
        unsafe_allow_html=True,
    )

    role_user = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]
    maintenant = datetime.now()
    acces_autorise = True

    if role_user == "Employé":
        st.info(
            "🕒 **Horaires d'ouverture ENGITAS :** Du lundi au vendredi, de 17h00 à 08h50."
        )
        jour_semaine = maintenant.weekday()
        heure_actuelle_time = maintenant.time()

        heure_ouverture = datetime.strptime("17:00:00", "%H:%M:%S").time()
        heure_fermeture = datetime.strptime("08:50:00", "%H:%M:%S").time()

        est_un_jour_ouvrable = 0 <= jour_semaine <= 4
        est_dans_la_plage_horaire = (
            heure_actuelle_time >= heure_ouverture
            or heure_actuelle_time <= heure_fermeture
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
        st.markdown("### Entrez vos coordonnées GPS actuelles")
        col1, col2 = st.columns(2)
        with col1:
            lat_user = st.number_input("Latitude", format="%.6f", value=0.0)
        with col2:
            lon_user = st.number_input("Longitude", format="%.6f", value=0.0)

        if st.button("Valider ma présence", type="primary"):
            if lat_user == 0.0 or lon_user == 0.0:
                st.warning("Veuillez renseigner des coordonnées valides.")
            else:
                point_reference = (CENTRE_LAT, CENTRE_LON)
                point_utilisateur = (lat_user, lon_user)
                distance = geodesic(point_reference, point_utilisateur).km

                date_du_jour = maintenant.strftime("%Y-%m-%d")
                heure_str = maintenant.strftime("%H:%M:%S")

                deja_pointe = any(
                    p["Nom"] == st.session_state.user_connecte
                    and p["Date"] == date_du_jour
                    for p in st.session_state.presences
                )

                if deja_pointe:
                    st.warning("Vous avez déjà pointé aujourd'hui.")
                elif distance <= RAYON_AUTORISE_KM:
                    presence_data = {
                        "Nom": st.session_state.user_connecte,
                        "Date": date_du_jour,
                        "Heure": heure_str,
                        "Distance (km)": round(distance, 3),
                        "Statut": "Présent(e)",
                    }
                    st.session_state.presences.append(presence_data)
                    sauvegarder_presences(st.session_state.presences)
                    st.success("✅ Présence validée avec succès chez ENGITAS !")
                else:
                    st.error(
                        f"❌ Trop loin du site ({round(distance, 2)} km)."
                    )

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
        else pd.DataFrame(columns=["Nom", "Date", "Heure", "Distance (km)", "Statut"])
    )

    presents_aujourd_hui = (
        df_global[
            (df_global["Date"] == date_auj)
            & (df_global["Nom"].isin(employes_inscrits))
        ]["Nom"]
        .unique()
        .tolist()
        if not df_global.empty
        else []
    )
    nb_presents_jour = len(presents_aujourd_hui)
    absents_aujourd_hui = [
        e for e in employes_inscrits if e not in presents_aujourd_hui
    ]
    nb_absents_jour = len(absents_aujourd_hui)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employés", total_employes)
    with col2:
        st.metric("Présents", nb_presents_jour)
    with col3:
        st.metric("Absents", nb_absents_jour)
    with col4:
        st.metric("Total Pointages", len(df_global))

    st.markdown("---")
    onglet_presents, onglet_absents = st.tabs(
        ["✅ Historique des Présents", "❌ Absents du jour"]
    )

    with onglet_presents:
        st.markdown("### Historique complet des présences")
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

            st.dataframe(df_affiche, width="stretch")
            csv_data = df_affiche.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger le rapport (CSV)",
                data=csv_data,
                file_name="rapport_presences_engitas.csv",
                mime="text/csv",
            )
        else:
            st.info("Aucune présence enregistrée.")

    with onglet_absents:
        st.markdown(f"### Absents du {date_auj}")
        if absents_aujourd_hui:
            df_absents = pd.DataFrame(
                {"Nom": absents_aujourd_hui, "Date": date_auj, "Statut": "Absent(e)"}
            )
            st.dataframe(df_absents, width="stretch")
        else:
            st.success("🎉 Aucun absent aujourd'hui chez ENGITAS !")