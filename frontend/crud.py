import streamlit as st
from st_aggrid import AgGrid

import pandas as pd
import requests
import uuid
from sqlite3 import connect


st.title("Coloque seu plano a venda")
with st.form(key = "plan"):
    input_id = st.text_input(label = "Insira seu CPF")
    input_qtd_kwh = st.number_input(label = "Insira a quantidade de KwH em crédito")
    input_value = st.number_input(label = "Insira o preço do plano")
    input_validity_time = st.number_input(label = "Insira o tempo de vigência")
    input_maturity_date = st.text_input(label = "Insira a data de vencimento")
    input_plan_type = st.selectbox(label = "Selecione o tipo de plano", options = ["Transmissão de Crédito", "A", "B"])
    input_button_submit = st.form_submit_button("Enviar")

if input_button_submit:
    st.success("Plano incluído com sucesso!")
    # r = requests.post(
    #     "http://127.0.0.1:5001/plans", 
    #     json = {
    #         "id": str(uuid.uuid3(uuid.NAMESPACE_DNS, input_id)),
    #         "seller_id": input_id,  
    #         "quantity_kwh": input_qtd_kwh,
    #         "value": input_value, 
    #         "validity_time": input_validity_time, 
    #         "maturity_date": input_maturity_date,
    #         "plan_type": input_plan_type})
    # if r.status_code == 201:
    #     st.success("Plano incluído com sucesso!")
    
    conn = connect('backend/database.bd')
    data = pd.read_sql('SELECT * FROM Plataform', conn)
    AgGrid(data)
    