from fastapi import FastAPI, HTTPException
from models import Infirmier
from config import get_snowflake_connection

app = FastAPI()

@app.post('/infirmiers', response_model=Infirmier)
async def ajouter_infirmier(infirmier: Infirmier):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO infirmiers (id, nom, service, email) 
            VALUES (%s, %s, %s, %s)
        """, (infirmier.id, infirmier.nom, infirmier.service, infirmier.email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return infirmier

@app.get('/infirmiers', response_model=list[Infirmier])
async def obtenir_infirmiers():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nom, service, email FROM infirmiers")
        infirmiers = cursor.fetchall()
        return [Infirmier(id=row[0], nom=row[1], service=row[2], email=row[3]) for row in infirmiers]
    finally:
        cursor.close()
        conn.close()



@app.put('/infirmiers/{id}', response_model=Infirmier)
async def mettre_a_jour_infirmier(id: int, infirmier: Infirmier):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE infirmiers SET nom = %s, service = %s, email = %s 
            WHERE id = %s
        """, (infirmier.nom, infirmier.service, infirmier.email, id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return infirmier

@app.delete('/infirmiers/{id}', response_model=dict)
async def supprimer_infirmier(id: int):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM infirmiers WHERE id = %s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return {"message": "Infirmier supprimé avec succès"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8803)
