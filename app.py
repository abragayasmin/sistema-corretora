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

# Oculta a barra lateral totalmente
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

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
            telefone = st.text_input("Telefone / WhatsApp", placeholder="Ex: (82) 99999-9999")
            
            c1, c2 = st.columns(2)
            with c1:
                renda = st.number_input("Renda Mensal (R$)", min_value=0.0, step=500.0)
            with c2:
                data_nasc = st.date_input("Data de Nascimento")

            senha = st.text_input("Senha", type="password", placeholder="Crie uma senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")

            st.caption("Requisitos da senha: mínimo de 6 caracteres, 1 caractere especial e 1 letra maiúscula.")
            st.write("")
            submit_cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

        if submit_cadastrar:
            cpf_limpo = re.sub(r"\D", "", cpf)

            if not nome or not cpf_limpo or not email or not telefone or not senha:
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
                    "telefone": telefone,
                    "nascimento": str(data_nasc),
                    "renda": renda,
                    "senha": senha,
                }
                st.success("Cadastro efetuado com sucesso! Faça seu login utilizando seu CPF.")
                st.session_state["etapa_fluxo"] = "login"
                st.rerun()

        st.write("")
        if st.button("Voltar para o Login", use_container_width=True):
            st.session_state["etapa_fluxo"] = "login"
            st.rerun()

# --- 4. PAINEL GERAL (OPORTUNIDADES E BOTÃO SIMULE SUA ENTRADA) ---
elif st.session_state["etapa_fluxo"] == "painel_geral":
    st.markdown("<h1>Sua casa a um passo de você</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Encontre o lar perfeito para criar as melhores memórias com quem você ama.</h3>", unsafe_allow_html=True)
    st.write("Bem-vindo ao sistema de gestão imobiliária G&G Imóveis.")

    st.write("")
    st.subheader("Oportunidades e Destaques da Semana")

    col_img1, col_img2, col_img3 = st.columns(3)

    with col_img1:
        img_bosque = carregar_imagem_padronizada(CAMINHO_BOSQUE)
        if img_bosque:
            st.image(img_bosque, use_container_width=True)
        st.subheader("Residencial Bosque Imperial")
        st.write("Conforto, segurança e área de lazer completa para a família.")
        st.write("**Valores a partir de R$ 350 mil**")
        if st.button("Simule sua entrada", key="btn_bosque", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Residencial Bosque Imperial - R$ 350.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

    with col_img2:
        img_palmeiras = carregar_imagem_padronizada(CAMINHO_PALMEIRAS)
        if img_palmeiras:
            st.image(img_palmeiras, use_container_width=True)
        st.subheader("Condomínio Jardim das Palmeiras")
        st.write("O lugar ideal para viver seus melhores momentos ao ar livre.")
        st.write("**Valores a partir de R$ 220 mil**")
        if st.button("Simule sua entrada", key="btn_palmeiras", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Condomínio Jardim das Palmeiras - R$ 220.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

    with col_img3:
        img_vista = carregar_imagem_padronizada(CAMINHO_VISTA)
        if img_vista:
            st.image(img_vista, use_container_width=True)
        st.subheader("Residencial Vista Verde")
        st.write("Seu novo lar cercado de tranquilidade e natureza.")
        st.write("**Valores a partir de R$ 185 mil**")
        if st.button("Simule sua entrada", key="btn_vista", use_container_width=True):
            st.session_state["imovel_selecionado"] = "Residencial Vista Verde - R$ 185.000,00"
            st.session_state["etapa_fluxo"] = "passo1_cliente"
            st.rerun()

# --- 5. PASSO 1: CADASTRO/COMPLETAÇÃO DE DADOS DO CLIENTE ---
elif st.session_state["etapa_fluxo"] == "passo1_cliente":
    st.header("Passo 1 de 3: Cadastro e Ficha do Cliente")
    st.write("Confirme ou complete suas informações cadastrais para prosseguir.")

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
        tel_cli = st.text_input("Telefone / WhatsApp", value=dados_atuais.get("telefone", ""))
        
        c1, c2 = st.columns(2)
        with c1:
            renda_cli = st.number_input("Renda Mensal (R$)", value=float(dados_atuais.get("renda", 0.0)), step=500.0)
        with c2:
            nasc_cli = st.text_input("Data de Nascimento", value=dados_atuais.get("nascimento", ""))

        btn_avancar = st.form_submit_button("Salvar e Avançar para o Cadastro de Corretor →", use_container_width=True)

    if btn_avancar:
        cpf_salvar = dados_atuais.get("cpf", cpf_atual)
        if not cpf_salvar or not nome_cli or not email_cli:
            st.error("Preencha ao menos Nome e E-mail.")
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
        