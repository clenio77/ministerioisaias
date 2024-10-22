import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import base64
import requests
from io import BytesIO

# Configuração do banco de dados
Base = declarative_base()
engine = create_engine('sqlite:///blog.db', echo=True)
Session = sessionmaker(bind=engine)

# Modelo de dados
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    category = Column(String(20), nullable=False)
    image = Column(LargeBinary, nullable=True)  # Novo campo para a imagem

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
        # Função para obter uma imagem de exemplo
        def get_example_image(url):
            response = requests.get(url)
            return BytesIO(response.content).read()

        example_posts = [
            Post(
                title="Meditação Semanal: O Poder do Louvor",
                content="Nesta semana, refletimos sobre o poder transformador do louvor em nossas vidas. O Salmo 22:3 nos diz que Deus habita nos louvores do seu povo. Quando louvamos, não apenas expressamos nossa gratidão, mas também convidamos a presença de Deus para nossas vidas...",
                category="meditacao",
                date_posted=datetime.now(),
                image=get_example_image("https://example.com/path/to/meditation_image.jpg")
            ),
            Post(
                title="Tutorial: Acordes Básicos no Violão",
                content="Neste tutorial, vamos aprender os acordes básicos no violão que são essenciais para acompanhar muitos hinos e canções de louvor. Começaremos com os acordes de Dó (C), Sol (G) e Ré (D). Para formar o acorde de Dó, coloque o dedo indicador na primeira casa da segunda corda...",
                category="tutorial",
                date_posted=datetime.now(),
                image=get_example_image("https://example.com/path/to/guitar_tutorial_image.jpg")
            ),
            Post(
                title="Próximo Evento: Noite de Louvor e Adoração",
                content="Estamos animados para anunciar nossa próxima Noite de Louvor e Adoração! O evento acontecerá no próximo sábado, às 19h, no salão principal da igreja. Teremos a participação especial do grupo de louvor 'Vozes para Cristo'. Venha se juntar a nós para uma noite de música, oração e comunhão...",
                category="noticia",
                date_posted=datetime.now(),
                image=get_example_image("https://example.com/path/to/event_image.jpg")
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

# CSS personalizado inspirado no Material Design
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
</style>
""", unsafe_allow_html=True)

# Interface do Streamlit
st.title('Blog do Ministério de Música Isaías')

menu = ['Home', 'Meditações', 'Tutoriais', 'Notícias e Eventos', 'Adicionar Post']
choice = st.sidebar.selectbox('Menu', menu)

# Adicione esta linha:
add_example_posts()

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
                <a href="#" onclick="return false;">Leia mais</a>
            </div>
            """, unsafe_allow_html=True)

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

elif choice == 'Adicionar Post':
    st.header('Adicionar Novo Post')
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input('Título')
        category = st.selectbox('Categoria', ['meditacao', 'tutorial', 'noticia'])
    with col2:
        content = st.text_area('Conteúdo', height=200)
    if st.button('Adicionar Post'):
        add_post(title, content, category)
        st.success('Post adicionado com sucesso!')

# Rodapé
st.markdown("""
<div style="position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #F5F5F5;">
    <p>© 2024 Ministério de Música Isaías. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
