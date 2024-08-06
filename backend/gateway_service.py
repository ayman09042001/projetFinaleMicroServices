from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Médecins Endpoints
@app.post('/medecins')
async def ajouter_medecin(medecin: dict):
    try:
        response = requests.post("http://127.0.0.1:8803/medecins", json=medecin)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/medecins')
async def obtenir_medecins():
    try:
        response = requests.get("http://127.0.0.1:8803/medecins")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/medecins/{id}')
async def obtenir_medecin(id: int):
    try:
        response = requests.get(f"http://127.0.0.1:8803/medecins/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/medecins/{id}')
async def mettre_a_jour_medecin(id: int, medecin: dict):
    try:
        response = requests.put(f"http://127.0.0.1:8803/medecins/{id}", json=medecin)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/medecins/{id}')
async def supprimer_medecin(id: int):
    try:
        response = requests.delete(f"http://127.0.0.1:8803/medecins/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Infirmiers Endpoints
@app.post('/infirmiers')
async def ajouter_infirmier(infirmier: dict):
    try:
        response = requests.post("http://127.0.0.1:8804/infirmiers", json=infirmier)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/infirmiers')
async def obtenir_infirmiers():
    try:
        response = requests.get("http://127.0.0.1:8803/infirmiers")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/infirmiers/{id}')
async def obtenir_infirmier(id: int):
    try:
        response = requests.get(f"http://127.0.0.1:8804/infirmiers/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/infirmiers/{id}')
async def mettre_a_jour_infirmier(id: int, infirmier: dict):
    try:
        response = requests.put(f"http://127.0.0.1:8804/infirmiers/{id}", json=infirmier)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/infirmiers/{id}')
async def supprimer_infirmier(id: int):
    try:
        response = requests.delete(f"http://127.0.0.1:8804/infirmiers/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
async def read_root():
    return {"message": "Bienvenue sur la passerelle API de gestion des médecins et infirmiers!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8807)
