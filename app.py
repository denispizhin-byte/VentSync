import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from analysis_module import analyze_multiple_cycles

st.set_page_config(page_title="VentSync MVP", layout="wide")

st.title("🫁 VentSync — Analisador de Interação Paciente–Ventilador")

uploaded_file = st.sidebar.file_uploader("Carrega um CSV com time, flow, pressure", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if not {"time", "flow", "pressure"}.issubset(df.columns):
        st.error("O CSV deve conter as colunas: time, flow, pressure")
    else:
        time = df["time"].values
        flow = df["flow"].values
        pressure = df["pressure"].values

        st.success("Arquivo carregado!")

        # --- ANÁLISE ---
        result = analyze_multiple_cycles(time, flow, pressure)

        st.subheader("📊 Resultados dos ciclos")
        st.dataframe(pd.DataFrame(result["cycles"]))

        # --- GRÁFICO ---
        fig, ax = plt.subplots(2, 1, figsize=(16, 10))

        ax[0].plot(time, flow, color="blue")
        ax[0].set_title("Fluxo")

        ax[1].plot(time, pressure, color="red")
        ax[1].set_title("Pressão")

        for cycle in result["cycles"]:
            start = cycle["cycle_start"]
            end = cycle["cycle_end"]

            ax[0].axvline(start, color="green", linestyle="--", alpha=0.7)
            ax[0].axvline(end, color="orange", linestyle="--", alpha=0.7)

            ax[1].axvline(start, color="green", linestyle="--", alpha=0.7)
            ax[1].axvline(end, color="orange", linestyle="--", alpha=0.7)

        st.pyplot(fig)

else:
    st.info("Carrega um arquivo CSV para começar.")