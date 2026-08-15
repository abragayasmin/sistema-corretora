import base64
import os
import re
import streamlit as st

# --- CONFIGURAÇÃO DE CAMINHOS ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOGO = os.path.join(DIRETORIO_ATUAL, "logo_G&G.png")
CAMINHO_SIDEBAR = os.path.join(DIRETORIO_ATUAL, "Barra_lateral.png")

LOGO_EXISTE = os.path.exists(CAMINHO_LOGO)
SIDEBAR_EXISTE = os.path.exists(CAMINHO_SIDEBAR)


def get_image_base64(path):
    """Converte uma imagem local em string Base64."""
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    return ""


def validar_senha(senha: str) -> bool:
    """Valida se a senha tem no mínimo 6 caracteres, 1 letra maiúscula e 1 caractere especial."""
    if len(senha) < 6:
        return False
    tem_maiuscula = bool(re.search(r"[A-Z]", senha))
    tem_especial = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\]", senha))
    return tem_maiuscula and tem_especial


# --- 1. CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Sistema Corretora",
    page_icon=CAMINHO_LOGO if LOGO_EXISTE else "📈",
    layout="wide",
)

if "tela" not in st.session_state:
    st.session_state["tela"] = "login"

# Esconde a barra lateral nas telas de Login e Cadastro
if st.session_state["tela"] in ["login", "cadastro_inicial"]:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- 2. TELA INICIAL: LOGIN ---
if st.session_state["tela"] == "login":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if LOGO_EXISTE:
            img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
            with img_col2:
                st.image(CAMINHO_LOGO, use_container_width=True)

        st.markdown(
            "<h2 style='text-align: center;'>Acesso ao Sistema</h2>",
            unsafe_allow_html=True,
        )
        st.write("")

        with st.form("form_login"):
            cpf = st.text_input("CPF / Usuário", placeholder="Digite seu CPF")
            senha = st.text_input(
                "Senha", type="password", placeholder="Digite sua senha"
            )
            st.write("")

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                submit_login = st.form_submit_button(
                    "Entrar", use_container_width=True
                )
            with btn_col2:
                submit_cancelar = st.form_submit_button(
                    "Cancelar", use_container_width=True
                )

        if submit_login:
            if len(cpf) >= 6 and validar_senha(senha):
                st.success("Login realizado com sucesso! Bem-vindo(a).")
                st.session_state["tela"] = "sistema"
                st.rerun()
            else:
                st.error(
                    "Credenciais inválidas! A senha deve ter no mínimo 6 caracteres, "
                    "incluindo 1 letra maiúscula e 1 caractere especial."
                )

        st.divider()

        st.write("Não possui conta?")
        if st.button("Me cadastrar", use_container_width=True):
            st.session_state["tela"] = "cadastro_inicial"
            st.rerun()

# --- 3. TELA DE CADASTRO INICIAL DO CLIENTE ---
elif st.session_state["tela"] == "cadastro_inicial":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if LOGO_EXISTE:
            img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
            with img_col2:
                st.image(CAMINHO_LOGO, use_container_width=True)

        st.markdown(
            "<h2 style='text-align: center;'>Cadastro de Novo Cliente</h2>",
            unsafe_allow_html=True,
        )
        st.write("")

        with st.form("form_cadastro"):
            nome = st.text_input(
                "Nome Completo", placeholder="Digite seu nome completo"
            )
            cpf = st.text_input("CPF", placeholder="Digite seu CPF")
            email = st.text_input("E-mail", placeholder="Digite seu e-mail")
            senha = st.text_input(
                "Senha", type="password", placeholder="Crie uma senha"
            )
            confirmar_senha = st.text_input(
                "Confirmar Senha", type="password", placeholder="Repita a senha"
            )

            st.caption(
                " Requisitos da senha: mínimo de 6 caracteres, 1 caractere especial e 1 letra maiúscula."
            )
            st.write("")
            submit_cadastrar = st.form_submit_button(
                "Cadastrar", use_container_width=True
            )

        if submit_cadastrar:
            if not nome or not cpf or not email or not senha:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            elif not validar_senha(senha):
                st.error(
                    "A senha não atende aos requisitos mínimos (6+ caracteres, 1 maiúscula e 1 caractere especial)."
                )
            elif senha != confirmar_senha:
                st.error("As senhas digitadas não coincidem.")
            else:
                st.success("Cadastro efetuado com sucesso!")
                st.session_state["tela"] = "login"
                st.rerun()

        st.write("")
        if st.button("Voltar para o Login", use_container_width=True):
            st.session_state["tela"] = "login"
            st.rerun()

