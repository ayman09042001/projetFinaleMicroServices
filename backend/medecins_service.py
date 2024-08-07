from fastapi import FastAPI, HTTPException
from models import Medecin, HoraireHebdomadaire
from config import get_snowflake_connection
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post('/medecins', response_model=Medecin)
async def ajouter_medecin(medecin: Medecin):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO medecins (id, nom, specialite, email) 
            VALUES (%s, %s, %s, %s)
        """, (medecin.id, medecin.nom, medecin.specialite, medecin.email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return medecin

@app.get('/medecins', response_model=list[Medecin])
async def obtenir_medecins():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nom, specialite, email FROM medecins")
        medecins = cursor.fetchall()
        return [Medecin(id=row[0], nom=row[1], specialite=row[2], email=row[3]) for row in medecins]
    finally:
        cursor.close()
        conn.close()

@app.get('/medecins/{id}', response_model=Medecin)
async def obtenir_medecin(id: int):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nom, specialite, email FROM medecins WHERE id = %s", (id,))
        medecin = cursor.fetchone()
        if medecin is None:
            raise HTTPException(status_code=404, detail="Médecin non trouvé")
        return Medecin(id=medecin[0], nom=medecin[1], specialite=medecin[2], email=medecin[3])
    finally:
        cursor.close()
        conn.close()

@app.put('/medecins/{id}', response_model=Medecin)
async def mettre_a_jour_medecin(id: int, medecin: Medecin):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE medecins SET nom = %s, specialite = %s, email = %s 
            WHERE id = %s
        """, (medecin.nom, medecin.specialite, medecin.email, id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return medecin

@app.delete('/medecins/{id}', response_model=dict)
async def supprimer_medecin(id: int):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medecins WHERE id = %s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return {"message": "Médecin supprimé avec succès"}

@app.post('/medecins/{id}/horaires', response_model=HoraireHebdomadaire)
async def ajouter_horaire(id: int, horaire: HoraireHebdomadaire):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        print(f"Inserting schedule: {horaire}")
        cursor.execute("""
            INSERT INTO CENTRE_MEDECINE.CENTREM.HORAIREHEBDOMADAIRE 
            (ID_MEDECIN, JOUR_SEMAINE, HEURE_DEBUT, HEURE_FIN) 
            VALUES (%s, %s, %s, %s)
        """, (id, horaire.jour_semaine, horaire.heure_debut, horaire.heure_fin))
        conn.commit()
        print("Insertion committed")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'insertion de l'horaire")
    finally:
        cursor.close()
        conn.close()
    return horaire



@app.get('/medecins/{id}/horaires', response_model=list[HoraireHebdomadaire])
async def obtenir_horaires(id: int):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT JOUR_SEMAINE, HEURE_DEBUT, HEURE_FIN 
            FROM CENTRE_MEDECINE.CENTREM.HORAIREHEBDOMADAIRE 
            WHERE ID_MEDECIN = %s
        """, (id,))
        horaires = cursor.fetchall()
        return [HoraireHebdomadaire(jour_semaine=row[0], heure_debut=row[1], heure_fin=row[2]) for row in horaires]
    finally:
        cursor.close()
        conn.close()

@app.put('/medecins/{id}/horaires/{horaire_id}', response_model=HoraireHebdomadaire)
async def mettre_a_jour_horaire(id: int, horaire_id: int, horaire: HoraireHebdomadaire):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE CENTRE_MEDECINE.CENTREM.HORAIREHEBDOMADAIRE 
            SET JOUR_SEMAINE = %s, HEURE_DEBUT = %s, HEURE_FIN = %s 
            WHERE ID_MEDECIN = %s AND ID = %s
        """, (horaire.jour_semaine, horaire.heure_debut, horaire.heure_fin, id, horaire_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return horaire

@app.delete('/medecins/{id}/horaires/{horaire_id}', response_model=dict)
async def supprimer_horaire(id: int, horaire_id: int):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM CENTRE_MEDECINE.CENTREM.HORAIREHEBDOMADAIRE 
            WHERE ID_MEDECIN = %s AND ID = %s
        """, (id, horaire_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return {"message": "Horaire supprimé avec succès"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8803)
