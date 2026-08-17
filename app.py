import base64
import os
import re
from PIL import Image
import streamlit as st

# --- CONFIGURAÇÃO DE CAMINHOS ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOGO = os.path.join(DIRETORIO_ATUAL, "logo_G&G.png")
CAMINHO_SIDEBAR = os.path.join(DIRETORIO_ATUAL, "Barra_lateral.png")

def buscar_imagem(nome_base):
    for arquivo in os.listdir(DIRETORIO_ATUAL):
        if nome_base.lower() in arquivo.lower() and arquivo.endswith((".png", ".jpg", ".jpeg")):
            return os.path.join(DIRETORIO_ATUAL, arquivo)
    return ""

CAMINHO_BOSQUE = buscar_imagem("bosque")
CAMINHO_PALMEIRAS = buscar_imagem("palmeira") or buscar_imagem("jardim")
CAMINHO_VISTA = buscar_imagem("vista")

LOGO_EXISTE = os.path.exists(CAMINHO_LOGO)


@st.cache_data
def get_image_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    return ""


@st.cache_data
def carregar_imagem_padronizada(caminho, largura=600, altura=400):
    if caminho and os.path.exists(caminho):
        img = Image.open(caminho)
        img_proporcional = img.copy()
        img_proporcional.thumbnail((largura, altura * 2))
        
        w, h = img_proporcional.size
        left = (w - largura) / 2 if w > largura else 0
        top = (h - altura) / 2 if h > altura else 0
        right = (w + largura) / 2 if w > largura else w
        bottom = (h + altura) / 2 if h > altura else h
        
        img_cropped = img_proporcional.crop((left, top, right, bottom))
        return img_cropped.resize((largura, altura))
    return None


def validar_senha(senha: str) -> bool:
    if len(senha) < 6:
        return False
    tem_maiuscula = bool(re.search(r"[A-Z]", senha))
    tem_especial = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\]", senha))
    return tem_maiuscula and tem_especial


# --- BANCOS DE DADOS EM MEMÓRIA ---
if "banco_clientes" not in st.session_state:
    st.session_state["banco_clientes"] = {
        "12345678900": {
            "cpf": "12345678900",
            "nome": "Cliente Exemplo",
            "email": "cliente@email.com",
            "telefone": "(82) 99999-9999",
            "nascimento": "1990-01-01",
            "renda": 5000.0,
            "senha": "Senha@123"
        }
    }

if "banco_corretores" not in st.session_state:
    st.session_state["banco_corretores"] = {}

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# --- 1. CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="G&G Imóveis",
    layout="wide",
)

if "tela" not in st.session_state:
    st.session_state["tela"] = "login"

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
            cpf = st.text_input("CPF / Usuário", placeholder="Digite apenas números")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            st.write("")

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                submit_login = st.form_submit_button("Entrar", use_container_width=True)
            with btn_col2:
                submit_cancelar = st.form_submit_button("Cancelar", use_container_width=True)

        if submit_login:
            cpf_limpo = re.sub(r"\D", "", cpf)
            if cpf_limpo in st.session_state["banco_clientes"]:
                usuario = st.session_state["banco_clientes"][cpf_limpo]
                if usuario["senha"] == senha:
                    st.session_state["usuario_logado"] = cpf_limpo
                    st.session_state["tela"] = "sistema"
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
            else:
                st.error("CPF não cadastrado no sistema!")

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
            nome = st.text_input("Nome Completo", placeholder="Ex: João da Silva")
            cpf = st.text_input("CPF", placeholder="Apenas números")
            email = st.text_input("E-mail", placeholder="seuemail@exemplo.com")
            telefone = st.text_input("Telefone / WhatsApp", placeholder="Ex: (82) 99999-9999")
            
            c1, c2 = st.columns(2)
            with c1:
                data_nasc = st.date_input("Data de Nascimento")
            with c2:
                renda = st.number_input("Renda Familiar Mensal (R$)", min_value=0.0, step=500.0)

            senha = st.text_input("Senha", type="password", placeholder="Crie uma senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")

            st.caption("Requisitos da senha: mínimo de 6 caracteres, 1 caractere especial e 1 letra maiúscula.")
            st.write("")
            submit_cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

        if submit_cadastrar:
            cpf_limpo = re.sub(r"\D", "", cpf)

            if not nome or not cpf_limpo or not email or not telefone or not senha:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            elif cpf_limpo in st.session_state["banco_clientes"]:
                st.error("Este CPF já está cadastrado na plataforma!")
            elif not validar_senha(senha):
                st.error("A senha não atende aos requisitos mínimos (6+ caracteres, 1 maiúscula e 1 caractere especial).")
            elif senha != confirmar_senha:
                st.error("As senhas digitadas não coincidem.")
            else:
                st.session_state["banco_clientes"][cpf_limpo] = {
                    "cpf": cpf_limpo,
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "nascimento": str(data_nasc),
                    "renda": renda,
                    "senha": senha,
                }
                st.success("Cadastro efetuado com sucesso! Agora faça seu login.")
                st.session_state["tela"] = "login"
                st.rerun()

        st.write("")
        if st.button("Voltar para o Login", use_container_width=True):
            st.session_state["tela"] = "login"
            st.rerun()

