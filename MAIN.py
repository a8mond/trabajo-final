import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


df = pd.read_csv('datasetPerroneta.csv', sep=';', header=0)
df['FechaCita'] = pd.to_datetime(df['FechaCita'], dayfirst=True)


st.title('La perroneta: Dashboard Atención al cliente')


#Desarrollo

#Ver detalles de c/ cita por dia escogido
fecha_seleccionada = st.sidebar.date_input('Selecciona una fecha para ver las citas')
st.subheader(f'Citas el {fecha_seleccionada.strftime("%Y/%m/%d")}')
citas_fecha = df[df['FechaCita'].dt.date == fecha_seleccionada]

if citas_fecha.empty:
    st.write('No hay citas en esta fecha.')
else:
    st.write(citas_fecha[['NombreCliente', 'RazaMascota', 'Servicio 1', 'Servicio 2']])

#Los 10 clientes en el top
st.subheader('Top 10 clientes más habituales')
top_clientes = df['NombreCliente'].value_counts().head(10)
colores = plt.cm.Spectral(np.linspace(0, 1, len(top_clientes)))

fig, ax = plt.subplots(figsize=(10, 6))  # Puedes ajustar el tamaño según tus necesidades
top_clientes_df = pd.DataFrame({
    'Clientes': top_clientes.index,
    'Citas': top_clientes.values
}).set_index('Clientes')

top_clientes_df.plot(kind='area', stacked=True, color=colores, alpha=0.5, ax=ax)

cliente_frecuente = df['NombreCliente'].value_counts().idxmax()
st.write("El cliente más frecuente es:", cliente_frecuente)

# Añadir estilo
ax.set_ylabel('Número de Citas')
ax.set_xticks(range(len(top_clientes)))
ax.set_xticklabels(top_clientes.index, rotation=45, ha='right')
ax.set_facecolor('lightgrey')  # Cambia el color de fondo
plt.setp(ax.spines.values(), visible=False)  # Oculta el marco
st.pyplot(fig)


#Razas
st.subheader('Distribución de razas de mascota atendidas')
fig, ax = plt.subplots()
df['RazaMascota'].value_counts().head(10).plot(kind='barh', ax=ax)  # Top 10 razas
ax.set_xlabel('Cantidad')
ax.set_ylabel('Raza de Mascota')
st.pyplot(fig)

raza_comun = df['RazaMascota'].value_counts().idxmax()
st.write("La raza de perro más atendida es:", raza_comun)

# Opiniones de los clientes 
st.subheader('Opiniones de los clientes')
opiniones = df['Opinion'].value_counts()

explode = tuple([0.1] + [0] * (len(opiniones) - 1))

fig, ax = plt.subplots()
opiniones.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, counterclock=False, explode=explode, shadow=True, colors=plt.cm.tab20c.colors)
ax.set_ylabel('')
plt.setp(ax.spines.values(), visible=False)  # Oculta el marco
ax.set_facecolor('lightgrey')  # Cambia el color de fondo
st.pyplot(fig)


# Cantidad de clientes por distrito 
st.subheader('Cantidad de clientes por distrito')
fig, ax = plt.subplots()
distritos = df['Distrito'].value_counts()
distritos.plot(kind='bar', ax=ax, color=plt.cm.viridis(np.linspace(0.1, 0.9, len(distritos))))
ax.set_xlabel('Distrito')
ax.set_ylabel('Cantidad de Clientes')
st.pyplot(fig)

#distrito con más clientes
distrito_popular = df['Distrito'].value_counts().idxmax()
cantidad_distrito = df['Distrito'].value_counts().max()
st.write(f"El distrito con más clientes es {distrito_popular} con {cantidad_distrito} clientes.")

distrito_seleccionado = st.sidebar.selectbox('Selecciona un distrito', df['Distrito'].unique())
st.subheader(f'Clientes en el distrito: {distrito_seleccionado}')

# Filtrar por distrito seleccionado
clientes_distrito = df[df['Distrito'] == distrito_seleccionado]

# Mostrar resultados
if clientes_distrito.empty:
    st.write('No hay clientes en este distrito.')
else:
    st.write(clientes_distrito[['NombreCliente', 'RazaMascota', 'Servicio 1', 'Servicio 2']])
