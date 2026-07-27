import json
import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="ENGITAS - Système de Présence", page_icon="🏢", layout="wide"
)

# Style CSS personnalisé
st.markdown(
    """
    <style>
    .hero-container { padding: 2rem 0; }
    .hero-title { font-size: 2.5rem; font-weight: 800; color: #ffffff; margin-bottom: 1rem; }
    .hero-highlight { color: #00b4d8; }
    .hero-subtitle { font-size: 1.1rem; color: #a0a0a0; margin-bottom: 2rem; }
    .card-grid { display: flex; gap: 1.5rem; margin-top: 2rem; }
    .info-card { background-color: #1e1e1e; border: 1px solid #333333; padding: 1.5rem; border-radius: 8px; flex: 1; text-align: center; }
    .info-card h3 { color: #00b4d8; margin-bottom: 0.5rem; }
    .info-card p { color: #cccccc; margin: 0; font-size: 0.9rem; }
    </style>
""",
    unsafe_allow_html=True,
)

# Coordonnées géographiques de référence du bureau ENGITAS (Exemple : Douala, Cameroun)
LAT_BUREAU = 4.0511
LON_BUREAU = 9.7679
RAYON_AUTORISE_KM = 50.0  # Rayon de tolérance large pour la géolocalisation par IP


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


# Fonction pour récupérer automatiquement la géolocalisation par IP
def obtenir_geolocalisation_auto():
    try:
        reponse = requests.get("https://ipapi.co/json/", timeout=5)
        if reponse.status_code == 200:
            data = reponse.json()
            return data.get("latitude", LAT_BUREAU), data.get(
                "longitude", LON_BUREAU
            ), data.get("city", "Inconnue")
    except Exception:
        pass
    return LAT_BUREAU, LON_BUREAU, "Bureau (Par défaut)"


# --- BARRE LATÉRALE ---
st.sidebar.markdown(
    "<h2 style='color: #00b4d8; text-align: center;'>ENGITAS</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #a0a0a0; font-size: 14px;'>Système de Présence & Géo-pointage</p>",
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
                Accompagner les entreprises au Cameroun et en Afrique dans leur transformation numérique avec des solutions IT sur mesure.
            </div>
            <div class="card-grid">
                <div class="info-card"><h3>360°</h3><p>Cybersécurité & Protection</p></div>
                <div class="info-card"><h3>24/7</h3><p>Infrastructure IT</p></div>
                <div class="info-card"><h3>25+</h3><p>Années d'expertise</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Connexion à votre compte")
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

# --- 3. SIGNER MA PRÉSENCE (Arrivée avec géolocalisation automatique) ---
elif menu == "Signer ma présence":
    st.markdown("### 📝 Pointer mon Arrivée (Géolocalisation Automatique)")
    st.info(
        "Votre position géographique est détectée automatiquement par le système."
    )

    with st.form("form_presence"):
        submit_presence = st.form_submit_button("Valider mon arrivée en ligne")

        if submit_presence:
            lat_employe, lon_employe, ville = obtenir_geolocalisation_auto()

            # Calcul de distance (Haversine)
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
                lat_employe, lon_employe, LAT_BUREAU, LON_BUREAU
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
                        "temps_passe": "En cours",
                        "localisation": ville,
                    }
                    st.session_state.presences.append(nouvelle_presence)
                    sauvegarder_donnees(
                        "presences.json", st.session_state.presences
                    )
                    st.success(
                        f"✅ Arrivée enregistrée à {heure_arrivee} (Localisation : {ville}) !"
                    )
            else:
                st.error("❌ Pointage refusé : Hors de la zone autorisée.")

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
                        heure_actuelle_str = datetime.now().strftime("%H:%M:%S")
                        p["depart"] = heure_actuelle_str

                        # Calcul du temps passé en entreprise
                        fmt = "%H:%M:%S"
                        t_arrivee = datetime.strptime(p["arrivee"], fmt)
                        t_depart = datetime.strptime(heure_actuelle_str, fmt)
                        duree = t_depart - t_arrivee
                        p["temps_passe"] = str(duree)

                        sauvegarder_donnees(
                            "presences.json", st.session_state.presences
                        )
                        st.success(
                            f"✅ Départ enregistré à {heure_actuelle_str} ! Temps total en entreprise : {duree}"
                        )
                        trouve = True
                    else:
                        st.info("Vous avez déjà pointé votre départ aujourd'hui.")
                        trouve = True
                    break
            if not trouve:
                st.warning("Aucune arrivée enregistrée pour aujourd'hui.")

# --- 5. TABLEAU DE BORD ADMIN & HISTORIQUE ---
elif menu == "Tableau de bord Admin" and role_actuel == "Administrateur":
    st.markdown("### 📊 Tableau de bord Administrateur - ENGITAS")

    if st.session_state.presences:
        df_presences = pd.DataFrame(st.session_state.presences)
        st.dataframe(df_presences, use_container_width=True)

        # Bouton de téléchargement du Backup / Historique en CSV
        csv = df_presences.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger l'historique et le Backup complet (CSV)",
            data=csv,
            file_name=f"backup_presences_engitas_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aucun historique de présence pour le moment.")