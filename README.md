# Desafio Técnico - Analista de Dados Pleno - CantuStore

**Candidato:** Dyegho Moraes Costa Gama Cunha

---

## 1. Visão Geral do Projeto

Este repositório contém a resolução completa do desafio técnico para a vaga de Analista de Dados Pleno. O projeto é dividido em duas partes principais:

* **Parte 1:** Resolução de problemas de lógica de dados avançada utilizando SQL.
* **Parte 2:** Um pipeline de análise de dados (ETL) completo, focado na análise de carrinhos abandonados, desenvolvido em Databricks com PySpark.

A entrega final inclui este repositório, o notebook de análise para a parte 1 e o notebook do pipeline ETL para a parte 2, ambos documentados e comentados para facilitar a compreensão.
Não foram feitos DashBoards no Power BI, mas o notebook está preparado para integração direta.

---

## 2. Tecnologias Utilizadas

* **Pipeline de Dados:** Databricks (PySpark e SQL)
* **Versionamento:** Git / GitHub
* **Visualização:** Power BI (Conectado ao Databricks) - Não incluso no repositório
* **Linguagens:** SQL, Python (PySpark)
---

## 3. Instruções para Execução (Importante)

O notebook (`.ipynb`) não contém os dados de origem. Para executar este projeto e replicar a análise, são necessários os seguintes passos:

1.  **Upload dos Dados:** Fazer o upload dos 8 arquivos de dados (Parquet e CSV) fornecidos no desafio para o Databricks (via menu "Data" > "Upload data").
2.  **Conversão (Opcional):** O script local `converter.py`  foi usado para converter os 4 arquivos `.csv` em `.parquet` antes do upload, para otimização e consistência.
3.  **Criação das Tabelas "Bronze":** Usar a UI "Create or modify table" para criar as 8 tabelas "Bronze" no schema `workspace.default` (ex: `tb_carts`, `tb_users`, etc.).
4.  **Execução do Notebook:** Anexar o notebook `[Desafio de Análise de Dados CantuStore.ipynb]` a um cluster e executá-lo. O notebook lerá as tabelas "Bronze" criadas, executará todo o pipeline ETL (Silver/Gold) e gerará as saídas de análise.

---

## 4. Parte 1: Resolução SQL

As três consultas SQL estão localizadas no notebook da Parte 1, em células de código separadas e executadas com o comando `%sql`. Elas demonstram:

* **1.1 Campeonato:** Lógica de `UNION ALL` para unificar resultados de mandantes/visitantes e `GROUP BY` para agregação de pontos.
* **1.2 Comissões:** Uso de Funções de Janela (`ROW_NUMBER()`) para ranquear comissões e `HAVING SUM(...)` para aplicar a lógica de negócio.
* **1.3 Organização:** Uso de CTEs Recursivas para mapear a hierarquia organizacional.

---

## 5. Parte 2: Pipeline de Análise (PySpark)

O notebook principal implementa um pipeline ETL completo seguindo a arquitetura Medallion (Bronze/Silver/Gold).

### Camada Bronze
Carregamento dos dados brutos (as 8 tabelas criadas no Passo 3 das instruções) para DataFrames PySpark (ex: `df_carts_bronze`).

### Camada Silver
Esta é a camada de limpeza e transformação (Células 7 e 10). O objetivo é criar um DataFrame desnormalizado (`df_base_completo`) que sirva como fonte única da verdade para a análise.

As seguintes transformações críticas são aplicadas:

1.  **Tratamento de Chaves Ambíguas:** Colunas ambíguas (`PK`, `createdTS`) presentes em múltiplas tabelas são renomeadas na fonte (ex: `cart_PK`, `entry_createdTS`).
2.  **Correção de Tipos e Nulos:**
    * Valores monetários (`p_totalprice`) são arredondados para 2 casas decimais.
    * Nulos em colunas de cálculo (`p_totalprice`, `p_quantity`) são preenchidos com `0`.
    * Nulos em `p_installments` são preenchidos com `1` (assumindo pagamento único).
3.  **Filtragem de Dados Inválidos:** Registros em `tb_carts` com `cart_createdTS` nulo (identificados na Célula 17) são removidos (`.na.drop()`), pois são inutilizáveis para análise temporal.
4.  **Lógica de JOIN Corrigida:** O `JOIN` de `tb_carts` com `tb_addresses` é feito usando a chave `c.p_deliveryaddress`, pois foi identificado que `c.p_paymentaddress` estava 99% nulo, quebrando a análise de região.

### Camada Gold
Esta camada consiste nos DataFrames de resultado (agregados) que respondem diretamente às perguntas de negócio. Cada DataFrame "Gold" é salvo como uma tabela no Databricks para consumo do Power BI.

* `df_estados_abandonados` (Salvo como `gold_estados_abandono`)
* `df_relatorio_mensal` (Salvo como `gold_relatorio_mensal`)
* `df_relatorio_diario` (Salvo como `gold_relatorio_diario`)
* `df_output` (Resultado final do `.txt`, salvo como `cantu_top_50_output`)

---

## 6. Principais Descobertas de Negócio

A análise dos dados (especificamente da Célula 21) revelou um insight de negócio crucial:

* **1.94 Milhão de Abandonos (90%+)** ocorrem **antes** do usuário preencher o endereço de entrega (`p_deliveryaddress` nulo).
* **~200 Mil Abandonos (10%-)** ocorrem **depois** do usuário preencher o endereço (provavelmente durante o cálculo do frete ou seleção de pagamento).

Isso sugere que o principal ponto de atrito do e-commerce não está no checkout, mas sim na fase inicial da jornada de compra (página de produto ou visualização do carrinho).