# --- 4. ÁREA PRINCIPAL DO SISTEMA ---
elif st.session_state["tela"] == "sistema":
    # CSS personalizado para fixar a barra lateral e formatar o conteúdo
    st.markdown(
        """
        <style>
            /* Fixa a largura da barra lateral no tamanho ideal do print */
            [data-testid="stSidebar"] {
                min-width: 350px !important;
                max-width: 350px !important;
            }
            
            /* Remove margens superiores da barra lateral */
            [data-testid="stSidebarHeader"] {
                display: none !important;
            }
            [data-testid="stSidebarContent"] {
                padding-top: 0rem !important;
            }
            [data-testid="stSidebarUserContent"] {
                padding: 0rem !important;
            }

            /* Garante que a imagem do topo ocupe toda a largura sem bordas */
            [data-testid="stSidebarUserContent"] div[data-testid="stImage"] {
                margin: 0rem !important;
                padding: 0rem !important;
                width: 100% !important;
            }
            [data-testid="stSidebarUserContent"] img {
                border-radius: 0px !important;
                width: 100% !important;
            }

            /* Espaçamento das seções de texto e menu abaixo da imagem */
            .sidebar-content {
                padding: 1rem 1.2rem;
            }

            /* Cartões estilizados para os imóveis */
            .card-imovel {
                background-color: #1e222d;
                border-left: 4px solid #00d26a;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 12px;
            }
            .card-imovel h4 {
                margin: 0 0 4px 0;
                color: #ffffff;
                font-size: 14px;
            }
            .card-imovel p {
                margin: 2px 0;
                color: #b0b8c4;
                font-size: 12px;
            }
            .card-imovel .valor {
                color: #00d26a;
                font-weight: bold;
                font-size: 13px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 1. Imagem no topo da barra lateral
    if SIDEBAR_EXISTE:
        st.sidebar.image(CAMINHO_SIDEBAR, use_container_width=True)

    # 2. Navegação do Sistema
    st.sidebar.title("Navegação")
    menu = st.sidebar.radio(
        "Selecione a Tela:",
        [
            "Painel Geral",
            "Cadastrar Cliente",
            "Cadastrar Ativo",
            "Registrar Transação",
            "Consultar Clientes",
            "Consultar Ativos",
            "Consultar Transações",
            "Relatório Financeiro",
            "Sair",
        ],
    )

    st.sidebar.divider()

    # 3. Lista de Imóveis em Destaque abaixo do menu
    st.sidebar.subheader("🏢 Imóveis em Destaque")

    st.sidebar.markdown(
        """
        <div class="card-imovel">
            <h4>Residencial Bosque Imperial</h4>
            <p><i>Conforto, segurança e qualidade de vida.</i></p>
            <p class="valor">Valores a partir de R$ 350 mil</p>
        </div>
        
        <div class="card-imovel">
            <h4>Condomínio Jardim das Palmeiras</h4>
            <p><i>O lugar ideal para viver seus melhores momentos.</i></p>
            <p class="valor">Valores a partir de R$ 220 mil</p>
        </div>
        
        <div class="card-imovel">
            <h4>Residencial Vista Verde</h4>
            <p><i>Seu novo lar cercado de tranquilidade.</i></p>
            <p class="valor">Valores a partir de R$ 185 mil</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Lógica de navegação do painel principal
    if menu == "Sair":
        st.session_state["tela"] = "login"
        st.rerun()
    elif menu == "Painel Geral":
        st.title("Painel Geral da Corretora")
        st.write("Bem-vindo ao sistema de gestão de ativos e clientes!")
    elif menu == "Cadastrar Cliente":
        st.title("Cadastro de Clientes")
        nome_cli = st.text_input("Nome Completo")
        cpf_cli = st.text_input("CPF")
        if st.button("Salvar Cliente"):
            st.success(f"Cliente {nome_cli} cadastrado com sucesso!")
    else:
        st.title(menu)
        st.write(f"Conteúdo da tela de **{menu}** em desenvolvimento.")
        