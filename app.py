import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st
import base64
import requests
from io import BytesIO
from PIL import Image  # Adicione esta importação no topo do seu arquivo

# Configuração do banco de dados
Base = declarative_base()
   
# Use SQLite em memória para o Streamlit Cloud
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

# Modelo de dados
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    category = Column(String(20), nullable=False)
    image = Column(LargeBinary, nullable=True)

# Criar tabelas
Base.metadata.create_all(engine)

# Funções do banco de dados
def add_post(title, content, category, image=None):
    session = Session()
    new_post = Post(title=title, content=content, category=category, image=image)
    session.add(new_post)
    session.commit()
    session.close()

def get_posts():
    session = Session()
    posts = session.query(Post).order_by(Post.date_posted.desc()).all()
    session.close()
    return posts

def add_example_posts():
    session = Session()
    if session.query(Post).count() == 0:
        def get_example_image(url):
            response = requests.get(url)
            return BytesIO(response.content).read()

        example_posts = [
            Post(
                title="Meditação Semanal: O Poder do Louvor",
                content="Nesta semana, refletimos sobre o poder transformador do louvor em nossas vidas. O Salmo 22:3 nos diz que Deus habita nos louvores do seu povo. Quando louvamos, não apenas expressamos nossa gratidão, mas também convidamos a presença de Deus para nossas vidas...",
                category="meditacao",
                date_posted=datetime.now(),
                image=get_example_image("https://images.unsplash.com/photo-1515705576963-95cad62945b6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80")
            ),
            Post(
                title="Tutorial: Acordes Básicos no Violão",
                content="Neste tutorial, vamos aprender os acordes básicos no violão que são essenciais para acompanhar muitos hinos e canções de louvor. Começaremos com os acordes de Dó (C), Sol (G) e Ré (D). Para formar o acorde de Dó, coloque o dedo indicador na primeira casa da segunda corda...",
                category="tutorial",
                date_posted=datetime.now(),
                image=get_example_image("https://images.unsplash.com/photo-1510915361894-db8b60106cb1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80")
            ),
            Post(
                title="Próximo Evento: Noite de Louvor e Adoração",
                content="Estamos animados para anunciar nossa próxima Noite de Louvor e Adoração! O evento acontecerá no próximo sábado, às 19h, no salão principal da igreja. Teremos a participação especial do grupo de louvor 'Vozes para Cristo'. Venha se juntar a nós para uma noite de música, oração e comunhão...",
                category="noticia",
                date_posted=datetime.now(),
                image=get_example_image("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80")
            )
        ]
        session.add_all(example_posts)
        session.commit()
    session.close()

# Função auxiliar para converter a imagem em base64
def get_image_base64(image):
    if image:
        return base64.b64encode(image).decode()
    return None

# Configuração da página
st.set_page_config(page_title="Blog Ministério de Música Isaías", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    body {
        color: #212121;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #6200EE;
        color: white;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: 500;
        border: none;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #3700B3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 4px;
        border: 1px solid #BDBDBD;
        padding: 10px;
    }
    h1 {
        color: #6200EE;
        font-weight: 300;
    }
    h2 {
        color: #3700B3;
        font-weight: 400;
    }
    .main-content {
        max-width: 800px;
        margin: auto;
        padding: 0 20px;
    }
    .post-card {
        background-color: white;
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        transition: all 0.3s;
    }
    .post-card:hover {
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }
    .category-chip {
        background-color: #E0E0E0;
        color: #212121;
        padding: 4px 8px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    .sidebar {
        padding: 10px;
        border-left: 1px solid #e0e0e0;
    }
    .stButton>button {
        background: none!important;
        border: none;
        padding: 0!important;
        color: #069;
        text-decoration: underline;
        cursor: pointer;
    }
    .centered {
        display: flex;
        justify-content: center;
    }
    .sidebar-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
    }
    .sidebar-logo img {
        max-width: 80%;
        height: auto;
    }
    .reportview-container {
        flex-direction: row;
        padding-top: 0rem;
    }
    .main .block-container {
        padding-top: 5rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 4rem;
        background-color: #f0f2f6;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .fixed-header h1 {
        color: #262730;
        font-size: 2rem;
        margin: 0;
        padding: 0.5rem 1rem;
        background: linear-gradient(45deg, #1e3799, #0c2461);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-content {
        margin-top: 60px;  /* Ajuste este valor de acordo com a altura do seu cabeçalho fixo */
    }
    .stButton > button {
        background-color: #f0f2f6;
        color: #262730;
        border: 1px solid #d1d5db;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 0.375rem;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        text-decoration: none !important;
        display: inline-block;
        line-height: 1.5;
    }

    .stButton > button:hover {
        background-color: #e5e7eb;
        border-color: #9ca3af;
    }

    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
    }

    /* Estilo específico para o botão "Adicionar Post" */
    .stButton > button[kind="primary"] {
        background-color: #e6f3ff;  /* Azul claro suave */
        color: #0066cc;  /* Azul mais escuro para o texto */
        border-color: #b3d9ff;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #cce7ff;
        border-color: #80bfff;
    }

    /* Remover sublinhado de todos os elementos dentro do botão */
    .stButton > button *,
    .stButton > button *::before,
    .stButton > button *::after {
        text-decoration: none !important;
        border-bottom: none !important;
    }

    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }

    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }

    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho fixo
