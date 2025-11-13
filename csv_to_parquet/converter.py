import pandas as pd
import os

arquivos_csv = [
    "tb_cmssitelp.csv",
    "tb_paymentmodes.csv",
    "tb_regions.csv",
    "tb_users.csv"
]

print("Iniciando a conversão de CSV para Parquet...")

for arquivo in arquivos_csv:
    try:
        novo_nome = arquivo.replace(".csv", ".parquet")
        df = pd.read_csv(arquivo,sep='|')
        df.to_parquet(novo_nome, index=False)
        print(f"Arquivo convertido com sucesso:{arquivo} -> {novo_nome}")
    except Exception as e:
        print(f"Erro ao converter o arquivo {arquivo}: {e}")
print("Conversão concluída.")