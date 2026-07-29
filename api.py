from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="ENGITAS API", version="1.0")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>ENGITAS - Engineering and IT Advisory Services</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: white; text-align: center; padding: 50px;">
            <h1>Conseil stratégique et transformation digitale</h1>
            <p>Accompagner les entreprises au Cameroun et en Afrique dans leur transformation numérique.</p>
        </body>
    </html>
    """


@app.get("/api/services")
async def get_services():
    return {
        "services": [
            {"title": "Cybersécurité", "description": "Protection complète à 360°"},
            {"title": "Infrastructure", "description": "Disponibilité 24/7"},
        ]
    }