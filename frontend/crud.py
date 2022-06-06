import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import requests
import uuid
import os
from sqlite3 import connect

DIRNAME = os.path.dirname(os.path.abspath( '.'))
BACKEND = os.path.join(DIRNAME, "backend")
DATABASE  = os.path.join(BACKEND, 'database.db')


st.title("Veja os planos disponíveis")
conn = connect(DATABASE)
data = pd.read_sql('SELECT id, quantity_kwh, distribuidora, value, validity_time, maturity_date, plan_type, status FROM plans ORDER BY maturity_date', conn)
data["Planos Disponíveis"] = [f'Crédito Solar - {q}KwH' for q in data["quantity_kwh"]]
data.columns = ["Número do plano", "quantity_kwh", "Distribuidora", "Valor", "Tempo de Vigência", "Vencimento", "Tipo de plano", "Status", "Planos Disponíveis"]
AgGrid(data[["Planos Disponíveis", "Vencimento", "Tempo de Vigência", "Distribuidora", "Tipo de plano", "Valor", "Status", "Número do plano"]])
conn.close()

st.title("Compre um plano")
with st.form(key = "buy"):
    input_id = st.text_input(label = "Insira seu CPF")
    input_planid = st.text_input(label = "Insira o número do Plano")
    input_date = st.text_input(label = "Insira a data da compra")
    input_button_submit = st.form_submit_button("Comprar")
    
    if input_button_submit:
        r = requests.post(
            "http://127.0.0.1:5001/orders", 
            json = {
                "id": str(uuid.uuid4().hex),
                "buyer_id": input_id,  
                "plan_id": input_planid,
                "date": input_date})

        st.success("Plano comprado com sucesso!")
        
st.title("Coloque seu plano a venda")
with st.form(key = "plan"):
    input_id = st.text_input(label = "Insira seu CPF")
    input_qtd_kwh = st.number_input(label = "Insira a quantidade de KwH em crédito")
    input_value = st.number_input(label = "Insira o preço do plano")
    input_validity_time = st.number_input(label = "Insira o tempo de vigência")
    input_distribuidora = st.text_input(label = "Insira a distribuidora")
    input_maturity_date = st.text_input(label = "Insira a data de vencimento")
    input_plan_type = st.selectbox(label = "Selecione o tipo de plano", options = ["Transmissão de Crédito", "A", "B"])
    input_button_submit = st.form_submit_button("Enviar")

if input_button_submit:
    r = requests.post(
        "http://127.0.0.1:5001/plans", 
        json = {
            "id": str(uuid.uuid4().hex),
            "seller_id": input_id,  
            "quantity_kwh": input_qtd_kwh,
            "distribuidora": input_distribuidora,
            "value": input_value, 
            "validity_time": input_validity_time, 
            "maturity_date": input_maturity_date,
            "plan_type": input_plan_type})
    if r.status_code == 201:
         st.success("Plano incluído com sucesso!")

    conn = connect(DATABASE)
    df = pd.read_sql('SELECT id, quantity_kwh, distribuidora, value, validity_time, maturity_date, plan_type, status FROM plans ORDER BY maturity_date', conn)
    df["Planos Disponíveis"] = [f'Crédito Solar - {q}KwH' for q in df["quantity_kwh"]]
    df.columns = ["Número do plano", "quantity_kwh", "Distribuidora", "Valor", "Tempo de Vigência", "Vencimento", "Tipo de plano", "Status", "Planos Disponíveis"]
    AgGrid(df[["Planos Disponíveis", "Vencimento", "Tempo de Vigência", "Distribuidora", "Tipo de plano", "Valor", "Status", "Número do plano"]])
    conn.close()

