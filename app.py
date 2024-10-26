import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st
import base64

# Configuração do banco de dados
Base = declarative_base()

# Use SQLite em memória para o Streamlit Cloud
engine = create_engine('sqlite:///blog-isaias.db', connect_args={'timeout': 15}, echo=True)
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
    try:
        image_data = image.read() if image else None
        new_post = Post(title=title, content=content, category=category, image=image_data)
        session.add(new_post)
        session.commit()
    except Exception as e:
        session.rollback()  # Reverte a transação em caso de erro
        st.error(f"Ocorreu um erro ao adicionar o post: {e}")  # Exibe o erro no Streamlit
    finally:
        session.close()

def get_posts():
    session = Session()
    posts = session.query(Post).order_by(Post.date_posted.desc()).all()
    session.close()
    return posts

# Função auxiliar para converter a imagem em base64
def get_image_base64(image):
    if image:
        return base64.b64encode(image).decode()
    return None

# Configuração da página
st.set_page_config(page_title="Blog Ministério de Música Isaías1", layout="wide")

# Inicializar o estado da sessão para o post selecionado
if 'selected_post_id' not in st.session_state:
    st.session_state.selected_post_id = None  # Inicializa a variável

# Incluir CSS personalizado
st.markdown("""
<style>
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background-color: #F5F5F5;  /* Cinza claro, neutro e acolhedor */
        margin: 0;
        padding: 0;
    }
    .header {
        background: #8B4513;  /* Marrom escuro, simbolizando estabilidade */
        margin: 0;  /* Remove qualquer margem */
        padding: 0;  /* Remove qualquer padding */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .header h1 {
        margin: 0;  /* Remove a margem padrão do h1 */
        padding: 10px 0;  /* Ajuste o padding vertical do h1, se necessário */
        text-align: center;
        color: #FFFFFF;  /* Branco para contraste */
        font-size: 2.5em;
    }
    .container {
        max-width: 800px;
        margin: 100px auto 20px;  /* Aumenta a margem superior para evitar sobreposição com o cabeçalho fixo */
        padding: 20px;
        background: #FFFFFF;  /* Branco, para clareza */
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3, h4, h5, h6 {  /* Centraliza todos os cabeçalhos */
        text-align: center;
        color: #003366;  /* Azul escuro, simbolizando confiança e serenidade */
    }
    .card {
        background: #FAFAD2;  /* Amarelo claro, simbolizando alegria */
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .card-title {
        text-align: center;
        font-size: 1.8em;
        margin: 0;
        color: #8B0000;  /* Vermelho escuro, simbolizando amor e sacrifício */
    }
    .btn {
        background-color: #006400;  /* Verde escuro, simbolizando esperança */
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #228B22;  /* Verde mais claro */
    }
    .input-field label {
        margin-bottom: 5px;
        font-weight: bold;
        color: #003366;  /* Azul escuro */
    }
    .whatsapp-icon {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #25D366; /* Cor do WhatsApp */
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        text-align: center;
        transition: background-color 0.3s, transform 0.3s;
    }
    .whatsapp-icon:hover {
        background-color: #128C7E; /* Cor do WhatsApp ao passar o mouse */
        transform: scale(1.1); /* Aumenta o ícone ao passar o mouse */
    }
    .whatsapp-icon img {
        width: 50px; /* Tamanho do ícone */
        height: 50px; /* Tamanho do ícone */
    }
</style>
""", unsafe_allow_html=True)

# Adicionar a logo acima do menu
logo_path = "logo.png"  # Substitua pelo caminho correto da sua logo
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
else:
    st.sidebar.warning("Logo não encontrada.")

# Cabealho fixo
st.markdown("""
    <div class="header">
        <h1>Blog do Ministério de Música Isaías</h1>
    </div>
""", unsafe_allow_html=True)

# Interface do Streamlit
#st.title('Blog do Ministério de Música Isaías')

# Criando a coluna lateral esquerda
st.sidebar.title("Menu")
menu = ["Home", "Meditações", "Tutoriais", "Notícias e Eventos", "Adicionar Post", "Contato", "Vídeos"]
choice = st.sidebar.selectbox("Menu", menu)

