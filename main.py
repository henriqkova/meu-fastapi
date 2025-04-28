from fastapi import FastAPI, Query
import pandas as pd
import numpy as np 

app = FastAPI()

# Carrega o Excel
df = pd.read_excel("aham.xlsx")
df = df.replace({np.nan: None})

# Lista de colunas permitidas
colunas_permitidas = [
    "ID RH", "Genero", "Cidade"
]

permitir_colunas = False #mude para Trie se quiser limitar as colunas

# Rota de paginação
@app.get("/tabela_paginada")
def tabela_paginada(pagina: int = Query(1, ge=1), tamanho_pagina: int = Query(50, ge=1)):
    try:
        
        # Filtra apenas as colunas desejadas
        df_filtrado = df[colunas_permitidas]

        if permitir_colunas:
            df_filtrado = df[colunas_permitidas]

        else:
            df_filtrado =df 

        # Faz o cálculo de início e fim
        inicio = (pagina - 1) * tamanho_pagina
        fim = inicio + tamanho_pagina   

        # filtra o DataFrame
        dados_paginados = df_filtrado.iloc[inicio:fim]

        # Se não tiver mais dados
        if dados_paginados.empty:
            return {"Erro": "Não há mais dados para essa página."}
        
        return { 
            "pagina": pagina,
            "tamanho_pagina": tamanho_pagina,
            "dados": dados_paginados.to_dict(orient="records")
        }
    except Exception as e:
        return {"Erro": str(e)} 






