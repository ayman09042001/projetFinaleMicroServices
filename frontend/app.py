import streamlit as st
import requests
from datetime import time

BASE_URL = "http://127.0.0.1:8803"

def main():
    st.title("Gestion des Médecins et Infirmiers")

    menu = st.sidebar.selectbox("Choisissez une option", ["Médecins", "Infirmiers"])

    if menu == "Médecins":
        show_medecins()
    elif menu == "Infirmiers":
        show_infirmiers()

def show_medecins():
    st.header("Gestion des Médecins")
    
    action = st.selectbox("Choisissez une action", ["Ajouter", "Afficher", "Modifier", "Supprimer", "Ajouter Horaire", "Modifier Horaire"])
    
    if action == "Ajouter":
        ajouter_medecin()
    elif action == "Afficher":
        afficher_medecins()
    elif action == "Modifier":
        modifier_medecin()
    elif action == "Supprimer":
        supprimer_medecin()
    elif action == "Ajouter Horaire":
        ajouter_horaire_medecin()
    elif action == "Modifier Horaire":
        modifier_horaire()

def show_infirmiers():
    st.header("Gestion des Infirmiers")
    
    action = st.selectbox("Choisissez une action", ["Ajouter", "Afficher", "Modifier", "Supprimer", "Ajouter Horaire"])
    
    if action == "Ajouter":
        ajouter_infirmier()
    elif action == "Afficher":
        afficher_infirmiers()
    elif action == "Modifier":
        modifier_infirmier()
    elif action == "Supprimer":
        supprimer_infirmier()
    elif action == "Ajouter Horaire":
        ajouter_horaire_infirmier()
    elif action == "Modifier Horaire":
        modifier_horaire()