st.markdown("""
    <div class="fixed-header">
        <h1>Blog do Ministério de Música Isaías</h1>
    </div>
""", unsafe_allow_html=True)

# Função para pesquisar posts
def search_posts(query):
    session = Session()
    posts = session.query(Post).filter(
        (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
    ).all()
    session.close()
    return posts

# Inicializar o estado da sessão para o post selecionado
if 'selected_post_id' not in st.session_state:
    st.session_state.selected_post_id = None

# Função para atualizar o post selecionado
def select_post(post_id):
    st.session_state.selected_post_id = post_id
    st.rerun()

# Interface do Streamlit
st.title('Blog do Ministério de Música Isaías')

# Criando a coluna lateral esquerda
st.sidebar.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)

# Obtenha o diretório do script atual
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, 'logo.png')

# Verifique se o arquivo existe
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_column_width=True)
else:
    st.sidebar.warning(f"Logo não encontrada em: {logo_path}")
    # Use um texto como fallback
    st.sidebar.markdown('<h1 style="color: #6200EE;">MM Isaías</h1>', unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("Menu")

menu = ['Home', 'Meditações', 'Tutoriais', 'Notícias e Eventos', 'Adicionar Post']
choice = st.sidebar.radio('Navegação', menu)

# Adicionar posts de exemplo
add_example_posts()

# Conteúdo principal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == 'Adicionar Post':
    st.header('Adicionar Novo Post')
    
    # Formulário para adicionar novo post
    title = st.text_input("Título")
    content = st.text_area("Conteúdo")
    category = st.selectbox("Categoria", ['meditacao', 'tutorial', 'noticia'])
    image = st.file_uploader("Imagem (opcional)", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Adicionar", key="add_post", type="primary"):
        if title and content and category:
            session = Session()
            new_post = Post(
                title=title,
                content=content,
                category=category,
                date_posted=datetime.now()
            )
            if image:
                new_post.image = image.read()
            session.add(new_post)
            session.commit()
            session.close()
            st.success("Post adicionado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

else:
    # Criando o layout principal com duas colunas
    col1, col2 = st.columns([3, 1])

    # Coluna principal (conteúdo)
    with col1:
        if st.session_state.selected_post_id is not None:
            # Exibir o post selecionado
            session = Session()
            post = session.query(Post).filter(Post.id == st.session_state.selected_post_id).first()
            session.close()
            
            if post:
                st.title(post.title)
                st.write(f"Data: {post.date_posted.strftime('%d/%m/%Y')}")
                st.write(f"Categoria: {post.category}")
                if post.image:
                    st.image(post.image)
                st.write(post.content)
                if st.button("Voltar à página inicial"):
                    st.session_state.selected_post_id = None
                    st.rerun()
            else:
                st.error("Post não encontrado.")
        else:
            # Exibir a lista de posts normalmente
            if choice == 'Home':
                st.header('Posts Recentes')
                posts = get_posts()
                for post in posts:
                    with st.container():
                        image_b64 = get_image_base64(post.image)
                        image_html = f'<img src="data:image/png;base64,{image_b64}" style="max-width:100%; height:auto;">' if image_b64 else ''
                        st.markdown(f"""
                        <div class="post-card">
                            <h2>{post.title}</h2>
                            <p><em>{post.date_posted.strftime('%d/%m/%Y')}</em> 
                            <span class="category-chip">{post.category}</span></p>
                            {image_html}
                            <p>{post.content[:200]}...</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Leia mais: {post.title}", key=f"read_more_{post.id}"):
                            select_post(post.id)
            elif choice in ['Meditações', 'Tutoriais', 'Notícias e Eventos']:
                st.header(choice)
                category_map = {'Meditações': 'meditacao', 'Tutoriais': 'tutorial', 'Notícias e Eventos': 'noticia'}
                posts = [post for post in get_posts() if post.category == category_map[choice]]
                for post in posts:
                    with st.container():
                        image_b64 = get_image_base64(post.image)
                        image_html = f'<img src="data:image/png;base64,{image_b64}" style="max-width:100%; height:auto;">' if image_b64 else ''
                        st.markdown(f"""
                        <div class="post-card">
                            <h2>{post.title}</h2>
                            <p><em>{post.date_posted.strftime('%d/%m/%Y')}</em></p>
                            {image_html}
                            <p>{post.content}</p>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Coluna lateral direita
    with col2:
        st.subheader("Pesquisar")
        search_query = st.text_input("Buscar no blog")
        if search_query:
            session = Session()
            search_results = session.query(Post).filter(
                (Post.title.contains(search_query)) | (Post.content.contains(search_query))
            ).all()
            session.close()
            st.write(f"Resultados da pesquisa para '{search_query}':")
            for post in search_results:
                if st.button(post.title, key=f"search_{post.id}"):
                    st.session_state.selected_post_id = post.id
                    st.rerun()

        st.subheader("Últimos Posts")
        recent_posts = Session().query(Post).order_by(Post.date_posted.desc()).limit(5).all()
        for post in recent_posts:
            if st.button(post.title, key=f"recent_{post.id}"):
                st.session_state.selected_post_id = post.id
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)






