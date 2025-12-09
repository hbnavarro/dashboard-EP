# %%
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_plotly_events import plotly_events

#alt.theme.enable("dark")
alt.theme.enable("ggplot2")# estilo ggplot2


st.set_page_config(
    page_title="Física no ENEM",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded")

df = pd.read_csv("Base de dados - ENEM EPUFABC.csv", sep=",")

st.title("🔭 Física ENEM")

# ==============================================================================
# 1. BARRA LATERAL (FILTROS)
# ==============================================================================
st.sidebar.header("Filtros Globais")
anos_disponiveis = sorted(df["Ano"].unique())

ano_inicio, ano_fim = st.sidebar.selectbox("Ano inicial", anos_disponiveis), \
                      st.sidebar.selectbox("Ano final", anos_disponiveis)

if ano_inicio > ano_fim:
    st.sidebar.error("O ano inicial deve ser menor ou igual ao ano final.")

df_filtered = df[(df["Ano"] >= ano_inicio) & (df["Ano"] <= ano_fim)]

# ==============================================================================
# 2. SEÇÃO DE KPIS (RESUMO EXECUTIVO)
# ==============================================================================
# Cálculos simples para o topo do dashboard
total_questoes = df_filtered.shape[0]
frente_top = df_filtered["Frente"].value_counts().idxmax() if not df_filtered.empty else "-"
qtd_frentes = df_filtered["Frente"].nunique()
media_anual = total_questoes / len(range(ano_inicio, ano_fim + 1))

# Container visual para os KPIs
with st.container(border=True):
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    col_kpi1.metric("Total de Questões", f"{total_questoes}")
    col_kpi2.metric("Frente Mais Cobrada", f"{frente_top}")
    col_kpi3.metric("Média Questões/Ano", f"{media_anual:.1f}")
    col_kpi4.metric("Frentes Abordadas", f"{qtd_frentes}")

st.markdown("---") # Linha divisória elegante


st.markdown("## 🌎 Visão Geral")

# Processamento dos dados
contagem_frentes = df_filtered["Frente"].value_counts().reset_index()
contagem_frentes.columns = ["Frente", "Quantidade"]

with st.container(border=True):
    colA, colB = st.columns([2, 1])

    # --- GRÁFICO DE BARRAS (ESQUERDA) ---
    with colA:
        fig1 = px.bar(
            contagem_frentes,
            x="Frente",
            y="Quantidade",
            text="Quantidade",
            title="Volume de Questões por Frente",
            color="Quantidade",              # Gradiente baseado no valor
            color_continuous_scale="Greens"  # Paleta Verde
        )
        # Limpeza visual (Clean Academic Style)
        fig1.update_layout(
            xaxis_title=None, # Remove título redundante
            yaxis_title=None,
            coloraxis_showscale=False, # Remove barra de cores lateral
            paper_bgcolor="rgba(0,0,0,0)", # Fundo transparente para integrar com o container
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, width='stretch')

    # --- GRÁFICO DE PIZZA (DIREITA) ---
    with colB:
        fig_pizza = px.pie(
            contagem_frentes,
            names="Frente",
            values="Quantidade",
            title="Proporção",
            hole=0.4,
            # Usando tons de verde discretos (reverse para começar escuro)
            color_discrete_sequence=['#0c3d0e', '#ed3d00', '#f5ac19']
            #color_discrete_sequence=px.colors.qualitative.Dark2
        )
        fig_pizza.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", # Fundo transparente
            showlegend=False, # Opcional: remover legenda se houver pouco espaço
            #margin=dict(t=40, b=0, l=0, r=0)
        )
        fig_pizza.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_pizza, width='stretch')

# ===== Linha 2 ===== #

# ===== GRÁFICO 2: Proporção de questões Conceituais vs Conta =====

#with st.container(border=True):

col1, col2 = st.columns(2)

contagem_tipos = df_filtered["Tipo"].value_counts().reset_index()
contagem_tipos.columns = ["Tipo", "Quantidade"]

fig2 = px.pie(
    contagem_tipos,
    names="Tipo",
    values="Quantidade",
    title="Distribuição de tipos de questão (Conceitual vs Conta)",
    hole=0.4,
    color_discrete_sequence=['#0c3d0e', '#ed3d00', '#f5ac19']
    #color_discrete_sequence=px.colors.qualitative.Dark2
)

