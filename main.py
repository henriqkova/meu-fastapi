from fastapi import FastAPI, Query
import pandas as pd
import numpy as np 

app = FastAPI()

# Carrega o Excel
df = pd.read_excel("aham.xlsx")
df = df.replace({np.nan: None})

colunas = ["ID RH","Genero","Cidade",]

@app.get("/pagina_coluna/{pagina}")
def get_coluna_por_pagina(pagina: int):
    

    try:
        # Calcula o índice da coluna baseado na página
        indice_coluna = pagina - 1

        if indice_coluna >= len(colunas):
            return {"Erro": "Página fora do número de colunas disponíveis"}

        nome_coluna = colunas[indice_coluna]
        dados = df[nome_coluna].tolist()

        return {nome_coluna: dados}
    
    except Exception as e:
        return {"Erro": str(e)}
 