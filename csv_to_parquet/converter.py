import pandas as pd
import os

arquivos_csv = [
    "tb_users.csv"
]
tipos_de_dados = {
    "p_dddphone": str,
    "p_phone": str,
    "p_originaluid": str,
    "p_uid": str,
    "hjmpTS": str,
    "createdTS": str,
    "p_dddphone":str,
    "p_dddcellphoneaditional":str

}
print("Iniciando a conversão de CSV para Parquet...")

for arquivo in arquivos_csv:
    try:
        novo_nome = arquivo.replace(".csv", ".parquet")
        df = pd.read_csv(arquivo,sep='|', dtype=tipos_de_dados, low_memory=False)
        df.to_parquet(novo_nome, index=False)
        print(f"Arquivo convertido com sucesso:{arquivo} -> {novo_nome}")
    except Exception as e:
        print(f"Erro ao converter o arquivo {arquivo}: {e}")
print("Conversão concluída.")