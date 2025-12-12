import streamlit as st
from utils import menu_lateral # Importa a função nova

st.set_page_config(
    page_title="Dashboard ENEM - Ciências da Natureza EPUFABC",
    page_icon="🎓",
    layout="centered", # Layout centralizado fica melhor para landing pages
    initial_sidebar_state="collapsed" # Esconde a sidebar na home para dar foco nos botões
)

menu_lateral() # <--- Adicione esta linha aqui para desenhar a sidebar
# Configuração da página inicial

# Título e Introdução
st.title("🎓 Análise ENEM: Ciências da Natureza")

st.markdown("""
### Bem-vindo ao portal de dados da EPUFABC.

Este dashboard consolida dados históricos das provas do ENEM, permitindo uma análise 
detalhada das tendências, tópicos mais cobrados e evolução das questões ao longo dos anos.

**Selecione abaixo a disciplina que deseja analisar:**
""")

st.markdown("---")

# Criação das Colunas para os Botões/Links
col1, col2, col3 = st.columns(3)

# Botão Física
with col1:
    st.image("https://img.icons8.com/ios/100/FFFFFF/atom-editor.png", width=80) # Exemplo de ícone
    st.page_link("pages/fisica.py", label="FÍSICA", icon="⚛️", use_container_width=True)

# Botão Química
with col2:
    st.image("https://img.icons8.com/ios/100/FFFFFF/test-tube.png", width=80) 
    st.page_link("pages/quimica.py", label="QUÍMICA", icon="🧪", use_container_width=True)

# Botão Biologia
with col3:
    st.image("https://img.icons8.com/ios/100/FFFFFF/dna-helix.png", width=80)
    st.page_link("pages/biologia.py", label="BIOLOGIA", icon="🧬", use_container_width=True)

st.markdown("---")
st.info("Desenvolvido pela equipe EPUFABC")