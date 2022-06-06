import pandas as pd
from sqlite3 import connect

conn = connect('database.db')
data = pd.read_sql('select * from plans', conn)

data = pd.read_sql('SELECT quantity_kwh, distribuidora, value, validity_time, maturity_date, plan_type, status FROM plans ORDER BY maturity_date', conn)
data["Planos Disponíveis"] = [f'Crédito Solar - {q}KwH' for q in data["quantity_kwh"]]
data.columns = ["quantity_kwh", "Distribuidora", "Valor", "Tempo de Vigência", "Vencimento", "Tipo de plano", "Status", "Planos Disponíveis"]
print(data[["Planos Disponíveis", "Vencimento", "Tempo de Vigência", "Distribuidora", "Tipo de plano", "Valor", "Status"]])
conn.close()
#[f'Crédito Solar - {q}KwH' for q in data[["quantity_kwh"]]]
#data["Planos Disponíveis"] = [f'Crédito Solar - {q}KwH' for q in data[["quantity_kwh"]]]