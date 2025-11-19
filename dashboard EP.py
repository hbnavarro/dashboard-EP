import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

#alt.theme.enable("dark")
alt.theme.enable("ggplot2")# estilo ggplot2


st.set_page_config(
    page_title="Física no ENEM",
    page_icon="📗",
    layout="wide",
    initial_sidebar_state="expanded")

df = pd.read_csv("Base de dados - ENEM EPUFABC.csv", sep=",")

st.title("📗 EPUFABC - Física ENEM")

st.markdown("## 🔎 Visão Geral")

# ========== FILTRO POR ANO (intervalo) ==========
anos_disponiveis = sorted(df["Ano"].unique())

ano_inicio, ano_fim = st.sidebar.selectbox("Ano inicial", anos_disponiveis), \
                      st.sidebar.selectbox("Ano final", anos_disponiveis)

if ano_inicio > ano_fim:
    st.sidebar.error("O ano inicial deve ser menor ou igual ao ano final.")

df_filtered = df[(df["Ano"] >= ano_inicio) & (df["Ano"] <= ano_fim)]

# ========== FILTRO POR FRENTE (multiselect) ==========
frentes_disponiveis = sorted(df_filtered["Frente"].unique())

frentes_selecionadas = st.sidebar.multiselect(
    "Frente(s))",
    frentes_disponiveis
)

if frentes_selecionadas:  
    df_filtered = df_filtered[df_filtered["Frente"].isin(frentes_selecionadas)]

# ========== FILTRO POR TÓPICO (multiselect) ==========
topicos_disponiveis = sorted(df_filtered["Tópico"].unique())

topicos_selecionados = st.sidebar.multiselect(
    "Tópico(s)",
    topicos_disponiveis
)

if topicos_selecionados:
    df_filtered = df_filtered[df_filtered["Tópico"].isin(topicos_selecionados)]

# ========== TABELA FINAL ==========
#df_filtered


# ===== GRÁFICO 1: Número total de questões por frente =====

contagem_frentes = df_filtered["Frente"].value_counts().reset_index()
contagem_frentes.columns = ["Frente", "Quantidade"]

fig1 = px.bar(
    contagem_frentes,
    x="Frente",
    y="Quantidade",
    title="Número total de questões por frente",
    text="Quantidade"
)

fig1.update_layout(xaxis_title="Frente", yaxis_title="Quantidade")
fig1.update_traces(textposition="outside")

st.plotly_chart(fig1)

col1, col2 = st.columns(2)

# ===== GRÁFICO 2: Proporção de questões Conceituais vs Conta =====

contagem_tipos = df_filtered["Tipo"].value_counts().reset_index()
contagem_tipos.columns = ["Tipo", "Quantidade"]

fig2 = px.pie(
    contagem_tipos,
    names="Tipo",
    values="Quantidade",
    title="Distribuição de tipos de questão (Conceitual vs Conta)",
    hole=0.3
)

col1.plotly_chart(fig2)

# ===== GRÁFICO 3: Tópicos mais cobrados (Plotly, com gradiente) =====
import plotly.graph_objects as go  # <-- certifique-se de ter esta importação no topo do script

# preparar os dados
contagem_topicos = (
    df_filtered["Tópico"]
    .value_counts()
    .reset_index(name="Quantidade")
)
contagem_topicos.columns = ["Tópico", "Quantidade"]

# ordenar do maior para o menor (queremos os maiores no topo)
contagem_topicos = contagem_topicos.sort_values("Quantidade", ascending=False).reset_index(drop=True)

# normalizar para escala visual das barras (0..1)
contagem_topicos["Porcentagem"] = contagem_topicos["Quantidade"] / contagem_topicos["Quantidade"].max()

# construir a figura
fig_topicos = go.Figure()

fig_topicos.add_trace(
    go.Bar(
        x=contagem_topicos["Porcentagem"],     # comprimento da barra (normalizado)
        y=contagem_topicos["Tópico"],
        orientation="h",
        marker=dict(
            color=contagem_topicos["Quantidade"],  # cor baseada na quantidade -> gradiente
            colorscale="Blues",
            showscale=False
        ),
        text=contagem_topicos["Quantidade"],    # valor numérico mostrado
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Questões: %{text}<extra></extra>",
    )
)