# --- 4. ÁREA PRINCIPAL DO SISTEMA ---
elif st.session_state["tela"] == "sistema":
    sidebar_bg = get_image_base64(CAMINHO_SIDEBAR)

    st.markdown(
        f"""
        <style>
            [data-testid="stHeader"] {{
                background: linear-gradient(90deg, #101c2c 0%, #1b2d42 100%) !important;
            }}
            .stApp {{
                background-color: #f8fafc;
                color: #0f172a;
            }}
            label, [data-testid="stWidgetLabel"] p {{
                color: #0f172a !important;
                font-weight: 600 !important;
                font-size: 15px !important;
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
            .card-imovel-main {{
                background-color: #ffffff;
                border-radius: 0 0 12px 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                border: 1px solid #e2e8f0;
                border-top: none;
                margin-top: -10px;
            }}
            .card-imovel-main h3 {{
                margin: 0 0 8px 0;
                color: #0f172a;
                font-size: 18px;
                font-weight: 700;
            }}
            .card-imovel-main p {{
                margin: 6px 0;
                color: #475569;
                font-size: 14px;
            }}
            .card-imovel-main .valor {{
                color: #d97706;
                font-weight: bold;
                font-size: 16px;
                margin-top: 12px;
            }}
            .titulo-principal {{
                color: #0f172a;
                font-size: 32px;
                font-weight: 800;
                margin-bottom: 2px;
            }}
            .subtitulo-comercial {{
                color: #0f172a;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            .texto-boasvindas {{
                color: #64748b;
                font-size: 14px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

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

    if menu == "Sair":
        st.session_state["usuario_logado"] = None
        st.session_state["tela"] = "login"
        st.rerun()

    elif menu == "Painel Geral":
        st.markdown("<h1 class='titulo-principal'>Sua casa a um passo de você</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo-comercial'>Encontre o lar perfeito para criar as melhores memórias com quem você ama.</p>", unsafe_allow_html=True)
        st.markdown("<p class='texto-boasvindas'>Bem-vindo ao sistema de gestão imobiliária G&G Imóveis.</p>", unsafe_allow_html=True)

        st.write("")
        st.subheader("Oportunidades e Destaques da Semana")

        col_img1, col_img2, col_img3 = st.columns(3)

        with col_img1:
            img_bosque = carregar_imagem_padronizada(CAMINHO_BOSQUE)
            if img_bosque:
                st.image(img_bosque, use_container_width=True)
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

        with col_img2:
            img_palmeiras = carregar_imagem_padronizada(CAMINHO_PALMEIRAS)
            if img_palmeiras:
                st.image(img_palmeiras, use_container_width=True)
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

        with col_img3:
            img_vista = carregar_imagem_padronizada(CAMINHO_VISTA)
            if img_vista:
                st.image(img_vista, use_container_width=True)
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
        st.title("Cadastro e Ficha do Cliente")
        st.write("Preencha ou atualize os dados primordiais do cliente no sistema.")

        cpf_atual = st.session_state.get("usuario_logado", "")
        dados_atuais = st.session_state["banco_clientes"].get(cpf_atual, {})

        with st.form("form_atualizar_cliente"):
            nome_cli = st.text_input("Nome Completo", value=dados_atuais.get("nome", ""))
            cpf_cli = st.text_input("CPF do Cliente", value=dados_atuais.get("cpf", cpf_atual), placeholder="Digite apenas os números")
            email_cli = st.text_input("E-mail", value=dados_atuais.get("email", ""))
            tel_cli = st.text_input("Telefone / WhatsApp", value=dados_atuais.get("telefone", ""))
            
            c1, c2 = st.columns(2)
            with c1:
                renda_cli = st.number_input("Renda Familiar Mensal (R$)", value=float(dados_atuais.get("renda", 0.0)), step=500.0)
            with c2:
                nasc_cli = st.text_input("Data de Nascimento", value=dados_atuais.get("nascimento", ""))

            btn_salvar = st.form_submit_button("Salvar Ficha do Cliente")

        if btn_salvar:
            cpf_novo_limpo = re.sub(r"\D", "", cpf_cli)
            
            if not cpf_novo_limpo or not nome_cli or not email_cli:
                st.error("Preencha ao menos Nome, CPF e E-mail.")
            else:
                st.session_state["banco_clientes"][cpf_novo_limpo] = {
                    "cpf": cpf_novo_limpo,
                    "nome": nome_cli,
                    "email": email_cli,
                    "telefone": tel_cli,
                    "renda": renda_cli,
                    "nascimento": nasc_cli,
                    "senha": dados_atuais.get("senha", "Senha@123")
                }
                
                if cpf_atual and cpf_atual != cpf_novo_limpo and cpf_atual in st.session_state["banco_clientes"]:
                    del st.session_state["banco_clientes"][cpf_atual]
                    st.session_state["usuario_logado"] = cpf_novo_limpo
                    
                st.success(f"Ficha do cliente registrada com sucesso e atrelada ao CPF {cpf_novo_limpo}!")

    elif menu == "Cadastro de Corretor":
        st.title("Cadastro de Corretor")
        st.write("Informe os dados do corretor parceiro para inclusão no sistema:")

        with st.form("form_cadastro_corretor"):
            nome_corr = st.text_input("Nome Completo do Corretor", placeholder="Ex: Carlos Eduardo Silva")
            cpf_corr = st.text_input("CPF do Corretor", placeholder="Digite apenas os números")
            creci = st.text_input("Número do CRECI", placeholder="Ex: 12345-F")
            telefone_corr = st.text_input("Telefone / WhatsApp", placeholder="Ex: (82) 98888-8888")

            btn_salvar_corr = st.form_submit_button("Salvar Corretor")

        if btn_salvar_corr:
            cpf_corr_limpo = re.sub(r"\D", "", cpf_corr)

            if not nome_corr or not cpf_corr_limpo or not creci:
                st.error("Por favor, preencha os campos obrigatórios (Nome, CPF e CRECI).")
            else:
                st.session_state["banco_corretores"][cpf_corr_limpo] = {
                    "nome": nome_corr,
                    "cpf": cpf_corr_limpo,
                    "creci": creci,
                    "telefone": telefone_corr,
                }
                st.success(f"Corretor **{nome_corr}** (CRECI: {creci}) cadastrado com sucesso!")

    elif menu == "Simulação":
        st.title("Simulação de Financiamento")
        st.write("Calcule a estimativa de financiamento para o cliente:")

        # Mapeamento dos imóveis e seus respectivos valores numéricos
        imoveis_opcoes = {
            "Residencial Bosque Imperial - R$ 350.000,00": 350000.0,
            "Condomínio Jardim das Palmeiras - R$ 220.000,00": 220000.0,
            "Residencial Vista Verde - R$ 185.000,00": 185000.0
        }

        imovel_selecionado = st.selectbox(
            "Selecione o Imóvel:",
            options=list(imoveis_opcoes.keys())
        )
        
        # Puxa apenas o valor do imóvel selecionado
        valor_imovel = imoveis_opcoes[imovel_selecionado]

        entrada = st.number_input("Valor da Entrada (R$)", value=50000.0, step=5000.0)

        if st.button("Simular Financiamento"):
            if entrada >= valor_imovel:
                st.error("O valor da entrada não pode ser igual ou superior ao valor do imóvel.")
            else:
                saldo_devedor = valor_imovel - entrada
                st.info(f"**Valor do Imóvel Selecionado:** R$ {valor_imovel:,.2f}")
                st.success(f"**Saldo a Financiar (Valor do Imóvel - Entrada):** R$ {saldo_devedor:,.2f}")

                