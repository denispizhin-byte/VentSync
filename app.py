import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="VentSync — Analisador de Interação Paciente–Ventilador",
    layout="wide",
)

st.title("🫁 VentSync — Analisador de Interação Paciente–Ventilador")

st.sidebar.header("Upload de dados")
uploaded_file = st.sidebar.file_uploader(
    "Carrega um CSV com time, flow, pressure",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Carrega um arquivo CSV para começar.")
    st.stop()

# 1) Ler CSV
df = pd.read_csv(uploaded_file)

st.subheader("Dados brutos do CSV")
st.dataframe(df, use_container_width=True)

# 2) Tabela editável
st.subheader("Editar dados antes da análise")

editable_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

st.success("Tabela editável carregada!")

# 3) Extrair séries já editadas
try:
    time = editable_df["time"].values
    flow = editable_df["flow"].values
    pressure = editable_df["pressure"].values
except KeyError:
    st.error("O CSV precisa ter colunas: 'time', 'flow', 'pressure'.")
    st.stop()

# 4) Análise simples (placeholder para o teu motor)
st.subheader("Resumo simples dos dados")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Nº de pontos", len(time))
with col2:
    st.metric("Flow médio", f"{np.mean(flow):.1f}")
with col3:
    st.metric("Pressão média", f"{np.mean(pressure):.1f}")

st.subheader("Gráfico de fluxo e pressão")

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(10, 4))

ax1.plot(time, flow, color="tabblue", label="Flow")
ax1.set_xlabel("Tempo")
ax1.set_ylabel("Flow", color="tabblue")
ax1.tick_params(axis="y", labelcolor="tabblue")

ax2 = ax1.twinx()
ax2.plot(time, pressure, color="tabred", label="Pressure")
ax2.set_ylabel("Pressão", color="tabred")
ax2.tick_params(axis="y", labelcolor="tabred")

fig.tight_layout()
st.pyplot(fig)