with col1:
    with st.container(border=True, height=500):
        st.plotly_chart(fig2, width='stretch')


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
            colorscale="Greens",
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

with col2:
    with st.container(border=True, height=500):
        st.plotly_chart(fig_topicos, width='stretch')

#col2.plotly_chart(fig_topicos, width='stretch')


#----------------------------------------------------------------------------

#----------------------------------------------------------------------------

st.subheader("📈 Evolução da Cobrança por Frente ao Longo dos Anos")

# corrigir frentes
frentes_evolucao = (
    df["Frente"]
    .dropna()
    .astype(str)
    .unique()
)
frentes_evolucao = sorted(frentes_evolucao)

frentes_escolhidas_evolucao = st.multiselect(
    "Selecione as frentes para visualizar a evolução:",
    frentes_evolucao,
    default=frentes_evolucao
)

# Filtrar apenas pelo intervalo de ano
df_evo = df[(df["Ano"] >= ano_inicio) & (df["Ano"] <= ano_fim)]

# Garantir que só filtra por frente aqui (não na visão geral)
if frentes_escolhidas_evolucao:
    df_evo = df_evo[df_evo["Frente"].isin(frentes_escolhidas_evolucao)]

# ==============================
# 1. Lista completa de anos no intervalo
# ==============================
anos_completos = list(range(ano_inicio, ano_fim + 1))

# ==============================
# 2. Criar todas as combinações Ano × Frente
# ==============================
import itertools

frentes_usadas = sorted(df_evo["Frente"].unique())

combinacoes = pd.DataFrame(
    list(itertools.product(anos_completos, frentes_usadas)),
    columns=["Ano", "Frente"]
)

# ==============================
# 3. Contar questões reais e preencher ausentes com zero
# ==============================
evo_real = (
    df_evo.groupby(["Ano", "Frente"])
    .size()
    .reset_index(name="Quantidade")
)

# Merge completo
evolucao_frentes = combinacoes.merge(
    evo_real,
    on=["Ano", "Frente"],
    how="left"
).fillna({"Quantidade": 0})

# Garantir tipo numérico
evolucao_frentes["Quantidade"] = evolucao_frentes["Quantidade"].astype(int)

# ==============================
# 4. Gráfico de evolução (Altair)
# ==============================

# Sua paleta personalizada
#cores_personalizadas = ['#0c3d0e', '#ed3d00', '#f5ac19']

grafico_evolucao = (
    alt.Chart(evolucao_frentes)
    .mark_line(point=True)
    .encode(
        x=alt.X("Ano:O", sort="ascending", title="Ano"),
        y=alt.Y("Quantidade:Q", title="Número de Questões", scale=alt.Scale(domainMin=0)),
        
        # --- MUDANÇA AQUI ---
        color=alt.Color("Frente:N", scale=alt.Scale(scheme='tableau10')),
        # --------------------

        tooltip=[
            alt.Tooltip("Ano:O"),
            alt.Tooltip("Frente:N"),
            alt.Tooltip("Quantidade:Q", title="Questões")
        ]
    )
    .properties(
        width=600,
        height=400
    )
    .interactive()
)

# Nota: O parâmetro correto moderno no Streamlit é use_container_width=True
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
colA, colB = st.columns(2)

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
    text="Quantidade",
    color="Quantidade",
    color_continuous_scale="Greens"
)

fig3.update_layout(xaxis_title="Tópico", yaxis_title="Quantidade")
fig3.update_traces(textposition="outside")

with colA:
    with st.container(border=True):
        st.plotly_chart(fig3, width='content')

# ====================== TABELA DE SUBTÓPICOS (COM FILTRO DE TÓPICO) ======================

# 1) Selecionar Tópico para filtrar a tabela
topicos_disponiveis = ["Todos os tópicos"] + sorted(df_detalhado["Tópico"].dropna().unique())

topico_filtro = colB.selectbox(
    "Filtrar tabela por Tópico:",
    topicos_disponiveis
)

