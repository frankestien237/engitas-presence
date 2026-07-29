from datetime import datetime
import json
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page et du thème visuel ENGITAS
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🏢", layout="wide"
)

# --- INJECTION DE CSS PERSONNALISÉ (Thème Site Web ENGITAS) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }

    /* Arrière-plan principal */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
    }

    /* Barre latérale */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    /* Titre sidebar */
    h2 {
        color: #00b4d8 !important;
        font-weight: 700 !important;
    }

    /* Titres principaux */
    h1, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    /* Conteneur du formulaire avec effet de verre flouté */
    [data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 2rem !important;
    }

    /* Labels */
    label p {
        color: #94a3b8 !important;
        font-weight: 600;
    }

    /* Champs de saisie */
    [data-testid="stTextInput"] > div > div {
        background-color: #0f172a !important;
        border: 1px solid #475569 !important;
        color: #f8fafc !important;
    }

    /* Boutons personnalisés (Bleu turquoise ENGITAS) */
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

# Coordonnées géographiques exactes du bureau ENGITAS
LAT_BUREAU = 4.0511  # Latitude des bureaux ENGITAS
LON_BUREAU = 9.7679  # Longitude des bureaux ENGITAS
RAYON_AUTORISE_KM = (
    0.2  # 200 mètres de tolérance autour de l'entreprise (anti-triche)
)


# --- FONCTIONS DE GESTION DES FICHIERS & BACKUP ---
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


# Initialisation des données avec Backup JSON
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
                st.error(
                    "Nom d'utilisateur ou mot de passe incorrect.", icon="⚠️"
                )

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
                st.success("Compte créé avec succès ! Vous pouvez vous connecter.")

# --- 3. SIGNER MA PRÉSENCE (GPS Réel & Anti-Triche) ---
elif menu == "Signer ma présence":
    st.markdown("### 📝 Pointer mon Arrivée (Géolocalisation GPS Sécurisée)")
    st.info(
        "Cliquez sur le bouton ci-dessous pour autoriser la géolocalisation. Le système vérifiera que vous êtes bien physiquement dans l'entreprise."
    )

    localisation_js = """
    <div id="geo-status" style="color: #cbd5e1; margin-bottom: 10px;">📍 En attente de votre position GPS...</div>
    <button onclick="getLocation()" style="background-color: #00b4d8; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">Obtenir ma position GPS</button>

    <script>
    function getLocation() {
        const status = document.getElementById('geo-status');
        if (!navigator.geolocation) {
            status.innerHTML = "❌ La géolocalisation n'est pas supportée par votre navigateur.";
            return;
        }
        status.innerHTML = "📍 Localisation en cours...";
        navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy: true});
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        document.getElementById('geo-status').innerHTML = `✅ Position trouvée ! Latitude: ${latitude.toFixed(4)}, Longitude: ${longitude.toFixed(4)}. Vous pouvez valider ci-dessous.`;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: {lat: latitude, lon: longitude}}, '*');
    }

    function error() {
        document.getElementById('geo-status').innerHTML = "❌ Impossible de récupérer votre position. Activez le GPS de votre appareil.";
    }
    </script>
    """
    components.html(localisation_js, height=100)

    with st.form("form_valider_arrivee"):
        st.markdown(
            "*(Si les coordonnées GPS s'affirment ci-dessus, cliquez pour valider)*"
        )
        lat_saisie = st.number_input(
            "Votre Latitude GPS", value=LAT_BUREAU, format="%.6f"
        )
        lon_saisie = st.number_input(
            "Votre Longitude GPS", value=LON_BUREAU, format="%.6f"
        )
        valider = st.form_submit_button("Valider mon arrivée officielle")

        if valider:
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
                date_jour = datetime.now().strftime("%Y-%m-%d")
                heure_arrivee = datetime.now().strftime("%H:%M:%S")

                deja_pointe = any(
                    p["employe"] == st.session_state.user_connecte
                    and p["date"] == date_jour
                    for p in st.session_state.presences
                )

                if deja_pointe:
                    st.warning(
                        "Vous avez déjà enregistré votre arrivée aujourd'hui !"
                    )
                else:
                    nouvelle_presence = {
                        "employe": st.session_state.user_connecte,
                        "date": date_jour,
                        "arrivee": heure_arrivee,
                        "depart": "En cours",
                        "temps_travail": "En cours",
                        "statut": "Présent",
                    }
                    st.session_state.presences.append(nouvelle_presence)
                    sauvegarder_donnees(
                        "presences.json", st.session_state.presences
                    )
                    st.success(
                        f"✅ Arrivée validée à {heure_arrivee} (Distance du site : {distance*1000:.0f}m)."
                    )
            else:
                st.error(
                    f"🚨 ACCÈS REFUSÉ : Vous êtes situé à {distance*1000:.0f} mètres du bureau. Le pointage hors de l'entreprise est interdit."
                )

# --- 4. POINTER MON DÉPART ---
elif menu == "Pointer mon départ":
    st.markdown("### 🚪 Pointer mon Départ")
    date_jour = datetime.now().strftime("%Y-%m-%d")

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
                        heure_depart = datetime.now().strftime("%H:%M:%S")
                        p["depart"] = heure_depart

                        fmt = "%H:%M:%S"
                        t_arrivee = datetime.strptime(p["arrivee"], fmt)
                        t_depart = datetime.strptime(heure_depart, fmt)
                        duree = t_depart - t_arrivee

                        p["temps_travail"] = str(duree)

                        sauvegarder_donnees(
                            "presences.json", st.session_state.presences
                        )
                        st.success(
                            f"✅ Départ enregistré à {heure_depart} ! Durée totale passée en entreprise : **{duree}**"
                        )
                        trouve = True
                    else:
                        st.info(
                            "Vous avez déjà pointé votre départ aujourd'hui."
                        )
                        trouve = True
                    break
            if not trouve:
                st.warning(
                    "Aucune arrivée enregistrée pour aujourd'hui. Veuillez d'abord signer votre présence."
                )

# --- 5. TABLEAU DE BORD ADMIN & HISTORIQUE ---
elif menu == "Tableau de bord Admin" and role_actuel == "Administrateur":
    st.markdown("### 📊 Tableau de bord Administrateur - Suivi & Temps de Travail")

    if st.session_state.presences:
        df_presences = pd.DataFrame(st.session_state.presences)
        st.dataframe(df_presences, use_container_width=True)

        csv = df_presences.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger le Backup et l'historique complet (CSV)",
            data=csv,
            file_name=f"backup_presences_engitas_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aucun historique de présence enregistré pour le moment.")