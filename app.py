import streamlit as st

# Configuração inicial da página
st.set_page_config(page_title="Sistema Corretora", layout="wide")

# Inicializa a tela atual no estado da sessão (padrão é "login")
if "tela" not in st.session_state:
    st.session_state["tela"] = "login"

# Esconde a barra lateral enquanto estiver na tela de Login ou Cadastro Inicial
if st.session_state["tela"] in ["login", "cadastro_inicial"]:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. TELA INICIAL: LOGIN ---
if st.session_state["tela"] == "login":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
        st.write("")

        with st.form("form_login"):
            cpf = st.text_input("CPF / Usuário", placeholder="Digite seu CPF")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            st.write("")
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                submit_login = st.form_submit_button("Entrar", use_container_width=True)
            with btn_col2:
                submit_cancelar = st.form_submit_button("Cancelar", use_container_width=True)

        if submit_login:
            if len(cpf) >= 6 and len(senha) >= 6:
                st.success(f"Login realizado com sucesso! Bem-vindo(a).")
                # Ao fazer login com sucesso, libera o sistema principal
                st.session_state["tela"] = "sistema"
                st.rerun()
            else:
                st.error("Informe um CPF e Senha válidos (mínimo 6 caracteres).")

        st.divider()

        # Botão para redirecionar para a tela de cadastro
        st.write("Não possui conta?")
        if st.button("Me cadastrar", use_container_width=True):
            st.session_state["tela"] = "cadastro_inicial"
            st.rerun()

# --- 2. TELA DE CADASTRO INICIAL DO CLIENTE ---
elif st.session_state["tela"] == "cadastro_inicial":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h2 style='text-align: center;'>Cadastro de Novo Cliente</h2>", unsafe_allow_html=True)
        st.write("")

        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo", placeholder="Digite seu nome completo")
            cpf = st.text_input("CPF", placeholder="Digite seu CPF")
            email = st.text_input("E-mail", placeholder="Digite seu e-mail")
            senha = st.text_input("Senha", type="password", placeholder="Crie uma senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")
            
            st.write("")
            submit_cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

        if submit_cadastrar:
            if not nome or not cpf or not email or not senha:
                st.error("Por favor, preencha todos os campos obrigatórios.")
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

# --- 3. ÁREA PRINCIPAL DO SISTEMA (COM MENU LATERAL) ---
elif st.session_state["tela"] == "sistema":
    # Exibe o menu lateral apenas dentro do sistema
    st.sidebar.title("Corretora - Navegação")
    menu = st.sidebar.radio(
        "Selecione a Tela:",
        [
            "Painel Geral",
            "Cadastrar Cliente", "Cadastrar Ativo", "Registrar Transação",
            "Consultar Clientes", "Consultar Ativos", "Consultar Transações",
            "Relatório Financeiro", "Sair"
        ]
    )

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
        

