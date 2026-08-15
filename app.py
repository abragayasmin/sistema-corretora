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
    sidebar_bg = get_image_base64(CAMINHO_SIDEBAR)

    # Estilização CSS para remover totalmente o fundo escuro da navegação
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                background-image: url("{sidebar_bg}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            [data-testid="stSidebar"] > div:first-child {{
                background-color: transparent !important;
            }}
            [data-testid="stSidebarContent"] {{
                background-color: transparent !important;
                padding-top: 0rem !important;
            }}
            /* Espaçamento superior mantido para não cobrir a logomarca */
            [data-testid="stSidebarUserContent"] {{
                margin-top: 280px !important;
                background-color: transparent !important; /* Totalmente transparente */
                padding: 1rem !important;
            }}
            /* Sombra nas letras para garantir boa leitura sobre a imagem */
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
                color: #FFFFFF !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            }}

            /* Estilo dos cartões de imóveis na área principal */
            .card-container {{
                display: flex;
                gap: 20px;
                margin-top: 20px;
                flex-wrap: wrap;
            }}
            .card-imovel-main {{
                background-color: #1e222d;
                border-top: 4px solid #00d26a;
                padding: 18px;
                border-radius: 8px;
                flex: 1;
                min-width: 250px;
            }}
            .card-imovel-main h3 {{
                margin: 0 0 8px 0;
                color: #ffffff;
                font-size: 16px;
            }}
            .card-imovel-main p {{
                margin: 4px 0;
                color: #b0b8c4;
                font-size: 13px;
            }}
            .card-imovel-main .valor {{
                color: #00d26a;
                font-weight: bold;
                font-size: 15px;
                margin-top: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Menu de Navegação na Barra Lateral
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

    # Lógica de navegação
    if menu == "Sair":
        st.session_state["tela"] = "login"
        st.rerun()
    elif menu == "Painel Geral":
        st.title("Painel Geral da Corretora")
        st.write("Bem-vindo ao sistema de gestão de ativos e clientes!")

        st.write("")
        st.subheader("🏢 Imóveis em Destaque")

        # Exibe os imóveis logo abaixo do título do Painel Geral
        st.markdown(
            """
            <div class="card-container">
                <div class="card-imovel-main">
                    <h3>Residencial Bosque Imperial</h3>
                    <p><i>Conforto, segurança e qualidade de vida.</i></p>
                    <p class="valor">Valores a partir de R$ 350 mil</p>
                </div>
                <div class="card-imovel-main">
                    <h3>Condomínio Jardim das Palmeiras</h3>
                    <p><i>O lugar ideal para viver seus melhores momentos.</i></p>
                    <p class="valor">Valores a partir de R$ 220 mil</p>
                </div>
                <div class="card-imovel-main">
                    <h3>Residencial Vista Verde</h3>
                    <p><i>Seu novo lar cercado de tranquilidade.</i></p>
                    <p class="valor">Valores a partir de R$ 185 mil</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif menu == "Cadastrar Cliente":
        st.title("Cadastro de Clientes")
        nome_cli = st.text_input("Nome Completo")
        cpf_cli = st.text_input("CPF")
        if st.button("Salvar Cliente"):
            st.success(f"Cliente {nome_cli} cadastrado com sucesso!")
    else:
        st.title(menu)
        st.write(f"Conteúdo da tela de **{menu}** em desenvolvimento.")
        