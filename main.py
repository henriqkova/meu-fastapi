from fastapi import FastAPI, Query, HTTPException
from fastapi import HTTPException
import pandas as pd
import numpy as np 

app = FastAPI()

# Lista de colunas permitidas
colunas_permitidas = [
    "ID RH", "Genero", "Cidade"
]

limitar_colunas = True
# mude para True se quiser limitar as colunas

def carregar_dados():
    df = pd.read_excel("aham.xlsx")
    df = df.replace({np.nan: None})
    return df

# Rota de paginação
@app.get("/tabela_paginada")
def tabela_paginada(pagina: int = Query(1, ge=1), tamanho_pagina: int = Query(50, ge=1)):
    try:
        df = carregar_dados()

        # Filtra apenas as colunas desejadas
        if limitar_colunas:
            df_filtrado = df[colunas_permitidas]
        else:
            df_filtrado = df

        # Faz o cálculo de início e fim
        inicio = (pagina - 1) * tamanho_pagina
        fim = inicio + tamanho_pagina   

        # Filtra o DataFrame
        dados_paginados = df_filtrado.iloc[inicio:fim]

        # Se não tiver mais dados
        if dados_paginados.empty:
            raise HTTPException(status_code=404, detail=f"A página {pagina} não existe na tabela!")

        return { 
            "pagina": pagina,
            "tamanho_pagina": tamanho_pagina,
            "dados": dados_paginados.to_dict(orient="records")
        }
    except Exception as e:
        return {"Erro": str(e)}
