import base64
import os
import re
import streamlit as st

# --- CONFIGURAÇÃO DE CAMINHOS ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOGO = os.path.join(DIRETORIO_ATUAL, "logo_G&G.png")
CAMINHO_SIDEBAR = os.path.join(DIRETORIO_ATUAL, "Barra_lateral.png")

# Função auxiliar para buscar imagem aceitando variações de nome de arquivo
def buscar_imagem(nome_base):
    for arquivo in os.listdir(DIRETORIO_ATUAL):
        if nome_base.lower() in arquivo.lower() and arquivo.endswith((".png", ".jpg", ".jpeg")):
            return os.path.join(DIRETORIO_ATUAL, arquivo)
    return ""

CAMINHO_BOSQUE = buscar_imagem("bosque")
CAMINHO_PALMEIRAS = buscar_imagem("palmeira") or buscar_imagem("jardim")
CAMINHO_VISTA = buscar_imagem("vista")

LOGO_EXISTE = os.path.exists(CAMINHO_LOGO)
SIDEBAR_EXISTE = os.path.exists(CAMINHO_SIDEBAR)


@st.cache_data
def get_image_base64(path):
    """Converte uma imagem local em string Base64 (com cache para performance)."""
    if path and os.path.exists(path):
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
    page_title="G&G Imóveis",
    page_icon=CAMINHO_LOGO if LOGO_EXISTE else "🏠",
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
            "<h2 style='text-align: center; color: #1e293b;'>Acesso ao Sistema</h2>",
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
            "<h2 style='text-align: center; color: #1e293b;'>Cadastro de Novo Cliente</h2>",
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

    # Estilização CSS: Tema Claro, Solar, Familiar e Acolhedor
    st.markdown(
        f"""
        <style>
            /* Fundo principal mais claro e limpo */
            .stApp {{
                background-color: #f8fafc;
                color: #1e293b;
            }}
            
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
            [data-testid="stSidebarUserContent"] {{
                margin-top: 280px !important;
                background-color: transparent !important;
                padding: 1rem !important;
            }}
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
                color: #FFFFFF !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            }}

            /* Estilo dos Cards em Tom Claro com Sombra Suave */
            .card-imovel-main {{
                background-color: #ffffff;
                border-radius: 0 0 12px 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                border: 1px solid #e2e8f0;
                border-top: none;
                margin-top: -10px;
                transition: transform 0.2s ease;
            }}
            .card-imovel-main h3 {{
                margin: 0 0 8px 0;
                color: #0f172a;
                font-size: 18px;
                font-weight: 700;
            }}
            .card-imovel-main p {{
                margin: 6px 0;
                color: #64748b;
                font-size: 14px;
            }}
            .card-imovel-main .valor {{
                color: #d97706; /* Dourado / Laranja Quente */
                font-weight: bold;
                font-size: 16px;
                margin-top: 12px;
            }}
            
            /* Título Comercial */
            .titulo-principal {{
                color: #0f172a;
                font-size: 32px;
                font-weight: 800;
                margin-bottom: 2px;
            }}
            .subtitulo-comercial {{
                color: #0284c7; /* Azul Mar / Verão */
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            .texto-boasvindas {{
                color: #64748b;
                font-size: 15px;
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
            "Cadastro de Cliente",
            "Cadastro de Corretor",
            "Simulação",
            "Sair",
        ],
    )

    # Lógica de navegação
    if menu == "Sair":
        st.session_state["tela"] = "login"
        st.rerun()

    elif menu == "Painel Geral":
        # Cabeçalho Focado na Venda e no Sonho da Casa Própria
        st.markdown("<h1 class='titulo-principal'>Sua casa a um passo de você ☀️🔑</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo-comercial'>Encontre o lar perfeito para criar as melhores memórias com quem você ama.</p>", unsafe_allow_html=True)
        st.markdown("<p class='texto-boasvindas'>Bem-vindo ao sistema de gestão imobiliária <b>G&G Imóveis</b>.</p>", unsafe_allow_html=True)

        st.write("")
        st.subheader("🏡 Oportunidades e Destaques da Semana")

        col_img1, col_img2, col_img3 = st.columns(3)

        # Imóvel 1: Bosque Imperial
        with col_img1:
            if CAMINHO_BOSQUE and os.path.exists(CAMINHO_BOSQUE):
                st.image(CAMINHO_BOSQUE, use_container_width=True)
            st.markdown(
                """
                <div class="card-imovel-main">
                    <h3>Residencial Bosque Imperial</h3>
                    <p><i>Conforto, segurança e área de lazer completa para a família.</i></p>
                    <p class="valor">Valores a partir de R$ 350 mil</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Imóvel 2: Jardim das Palmeiras
        with col_img2:
            if CAMINHO_PALMEIRAS and os.path.exists(CAMINHO_PALMEIRAS):
                st.image(CAMINHO_PALMEIRAS, use_container_width=True)
            st.markdown(
                """
                <div class="card-imovel-main">
                    <h3>Condomínio Jardim das Palmeiras</h3>
                    <p><i>O lugar ideal para viver seus melhores momentos ao ar livre.</i></p>
                    <p class="valor">Valores a partir de R$ 220 mil</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Imóvel 3: Vista Verde
        with col_img3:
            if CAMINHO_VISTA and os.path.exists(CAMINHO_VISTA):
                st.image(CAMINHO_VISTA, use_container_width=True)
            st.markdown(
                """
                <div class="card-imovel-main">
                    <h3>Residencial Vista Verde</h3>
                    <p><i>Seu novo lar cercado de tranquilidade e natureza.</i></p>
                    <p class="valor">Valores a partir de R$ 185 mil</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif menu == "Cadastro de Cliente":
        st.title("Cadastro de Cliente")
        nome_cli = st.text_input("Nome Completo do Cliente")
        cpf_cli = st.text_input("CPF")
        email_cli = st.text_input("E-mail")
        if st.button("Salvar Cliente"):
            st.success(f"Cliente {nome_cli} cadastrado com sucesso!")

    elif menu == "Cadastro de Corretor":
        st.title("Cadastro de Corretor")
        nome_corr = st.text_input("Nome Completo do Corretor")
        creci = st.text_input("Número do CRECI")
        telefone_corr = st.text_input("Telefone/WhatsApp")
        if st.button("Salvar Corretor"):
            st.success(f"Corretor {nome_corr} cadastrado com sucesso!")

    elif menu == "Simulação":
        st.title("Simulação de Financiamento")
        st.write("Calcule a estimativa de parcelas para o seu cliente:")
        valor_imovel = st.number_input("Valor do Imóvel (R$)", value=300000)
        entrada = st.number_input("Valor da Entrada (R$)", value=60000)
        parcelas = st.slider("Número de Parcelas (Meses)", 12, 420, 360)

        if st.button("Simular"):
            saldo_devedor = valor_imovel - entrada
            parcela_estimada = saldo_devedor / parcelas
            st.info(f"Valor a financiar: R$ {saldo_devedor:,.2f}")
            st.success(f"Valor estimado da parcela simples: R$ {parcela_estimada:,.2f}")

            