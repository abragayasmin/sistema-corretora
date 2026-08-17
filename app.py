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
        top = (h - altura) / 2 if h > largura else 0
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
            "renda": 3000.0,
            "senha": "Senha@123"
        }
    }

if "banco_corretores" not in st.session_state:
    st.session_state["banco_corretores"] = {}

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if "imovel_selecionado" not in st.session_state:
    st.session_state["imovel_selecionado"] = None

if "etapa_fluxo" not in st.session_state:
    st.session_state["etapa_fluxo"] = "login"

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="G&G Imóveis",
    layout="wide",
)

sidebar_bg_base64 = get_image_base64(CAMINHO_SIDEBAR)
exibir_sidebar = st.session_state["etapa_fluxo"] not in ["login", "cadastro_inicial"]

# Estilização CSS adaptável por tela
st.markdown(
    f"""
    <style>
        /* Fundo Principal Claro */
        .stApp {{
            background-color: #F8F9FA !important;
            color: #0E1D2F !important;
        }}
        
        /* Títulos e Textos Principais */
        h1, h2, h3, h4, h5, h6, p, span, label {{
            color: #0E1D2F !important;
        }}
        
        .subtitulo-cinza {{
            color: #556070 !important;
        }}

        /* Esconde a barra lateral nas telas de Login e Cadastro */
        [data-testid="stSidebar"] {{
            display: {"block" if exibir_sidebar else "none"} !important;
            background-image: url("{sidebar_bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-width: 280px !important;
            max-width: 280px !important;
        }}
        
        /* Oculta botão de recolher sidebar */
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        /* Cartões de Imóveis */
        div[data-testid="stColumn"] > div {{
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        }}

        /* Botões padronizados */
        .stButton>button {{
            background-color: #0E1D2F !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
        }}
        
        .stButton>button:hover {{
            background-color: #1A2E47 !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

if exibir_sidebar:
    with st.sidebar:
        st.empty()

# --- 2. TELA INICIAL: LOGIN ---
if st.session_state["etapa_fluxo"] == "login":
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
            cpf = st.text_input("CPF do Cliente", placeholder="Digite apenas os 11 números do seu CPF")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            st.write("")

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                submit_login = st.form_submit_button("Entrar", use_container_width=True)
            with btn_col2:
                submit_cancelar = st.form_submit_button("Cancelar", use_container_width=True)

        if submit_login:
            cpf_limpo = re.sub(r"\D", "", cpf)

            if not cpf_limpo or len(cpf_limpo) != 11:
                st.error("Acesso permitido apenas via CPF! Digite um CPF válido com 11 números.")
            elif cpf_limpo in st.session_state["banco_clientes"]:
                usuario = st.session_state["banco_clientes"][cpf_limpo]
                if usuario["senha"] == senha:
                    st.session_state["usuario_logado"] = cpf_limpo
                    st.session_state["etapa_fluxo"] = "painel_geral"
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
            else:
                st.error("CPF não cadastrado no sistema!")

        st.divider()

        st.write("Não possui conta?")
        if st.button("Me cadastrar", use_container_width=True):
            st.session_state["etapa_fluxo"] = "cadastro_inicial"
            st.rerun()

# --- 3. TELA DE CADASTRO INICIAL DO CLIENTE ---
elif st.session_state["etapa_fluxo"] == "cadastro_inicial":
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
            nome = st.text_input("Nome Completo", placeholder="Ex: João da Silva")
            cpf = st.text_input("CPF", placeholder="Apenas os 11 números do CPF")
            email = st.text_input("E-mail", placeholder="seuemail@exemplo.com")

            senha = st.text_input("Senha", type="password", placeholder="Crie uma senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")

            st.caption("Requisitos da senha: mínimo de 6 caracteres, 1 caractere especial e 1 letra maiúscula.")
            st.write("")
            submit_cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

        if submit_cadastrar:
            cpf_limpo = re.sub(r"\D", "", cpf)

            if not nome or not cpf_limpo or not email or not senha:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            elif len(cpf_limpo) != 11:
                st.error("O CPF deve conter exatamente 11 dígitos numéricos.")
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
                    "telefone": "",
                    "nascimento": "",
                    "renda": 0.0,
                    "senha": senha,
                }
                st.success("Cadastro efetuado com sucesso! Faça seu login utilizando seu CPF.")
                st.session_state["etapa_fluxo"] = "login"
                st.rerun()

        st.write("")
        if st.button("Voltar para o Login", use_container_width=True):
            st.session_state["etapa_fluxo"] = "login"
            st.rerun()

# --- 4. PAINEL GERAL ---
elif st.session_state["etapa_fluxo"] == "painel_geral":
    st.markdown("<h1>Sua casa a um passo de você</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-cinza' style='font-size: 1.1rem; font-weight: 600;'>Encontre o lar perfeito para criar as melhores memórias com quem você ama.</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-cinza'>Bem-vindo ao sistema de gestão imobiliária G&G Imóveis.</p>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<h3>Oportunidades e Destaques da Semana</h3>", unsafe_allow_html=True)

    col_img1, col_img2, col_img3 = st.columns(3)

    with col_img1:
        img_bosque = carregar_imagem_padronizada(CAMINHO_BOSQUE)
        if img_bosque:
            st.image(img_bosque, use_container_width=True)
        st.markdown("<h4>Residencial Bosque Imperial</h4>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo-cinza'><i>Conforto, segurança e área de lazer completa para a família.</i></p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #C27803 !important; font-weight: bold;'>Valores a partir de R$ 350 mil</p>", unsafe_allow_html=True)
        if st.button("Simule sua entrada", key="btn_bosque", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Residencial Bosque Imperial - R$ 350.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

    with col_img2:
        img_palmeiras = carregar_imagem_padronizada(CAMINHO_PALMEIRAS)
        if img_palmeiras:
            st.image(img_palmeiras, use_container_width=True)
        st.markdown("<h4>Condomínio Jardim das Palmeiras</h4>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo-cinza'><i>O lugar ideal para viver seus melhores momentos ao ar livre.</i></p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #C27803 !important; font-weight: bold;'>Valores a partir de R$ 220 mil</p>", unsafe_allow_html=True)
        if st.button("Simule sua entrada", key="btn_palmeiras", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Condomínio Jardim das Palmeiras - R$ 220.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

    with col_img3:
        img_vista = carregar_imagem_padronizada(CAMINHO_VISTA)
        if img_vista:
            st.image(img_vista, use_container_width=True)
        st.markdown("<h4>Residencial Vista Verde</h4>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo-cinza'><i>Seu novo lar cercado de tranquilidade e natureza.</i></p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #C27803 !important; font-weight: bold;'>Valores a partir de R$ 185 mil</p>", unsafe_allow_html=True)
        if st.button("Simule sua entrada", key="btn_vista", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Residencial Vista Verde - R$ 185.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

# --- 5. PASSO 1: COMPLETAR FICHA DO CLIENTE ---
elif st.session_state["etapa_fluxo"] == "passo1_cliente":
    st.header("Passo 1 de 3: Cadastro e Ficha do Cliente")
    st.write("Complete as informações essenciais do cliente para poder realizar a simulação:")

    cpf_atual = st.session_state.get("usuario_logado", "")
    dados_atuais = st.session_state["banco_clientes"].get(cpf_atual, {})

    with st.form("form_atualizar_cliente_passo1"):
        nome_cli = st.text_input("Nome Completo", value=dados_atuais.get("nome", ""))
        
        cpf_cli = st.text_input(
            "CPF do Cliente",
            value=dados_atuais.get("cpf", cpf_atual),
            disabled=True,
            help="O CPF está vinculado à sua conta e não pode ser alterado."
        )
        
        email_cli = st.text_input("E-mail", value=dados_atuais.get("email", ""))
        tel_cli = st.text_input("Telefone / WhatsApp", value=dados_atuais.get("telefone", ""), placeholder="Ex: (82) 99999-9999")
        
        c1, c2 = st.columns(2)
        with c1:
            renda_cli = st.number_input("Renda Mensal (R$)", value=float(dados_atuais.get("renda", 0.0)), step=500.0)
        with c2:
            nasc_cli = st.text_input("Data de Nascimento", value=dados_atuais.get("nascimento", ""), placeholder="Ex: 01/01/1990")

        btn_avancar = st.form_submit_button("Salvar e Avançar para o Cadastro de Corretor →", use_container_width=True)

    if btn_avancar:
        cpf_salvar = dados_atuais.get("cpf", cpf_atual)
        if not cpf_salvar or not nome_cli or not email_cli or not tel_cli or renda_cli <= 0:
            st.error("Por favor, preencha todos os campos obrigatórios (incluindo WhatsApp e Renda Mensal).")
        else:
            st.session_state["banco_clientes"][cpf_salvar] = {
                "cpf": cpf_salvar,
                "nome": nome_cli,
                "email": email_cli,
                "telefone": tel_cli,
                "renda": renda_cli,
                "nascimento": nasc_cli,
                "senha": dados_atuais.get("senha", "Senha@123")
            }
            st.session_state["etapa_fluxo"] = "passo2_corretor"
            st.rerun()

# --- 6. PASSO 2: CADASTRO DO CORRETOR ---
elif st.session_state["etapa_fluxo"] == "passo2_corretor":
    st.header("Passo 2 de 3: Cadastro do Corretor")
    st.write("Informe os dados do corretor responsável ou parceiro para vinculação à simulação:")

    with st.form("form_cadastro_corretor_passo2"):
        nome_corr = st.text_input("Nome Completo do Corretor", placeholder="Ex: Carlos Eduardo Silva")
        cpf_corr = st.text_input("CPF do Corretor", placeholder="Digite apenas os números")
        creci = st.text_input("Número do CRECI", placeholder="Ex: 12345-F")
        telefone_corr = st.text_input("Telefone / WhatsApp", placeholder="Ex: (82) 98888-8888")

        btn_avancar_simulacao = st.form_submit_button("Salvar Corretor e Ir para Simulação →", use_container_width=True)

    if btn_avancar_simulacao:
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
            st.session_state["etapa_fluxo"] = "passo3_simulacao"
            st.rerun()

# --- 7. PASSO 3: SIMULAÇÃO DO FINANCIAMENTO ---
elif st.session_state["etapa_fluxo"] == "passo3_simulacao":
    st.header("Passo 3 de 3: Simulação de Financiamento")
    st.write("Confirme os dados de entrada para gerar a proposta completa de financiamento.")

    imoveis_opcoes = {
        "Residencial Bosque Imperial - R$ 350.000,00": 350000.0,
        "Condomínio Jardim das Palmeiras - R$ 220.000,00": 220000.0,
        "Residencial Vista Verde - R$ 185.000,00": 185000.0
    }

    imovel_padrao = st.session_state.get("imovel_selecionado", "Residencial Bosque Imperial - R$ 350.000,00")
    lista_chaves = list(imoveis_opcoes.keys())
    idx_padrao = lista_chaves.index(imovel_padrao) if imovel_padrao in lista_chaves else 0

    imovel_selecionado = st.selectbox(
        "Imóvel Selecionado:",
        options=lista_chaves,
        index=idx_padrao
    )
    
    valor_imovel = imoveis_opcoes[imovel_selecionado]
    entrada = st.number_input("Valor da Entrada (R$)", value=50000.0, step=5000.0)

    if st.button("Gerar Cálculo Final da Simulação", use_container_width=True):
        cpf_limpo = st.session_state.get("usuario_logado", "")

        if not cpf_limpo or cpf_limpo not in st.session_state["banco_clientes"]:
            st.error("CPF de cliente válido não encontrado na sessão. Retorne ao início.")
        elif entrada > valor_imovel:
            st.error("O valor da entrada não pode ser maior que o valor total do imóvel.")
        else:
            cliente = st.session_state["banco_clientes"][cpf_limpo]
            renda_cliente = cliente.get("renda", 0.0)

            salario_minimo = 1518.0
            qtd_salarios = renda_cliente / salario_minimo if salario_minimo > 0 else 0

            if qtd_salarios <= 1:
                taxa_juros_mensal = 0.5
            elif qtd_salarios <= 2:
                taxa_juros_mensal = 1.0
            elif qtd_salarios <= 3:
                taxa_juros_mensal = 2.0
            elif qtd_salarios <= 4:
                taxa_juros_mensal = 4.0
            else:
                taxa_juros_mensal = 6.0

            taxa_juros_anual = taxa_juros_mensal * 12

            porcentagem_entrada = (entrada / valor_imovel) * 100

            if porcentagem_entrada >= 100:
                pct_subsidio = 0.35
            elif porcentagem_entrada > 50:
                pct_subsidio = 0.20
            elif porcentagem_entrada > 45:
                pct_subsidio = 0.12
            elif porcentagem_entrada > 20:
                pct_subsidio = 0.07
            else:
                pct_subsidio = 0.02

            valor_subsidio = valor_imovel * pct_subsidio
            saldo_devedor = valor_imovel - entrada - valor_subsidio
            saldo_devedor_exibir = max(0.0, saldo_devedor)

            st.info(f"**Cliente:** {cliente.get('nome')} | **Renda Mensal:** R$ {renda_cliente:,.2f} ({qtd_salarios:.1f} Salários Mínimos)")
            st.info(f"**Taxa de Juros Aplicada:** {taxa_juros_mensal:.1f}% a.m. ({taxa_juros_anual:.1f}% a.a.)")
            st.info(f"**Valor do Imóvel Selecionado:** R$ {valor_imovel:,.2f}")
            st.info(f"**Subsídio Concedido ({pct_subsidio * 100:.0f}%):** R$ {valor_subsidio:,.2f}")
            st.success(f"**Saldo Final a Financiar:** R$ {saldo_devedor_exibir:,.2f}")

    st.write("")
    if st.button("← Voltar ao Painel Geral", use_container_width=True):
        st.session_state["etapa_fluxo"] = "painel_geral"
        st.rerun()
        