# 2) Preparar subtópicos como antes
sub1 = df_detalhado[["Tópico", "Subtópico 1"]].dropna(subset=["Subtópico 1"])
sub2 = df_detalhado[["Tópico", "Subtópico 2"]].dropna(subset=["Subtópico 2"])

sub1 = sub1.rename(columns={"Subtópico 1": "Conteúdo"})
sub2 = sub2.rename(columns={"Subtópico 2": "Conteúdo"})

tabela_subs = pd.concat([sub1, sub2], ignore_index=True)

# 3) Aplicar filtro pelo Tópico
if topico_filtro != "Todos os tópicos":
    tabela_subs = tabela_subs[tabela_subs["Tópico"] == topico_filtro]

# 4) Agrupar por Subtópico + Tópico
tabela_final = (
    tabela_subs.groupby(["Conteúdo", "Tópico"])
    .size()
    .reset_index(name="Quantidade")
    .sort_values("Quantidade", ascending=False)
)

# 6) Mostrar tabela
colB.dataframe(
    tabela_final,
    width='stretch',
    hide_index=True
)


#======================= SEGUNDA PARTE =======================================

colC, colD = st.columns(2) 


# ====================== GRÁFICO 3: Evolução temporal por tópico ======================

# 1) Filtrar apenas os anos disponíveis dentro do filtro global
anos_validos = sorted(df_detalhado["Ano"].unique())

# 2) Criar uma tabela completa Ano × Tópico garantindo zero onde não há questões
tabela = (
    df_detalhado.groupby(["Ano", "Tópico"])
    .size()
    .reset_index(name="Quantidade")
)

# Criar todos os pares possíveis Ano x Tópico
anos = df_detalhado["Ano"].unique()
topicos = df_detalhado["Tópico"].unique()

multi_index = pd.MultiIndex.from_product(
    [anos, topicos], names=["Ano", "Tópico"]
)

tabela_completa = (
    tabela.set_index(["Ano", "Tópico"])
    .reindex(multi_index, fill_value=0)
    .reset_index()
)

# Ordenar por ano para o gráfico ficar correto
tabela_completa = tabela_completa.sort_values("Ano")

# 3) Criar o gráfico de linhas com Plotly
fig_evolucao = px.line(
    tabela_completa,
    x="Ano",
    y="Quantidade",
    #color="Tópico",
    markers=True,
    title=f"Evolução temporal dos tópicos — Frente: {frente_escolhida}",
    color="Quantidade",
    color_discrete_sequence=px.colors.sequential.Greens_r
)


fig_evolucao.update_layout(
    xaxis_title="Ano",
    yaxis_title="Quantidade de Questões",
    legend_title="Tópico",
)

#colC.plotly_chart(fig_evolucao, width='stretch')


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
    title=f"Distribuição de tipos — {frente_escolhida}",
    hole=0.4,
    color_discrete_sequence=['#0c3d0e', '#ed3d00', '#f5ac19']
)

with colC:
    with st.container(border=True, height=450):
        st.plotly_chart(fig5, width='content')


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


# ====================== GRÁFICO: Heatmap Tópico × Ano ======================

df_temp = df_detalhado.copy()

# Seleciona apenas o ano e o tópico
df_temp = df_temp[["Ano", "Tópico"]].dropna()

# Conta quantas questões ocorreram para cada (Ano, Tópico)
contagem = df_temp.groupby(["Ano", "Tópico"]).size().reset_index(name="Quantidade")

# Pivot para formato matricial
tabela_heatmap = contagem.pivot_table(
    index="Tópico",
    columns="Ano",
    values="Quantidade",
    fill_value=0
)

# Ordena anos (colunas)
tabela_heatmap = tabela_heatmap.sort_index(axis=1)

# Cria o Heatmap
fig_heat = go.Figure(
    data=go.Heatmap(
        z=tabela_heatmap.values,
        x=tabela_heatmap.columns,
        y=tabela_heatmap.index,
        colorscale="Greens",
        colorbar=dict(title="Qtd.")
    )
)

fig_heat.update_layout(
    title=f"Mapa de Calor — Questões por Tópico e Ano ({frente_escolhida})",
    xaxis_title="Ano",
    yaxis_title="Tópico",
    #height=500
)

with colD:
    with st.container(border=True, height=450):
        st.plotly_chart(fig_heat, width='stretch')

