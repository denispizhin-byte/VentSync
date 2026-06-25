import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="VentSync — Analisador de Interação Paciente–Ventilador",
    layout="wide",
)

st.title("🫁 VentSync — Analisador de Interação Paciente–Ventilador")

# Upload
uploaded_file = st.sidebar.file_uploader(
    "Carrega um CSV com time, flow, pressure",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Carrega um arquivo CSV para começar.")
    st.stop()

# Ler CSV
df = pd.read_csv(uploaded_file)

st.subheader("Dados brutos do CSV")
st.dataframe(df, use_container_width=True)

# 🔑 Tabela editável (tem de estar depois de df existir)
st.subheader("Editar dados antes da análise")

editable_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

st.success("Tabela editável carregada!")

# Extrair dados editados
time = editable_df["time"].values
flow = editable_df["flow"].values
pressure = editable_df["pressure"].values

# Resumo simples
st.subheader("Resumo dos dados")
col1, col2, col3 = st.columns(3)
col1.metric("Nº de pontos", len(time))
col2.metric("Flow médio", f"{np.mean(flow):.1f}")
col3.metric("Pressão média", f"{np.mean(pressure):.1f}")

# Gráfico
st.subheader("Gráfico de fluxo e pressão")
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(time, flow, color="tab:blue", label="Flow")
ax1.set_xlabel("Tempo")
ax1.set_ylabel("Flow", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(time, pressure, color="tab:red", label="Pressure")
ax2.set_ylabel("Pressão", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

fig.tight_layout()
st.pyplot(fig)
