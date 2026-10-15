from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
import os

# 1. Configurações do Supabase
SUPABASE_URL = "https://ocnfvrwawmuydqjovveb.supabase.co"
SUPABASE_KEY = "sb_publishable_H3fqc3FpFiNoHxr36iCFZA_nBSjk2dj"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Imobiliária Python")

# 2. Rota que abre a página visual do site (HTML)
@app.get("/", response_class=HTMLResponse)
def home():
    caminho_html = os.path.join("templates", "index.html")
    with open(caminho_html, "r", encoding="utf-8") as file:
        return file.read()

# 3. Rota da API que busca os imóveis no Supabase
@app.get("/imoveis")
def listar_imoveis():
    resposta = supabase.table("imoveis").select("*").execute()
    return resposta.data