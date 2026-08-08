if response.status_code == 200:
            print("Compte créé avec succès !")
            print(response.json())
        else:
            # Affiche le texte brut renvoyé par le serveur pour comprendre l'erreur exacte
            print(f"Erreur ({response.status_code}) : {response.text}")