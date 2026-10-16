from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional
import os

# 1. Configurações e Conexão com o Supabase
SUPABASE_URL = "https://ocnfvrwawmuydqjovveb.supabase.co"
SUPABASE_KEY = "sb_publishable_H3fqc3FpFiNoHxr36iCFZA_nBSjk2dj"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Imobiliária Python")

# Habilita a pasta 'static' para servir arquivos de imagem local
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Modelo Pydantic ajustado para aceitar imagem opcional
class ImovelSchema(BaseModel):
    titulo: str
    descricao: Optional[str] = ""
    preco: float
    tipo: str  # 'venda' ou 'aluguel'
    categoria: str  # 'casa', 'apartamento', 'sala', 'salao', 'terreno', 'comercial'
    cidade: str
    bairro: str
    quartos: int = 0
    banheiros: int = 0
    vagas: int = 0
    area_m2: float = 0.0
    imagem_url: Optional[str] = None  # Aceita nulo/vazio sem dar erro!

# 3. Rota da Homepage
@app.get("/", response_class=HTMLResponse)
def home():
    caminho_html = os.path.join("templates", "index.html")
    with open(caminho_html, "r", encoding="utf-8") as file:
        return file.read()

# 4. Rota GET: Listar Imóveis com Filtros
@app.get("/imoveis")
def listar_imoveis(
    tipo: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None)
):
    query = supabase.table("imoveis").select("*")

    if tipo:
        query = query.ilike("tipo", f"%{tipo}%")

    if categoria:
        query = query.ilike("categoria", f"%{categoria}%")

    resposta = query.execute()
    return resposta.data

# 5. Rota POST: Cadastrar Novo Imóvel (com tratamento de imagem vazia)
@app.post("/imoveis")
def cadastrar_imovel(imovel: ImovelSchema):
    try:
        dados = imovel.dict()
        
        # Se a imagem não for informada ou for uma string vazia, usa uma imagem padrão de placeholder
        if not dados.get("imagem_url") or str(dados["imagem_url"]).strip() == "":
            dados["imagem_url"] = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800"

        resposta = supabase.table("imoveis").insert(dados).execute()
        
        if resposta.data:
            return {"status": "sucesso", "mensagem": "Imóvel cadastrado com sucesso!", "dados": resposta.data}
        else:
            raise HTTPException(status_code=400, detail="Erro ao inserir no banco de dados.")
    except Exception as e:
        print("Erro interno:", str(e))
        raise HTTPException(status_code=500, detail=str(e))