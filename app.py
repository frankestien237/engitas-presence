from datetime import datetime, time, timedelta, timezone
import json
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🏢", layout="wide"
)

# Fuseau horaire local (UTC+1)
TZ_LOCAL = timezone(timedelta(hours=1))

# --- STYLE CSS PERSONNALISÉ ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
    }
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    h2 {
        color: #00b4d8 !important;
        font-weight: 700 !important;
    }
    h1, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    [data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 2rem !important;
    }
    label p {
        color: #94a3b8 !important;
        font-weight: 600;
    }
    [data-testid="stTextInput"] > div > div {
        background-color: #0f172a !important;
        border: 1px solid #475569 !important;
        color: #f8fafc !important;
    }
    div.stButton > button {
        background-color: #00b4d8 !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #0369a1 !important;
    }
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# --- EN-TÊTE VISUEL STYLE SITE WEB ENGITAS (Fixe et permanent) ---
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; background-color: #0f172a; padding: 10px 20px; border-bottom: 1px solid #1e293b; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: #00b4d8; font-weight: bold; font-size: 20px;">🌐 ENGITAS</span>
            <span style="background-color: #00b4d8; color: white; padding: 4px 12px; border-radius: 4px; font-size: 14px; font-weight: bold;">Accueil</span>
            <span style="color: #94a3b8; font-size: 14px;">Services</span>
            <span style="color: #94a3b8; font-size: 14px;">Références</span>
            <span style="color: #94a3b8; font-size: 14px;">Formations</span>
            <span style="color: #94a3b8; font-size: 14px;">Contact</span>
        </div>
        <div>
            <span style="background-color: #00b4d8; color: white; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold;">Demander un devis</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Coordonnées géographiques exactes du bureau ENGITAS
LAT_BUREAU = 4.0511
LON_BUREAU = 9.7679
RAYON_AUTORISE_KM = 0.2
HEURE_LIMITE_ARRIVEE = time(9, 0, 0)  # 09:00:00 maximum pour pointer


def charger_donnees(nom_fichier, valeur_defaut):
    if not os.path.exists(nom_fichier) or os.path.getsize(nom_fichier) == 0:
        return valeur_defaut
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            if not contenu:
                return valeur_defaut
            return json.loads(contenu)
    except Exception:
        return valeur_defaut


def sauvegarder_donnees(nom_fichier, donnees):
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)


if "utilisateurs" not in st.session_state:
    st.session_state.utilisateurs = charger_donnees(
        "utilisateurs.json",
        {
            "admin": {
                "password": "adminpassword",
                "role": "Administrateur",
                "nom": "Administrateur",
            }
        },
    )

if "presences" not in st.session_state:
    st.session_state.presences = charger_donnees("presences.json", [])

