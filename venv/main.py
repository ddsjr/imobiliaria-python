from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
from typing import Optional
import os

# 1. Configurações e Conexão com o Supabase
SUPABASE_URL = "https://ocnfvrwawmuydqjovveb.supabase.co"
SUPABASE_KEY = "sb_publishable_H3fqc3FpFiNoHxr36iCFZA_nBSjk2dj"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Imobiliária Python")

# Habilita a pasta 'static' para servir imagens e logos
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Rota Principal (Entrega a Interface Web)
@app.get("/", response_class=HTMLResponse)
def home():
    caminho_html = os.path.join("templates", "index.html")
    with open(caminho_html, "r", encoding="utf-8") as file:
        return file.read()

# 3. Rota da API com FILTROS parametrizados
@app.get("/imoveis")
def listar_imoveis(
    tipo: Optional[str] = Query(None),       # Aceita 'venda' ou 'aluguel'
    categoria: Optional[str] = Query(None)   # Aceita 'casa', 'apartamento', 'comercial', 'sala', 'salao', 'terreno'
):
    # Inicia a consulta base na tabela 'imoveis'
    query = supabase.table("imoveis").select("*")

    # Se o usuário passou um filtro de tipo (Venda ou Aluguel), aplica o filtro SQL
    if tipo:
        query = query.ilike("tipo", f"%{tipo}%")

    # Se o usuário passou um filtro de categoria (ex: casa, comercial), aplica o filtro SQL
    if categoria:
        query = query.ilike("categoria", f"%{categoria}%")

    # Executa a busca no Supabase e retorna os dados
    resposta = query.execute()
    return resposta.data