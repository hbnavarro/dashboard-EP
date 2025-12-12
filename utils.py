import streamlit as st
import pandas as pd
import os

@st.cache_data
def carregar_dados(nome_da_aba):
    """
    Carrega uma aba específica do arquivo Excel local.
    :param nome_da_aba: Nome da aba (Planilha) no arquivo Excel (ex: 'Fisica')
    """
    
    # 1. Encontrar o caminho do arquivo de forma robusta
    # Isso garante que funcione tanto rodando da Home quanto das Pages
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, 'dados', 'dados_enem_natureza.xlsx')
    
    # Verifica se o arquivo existe para dar um erro amigável se não achar
    if not os.path.exists(caminho_arquivo):
        st.error(f"Arquivo não encontrado em: {caminho_arquivo}")
        return pd.DataFrame() # Retorna vazio para não quebrar o app

    try:
        # 2. Ler o Excel usando Pandas
        # sheet_name é o equivalente ao worksheet do gsheets
        df = pd.read_excel(caminho_arquivo, sheet_name=nome_da_aba)
        
        return df
        
    except ValueError:
        st.error(f"A aba '{nome_da_aba}' não foi encontrada no arquivo Excel.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao ler o arquivo local: {e}")
        return pd.DataFrame()
    
    # No final do arquivo utils.py

def menu_lateral():
    caminho_logo = "assets/Logo EPUFABC - Branco (2).png"
    # Título ou Logo na barra lateral
    # Exibe a imagem local. 
    # use_column_width=False permite controlar o tamanho com 'width'
    st.sidebar.image(caminho_logo, width=150)    
    st.sidebar.title("Navegação")
    
    # Links para as páginas
    # Nota: O caminho deve ser relativo à raiz onde você roda o comando streamlit run
    
    st.sidebar.page_link("home.py", label="Página Inicial", icon="🏠")
    
    st.sidebar.markdown("---") # Separador visual
    st.sidebar.subheader("Disciplinas")
    
    st.sidebar.page_link("pages/fisica.py", label="Física", icon="⚛️")
    st.sidebar.page_link("pages/quimica.py", label="Química", icon="🧪")
    st.sidebar.page_link("pages/biologia.py", label="Biologia", icon="🧬")