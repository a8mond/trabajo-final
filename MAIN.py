import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache
def load_data():
     url = 'https://docs.google.com/spreadsheets/d/1j05uIaAorDbsqwQaJonyTJUbCRsRsjDF/edit?usp=sharing&ouid=112107341849971302946&rtpof=true&sd=true'
     data = pd.read_excel(url)
     return data

df = load_data()
st.title('La perroneta')
st.subheader('Dashboard atención al cliente')

# Filtro de fechas
start_date = st.sidebar.date_input('Fecha de inicio', df['FechaCita'].min())
end_date = st.sidebar.date_input('Fecha de fin', df['FechaCita'].max())
filtered_df = df[(df['FechaCita'] >= start_date) & (df['FechaCita'] <= end_date)]

# Filtro por distrito
distrito = st.sidebar.multiselect('Selecciona el distrito', df['Distrito'].unique())

# Si se seleccionó algún distrito, filtrar por esos distritos
if distrito:
    filtered_df = filtered_df[filtered_df['Distrito'].isin(distrito)]


# Gráfico de barras de servicios más solicitados
st.subheader('Servicios más solicitados')
fig, ax = plt.subplots()
ax.bar(filtered_df['Servicio1'].value_counts().index, filtered_df['Servicio1'].value_counts().values)
st.pyplot(fig)

# Mostrar tabla de datos
st.subheader('Citas filtradas')
st.dataframe(filtered_df)

# Mostrar opiniones de clientes
st.subheader('Comentarios de los clientes')
st.write(filtered_df['Opinion'])

