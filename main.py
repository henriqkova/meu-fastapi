from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import numpy as np

app = FastAPI()

colunas_permitidas = ["ID RH", "Genero", "Cidade"]
limitar_colunas = True

def carregar_dados():
    df = pd.read_excel("aham.xlsx")
    df = df.replace({np.nan: None})
    return df

@app.get("/tabela_paginada")
def tabela_paginada(pagina: int = Query(1, ge=1), tamanho_pagina: int = Query(50, ge=1)):
    try:
        df = carregar_dados()

        if limitar_colunas:
            df_filtrado = df[colunas_permitidas]
        else:
            df_filtrado = df

        inicio = (pagina - 1) * tamanho_pagina
        fim = inicio + tamanho_pagina

        dados_paginados = df_filtrado.iloc[inicio:fim]

        if dados_paginados.empty:
            raise HTTPException(status_code=404,detail=f"Erro: a página {pagina} não existe na tabela.")

        return {
            "pagina": pagina,
            "tamanho_pagina": tamanho_pagina,
            "dados": dados_paginados.to_dict(orient="records")  
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
