from datetime import time
import requests

BASE_URL_MEDECINS = "http://127.0.0.1:8803/medecins"
BASE_URL_INFIRMIERS = "http://127.0.0.1:8804/infirmiers"

def test_ajouter_medecin():
    medecin = {"id": 3, "nom": "Dr. Test", "specialite": "Testologie", "email": "test@example.com"}
    response = requests.post(BASE_URL_MEDECINS, json=medecin)
    print(f"Ajouter Médecin: {response.status_code}, {response.json()}")
def test_ajouter_horaire(medecin_id):
    horaire = {
        "jour_semaine": "Lundi",
        "heure_debut": str(time(9, 0)),  # Format: HH:MM
        "heure_fin": str(time(17, 0))   # Format: HH:MM
    }
    url = f"{BASE_URL_MEDECINS}/{medecin_id}/horaires"
    response = requests.post(url, json=horaire)
    print(f"Ajouter Horaire au Médecin {medecin_id}: {response.status_code}, {response.json()}")


def test_obtenir_medecins():
    response = requests.get(BASE_URL_MEDECINS)
    print(f"Obtenir Médecins: {response.status_code}, {response.json()}")

def test_obtenir_medecin(id):
    response = requests.get(f"{BASE_URL_MEDECINS}/{id}")
    print(f"Obtenir Médecin {id}: {response.status_code}, {response.json()}")

def test_mettre_a_jour_medecin(id):
    medecin = {"nom": "Dr. Test Updated", "specialite": "Updated Testologie", "email": "test_updated@example.com"}
    response = requests.put(f"{BASE_URL_MEDECINS}/{id}", json=medecin)
    print(f"Mettre à Jour Médecin {id}: {response.status_code}, {response.json()}")

def test_supprimer_medecin(id):
    response = requests.delete(f"{BASE_URL_MEDECINS}/{id}")
    print(f"Supprimer Médecin {id}: {response.status_code}, {response.json()}")

def test_ajouter_infirmier():
    infirmier = {"id": 3, "nom": "Infirmier Test", "service": "Test Service", "email": "test@example.com"}
    response = requests.post(BASE_URL_INFIRMIERS, json=infirmier)
    print(f"Ajouter Infirmier: {response.status_code}, {response.json()}")

def test_obtenir_infirmiers():
    response = requests.get(BASE_URL_INFIRMIERS)
    print(f"Obtenir Infirmiers: {response.status_code}, {response.json()}")

def test_obtenir_infirmier(id):
    response = requests.get(f"{BASE_URL_INFIRMIERS}/{id}")
    print(f"Obtenir Infirmier {id}: {response.status_code}, {response.json()}")

def test_mettre_a_jour_infirmier(id):
    infirmier = {"nom": "Infirmier Test Updated", "service": "Updated Test Service", "email": "test_updated@example.com"}
    response = requests.put(f"{BASE_URL_INFIRMIERS}/{id}", json=infirmier)
    print(f"Mettre à Jour Infirmier {id}: {response.status_code}, {response.json()}")

def test_supprimer_infirmier(id):
    response = requests.delete(f"{BASE_URL_INFIRMIERS}/{id}")
    print(f"Supprimer Infirmier {id}: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    # Test Médecins
    # test_ajouter_medecin()
    test_obtenir_medecins()
    test_ajouter_horaire(3)
    
    # test_obtenir_medecin(3)
    # test_mettre_a_jour_medecin(3)
    # test_supprimer_medecin(3)

    # Test Infirmiers
    # test_ajouter_infirmier()
    # test_obtenir_infirmiers()
    # test_obtenir_infirmier(3)
    # test_mettre_a_jour_infirmier(3)
    # test_supprimer_infirmier(3)
