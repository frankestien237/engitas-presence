from datetime import datetime
import json
import os
from geopy.distance import geodesic
import pandas as pd
import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Gestion de Présence - Entreprise", page_icon="🏢", layout="wide"
)

# --- COORDONNÉES DE RÉFÉRENCE (Bureau / Siège) ---
CENTRE_LAT = 4.0511  # Exemple : Douala
CENTRE_LON = 9.7679
RAYON_AUTORISE_KM = 1.0  # Distance maximale autorisée en kilomètres

# --- FICHIERS POUR L'HISTORIQUE DE CONSERVATION ---
FICHIER_UTILISATEURS = "utilisateurs.json"
FICHIER_PRESENCES = "presences.json"


# --- FONCTIONS DE CHARGEMENT ET SAUVEGARDE (Persistance) ---
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


# --- INITIALISATION DE LA SESSION STATE AVEC L'HISTORIQUE ---
if "utilisateurs" not in st.session_state:
    st.session_state.utilisateurs = charger_utilisateurs()

if "presences" not in st.session_state:
    st.session_state.presences = charger_presences()

# --- NAVIGATION DANS LA BARRE LATÉRALE ---
st.sidebar.title("🏢 Système de Présence")

if "user_connecte" in st.session_state:
    st.sidebar.success(f"Connecté : **{st.session_state.user_connecte}**")
    role_actuel = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]

    options_menu = ["Signer ma présence"]
    if role_actuel == "Administrateur":
        options_menu.append("Tableau de bord Admin")

    options_menu.append("Déconnexion")
    menu = st.sidebar.radio("Menu", options_menu)

    if menu == "Déconnexion":
        del st.session_state.user_connecte
        st.rerun()
else:
    menu = st.sidebar.radio("Menu", ["Connexion", "S'inscrire"])


# --- 1. SECTION CONNEXION ---
if menu == "Connexion":
    st.subheader("🔐 Connexion à votre compte")
    with st.form("form_connexion"):
        nom = st.text_input("Nom d'utilisateur")
        mdp = st.text_input("Mot de passe", type="password")
        valider = st.form_submit_button("Se connecter")

        if valider:
            if (
                nom in st.session_state.utilisateurs
                and st.session_state.utilisateurs[nom]["mdp"] == mdp
            ):
                st.session_state.user_connecte = nom
                st.success(f"Bienvenue, {nom} !")
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")


# --- 2. SECTION INSCRIPTION (Employés illimités) ---
elif menu == "S'inscrire":
    st.subheader("📝 Créer un compte Employé")
    with st.form("form_inscription"):
        nouveau_nom = st.text_input("Nom d'utilisateur")
        nouveau_mdp = st.text_input("Mot de passe", type="password")
        valider_insc = st.form_submit_button("S'inscrire")

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


# --- 3. SECTION SIGNER LA PRÉSENCE ---
elif menu == "Signer ma présence":
    st.subheader("📍 Validation de présence par géolocalisation")

    role_user = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]
    maintenant = datetime.now()

    acces_autorise = True

    if role_user == "Employé":
        st.info(
            "🕒 **Horaires d'ouverture du pointage (Employés) :** Du lundi au vendredi."
        )
        jour_semaine = maintenant.weekday()
        est_un_jour_ouvrable = 0 <= jour_semaine <= 4

        if not est_un_jour_ouvrable:
            acces_autorise = False
            st.error(
                "❌ Le système de pointage est fermé les week-ends pour les employés."
            )
    else:
        st.info(
            "ℹ️ Vous êtes connecté en tant qu'administrateur. Aucune restriction ne s'applique."
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

                if distance <= RAYON_AUTORISE_KM:
                    presence_data = {
                        "Nom": st.session_state.user_connecte,
                        "Date": date_du_jour,
                        "Heure": heure_str,
                        "Distance (km)": round(distance, 3),
                        "Statut": "Présent(e)",
                    }
                    st.session_state.presences.append(presence_data)
                    sauvegarder_presences(st.session_state.presences)
                    st.success(
                        f"✅ Présence validée avec succès à {heure_str} ! Vous êtes à {round(distance * 1000)} mètres du site."
                    )
                else:
                    st.error(
                        f"❌ Échec : Vous êtes trop loin du site ({round(distance, 2)} km). Maximum autorisé : {RAYON_AUTORISE_KM} km."
                    )


# --- 4. SECTION TABLEAU DE BORD ADMIN ---
elif menu == "Tableau de bord Admin":
    st.subheader("📊 Tableau de Bord des Présences (Sessions 08H et 16H)")

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

    if not df_global.empty:
        df_global["Heure_dt"] = pd.to_datetime(
            df_global["Heure"], format="%H:%M:%S", errors="coerce"
        )

        # Session 08H : Pointages enregistrés avant 12h00
        presents_08h = (
            df_global[
                (df_global["Date"] == date_auj)
                & (df_global["Nom"].isin(employes_inscrits))
                & (df_global["Heure_dt"].dt.hour < 12)
            ]["Nom"]
            .unique()
            .tolist()
        )

        # Session 16H : Pointages enregistrés à partir de 12h00
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
        st.metric("Présents à 08H", nb_presents_08h)
    with col3:
        st.metric("Présents à 16H", nb_presents_16h)
    with col4:
        st.metric("Total Pointages", len(df_global))

    st.markdown("---")

    onglet_presents, onglet_absents = st.tabs(
        ["✅ Historique des Présents", "❌ Suivi des Absents (08H & 16H)"]
    )

    with onglet_presents:
        st.markdown(
            "### Historique complet de tous les pointages enregistrés"
        )
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

            df_affiche_clean = df_affiche.drop(
                columns=["Heure_dt"], errors="ignore"
            )
            st.dataframe(df_affiche_clean, use_container_width=True)

            csv_data = df_affiche_clean.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger le rapport complet (CSV)",
                data=csv_data,
                file_name="historique_rapport_presences.csv",
                mime="text/csv",
            )
        else:
            st.info("Aucune présence enregistrée dans l'historique.")

    with onglet_absents:
        st.markdown(f"### Suivi des absents du {date_auj}")
        col_abs1, col_abs2 = st.columns(2)

        with col_abs1:
            st.markdown("#### Session 08H")
            if absents_08h:
                df_abs_08 = pd.DataFrame(
                    {
                        "Nom": absents_08h,
                        "Date": date_auj,
                        "Session": "08H",
                        "Statut": "Absent(e)",
                    }
                )
                st.dataframe(df_abs_08, use_container_width=True)
            else:
                st.success("🎉 Aucun absent à 08H !")

        with col_abs2:
            st.markdown("#### Session 16H")
            if absents_16h:
                df_abs_16 = pd.DataFrame(
                    {
                        "Nom": absents_16h,
                        "Date": date_auj,
                        "Session": "16H",
                        "Statut": "Absent(e)",
                    }
                )
                st.dataframe(df_abs_16, use_container_width=True)
            else:
                st.success("🎉 Aucun absent à 16H !")