# Conteúdo principal
if choice == 'Adicionar Post':
    st.header('Adicionar Novo Post')
    
    # Inicializar os campos do formulário no estado da sessão
    if 'title' not in st.session_state:
        st.session_state.title = ""
    if 'content' not in st.session_state:
        st.session_state.content = ""
    if 'category' not in st.session_state:
        st.session_state.category = "meditacao"
    if 'image' not in st.session_state:
        st.session_state.image = None

    with st.form(key='add_post_form'):
        title = st.text_input("Título", value=st.session_state.title)
        content = st.text_area("Conteúdo", value=st.session_state.content)
        category = st.selectbox("Categoria", ['meditacao', 'tutorial', 'noticia'], index=['meditacao', 'tutorial', 'noticia'].index(st.session_state.category))
        image = st.file_uploader("Imagem (opcional)", type=['png', 'jpg', 'jpeg'], key='image_uploader')

        submit_button = st.form_submit_button(label='Adicionar Post')
        
    if submit_button:
        add_post(title, content, category, image)  # Chama a função para adicionar o post
        st.success("Post adicionado com sucesso!")  # Exemplo de ação
        
        # Limpar os campos do formulário
        st.session_state.title = ""
        st.session_state.content = ""
        st.session_state.category = "meditacao"
        st.session_state.image = None

        # Redirecionar para a visualização atual
        st.rerun()  # Força a re-renderização da página

