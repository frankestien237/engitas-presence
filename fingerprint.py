import uuid
import hashlib

def get_machine_fingerprint():
    # Récupère l'adresse MAC (identifiant unique de la carte réseau)
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 2*6, 2)][::-1])
    
    # On hache l'adresse MAC pour avoir un identifiant propre
    return hashlib.sha256(mac.encode()).hexdigest()

print(f"Empreinte unique de cette machine : {get_machine_fingerprint()}")