# --- BARRE LATÉRALE ---
st.sidebar.markdown(
    "<h2 style='color: #00b4d8; text-align: center;'>ENGITAS</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #a0a0a0; font-size: 14px;'>Sécurité & Pointage GPS</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

if "user_connecte" in st.session_state:
    st.sidebar.markdown(f"👤 Connecté : **{st.session_state.user_connecte}**")
    role_actuel = st.session_state.utilisateurs[st.session_state.user_connecte][
        "role"
    ]

    options_menu = [
        "Signer ma présence",
        "Départ Pause (12h)",
        "Retour Pause (13h)",
        "Pointer mon départ",
    ]
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
    st.markdown("### Connexion à votre compte ENGITAS")
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
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

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
                sauvegarder_donnees(
                    "utilisateurs.json", st.session_state.utilisateurs
                )
                st.success("Compte créé avec succès !")

# --- 3. SIGNER MA PRÉSENCE ---
elif menu == "Signer ma présence":
    st.markdown(
        "### 📝 Pointer mon Arrivée (Géolocalisation GPS Sécurisée & Limite 9h00)"
    )

    # Vérification immédiate de l'heure actuelle par rapport à 9h00
    maintenant_dt = datetime.now(TZ_LOCAL)
    if maintenant_dt.time() > HEURE_LIMITE_ARRIVEE:
        st.error(
            "⏳ **POINTAGE FERMÉ :** Il est plus de 09h00. Le pointage des arrivées n'est plus autorisé pour aujourd'hui."
        )
    else:
        st.info(
            "Cliquez sur le bouton ci-dessous pour autoriser la géolocalisation."
        )

        localisation_js = """
        <div id="geo-status" style="color: #cbd5e1; margin-bottom: 10px;">📍 En attente de votre position GPS...</div>
        <button onclick="getLocation()" style="background-color: #00b4d8; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">Obtenir ma position GPS</button>
        <script>
        function getLocation() {
            const status = document.getElementById('geo-status');
            if (!navigator.geolocation) {
                status.innerHTML = "❌ Non supporté.";
                return;
            }
            navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy: true});
        }
        function success(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById('geo-status').innerHTML = `✅ Position trouvée !`;
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: {lat: latitude, lon: longitude}}, '*');
        }
        function error() {
            document.getElementById('geo-status').innerHTML = "❌ Erreur GPS.";
        }
        </script>
        """
        components.html(localisation_js, height=100)

        with st.form("form_valider_arrivee"):
            lat_saisie = st.number_input(
                "Votre Latitude GPS", value=LAT_BUREAU, format="%.6f"
            )
            lon_saisie = st.number_input(
                "Votre Longitude GPS", value=LON_BUREAU, format="%.6f"
            )
            valider = st.form_submit_button("Valider mon arrivée officielle")

            if valider:
                # Double vérification au moment de la soumission du formulaire
                moment_validation = datetime.now(TZ_LOCAL)
                if moment_validation.time() > HEURE_LIMITE_ARRIVEE:
                    st.error(
                        "🚨 **DÉLAI DÉPASSÉ :** Il est maintenant plus de 09h00. Pointage refusé."
                    )
                else:
                    from math import asin, cos, radians, sin, sqrt

                    def calculer_distance(lat1, lon1, lat2, lon2):
                        R = 6371
                        dlat = radians(lat2 - lat1)
                        dlon = radians(lon2 - lon1)
                        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(
                            radians(lat2)
                        ) * sin(dlon / 2) ** 2
                        c = 2 * asin(sqrt(a))
                        return R * c

                    distance = calculer_distance(
                        lat_saisie, lon_saisie, LAT_BUREAU, LON_BUREAU
                    )

                    if distance <= RAYON_AUTORISE_KM:
                        date_jour = moment_validation.strftime("%Y-%m-%d")
                        heure_arrivee = moment_validation.strftime("%H:%M:%S")

                        deja_pointe = any(
                            p["employe"] == st.session_state.user_connecte
                            and p["date"] == date_jour
                            for p in st.session_state.presences
                        )
                        if deja_pointe:
                            st.warning("Vous avez déjà pointé aujourd'hui !")
                        else:
                            nouvelle_presence = {
                                "employe": st.session_state.user_connecte,
                                "date": date_jour,
                                "arrivee": heure_arrivee,
                                "depart_pause": "Non pointé",
                                "retour_pause": "Non pointé",
                                "depart": "En cours",
                                "temps_travail": "En cours",
                                "statut": "Présent",
                            }
                            st.session_state.presences.append(nouvelle_presence)
                            sauvegarder_donnees(
                                "presences.json", st.session_state.presences
                            )
                            st.success(f"✅ Arrivée validée à {heure_arrivee}")
                    else:
                        st.error(
                            f"🚨 ACCÈS REFUSÉ : Vous êtes à {distance*1000:.0f} mètres du bureau."
                        )

# --- 4. DÉPART PAUSE (12h) ---
elif menu == "Départ Pause (12h)":
    st.markdown("### 🍔 Pointer mon Départ en Pause (12h00)")
    date_jour = datetime.now(TZ_LOCAL).strftime("%Y-%m-%d")

    with st.form("form_depart_pause"):
        submit_dp = st.form_submit_button("Enregistrer mon départ en pause")
        if submit_dp:
            trouve = False
            for p in st.session_state.presences:
                if (
                    p["employe"] == st.session_state.user_connecte
                    and p["date"] == date_jour
                ):
                    if p["depart_pause"] == "Non pointé":
                        heure_dp = datetime.now(TZ_LOCAL).strftime("%H:%M:%S")
                        p["depart_pause"] = heure_dp
                        sauvegarder_donnees(
                            "presences.json", st.session_state.presences
                        )
                        st.success(f"✅ Départ en pause enregistré à {heure_dp}")
                        trouve = True
                    else:
                        st.info("Vous avez déjà pointé votre départ en pause.")
                        trouve = True
                    break
            if not trouve:
                st.warning("Aucune arrivée enregistrée aujourd'hui.")

# --- 5. RETOUR PAUSE (13h) ---
elif menu == "Retour Pause (13h)":
    st.markdown("### 💼 Pointer mon Retour de Pause (13h00)")
    date_jour = datetime.now(TZ_LOCAL).strftime("%Y-%m-%d")

    with st.form("form_retour_pause"):
        submit_rp = st.form_submit_button("Enregistrer mon retour de pause")
        if submit_rp:
            trouve = False
            for p in st.session_state.presences:
                if (
                    p["employe"] == st.session_state.user_connecte
                    and p["date"] == date_jour
                ):
                    if p["depart_pause"] != "Non pointé":
                        if p["retour_pause"] == "Non pointé":
                            heure_rp = datetime.now(TZ_LOCAL).strftime(
                                "%H:%M:%S"
                            )
                            p["retour_pause"] = heure_rp
                            sauvegarder_donnees(
                                "presences.json", st.session_state.presences
                            )
                            st.success(
                                f"✅ Retour de pause enregistré à {heure_rp}"
                            )
                            trouve = True
                        else:
                            st.info("Vous avez déjà pointé votre retour de pause.")
                            trouve = True
                    else:
                        st.warning(
                            "Vous devez d'abord pointer votre départ en pause !"
                        )
                        trouve = True
                    break
            if not trouve:
                st.warning("Aucune arrivée enregistrée aujourd'hui.")

# --- 6. POINTER MON DÉPART ---
elif menu == "Pointer mon départ":
    st.markdown("### 🚪 Pointer mon Départ de fin de journée")
    date_jour = datetime.now(TZ_LOCAL).strftime("%Y-%m-%d")

    with st.form("form_depart"):
        submit_depart = st.form_submit_button("Enregistrer mon départ")
        if submit_depart:
            trouve = False
            for p in st.session_state.presences:
                if (
                    p["employe"] == st.session_state.user_connecte
                    and p["date"] == date_jour
                ):
                    if p["depart"] == "En cours":
                        heure_depart = datetime.now(TZ_LOCAL).strftime(
                            "%H:%M:%S"
                        )
                        p["depart"] = heure_depart
                        t_arrivee = datetime.strptime(p["arrivee"], "%H:%M:%S")
                        t_depart = datetime.strptime(heure_depart, "%H:%M:%S")
                        duree = t_depart - t_arrivee
                        p["temps_travail"] = str(duree)
                        sauvegarder_donnees(
                            "presences.json", st.session_state.presences
                        )
                        st.success(f"✅ Départ enregistré : **{duree}**")
                        trouve = True
                    else:
                        st.info("Départ déjà pointé.")
                        trouve = True
                    break
            if not trouve:
                st.warning("Aucune arrivée enregistrée aujourd'hui.")

# --- 7. TABLEAU DE BORD ADMIN (SUIVI LUNDI -> VENDREDI) ---
elif menu == "Tableau de bord Admin" and role_actuel == "Administrateur":
    st.markdown(
        "### 📊 Tableau de bord Administrateur - Suivi Hebdomadaire (Lundi au Vendredi)"
    )

    employes_inscrits = [
        username
        for username, data in st.session_state.utilisateurs.items()
        if data.get("role") == "Employé"
    ]

    if not employes_inscrits:
        employes_inscrits = [
            u for u in st.session_state.utilisateurs.keys() if u != "admin"
        ]

    if employes_inscrits:
        auj = datetime.now(TZ_LOCAL).date()
        debut_semaine = auj - timedelta(days=auj.weekday())

        jours_ouvrables = [
            (debut_semaine + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(5)
        ]
        noms_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

        recap_data = []
        for emp in employes_inscrits:
            ligne = {"Employé": emp}
            for idx, jour in enumerate(jours_ouvrables):
                nom_col = f"{noms_jours[idx]} ({jour})"
                pointe = any(
                    p["employe"] == emp and p["date"] == jour
                    for p in st.session_state.presences
                )
                if jour > auj.strftime("%Y-%m-%d"):
                    ligne[nom_col] = "⏳ À venir"
                else:
                    ligne[nom_col] = (
                        "✅ Présent" if pointe else "❌ Absent (Manqué)"
                    )
            recap_data.append(ligne)

        st.markdown(
            "#### Grille des présences de la semaine (Lundi - Vendredi) - Tous les employés"
        )
        df_recap = pd.DataFrame(recap_data)
        st.dataframe(df_recap, use_container_width=True)

        st.markdown("---")
        st.markdown(
            "#### Historique détaillé des pointages (Arrivées, Pauses & Départs)"
        )
        if st.session_state.presences:
            df_presences = pd.DataFrame(st.session_state.presences)
            st.dataframe(df_presences, use_container_width=True)

            csv = df_presences.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger l'historique complet (CSV)",
                data=csv,
                file_name=f"backup_presences_{datetime.now(TZ_LOCAL).strftime('%Y-%m-%d')}.csv",
                mime="text/csv",
            )
        else:
            st.info("Aucun pointage enregistré pour l'instant.")
    else:
        st.info("Aucun employé inscrit pour le moment.")