elif choice == "Contato":
    st.header("Entre em Contato")
    
    col1, col2 = st.columns(2)
    
    with col1:


        # Inicializar os campos do formulário no estado da sessão
        if 'name' not in st.session_state:
            st.session_state.name = ""
        if 'email' not in st.session_state:
            st.session_state.email = ""
        if 'message' not in st.session_state:
            st.session_state.message = ""

        # Campos do formulário
        name = st.text_input("Nome", value=st.session_state.name, key="name_input")
        email = st.text_input("Email", value=st.session_state.email, key="email_input")
        message = st.text_area("Mensagem", value=st.session_state.message, key="message_input")

        # Botão de envio
        if st.button("Enviar"):
            if name and email and message:  # Verifica se todos os campos estão preenchidos
                # Formulário HTML para enviar os dados
                form_html = f"""
                <form action="https://formsubmit.co/ministeriomusicaisaias@gmail.com" method="POST" style="display: none;">
                    <input type="text" name="name" value="{name}" required>
                    <input type="email" name="email" value="{email}" required>
                    <textarea name="message" required>{message}</textarea>
                </form>
                <script>
                    document.forms[0].submit();
                </script>
                """
                st.markdown(form_html, unsafe_allow_html=True)

                st.session_state['form_submitted'] = True  # Marca que o formulário foi enviado
                st.success("Mensagem enviada com sucesso!")  # Mensagem de sucesso

                # Limpar os campos
                st.session_state.name = ""
                st.session_state.email = ""
                st.session_state.message = ""

                # Atualizar os campos para refletir a limpeza
                name = ""
                email = ""
                message = ""
            else:
                st.error("Por favor, preencha todos os campos.")

    with col2:
        st.markdown("<h2 style='text-align: center;'>Redes Sociais</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            * <a href="https://www.facebook.com/seu_perfil">Facebook</a><br>
            * <a href="https://www.instagram.com/seu_perfil">Instagram</a><br>
            * <a href="https://www.youtube.com/seu_canal">YouTube</a><br>
            * <a href="https://twitter.com/seu_perfil">Twitter</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center;'>Email</h2>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>ministeriomusicaisaias@gmail.com</div>", unsafe_allow_html=True)

elif choice == 'Vídeos':
    st.header("Vídeos do Ministério de Música Isaías")

    # Lista de links dos vídeos do YouTube
    video_links = [
        "https://www.youtube.com/watch?v=syy3xDlaWoA",  # Substitua VIDEO_ID_1 pelo ID do seu vídeo
        "https://www.youtube.com/watch?v=c_pBavHAkaY",  # Substitua VIDEO_ID_2 pelo ID do seu vídeo
        "https://www.youtube.com/shorts/Ot-8HL6NoZQ",  # Substitua VIDEO_ID_3 pelo ID do seu vídeo
    ]

    # Exibir os vídeos
    for link in video_links:
        st.video(link)

else:
    # Criando o layout principal com duas colunas
    col1, col2 = st.columns([3, 1])

    # Coluna principal (conteúdo)
    with col1:
        # Verifique se um post foi selecionado
        if 'selected_post_id' in st.session_state and st.session_state.selected_post_id is not None:
            # Exibir o post selecionado
            post = Session().query(Post).filter(Post.id == st.session_state.selected_post_id).first()
            if post:
                st.title(post.title)
                st.write(f"Data: {post.date_posted.strftime('%d/%m/%Y')}")
                st.write(f"Categoria: {post.category}")
                if post.image:
                    st.image(post.image)
                st.write(post.content)
                
                # Botão para voltar à lista de posts
                if st.button("Voltar à lista de posts"):
                    st.session_state.selected_post_id = None  # Limpa a seleção
                    st.rerun()  # Redireciona para a visualização da lista de posts
            else:
                st.error("Post não encontrado.")
        else:
            # Exibir a lista de posts normalmente
            if choice == 'Home':
                st.header('Posts Recentes')
                posts = Session().query(Post).order_by(Post.date_posted.desc()).all()
                
                for post in posts:
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-body">
                                <span class="card-title">{post.title}</span>
                                <p><em>{post.date_posted.strftime('%d/%m/%Y')}</em></p>
                                <p>{post.content[:200]}...</p>
                            </div>
                            <div class="card-action">
                        """, unsafe_allow_html=True)

                        # Aqui está o botão "Selecionar" fora da string HTML
                        if st.button("Selecionar", key=f"select_{post.id}"):
                            st.session_state.selected_post_id = post.id
                            st.rerun()  # Redireciona para a visualização do post

                        st.markdown("</div></div>", unsafe_allow_html=True)

            elif choice in ['Meditações', 'Tutoriais', 'Notícias e Eventos']:
                st.header(choice)
                category_map = {'Meditações': 'meditacao', 'Tutoriais': 'tutorial', 'Notícias e Eventos': 'noticia'}
                posts = [post for post in get_posts() if post.category == category_map[choice]]
                for post in posts:
                    with st.container():
                        image_b64 = get_image_base64(post.image)
                        image_html = f'<img src="data:image/png;base64,{image_b64}" style="max-width:100%; height:auto;">' if image_b64 else ''
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-content">
                                <span class="card-title">{post.title}</span>
                                <p><em>{post.date_posted.strftime('%d/%m/%Y')}</em></p>
                                {image_html}
                                <p>{post.content}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    # Coluna lateral direita
    with col2:
        st.subheader("Pesquisar")
        search_query = st.text_input("Pesquisar posts")

        if search_query:
            session = Session()
            try:
                results = session.query(Post).filter(
                    (Post.title.ilike(f'%{search_query}%')) | 
                    (Post.content.ilike(f'%{search_query}%'))
                ).all()

                if results:
                    for post in results:
                        st.subheader(post.title)
                        st.write(post.content)
                        st.write(f"Categoria: {post.category}")
                        st.write(f"Publicado em: {post.date_posted}")
                        if post.image:
                            st.image(post.image)
                else:
                    st.write("Nenhum post encontrado.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar os posts: {e}")
            finally:
                session.close()

        st.subheader("Últimos Posts")
        recent_posts = Session().query(Post).order_by(Post.date_posted.desc()).limit(5).all()
        for post in recent_posts:
            if st.button(post.title, key=f"recent_{post.id}"):
                st.session_state.selected_post_id = post.id
                st.rerun()

# Exibir o conteúdo do post selecionado
if 'selected_post_id' in st.session_state:
    selected_post_id = st.session_state.selected_post_id
    #st.write(f"Post selecionado ID: {selected_post_id}")  # Para depuração
    post = Session().query(Post).filter(Post.id == selected_post_id).first()

# Adicionar o ícone do WhatsApp
whatsapp_number = "5534998264603"  # Substitua pelo número do WhatsApp do blog (inclua o código do país)
st.markdown(f"""
<a href="https://wa.me/{whatsapp_number}" class="whatsapp-icon" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
</a>
""", unsafe_allow_html=True)