# Fonction pour ajouter un médecin
def ajouter_medecin():
    st.subheader("Ajouter un Médecin")
    id = st.number_input("ID", min_value=1)
    nom = st.text_input("Nom")
    specialite = st.text_input("Spécialité")
    email = st.text_input("Email")

    if st.button("Ajouter Médecin"):
        response = requests.post(f"{BASE_URL}/medecins", json={"id": id, "nom": nom, "specialite": specialite, "email": email})
        if response.status_code == 200:
            st.success("Médecin ajouté avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

# Fonction pour afficher tous les médecins
def afficher_medecins():
    st.subheader("Afficher tous les Médecins")
    response = requests.get(f"{BASE_URL}/medecins")
    medecins = response.json()
    if response.status_code == 200:
        for medecin in medecins:
            st.write(medecin)
    else:
        st.error("Erreur lors de la récupération des médecins")

# Fonction pour modifier un médecin
def modifier_medecin():
    st.subheader("Modifier un Médecin")
    id = st.number_input("ID du Médecin", min_value=1)
    nom = st.text_input("Nom")
    specialite = st.text_input("Spécialité")
    email = st.text_input("Email")

    if st.button("Modifier Médecin"):
        response = requests.put(f"{BASE_URL}/medecins/{id}", json={"nom": nom, "specialite": specialite, "email": email})
        if response.status_code == 200:
            st.success("Médecin mis à jour avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

def supprimer_medecin():
    st.subheader("Supprimer un Médecin")
    id = st.number_input("ID du Médecin à Supprimer", min_value=1)

    if st.button("Supprimer Médecin"):
        response = requests.delete(f"{BASE_URL}/medecins/{id}")
        if response.status_code == 200:
            st.success("Médecin supprimé avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

def ajouter_horaire_medecin():
    st.subheader("Ajouter des Horaires pour un Médecin")
    id = st.number_input("ID du Médecin", min_value=1)
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    horaires = []
    
    for jour in jours:
        st.write(f"Horaires pour {jour}")
        case = st.checkbox(f"{jour} ?", key=jour)
        if case:
            heure_debut = st.time_input(f"Heure de début pour {jour}", value=time(9, 0), key=f"debut_{jour}")
            heure_fin = st.time_input(f"Heure de fin pour {jour}", value=time(17, 0), key=f"fin_{jour}")
            horaires.append({
                "jour_semaine": jour,
                "heure_debut": heure_debut.isoformat(),
                "heure_fin": heure_fin.isoformat()
            })
    
    if st.button("Ajouter Horaires"):
        for horaire in horaires:
            response = requests.post(f"{BASE_URL}/medecins/{id}/horaires", json=horaire)
            if response.status_code == 200:
                st.success(f"Horaire pour {horaire['jour_semaine']} ajouté avec succès!")
            else:
                st.error(f"Erreur pour {horaire['jour_semaine']} : {response.json().get('detail')}")

def modifier_horaire():
    st.subheader("Modifier un Horaire pour un Médecin")
    
    id = st.number_input("ID du Médecin", min_value=1)
    
    response = requests.get(f"{BASE_URL}/medecins/{id}/horaires")
    horaires = response.json()
    
    if response.status_code == 200 and horaires:
        st.write("Sélectionnez l'horaire à modifier")
        horaires_dict = {f"{horaire['jour_semaine']} de {horaire['heure_debut']} à {horaire['heure_fin']}": horaire for horaire in horaires}
        horaire_selectionne = st.selectbox("Horaire à modifier", list(horaires_dict.keys()))
        
        if horaire_selectionne:
            horaire_data = horaires_dict[horaire_selectionne]
            jour_semaine = horaire_data['jour_semaine']
            heure_debut = st.time_input("Heure de début", value=time.fromisoformat(horaire_data['heure_debut']))
            heure_fin = st.time_input("Heure de fin", value=time.fromisoformat(horaire_data['heure_fin']))
            
            if st.button("Modifier Horaire"):
                horaire_id = horaires.index(horaire_data)
                response = requests.put(f"{BASE_URL}/medecins/{id}/horaires/{horaire_id}", json={
                    "jour_semaine": jour_semaine,
                    "heure_debut": heure_debut.isoformat(),
                    "heure_fin": heure_fin.isoformat()
                })
                if response.status_code == 200:
                    st.success(f"Horaire pour {jour_semaine} mis à jour avec succès!")
                else:
                    st.error(f"Erreur : {response.json().get('detail')}")
    else:
        st.error("Aucun horaire trouvé pour ce médecin.")

# Fonction pour ajouter un infirmier
def ajouter_infirmier():
    st.subheader("Ajouter un Infirmier")
    id = st.number_input("ID", min_value=1)
    nom = st.text_input("Nom")
    service = st.text_input("Service")
    email = st.text_input("Email")

    if st.button("Ajouter Infirmier"):
        response = requests.post(f"{BASE_URL}/infirmiers", json={"id": id, "nom": nom, "service": service, "email": email})
        if response.status_code == 200:
            st.success("Infirmier ajouté avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

# Fonction pour afficher tous les infirmiers
def afficher_infirmiers():
    st.subheader("Liste des Infirmiers")
    try:
        response = requests.get(f"{BASE_URL}/infirmiers")
        response.raise_for_status()
        st.write("Contenu brut de la réponse :", response.text)
        if response.headers.get('Content-Type') == 'application/json':
            infirmiers = response.json()
            st.write("Infirmiers :", infirmiers)
        else:
            st.error(f"Erreur : Réponse du serveur non JSON, type reçu: {response.headers.get('Content-Type')}")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Erreur HTTP : {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Erreur de requête : {err}")

# Fonction pour modifier un infirmier
def modifier_infirmier():
    st.subheader("Modifier un Infirmier")
    id = st.number_input("ID de l'Infirmier", min_value=1)
    nom = st.text_input("Nom")
    service = st.text_input("Service")
    email = st.text_input("Email")

    if st.button("Modifier Infirmier"):
        response = requests.put(f"{BASE_URL}/infirmiers/{id}", json={"nom": nom, "service": service, "email": email})
        if response.status_code == 200:
            st.success("Infirmier mis à jour avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

# Fonction pour supprimer un infirmier
def supprimer_infirmier():
    st.subheader("Supprimer un Infirmier")
    id = st.number_input("ID de l'Infirmier à Supprimer", min_value=1)

    if st.button("Supprimer Infirmier"):
        response = requests.delete(f"{BASE_URL}/infirmiers/{id}")
        if response.status_code == 200:
            st.success("Infirmier supprimé avec succès!")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

if __name__ == "__main__":
    main()