# layout e estilo
fig_topicos.update_layout(
    title="Tópicos mais cobrados",
    xaxis=dict(visible=False),
    yaxis=dict(autorange="reversed", title=""),  # autorange reversed para manter maiores no topo
    height=500
    #margin=dict(l=140, r=40, t=60, b=20)
)

# desenhar no col3
col2.plotly_chart(fig_topicos, width='content')




#----------------------------------------------------------------------------

st.subheader("📈 Evolução da Cobrança por Frente ao Longo dos Anos")

# Agrupar os dados
evolucao_frentes = (
    df_filtered
    .groupby(["Ano", "Frente"])
    .size()
    .reset_index(name="Quantidade")
)

# Gráfico de linhas: evolução por frente
grafico_evolucao = (
    alt.Chart(evolucao_frentes)
    .mark_line(point=True)
    .encode(
        x=alt.X("Ano:O", sort="ascending", title="Ano"),
        y=alt.Y("Quantidade:Q", title="Número de Questões"),
        color=alt.Color("Frente:N", title="Frente"),
        tooltip=[
            alt.Tooltip("Ano:O"),
            alt.Tooltip("Frente:N"),
            alt.Tooltip("Quantidade:Q", title="Questões")
        ]
    )
    .properties(
        width=600,      # <--- precisa ser número
        height=400
    )
    .interactive()
)

st.altair_chart(grafico_evolucao, width='stretch')


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


st.markdown("## 🔎 Análise detalhada por Frente")

# Filtro independente, respeitando o filtro de Ano
frentes_detalhe = sorted(df_filtered["Frente"].unique())

frente_escolhida = st.selectbox(
    "Selecione uma Frente para análise detalhada:",
    frentes_detalhe
)

# Filtrar pelo conjunto já filtrado por Ano + Frente
df_detalhado = df_filtered[df_filtered["Frente"] == frente_escolhida]

# Criar três colunas
colA, colB, colC = st.columns(3)

# ====================== GRÁFICO 1: Tópicos ======================
contagem_topicos = (
    df_detalhado["Tópico"]
    .value_counts()
    .reset_index()
)
contagem_topicos.columns = ["Tópico", "Quantidade"]

fig3 = px.bar(
    contagem_topicos,
    x="Tópico",
    y="Quantidade",
    title=f"Quantidade de questões por tópico — Frente: {frente_escolhida}",
    text="Quantidade"
)

fig3.update_layout(xaxis_title="Tópico", yaxis_title="Quantidade")
fig3.update_traces(textposition="outside")

colA.plotly_chart(fig3, width='content')

# ====================== GRÁFICO 2: Questões por Ano ======================
contagem_ano = (
    df_detalhado["Ano"]
    .value_counts()
    .reset_index()
    .sort_values("Ano")        # Ordenar pelo ano em ordem crescente
)

contagem_ano.columns = ["Ano", "Quantidade"]

fig4 = px.bar(
    contagem_ano,
    x="Ano",
    y="Quantidade",
    title=f"Quantidade de questões por ano — Frente: {frente_escolhida}",
    text="Quantidade"
)

fig4.update_layout(xaxis_title="Ano", yaxis_title="Quantidade")
fig4.update_xaxes(type="category")  # Garantir que o eixo X seja categórico e ordenado
fig4.update_traces(textposition="outside")

colB.plotly_chart(fig4,width='content')

# ====================== GRÁFICO 3: Conceitual vs Conta ======================
contagem_tipos = (
    df_detalhado["Tipo"]
    .value_counts()
    .reset_index()
)
contagem_tipos.columns = ["Tipo", "Quantidade"]

fig5 = px.pie(
    contagem_tipos,
    names="Tipo",
    values="Quantidade",
    title=f"Distribuição de tipos — Frente: {frente_escolhida}",
    hole=0.3
)

colC.plotly_chart(fig5, width='content')


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

st.markdown("## 🔎 Análise detalhada por tópico")
