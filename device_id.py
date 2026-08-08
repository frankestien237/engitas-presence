from plyer import uniqueid

def get_device_id():
    # Retourne un identifiant unique basé sur le matériel
    return uniqueid.id

device_id = get_device_id()
print(f"L'identifiant de cet appareil est : {device_id}")