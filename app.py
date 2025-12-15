# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# CONFIGURAÇÃO DO LOGIN
# ============================================

# Usuários e senhas (para produção, use secrets.toml ou banco de dados)
USERS = {
    "admin": "admin123",
    "gerente": "gerente123",
    "analista": "analista123"
}

# Inicializar estado de login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# ============================================
# FUNÇÃO DE LOGIN
# ============================================
def show_login():
    """Exibe a tela de login"""
    
    # Configuração da página de login
    st.set_page_config(
        page_title="Login - Cocred Dashboard",
        page_icon="🔐",
        layout="centered"
    )
    
    # CSS para página de login
    st.markdown("""
    <style>
        .main {
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .sicredi-logo {
            font-size: 80px;
            color: #003641;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .login-title {
            color: #003641;
            margin-bottom: 10px;
            font-size: 28px;
            font-weight: 700;
        }
        .login-subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        .stButton > button {
            background: linear-gradient(135deg, #00AE9D 0%, #003641 100%);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 10px;
            font-weight: bold;
            width: 100%;
            font-size: 16px;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 174, 157, 0.3);
        }
        .stTextInput > div > div > input {
            padding: 14px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            transition: border 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #00AE9D;
            box-shadow: 0 0 0 3px rgba(0, 174, 157, 0.1);
        }
        .credential-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #00AE9D;
        }
        .kpi-trend-indicator {
            display: none;
        }
        
        .filtro-campanha {
            min-width: 250px; /* ou o valor necessário */
            width: auto;
        }
        .filtro-campanha select,
        .filtro-campanha .dropdown {
            padding: 10px 15px;
            box-sizing: border-box;
        }
        .filtro-campanha select {
            width: 100%;
            max-width: 300px;
            padding: 12px 20px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px; /* tamanho de fonte adequado */
            line-height: 1.5;
        }
        
        
        
    </style>
    """, unsafe_allow_html=True)
    
    # Container de login
    st.markdown("""
    <div class="login-container">
        <div class="sicredi-logo"></div>
        <h1 class="login-title">COCRED Dashboard</h1>
        <p class="login-subtitle">
            Plataforma de Análise de Campanhas e Investimentos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulário de login
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                login_button = st.form_submit_button("🚀 Entrar no Dashboard", use_container_width=True)
                
                if login_button:
                    if not username or not password:
                        st.error("⚠️ Por favor, preencha todos os campos")
                    elif username in USERS and USERS[username] == password:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos")
            
            # Informações de acesso (em produção, remova esta seção)
            st.markdown("---")
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #777; font-size: 0.9rem; padding: 20px;'>"
        "© 2025 Cocred Cooperativa - Todos os direitos reservados<br>"
        "Sistema de Dashboard para Análise de Campanhas<br>"
        "Acesso restrito a pessoal autorizado"
        "</div>",
        unsafe_allow_html=True
    )

# ============================================
# VERIFICAÇÃO DE LOGIN
# ============================================
if not st.session_state["logged_in"]:
    show_login()
    st.stop()

# ============================================
# SE CHEGOU AQUI, USUÁRIO ESTÁ LOGADO
# ============================================

# ============================================
# CONFIGURAÇÕES DA MARCA COCRED - NOVA PALETA
# ============================================
COCRED_COLORS = {
    'verde_claro': '#C9D200',           # Verde Claro
    'verde_escuro': '#003641',          # Verde Escuro (principal)
    'roxo': '#49479D',                  # Roxo (apenas detalhes pequenos)
    'turquesa': '#00AE9D',              # Turquesa (secundário)
    'terra': '#8D6E63',                 # Cor de terra - referência agrícola
    'ouro': '#FFB300',                  # Dourado - referência a colheita
    'branco': '#FFFFFF',
    'cinza_claro': '#F5F5F5',
    'cinza_medio': '#9E9E9E',
    'cinza_escuro': '#424242',
    'verde_medio': "#565C01",
    'laranja': '#F57C00',               # Para destaques específicos
}

# ============================================
# THEME HELPERS (Light/Dark aware)
# ============================================
def get_current_theme():
    """Retorna propriedades do tema atual do Streamlit, com defaults sensatos."""
    try:
        base = st.get_option("theme.base") or "light"
    except Exception:
        base = "light"
    is_dark = (base == "dark")

    # Cores do tema (usam defaults se não houver config.toml)
    bg = st.get_option("theme.backgroundColor") or ("#0E1117" if is_dark else "#FFFFFF")
    sbg = st.get_option("theme.secondaryBackgroundColor") or ("#262730" if is_dark else "#F6F8FA")
    text = st.get_option("theme.textColor") or ("#FAFAFA" if is_dark else "#31333F")
    primary = st.get_option("theme.primaryColor") or COCRED_COLORS['turquesa']

    # Plotly template
    plotly_template = "plotly_dark" if is_dark else "plotly"

    # Cores auxiliares para borda/sombras
    subtle_border = "rgba(255,255,255,0.15)" if is_dark else "rgba(0,0,0,0.08)"
    subtle_shadow = "rgba(0,0,0,0.35)" if is_dark else "rgba(0,0,0,0.08)"

    return {
        "is_dark": is_dark,
        "bg": bg,
        "sbg": sbg,
        "text": text,
        "primary": primary,
        "plotly_template": plotly_template,
        "subtle_border": subtle_border,
        "subtle_shadow": subtle_shadow
    }

THEME = get_current_theme()

# Configuração da página Cocred Agrícola
st.set_page_config(
    page_title="Dashboard de Campanhas - COCRED",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS PERSONALIZADO - TEMA COCRED
# ============================================
st.markdown(f"""
<style>
    /* Fundo geral com textura sutil */
    .stApp {{
        background: linear-gradient(135deg, {COCRED_COLORS['branco']} 0%, #F9F9F9 100%);
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }}
    
    /* Sidebar com gradiente usando Verde Escuro e Turquesa */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COCRED_COLORS['verde_escuro']} 0%, #002933 100%);
        padding: 20px;
    }}
    
    /* Títulos com cor principal Verde Escuro */
    h1, h2, h3, .st-emotion-cache-10trblm {{
        color: {COCRED_COLORS['verde_escuro']} !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-align: left;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    
    /* Métricas/KPIs com fundo sólido e bordas definidas */
    .stMetric {{
        background: light-grey;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid {COCRED_COLORS['turquesa']};
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    
    .stMetric label {{
        font-weight: 700 !important;
        color: {COCRED_COLORS['verde_escuro']} !important;
        font-size: 14px !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {COCRED_COLORS['turquesa']} !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    
    /* Métricas na área principal com gradiente claro */
    .main .stMetric {{
        background: linear-gradient(135deg, #E6F4F1, white) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 2px solid {COCRED_COLORS['turquesa']} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }}
    
    /* Métricas na sidebar com transparência */
    [data-testid="stSidebar"] .stMetric {{
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}
    
    /* Tabs usando Verde Claro e Turquesa */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {COCRED_COLORS['cinza_claro']};
        padding: 8px;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        color: {COCRED_COLORS['cinza_escuro']};
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid {COCRED_COLORS['cinza_claro']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COCRED_COLORS['roxo']} 17%, {COCRED_COLORS['turquesa']} 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }}
    
    /* Texto na sidebar */
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
        font-weight: 600;
    }}
    
    [data-testid="stSidebar"] .stMetric label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {{
        color: {COCRED_COLORS['verde_claro']} !important;
    }}
    
    /* Detalhes em roxo conforme solicitado */
    .stMetric [data-testid="stMetricDelta"] {{
        color: {COCRED_COLORS['roxo']} !important;
    }}
    
    .stMetric [data-testid="stMarkdownContainer"] {{
        color: {COCRED_COLORS['roxo']} !important;
    }}
    
    /* Links e pequenos elementos */
    a, .small-detail {{
        color: {COCRED_COLORS['roxo']} !important;
    }}
    
    /* ESTILO ESPECÍFICO PARA O BOTÃO DE LOGOUT NA SIDEBAR */
    /* Usando o mesmo gradiente das tabs ativas */
    [data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(135deg, {COCRED_COLORS['roxo']} 17%, {COCRED_COLORS['turquesa']} 100%) !important;
        color: white !important;
        border: none;
        padding: 14px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100% !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        cursor: pointer;
    }}

    [data-testid="stSidebar"] .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(73, 71, 157, 0.4) !important;
        background: linear-gradient(135deg, {COCRED_COLORS['roxo']} 25%, {COCRED_COLORS['turquesa']} 100%) !important;
        color: white !important;
    }}

    /* Garantir que o texto fique branco */
    [data-testid="stSidebar"] .stButton > button p {{
        color: white !important;
        font-weight: bold !important;
        margin: 0;
    }}

    /* Remover qualquer estilo secundário do Streamlit */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background: linear-gradient(135deg, {COCRED_COLORS['roxo']} 17%, {COCRED_COLORS['turquesa']} 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }}

    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, {COCRED_COLORS['roxo']} 25%, {COCRED_COLORS['turquesa']} 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# CABEÇALHO DO DASHBOARD COM LOGOUT
# ============================================
col_header1, col_header2, col_header3 = st.columns([3, 2, 1])

with col_header1:
    st.markdown(f"""
       <div style="text-align: left; margin-bottom: 20px;">
    <h1 style="
        color: {COCRED_COLORS['verde_escuro']};
        font-size: 42px;
        font-weight: 700;
        margin: 0;
        padding: 10px 0;
        text-align: justify;
    ">
        📊 Dashboard de Campanhas - Análise de Investimentos
    </h1>
    
""", unsafe_allow_html=True)

with col_header3:
    st.markdown(f"""
        <div style="text-align: right; padding-top: 10px;">
            <div style="display: inline-block; background: rgba(0, 54, 65, 0.1); padding: 8px 16px; border-radius: 20px;">
                <span style="color: {COCRED_COLORS['verde_escuro']}; font-weight: bold;">
                    👤 {st.session_state['username'].capitalize()}
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Separador decorativo com novas cores
st.markdown(f"""
<div style="height: 4px; background: linear-gradient(90deg, {COCRED_COLORS['verde_claro']}, {COCRED_COLORS['turquesa']}, {COCRED_COLORS['verde_escuro']}); 
            border-radius: 2px; margin: 20px 0;"></div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR COM INFORMAÇÕES DO USUÁRIO E LOGOUT
# ============================================
with st.sidebar:
    # Informações do usuário
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 50px; color: white;"></div>
            <h3 style="color: white; margin-bottom: 5px; text-align: center;">COCRED Dashboard</h3>
            <div style="background: rgba(255, 255, 255, 0.2); padding: 10px; border-radius: 10px; margin: 10px 0;">
                <p style="margin: 0; font-weight: bold;">👤 {st.session_state['username'].capitalize()}</p>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Usuário logado</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Botão de logout com contêiner para estilo personalizado
    logout_container = st.container()
    with logout_container:
        if st.button("🚪 Sair do Sistema", 
                    type="secondary", 
                    use_container_width=True,
                    help="Clique para sair do sistema"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
    
    # Espaçamento após o botão
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Separador visual
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin: 20px 0;'>", unsafe_allow_html=True)

# ============================================
# DADOS DAS CAMPANHAS
# ============================================
data = [
    # campanha_investimentos_2025
    {"campanha": "campanha_investimentos_2025", "canal": "Rádio*", "Investimento": 130279.37, "porcentagem_investimento": 0.15054568046381514, "impactos": 5270645, "porcentagem_impactos": 0.11331211653406507, "cpm": 24.71791782599663},
    {"campanha": "campanha_investimentos_2025", "canal": "Painel de LED*", "Investimento": 6117.2, "porcentagem_investimento": 0.007068794057979019, "impactos": 56398, "porcentagem_impactos": 0.0012124847619766085, "cpm": 108.46483917869428},
    {"campanha": "campanha_investimentos_2025", "canal": "Revista*", "Investimento": 7500, "porcentagem_investimento": 0.008666702974374328, "impactos": 125000, "porcentagem_impactos": 0.0026873398923202255, "cpm": 60},
    {"campanha": "campanha_investimentos_2025", "canal": "TV*", "Investimento": 580123.84, "porcentagem_investimento": 0.6703681346177942, "impactos": 33760901, "porcentagem_impactos": 0.7258161284637903, "cpm": 17.183304438468628},
    {"campanha": "campanha_investimentos_2025", "canal": "Meta Ads", "Investimento": 10936.25, "porcentagem_investimento": 0.0126374973871335, "impactos": 5410725, "porcentagem_impactos": 0.11632365711099481, "cpm": 2.021217119702073},
    {"campanha": "campanha_investimentos_2025", "canal": "Google Ads", "Investimento": 4932.36, "porcentagem_investimento": 0.005699639877691328, "impactos": 618880, "porcentagem_impactos": 0.013305127300473129, "cpm": 7.969816442605998},
    {"campanha": "campanha_investimentos_2025", "canal": "Linkedin", "Investimento": 9991.97, "porcentagem_investimento": 0.011546324815847874, "impactos": 1244802, "porcentagem_impactos": 0.02676164858112001, "cpm": 8.026955290881602},
    {"campanha": "campanha_investimentos_2025", "canal": "Mídias Orgânicas", "Investimento": 0, "porcentagem_investimento": 0, "impactos": 27048, "porcentagem_impactos": 0.0005814973552598197, "cpm": 0},
    
    # campanha_credito_rural_2025
    {"campanha": "campanha_credito_rural_2025", "canal": "Rádio*", "Investimento": 81828.69, "porcentagem_investimento": 0.11, "impactos": 3774956, "porcentagem_impactos": 0.1097, "cpm": 21.68},
    {"campanha": "campanha_credito_rural_2025", "canal": "Painel de LED*", "Investimento": 43480.17, "porcentagem_investimento": 0.06, "impactos": 204739, "porcentagem_impactos": 0.006, "cpm": 212.37},
    {"campanha": "campanha_credito_rural_2025", "canal": "Revista*", "Investimento": 7500, "porcentagem_investimento": 0.01, "impactos": 125000, "porcentagem_impactos": 0.0036, "cpm": 60},
    {"campanha": "campanha_credito_rural_2025", "canal": "TV*", "Investimento": 491273.16, "porcentagem_investimento": 0.65, "impactos": 28732072, "porcentagem_impactos": 0.8353, "cpm": 17.1},
    {"campanha": "campanha_credito_rural_2025", "canal": "Meta Ads", "Investimento": 9177.95, "porcentagem_investimento": 0.01, "impactos": 1133576, "porcentagem_impactos": 0.033, "cpm": 8.1},
    {"campanha": "campanha_credito_rural_2025", "canal": "Google Ads", "Investimento": 5548.54, "porcentagem_investimento": 0.01, "impactos": 413067, "porcentagem_impactos": 0.012, "cpm": 13.43},
    {"campanha": "campanha_credito_rural_2025", "canal": "Mídias Orgânicas", "Investimento": 0, "porcentagem_investimento": 0, "impactos": 13391, "porcentagem_impactos": 0.0004, "cpm": 0},
    
    # campanha_credito_2025
    {"campanha": "campanha_credito_2025", "canal": "Rádio*", "Investimento": 38262.5, "porcentagem_investimento": 0.06922708611945404, "impactos": 2144860, "porcentagem_impactos": 0.09801629936945129, "cpm": 17.84},
    {"campanha": "campanha_credito_2025", "canal": "Painel de LED*", "Investimento": 58160, "porcentagem_investimento": 0.10522698016876698, "impactos": 2197139, "porcentagem_impactos": 0.10040535698381099, "cpm": 26.47},
    {"campanha": "campanha_credito_2025", "canal": "Revista*", "Investimento": 7500, "porcentagem_investimento": 0.013569503976371258, "impactos": 125000, "porcentagem_impactos": 0.005712278387018925, "cpm": 60},
    {"campanha": "campanha_credito_2025", "canal": "TV*", "Investimento": 435592.33, "porcentagem_investimento": 0.7881029138682428, "impactos": 16452414, "porcentagem_impactos": 0.7518461512519007, "cpm": 26.48},
    {"campanha": "campanha_credito_2025", "canal": "Meta Ads", "Investimento": 8288.83, "porcentagem_investimento": 0.01499670821926205, "impactos": 632210, "porcentagem_impactos": 0.028890876152457876, "cpm": 13.11},
    {"campanha": "campanha_credito_2025", "canal": "Google Ads", "Investimento": 4906.3, "porcentagem_investimento": 0.008876807647902708, "impactos": 331064, "porcentagem_impactos": 0.015129037855360267, "cpm": 14.82},
    {"campanha": "campanha_credito_2025", "canal": "Mídias Orgânicas", "Investimento": 0, "porcentagem_investimento": 0, "impactos": 0, "porcentagem_impactos": 0, "cpm": 0},
]

# Criar DataFrame
df = pd.DataFrame(data)

# ============================================
# FUNÇÃO DE AGREGAÇÃO PARA "TODAS AS CAMPANHAS"
# ============================================
def agregar_dados_contextuais(df, campanha_selecionada, canal_selecionado):
    """
    Agrega dados de forma inteligente:
    - Se 'Todas as Campanhas': agrega por canal (soma investimentos, cálculo correto de CPM)
    - Se campanha específica: mantém dados originais daquela campanha
    """
    df_filtrado = df.copy()
    if canal_selecionado:
        df_filtrado = df_filtrado[df_filtrado['canal'].isin(canal_selecionado)]
    
    if campanha_selecionada == 'Todas as Campanhas':
        df_agregado = df_filtrado.groupby('canal').agg({
            'Investimento': 'sum',
            'impactos': 'sum'
        }).reset_index()
        df_agregado['cpm'] = df_agregado.apply(
            lambda r: (r['Investimento'] / r['impactos'] * 1000) if r['impactos'] > 0 else 0, axis=1
        )
        total_invest_agregado = df_agregado['Investimento'].sum()
        total_impactos_agregado = df_agregado['impactos'].sum()
        df_agregado['porcentagem_investimento'] = (
            df_agregado['Investimento'] / total_invest_agregado if total_invest_agregado > 0 else 0
        )
        df_agregado['porcentagem_impactos'] = (
            df_agregado['impactos'] / total_impactos_agregado if total_impactos_agregado > 0 else 0
        )
        df_agregado['campanha'] = 'Todas as Campanhas'
        df_agregado = df_agregado[['campanha', 'canal', 'Investimento', 'porcentagem_investimento', 
                                   'impactos', 'porcentagem_impactos', 'cpm']]
        return df_agregado
    
    else:
        df_filtrado = df_filtrado[df_filtrado['campanha'] == campanha_selecionada]
        if not df_filtrado.empty:
            total_invest_campanha = df_filtrado['Investimento'].sum()
            total_impactos_campanha = df_filtrado['impactos'].sum()
            df_filtrado['porcentagem_investimento'] = (
                df_filtrado['Investimento'] / total_invest_campanha if total_invest_campanha > 0 else 0
            )
            df_filtrado['porcentagem_impactos'] = (
                df_filtrado['impactos'] / total_impactos_campanha if total_impactos_campanha > 0 else 0
            )
        return df_filtrado

# ============================================
# FUNÇÃO PARA DADOS COMPARATIVOS ENTRE CAMPANHAS
# ============================================
def calcular_metricas_por_campanha(df_filtrado):
    """Calcula métricas agregadas por campanha para comparação"""
    if df_filtrado['campanha'].nunique() <= 1:
        return None
    
    # Agrupar por campanha
    df_campanhas = df_filtrado.groupby('campanha').agg({
        'Investimento': 'sum',
        'impactos': 'sum'
    }).reset_index()
    
    # Calcular métricas derivadas
    df_campanhas['cpm_medio'] = df_campanhas.apply(
        lambda r: (r['Investimento'] / r['impactos'] * 1000) if r['impactos'] > 0 else 0, axis=1
    )
    
    df_campanhas['eficiencia'] = df_campanhas.apply(
        lambda r: r['impactos'] / r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
    )
    
    # Calcular percentuais
    total_invest = df_campanhas['Investimento'].sum()
    total_impactos = df_campanhas['impactos'].sum()
    
    df_campanhas['percentual_investimento'] = (df_campanhas['Investimento'] / total_invest) * 100
    df_campanhas['percentual_impactos'] = (df_campanhas['impactos'] / total_impactos) * 100
    
    # Ordenar por investimento (maior para menor)
    df_campanhas = df_campanhas.sort_values('Investimento', ascending=False)
    
    return df_campanhas

# ============================================
# SIDEBAR - FILTROS
# ============================================
with st.sidebar:
    st.markdown("### 🔍 Filtros de Análise")
    
    # Ordem personalizada das campanhas (como você especificou)
    ordem_campanhas = [
        'campanha_credito_2025',
        'campanha_credito_rural_2025', 
        'campanha_investimentos_2025'
    ]
    
    # Verificar quais campanhas realmente existem nos dados
    campanhas_existentes = [camp for camp in ordem_campanhas if camp in df['campanha'].unique()]
    
    # Adicionar "Todas as Campanhas" no final como solicitado
    opcoes_campanhas = ['Todas as Campanhas'] + campanhas_existentes
    
    # CSS específico para o selectbox - CORREÇÃO PARA TEXTO CORTADO VERTICALMENTE
    st.markdown(f"""
    <style>
        /* CORREÇÃO PARA TEXTO CORTADO VERTICALMENTE */
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 10px !important;
            /* AJUSTES CRÍTICOS PARA ALTURA */
            padding: 12px 15px !important;  /* Aumentei o padding vertical */
            min-height: 48px !important;    /* Altura mínima garantida */
            height: auto !important;        /* Altura automática */
            display: flex !important;       /* Flex para alinhamento */
            align-items: center !important; /* Centraliza verticalmente */
        }}
        
        /* Garante que o texto dentro do select tenha espaço vertical */
        [data-testid="stSidebar"] .stSelectbox > div > div > div {{
            color: white !important;
            font-weight: 500 !important;
            line-height: 1.5 !important;    /* Espaçamento entre linhas */
            padding: 0 !important;          /* Remove padding interno */
            display: flex !important;
            align-items: center !important;
            height: 100% !important;        /* Ocupa toda a altura */
        }}
        
        /* Ajusta o ícone do dropdown */
        [data-testid="stSidebar"] .stSelectbox > div > div > div:last-child {{
            margin-top: 0 !important;       /* Remove margem que pode desalinhar */
            display: flex !important;
            align-items: center !important;
        }}
        
        /* Garante que o label não sobreponha */
        [data-testid="stSidebar"] .stSelectbox label {{
            color: {COCRED_COLORS['verde_claro']} !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 10px !important;  /* Aumentei margem inferior */
            display: block !important;
            line-height: 1.2 !important;
        }}
        
        /* Aumenta o espaço entre os filtros */
        [data-testid="stSidebar"] .stSelectbox {{
            margin-bottom: 35px !important;  /* Mais espaço abaixo */
        }}
        
        /* Restante do seu CSS existente (mantenha tudo abaixo) */
        [data-testid="stSidebar"] .stSelectbox > div > div:hover {{
            border-color: {COCRED_COLORS['turquesa']} !important;
            box-shadow: 0 0 0 2px rgba(0, 174, 157, 0.2) !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] {{
            background-color: {COCRED_COLORS['verde_escuro']} !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="menu"] {{
            background-color: {COCRED_COLORS['verde_escuro']} !important;
            border-radius: 8px !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="option"] {{
            color: white !important;
            background-color: {COCRED_COLORS['verde_escuro']} !important;
            padding: 12px 15px !important;  /* Aumentei padding vertical aqui também */
            font-weight: 500 !important;
            line-height: 1.4 !important;    /* Para opções no dropdown */
            min-height: 44px !important;    /* Altura mínima para opções */
            display: flex !important;
            align-items: center !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="option"]:hover {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: {COCRED_COLORS['verde_claro']} !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [aria-selected="true"] {{
            background-color: {COCRED_COLORS['turquesa']} !important;
            color: white !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox [aria-selected="true"]:hover {{
            background-color: {COCRED_COLORS['turquesa']} !important;
            color: white !important;
        }}
        
        /* Estilo para o multiselect de canais */
        [data-testid="stSidebar"] .stMultiSelect {{
            margin-bottom: 25px !important;  /* Mais espaço aqui também */
        }}
        
        [data-testid="stSidebar"] .stMultiSelect > div > div {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;  /* Aumentei padding vertical */
            min-height: 48px !important;    /* Mesma altura do selectbox */
        }}
        
        [data-testid="stSidebar"] .stMultiSelect > div > div:hover {{
            border-color: {COCRED_COLORS['turquesa']} !important;
            box-shadow: 0 0 0 2px rgba(0, 174, 157, 0.2) !important;
        }}
        
        [data-testid="stSidebar"] .stMultiSelect > div > div > div > div {{
            color: white !important;
            line-height: 1.5 !important;    /* Espaçamento para texto */
            display: flex !important;
            align-items: center !important;
        }}
        
        [data-testid="stSidebar"] .stMultiSelect label {{
            color: {COCRED_COLORS['verde_claro']} !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 10px !important;  /* Margem igual ao selectbox */
            display: block !important;
        }}
        
        /* Tags selecionadas no multiselect */
        [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
            background-color: {COCRED_COLORS['turquesa']} !important;
            color: white !important;
            border-radius: 6px !important;
            margin: 2px !important;
            padding: 4px 8px !important;
            font-size: 12px !important;
            line-height: 1.4 !important;    /* Para tags também */
        }}
        
        [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]:hover {{
            background-color: {COCRED_COLORS['verde_claro']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Usar selectbox ao invés de select_slider
    campanha_selecionada = st.selectbox(
        "Selecione a Campanha:",
        options=opcoes_campanhas,
        index=0,  # Seleciona "Todas as Campanhas" por padrão
        key="campanha_filter"
    )
    
    # Obter lista de canais únicos e ordená-los
    canais = sorted(df['canal'].unique())
    
    canal_selecionado = st.multiselect(
        "Filtrar por Canal:",
        options=canais,
        default=[],
        key="canal_filter"
    )
    
    df_filtrado = agregar_dados_contextuais(
        df, 
        campanha_selecionada, 
        canal_selecionado if canal_selecionado else None
    )
    
    st.markdown("---")
    st.markdown("### ⚡ Métricas Rápidas")
    total_investimento = df_filtrado['Investimento'].sum()
    total_impactos = df_filtrado['impactos'].sum()
    df_cpm_valido = df_filtrado[df_filtrado['cpm'] > 0]
    if not df_cpm_valido.empty and df_cpm_valido['impactos'].sum() > 0:
        media_cpm = (df_cpm_valido['impactos'] * df_cpm_valido['cpm']).sum() / df_cpm_valido['impactos'].sum()
    else:
        media_cpm = 0
    st.metric("💰 Total Investido", f"R$ {total_investimento:,.2f}")
    st.metric("👁️ Total Impactos", f"{total_impactos:,}")
    st.metric("📈 CPM Médio", f"R$ {media_cpm:.2f}")

# ============================================
# KPIs PRINCIPAIS - COM DESTAQUES
# ============================================
st.subheader("📈 KPIs de Performance")
df_kpi = df_filtrado.copy()
total_invest_kpi = df_kpi['Investimento'].sum()
total_impactos_kpi = df_kpi['impactos'].sum()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Investimento Total", f"R$ {total_invest_kpi:,.2f}", delta_color="off",
              help="Valor total investido nos canais selecionados")
with col2:
    if total_impactos_kpi > 0:
        st.metric("👁️ Impactos Totais", f"{total_impactos_kpi:,}", delta_color="off",
                  help="Total de impressões alcançadas")
    else:
        st.metric("👁️ Impactos Totais", "0", help="Total de impressões alcançadas")
with col3:
    df_cpm_kpi = df_kpi[df_kpi['cpm'] > 0]
    if not df_cpm_kpi.empty and df_cpm_kpi['impactos'].sum() > 0:
        media_cpm_kpi = (df_cpm_kpi['impactos'] * df_cpm_kpi['cpm']).sum() / df_cpm_kpi['impactos'].sum()
    else:
        media_cpm_kpi = 0
    st.metric("🎯 CPM Médio", f"R$ {media_cpm_kpi:.2f}",
              help="Custo médio por mil impressões (ponderado pelos impactos)")
with col4:
    if total_impactos_kpi > 0 and total_invest_kpi > 0:
        eficiencia = total_impactos_kpi / total_invest_kpi
        eficiencia_formatada = f"{eficiencia:,.1f}"
        st.metric("⚡ Eficiência", eficiencia_formatada, delta="impressões por R$ 1,00",
                  delta_color="off",
                  help="Indica quantas impressões são geradas por cada R$ 1,00 investido")
    else:
        st.metric("⚡ Eficiência", "0.0", delta="impressões por R$ 1,00", delta_color="off",
                  help="Indica quantas impressões são geradas por cada R$ 1,00 investido")

st.markdown(f"""
<div style="height: 3px; background: linear-gradient(90deg, {COCRED_COLORS['verde_claro']}, {COCRED_COLORS['turquesa']}); 
            border-radius: 2px; margin: 30px 0;"></div>
""", unsafe_allow_html=True)

# ============================================
# VISUALIZAÇÕES PRINCIPAIS
# ============================================
# Ajuste no número de tabs para incluir a nova aba de comparação
tab_names = ["📊 Análise por Canal", "📈 Distribuição (Investimento)", "📈 Distribuição (Impacto)",
             "💰 Eficiência (CPM)", "📋 Dados Detalhados"]

# Adiciona aba de comparação apenas se "Todas as Campanhas" estiver selecionada
if campanha_selecionada == 'Todas as Campanhas':
    tab_names.append("🆚 Comparação entre Campanhas")

tabs = st.tabs(tab_names)

CORES_GRAFICOS = [
    COCRED_COLORS['verde_escuro'],
    COCRED_COLORS['turquesa'],
    COCRED_COLORS['verde_claro'],
    COCRED_COLORS['terra'],
    COCRED_COLORS['ouro'],
    COCRED_COLORS['laranja'],
    COCRED_COLORS['roxo'],
    '#1976D2',
]

# ---------------- TAB 1: Análise por Canal ----------------
with tabs[0]:
    st.markdown(f"""
    <h3 style="color: {COCRED_COLORS['verde_escuro']}; border-left: 6px solid {COCRED_COLORS['turquesa']}; padding-left: 15px;">
        📊 Análise de Desempenho por Canal
    </h3>
    """, unsafe_allow_html=True)
    contexto = "agregados de todas as campanhas" if campanha_selecionada == 'Todas as Campanhas' else f"da campanha {campanha_selecionada}"
    st.markdown(f"<p style='color: {COCRED_COLORS['cinza_medio']}; font-size: 14px; margin-bottom: 20px;'>Dados {contexto}</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if not df_filtrado.empty:
            df_invest = df_filtrado.sort_values('Investimento', ascending=False)
            fig_invest = go.Figure()
            fig_invest.add_trace(go.Bar(
                x=df_invest['canal'], y=df_invest['Investimento'], name='Investimento',
                marker_color=CORES_GRAFICOS[0], marker_line_color=COCRED_COLORS['cinza_escuro'], marker_line_width=2,
                text=df_invest['Investimento'].apply(lambda x: f'R$ {x:,.0f}'), textposition='outside',
                textfont=dict(size=12, color=COCRED_COLORS['cinza_escuro'], family='Segoe UI'),
                hovertemplate='<b>%{x}</b><br>' +
                              'Investimento: R$ %{y:,.2f}<br>' +
                              '% do total: %{customdata:.1%}<br>' +
                              'Campanha: ' + ('Todas' if campanha_selecionada == 'Todas as Campanhas' else campanha_selecionada) +
                              '<extra></extra>',
                customdata=df_invest['porcentagem_investimento']
            ))
            fig_invest.update_layout(
                title=dict(
                    text=f'Investimento por Canal ({campanha_selecionada})',
                    font=dict(size=20, color=COCRED_COLORS['verde_escuro'], family='Segoe UI'),
                    x=0.5, y=0.98, xanchor='center', yanchor='top', pad=dict(t=10, b=10)
                ),
                xaxis=dict(title=dict(text='Canal'), tickangle=45),
                yaxis=dict(title=dict(text='Investimento (R$)'), gridcolor='rgba(0,0,0,0.1)'),
                plot_bgcolor='white', paper_bgcolor='white', hovermode='x unified',
                height=500, margin=dict(t=80, b=120, l=80, r=40)
            )
            st.plotly_chart(fig_invest, use_container_width=True)
    with col2:
        if not df_filtrado.empty:
            df_impactos = df_filtrado.sort_values('impactos', ascending=False)
            fig_impactos = go.Figure()
            fig_impactos.add_trace(go.Bar(
                x=df_impactos['canal'], y=df_impactos['impactos'], name='Impactos',
                marker_color=CORES_GRAFICOS[1], marker_line_color=COCRED_COLORS['cinza_escuro'], marker_line_width=2,
                text=df_impactos['impactos'].apply(lambda x: f'{x/1000000:.1f}M' if x > 1000000 else f'{x/1000:.0f}K'),
                textposition='outside',
                textfont=dict(size=12, color=COCRED_COLORS['cinza_escuro'], family='Segoe UI'),
                hovertemplate='<b>%{x}</b><br>Impactos: %{y:,}<br>% do total: %{customdata:.1%}<br>' +
                              'Campanha: ' + ('Todas' if campanha_selecionada == 'Todas as Campanhas' else campanha_selecionada) +
                              '<extra></extra>',
                customdata=df_impactos['porcentagem_impactos']
            ))
            fig_impactos.update_layout(
                title=dict(
                    text=f'Impactos por Canal ({campanha_selecionada})',
                    font=dict(size=20, color=COCRED_COLORS['verde_escuro'], family='Segoe UI'),
                    x=0.5, y=0.95, xanchor='center', yanchor='top'
                ),
                xaxis=dict(title=dict(text='Canal'), tickangle=45),
                yaxis=dict(title=dict(text='Número de Impactos'), gridcolor='rgba(0,0,0,0.1)'),
                plot_bgcolor='white', paper_bgcolor='white', hovermode='x unified',
                height=500, margin=dict(t=80, b=120, l=80, r=40)
            )
            st.plotly_chart(fig_impactos, use_container_width=True)

# ---------------- TAB 2: Distribuição (Investimento) ----------------
with tabs[1]:
    st.markdown(f"""
    <h3 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']};
               border-left: 6px solid {COCRED_COLORS['verde_claro']};
               padding-left: 15px;">
        📈 Distribuição de Recursos (Investimento)
    </h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if not df_filtrado.empty:
            if campanha_selecionada == 'Todas as Campanhas':
                df_treemap = df.copy()
                df_treemap = df_treemap[df_treemap['Investimento'] > 0]
                df_treemap['eficiencia'] = df_treemap.apply(
                    lambda r: r['impactos']/r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
                )
                fig_treemap = px.treemap(
                    df_treemap,
                    path=[px.Constant("Todas as Campanhas"), 'campanha', 'canal'],
                    values='Investimento',
                    color='eficiencia',
                    color_continuous_scale=["#6AB06D", COCRED_COLORS['verde_escuro'], "#003300"],
                    color_continuous_midpoint=df_treemap['eficiencia'].median() if not df_treemap.empty else 0,
                    hover_data={'Investimento':':.2f', 'impactos':':,.0f', 'cpm':':.2f', 'eficiencia':':.2f'},
                    title='Mapa Hierárquico de Investimento'
                )
                customdata = df_treemap[['Investimento','impactos','cpm','eficiencia']].values
                fig_treemap.update_traces(
                    texttemplate='<b>%{label}</b><br>R$ %{value:,.2f}',
                    textposition='middle center',
                    hovertemplate=(
                        '<b>%{label}</b><br>-------------------<br>'
                        '💰 Investimento: R$ %{customdata[0]:,.2f}<br>'
                        '👁️ Impactos: %{customdata[1]:,.0f}<br>'
                        '🎯 CPM: R$ %{customdata[2]:.2f}<br>'
                        '⚡ Eficiência: %{customdata[3]:.2f} impactos/R$<extra></extra>'
                    ),
                    customdata=customdata,
                    marker=dict(cornerradius=5, line=dict(width=2, color='white' if not THEME['is_dark'] else '#2F2F2F'))
                )
            else:
                df_treemap = df_filtrado.copy()
                df_treemap = df_treemap[df_treemap['Investimento'] > 0]
                if not df_treemap.empty:
                    df_treemap['eficiencia'] = df_treemap.apply(
                        lambda r: r['impactos']/r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
                    )
                    fig_treemap = px.treemap(
                        df_treemap,
                        path=[px.Constant(f"Campanha: {campanha_selecionada}"), 'canal'],
                        values='Investimento',
                        color='eficiencia',
                        color_continuous_scale=["#6AB06D", COCRED_COLORS['verde_escuro'], "#003300"],
                        color_continuous_midpoint=df_treemap['eficiencia'].median() if not df_treemap.empty else 0,
                        hover_data={'Investimento':':.2f','impactos':':,.0f','cpm':':.2f','eficiencia':':.2f','porcentagem_investimento':':.2%'},
                        title=f'Distribuição de Investimento - {campanha_selecionada}'
                    )
                    customdata = df_treemap[['Investimento','impactos','cpm','eficiencia','porcentagem_investimento']].values
                    fig_treemap.update_traces(
                        texttemplate='<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percentParent:.1%}',
                        textposition='middle center',
                        hovertemplate=(
                            '<b>%{label}</b><br>-------------------<br>'
                            '💰 Investimento: R$ %{customdata[0]:,.2f}<br>'
                            '📊 % do Total: %{customdata[4]:.1%}<br>'
                            '👁️ Impactos: %{customdata[1]:,.0f}<br>'
                            '🎯 CPM: R$ %{customdata[2]:.2f}<br>'
                            '⚡ Eficiência: %{customdata[3]:.2f} impactos/R$<extra></extra>'
                        ),
                        customdata=customdata,
                        marker=dict(cornerradius=5, line=dict(width=2, color='white' if not THEME['is_dark'] else '#2F2F2F'))
                    )

            fig_treemap.update_layout(
                template=THEME['plotly_template'],
                paper_bgcolor=THEME['bg'],
                plot_bgcolor=THEME['sbg'],
                font=dict(color=THEME['text'], family="Segoe UI"),
                height=600,
                margin=dict(t=60, b=20, l=20, r=20),
                title=dict(
                    font=dict(size=22, color=THEME['text']),
                    x=0.5, y=0.98, xanchor='center', yanchor='top'
                ),
                coloraxis_colorbar=dict(
                    title=dict(text="Eficiência", font=dict(size=14, color=THEME['text'])),
                    tickfont=dict(size=12, color=THEME['text']),
                    thickness=20, len=0.8, yanchor="middle", y=0.5
                )
            )
            st.plotly_chart(fig_treemap, use_container_width=True)

    with col2:
        box_bg = THEME['sbg']
        title_color = THEME['text']
        border_color = THEME['subtle_border']
        shadow = THEME['subtle_shadow']
        st.markdown(f"""
        <div style="
            background: {box_bg};
            padding: 16px;
            border-radius: 12px;
            border: 1px solid {border_color};
            box-shadow: 0 6px 16px {shadow};
        ">
            <h4 style="color: {title_color}; margin-top: 0;">📋 Insights do Investimento</h4>
        """, unsafe_allow_html=True)

        if not df_filtrado.empty:
            df_stats = df_filtrado[df_filtrado['Investimento'] > 0].copy()
            if not df_stats.empty:
                maior_invest = df_stats.loc[df_stats['Investimento'].idxmax()]
                menor_invest = df_stats.loc[df_stats['Investimento'].idxmin()]
                top_3 = df_stats.nlargest(3, 'Investimento')
                perc_top_3 = top_3['porcentagem_investimento'].sum() * 100

                df_stats['eficiencia'] = df_stats.apply(
                    lambda r: r['impactos']/r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
                )
                eficiencia_media = df_stats['eficiencia'].mean()

                st.metric("🎯 Canais Analisados", f"{len(df_stats)}", help="Número de canais com investimento positivo")
                st.markdown("---")
                st.markdown(
                    f"<div style='color:{title_color};'><b>🏆 Maior Investimento</b><br>"
                    f"Canal: {maior_invest['canal']}<br>"
                    f"Valor: R$ {maior_invest['Investimento']:,.2f}<br>"
                    f"% Total: {maior_invest['porcentagem_investimento']*100:.1f}%</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>📉 Menor Investimento</b><br>"
                    f"Canal: {menor_invest['canal']}<br>"
                    f"Valor: R$ {menor_invest['Investimento']:,.2f}<br>"
                    f"% Total: {menor_invest['porcentagem_investimento']*100:.1f}%</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>📊 Concentração</b><br>"
                    f"Top 3 canais concentram <b>{perc_top_3:.1f}%</b> do investimento</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>⚡ Eficiência Média</b><br>"
                    f"<b>{eficiencia_media:,.0f}</b> impactos por R$ 1,00</div>",
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- TAB 3: Distribuição (Impacto) ----------------
with tabs[2]:
    st.markdown(f"""
    <h3 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']};
               border-left: 6px solid {COCRED_COLORS['turquesa']}; padding-left: 15px;">
        📈 Distribuição de Recursos (Impacto)
    </h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if not df_filtrado.empty:
            if campanha_selecionada == 'Todas as Campanhas':
                df_treemap_impact = df.copy()
                df_treemap_impact = df_treemap_impact[df_treemap_impact['impactos'] > 0]
                df_treemap_impact['relacao_impacto_invest'] = df_treemap_impact.apply(
                    lambda r: r['impactos']/r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
                )
                fig_treemap_impact = px.treemap(
                    df_treemap_impact,
                    path=[px.Constant("Todas as Campanhas"), 'campanha', 'canal'],
                    values='impactos',
                    color='relacao_impacto_invest',
                    color_continuous_scale=["#00AE9D", COCRED_COLORS['turquesa'], "#006B5F"],
                    hover_data={'impactos':':,.0f','Investimento':':.2f','cpm':':.2f','porcentagem_impactos':':.2%'},
                    title='Mapa Hierárquico de Impactos'
                )
                customdata = df_treemap_impact[['impactos','Investimento','cpm','porcentagem_impactos','relacao_impacto_invest']].values
                fig_treemap_impact.update_traces(
                    texttemplate='<b>%{label}</b><br>%{value:,.0f} impactos',
                    textposition='middle center',
                    hovertemplate=(
                        '<b>%{label}</b><br>-------------------<br>'
                        '👁️ Impactos: %{customdata[0]:,.0f}<br>'
                        '📊 % do Total: %{customdata[3]:.1%}<br>'
                        '💰 Investimento: R$ %{customdata[1]:,.2f}<br>'
                        '🎯 CPM: R$ %{customdata[2]:.2f}<br>'
                        '⚡ Impactos/R$: %{customdata[4]:.2f}<extra></extra>'
                    ),
                    customdata=customdata,
                    marker=dict(cornerradius=5, line=dict(width=2, color='white' if not THEME['is_dark'] else '#2F2F2F'))
                )
            else:
                df_treemap_impact = df_filtrado.copy()
                df_treemap_impact = df_treemap_impact[df_treemap_impact['impactos'] > 0]
                if not df_treemap_impact.empty:
                    df_treemap_impact['relacao_impacto_invest'] = df_treemap_impact.apply(
                        lambda r: r['impactos']/r['Investimento'] if r['Investimento'] > 0 else 0, axis=1
                    )
                    fig_treemap_impact = px.treemap(
                        df_treemap_impact,
                        path=[px.Constant(f"Campanha: {campanha_selecionada}"), 'canal'],
                        values='impactos',
                        color='relacao_impacto_invest',
                        color_continuous_scale=["#00AE9D", COCRED_COLORS['turquesa'], "#006B5F"],
                        hover_data={'impactos':':,.0f','Investimento':':.2f','cpm':':.2f','porcentagem_impactos':':.2%','relacao_impacto_invest':':.2f'},
                        title=f'Distribuição de Impactos - {campanha_selecionada}'
                    )
                    customdata = df_treemap_impact[['impactos','Investimento','cpm','porcentagem_impactos','relacao_impacto_invest']].values
                    fig_treemap_impact.update_traces(
                        texttemplate='<b>%{label}</b><br>%{value:,.0f}<br>%{percentParent:.1%}',
                        textposition='middle center',
                        hovertemplate=(
                            '<b>%{label}</b><br>-------------------<br>'
                            '👁️ Impactos: %{customdata[0]:,.0f}<br>'
                            '📊 % do Total: %{customdata[3]:.1%}<br>'
                            '💰 Investimento: R$ %{customdata[1]:,.2f}<br>'
                            '🎯 CPM: R$ %{customdata[2]:.2f}<br>'
                            '⚡ Eficiência: %{customdata[4]:.2f} impactos/R$<extra></extra>'
                        ),
                        customdata=customdata,
                        marker=dict(cornerradius=5, line=dict(width=2, color='white' if not THEME['is_dark'] else '#2F2F2F'))
                    )

            fig_treemap_impact.update_layout(
                template=THEME['plotly_template'],
                paper_bgcolor=THEME['bg'],
                plot_bgcolor=THEME['sbg'],
                font=dict(color=THEME['text'], family="Segoe UI"),
                height=600,
                margin=dict(t=60, b=20, l=20, r=20),
                title=dict(
                    font=dict(size=22, color=THEME['text']),
                    x=0.5, y=0.98, xanchor='center', yanchor='top'
                ),
                coloraxis_colorbar=dict(
                    title=dict(text="Impacto/R$", font=dict(size=14, color=THEME['text'])),
                    tickfont=dict(size=12, color=THEME['text']),
                    thickness=20, len=0.8, yanchor="middle", y=0.5
                )
            )
            st.plotly_chart(fig_treemap_impact, use_container_width=True)

    with col2:
        box_bg = THEME['sbg']
        title_color = THEME['text']
        border_color = THEME['subtle_border']
        shadow = THEME['subtle_shadow']
        st.markdown(f"""
        <div style="
            background: {box_bg};
            padding: 16px;
            border-radius: 12px;
            border: 1px solid {border_color};
            box-shadow: 0 6px 16px {shadow};
        ">
            <h4 style="color: {title_color}; margin-top: 0;">📊 Insights dos Impactos</h4>
        """, unsafe_allow_html=True)

        if not df_filtrado.empty:
            df_stats_impact = df_filtrado[df_filtrado['impactos'] > 0].copy()
            if not df_stats_impact.empty:
                maior_impacto = df_stats_impact.loc[df_stats_impact['impactos'].idxmax()]
                menor_impacto = df_stats_impact.loc[df_stats_impact['impactos'].idxmin()]
                top_3_impactos = df_stats_impact.nlargest(3, 'impactos')
                perc_top_3_impact = top_3_impactos['porcentagem_impactos'].sum() * 100
                cpm_medio = (df_stats_impact['impactos'] * df_stats_impact['cpm']).sum() / df_stats_impact['impactos'].sum()
                alcance_por_mil = (
                    df_stats_impact['impactos'].sum() / (df_stats_impact['Investimento'].sum()/1000)
                    if df_stats_impact['Investimento'].sum() > 0 else 0
                )
                st.metric("🎯 Canais com Impacto", f"{len(df_stats_impact)}", help="Número de canais com impactos positivos")
                st.markdown("---")
                st.markdown(
                    f"<div style='color:{title_color};'><b>🏆 Maior Impacto</b><br>"
                    f"Canal: {maior_impacto['canal']}<br>"
                    f"Impactos: {maior_impacto['impactos']:,}<br>"
                    f"% Total: {maior_impacto['porcentagem_impactos']*100:.1f}%</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>📉 Menor Impacto</b><br>"
                    f"Canal: {menor_impacto['canal']}<br>"
                    f"Impactos: {menor_impacto['impactos']:,}<br>"
                    f"% Total: {menor_impacto['porcentagem_impactos']*100:.1f}%</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>📊 Concentração</b><br>"
                    f"Top 3 canais concentram <b>{perc_top_3_impact:.1f}%</b> dos impactos</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='color:{title_color};'><b>💰 Custo-Efetividade</b><br>"
                    f"CPM Médio: <b>R$ {cpm_medio:.2f}</b><br>"
                    f"Alcance por R$ 1.000: <b>{alcance_por_mil:,.0f}</b> pessoas</div>",
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- TAB 4: Eficiência (CPM) ----------------
with tabs[3]:
    st.markdown(f"""
    <h3 style="color: {COCRED_COLORS['verde_escuro']}; border-left: 6px solid {COCRED_COLORS['verde_claro']}; padding-left: 15px;">
        💰 Análise de Eficiência (CPM)
    </h3>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if not df_filtrado.empty:
            df_cpm = df_filtrado[df_filtrado['cpm'] > 0]
            if not df_cpm.empty:
                df_cpm = df_cpm.sort_values('cpm', ascending=True)
                fig_cpm = go.Figure()
                fig_cpm.add_trace(go.Bar(
                    y=df_cpm['canal'], x=df_cpm['cpm'], name='CPM', orientation='h',
                    marker_color=COCRED_COLORS['turquesa'], marker_line_color=COCRED_COLORS['cinza_escuro'],
                    marker_line_width=2, text=df_cpm['cpm'].apply(lambda x: f'R$ {x:.2f}'),
                    textposition='outside',
                    textfont=dict(size=12, color=COCRED_COLORS['cinza_escuro'], family='Segoe UI'),
                    hovertemplate='<b>%{y}</b><br>CPM: R$ %{x:.2f}<br>Investimento: R$ %{customdata:,.2f}<br>' +
                                  'Campanha: ' + ('Todas' if campanha_selecionada == 'Todas as Campanhas' else campanha_selecionada) +
                                  '<extra></extra>',
                    customdata=df_cpm['Investimento']
                ))
                fig_cpm.update_layout(
                    title=dict(
                        text=f'Custo por Mil Impressões (CPM) por Canal ({campanha_selecionada})',
                        xanchor='center', yanchor='top',
                        font=dict(size=18, color=COCRED_COLORS['verde_escuro'], family='Segoe UI'), x=0.5
                    ),
                    yaxis=dict(title=dict(text='Canal'), tickfont=dict(size=12)),
                    xaxis=dict(title=dict(text='CPM (R$)'), tickfont=dict(size=12), gridcolor='rgba(0,0,0,0.1)'),
                    plot_bgcolor='white', paper_bgcolor='white', hovermode='y unified',
                    height=500, margin=dict(t=80, b=80, l=150, r=40)
                )
                st.plotly_chart(fig_cpm, use_container_width=True)
    with col2:
        if not df_filtrado.empty:
            df_scatter = df_filtrado[df_filtrado['Investimento'] > 0]
            if not df_scatter.empty and len(df_scatter) > 1:
                fig_scatter = px.scatter(
                    df_scatter,
                    x='Investimento',
                    y='impactos',
                    size='cpm',
                    color='canal',
                    title=f'Relação: Investimento vs Impactos ({campanha_selecionada})',
                    hover_data=['canal', 'cpm', 'porcentagem_investimento'],
                    size_max=60,
                    color_discrete_sequence=CORES_GRAFICOS
                )
                fig_scatter.update_layout(
                    xaxis=dict(title=dict(text='Investimento (R$)'), gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(title=dict(text='Impactos'), gridcolor='rgba(0,0,0,0.1)'),
                    plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Segoe UI"),
                    height=500,
                    legend=dict(
                        font=dict(size=11, color=COCRED_COLORS['cinza_escuro']),
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor=COCRED_COLORS['cinza_claro'],
                        borderwidth=2
                    )
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------- TAB 5: Dados Detalhados ----------------
with tabs[4]:
    st.markdown(f"""
    <h3 style="color: {COCRED_COLORS['verde_escuro']}; border-left: 6px solid {COCRED_COLORS['turquesa']}; padding-left: 15px;">
        📋 Dados Detalhados
    </h3>
    """, unsafe_allow_html=True)
    df_display = df_filtrado.copy()
    df_display['Investimento_fmt'] = df_display['Investimento'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['porcentagem_investimento_fmt'] = df_display['porcentagem_investimento'].apply(lambda x: f"{x*100:.2f}%")
    df_display['impactos_fmt'] = df_display['impactos'].apply(lambda x: f"{x:,}")
    df_display['porcentagem_impactos_fmt'] = df_display['porcentagem_impactos'].apply(lambda x: f"{x*100:.2f}%")
    df_display['cpm_fmt'] = df_display['cpm'].apply(lambda x: f"R$ {x:.2f}" if x > 0 else "R$ 0.00")
    df_display['eficiencia'] = df_display.apply(
        lambda row: row['impactos'] / row['Investimento'] if row['Investimento'] > 0 else 0,
        axis=1
    )
    df_display['eficiencia_fmt'] = df_display['eficiencia'].apply(lambda x: f"{x:.2f}")
    df_display = df_display[[
        'campanha', 'canal', 'Investimento_fmt', 'porcentagem_investimento_fmt',
        'impactos_fmt', 'porcentagem_impactos_fmt', 'cpm_fmt', 'eficiencia_fmt'
    ]]
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "campanha": st.column_config.TextColumn("Campanha", width="medium"),
            "canal": st.column_config.TextColumn("Canal", width="medium"),
            "Investimento_fmt": st.column_config.TextColumn("Investimento", width="medium"),
            "porcentagem_investimento_fmt": st.column_config.TextColumn("% Invest.", width="small"),
            "impactos_fmt": st.column_config.TextColumn("Impactos", width="medium"),
            "porcentagem_impactos_fmt": st.column_config.TextColumn("% Impactos", width="small"),
            "cpm_fmt": st.column_config.TextColumn("CPM", width="small"),
            "eficiencia_fmt": st.column_config.TextColumn("Eficiência", width="small", 
                                                         help="Impactos por R$ 1,00 investido")
        }
    )
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.download_button(
            label="📥 Exportar Dados para CSV",
            data=csv,
            file_name=f"dados_campanhas_cocred_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ---------------- TAB 6: Comparação entre Campanhas (APENAS quando "Todas as Campanhas" está selecionada) ----------------
# ---------------- TAB 6: Comparação entre Campanhas (APENAS quando "Todas as Campanhas" está selecionada) ----------------
if campanha_selecionada == 'Todas as Campanhas' and len(tabs) > 5:
    with tabs[5]:
        st.markdown(f"""
        <h3 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; border-left: 6px solid {COCRED_COLORS['roxo']}; padding-left: 15px;">
            🆚 Comparação entre Campanhas
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <p style='color: {THEME['text']}; font-size: 14px; margin-bottom: 20px;'>
        Análise comparativa entre todas as campanhas disponíveis. Use esta aba para identificar padrões,
        tendências e performance relativa entre diferentes iniciativas.
        </p>
        """, unsafe_allow_html=True)
        
        # Calcular métricas por campanha
        df_campanhas_comparacao = calcular_metricas_por_campanha(df)
        
        if df_campanhas_comparacao is not None:
            # Gráfico 1: Investimento por Campanha (Barras Horizontais)
            st.markdown(f"""
            <h4 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; margin-top: 20px;">
                📊 Comparativo de Investimento por Campanha
            </h4>
            """, unsafe_allow_html=True)
            
            df_invest_camp = df_campanhas_comparacao.sort_values('Investimento', ascending=True)
            fig_invest_camp = go.Figure()
            fig_invest_camp.add_trace(go.Bar(
                y=df_invest_camp['campanha'],
                x=df_invest_camp['Investimento'],
                name='Investimento',
                orientation='h',
                marker_color=CORES_GRAFICOS[0],
                marker_line_color=COCRED_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_invest_camp['Investimento'].apply(lambda x: f'R$ {x:,.0f}'),
                textposition='outside',
                textfont=dict(
                    size=12, 
                    color=THEME['text'] if THEME['is_dark'] else COCRED_COLORS['cinza_escuro'], 
                    family='Segoe UI'
                ),
                hovertemplate='<b>%{y}</b><br>' +
                              'Investimento: R$ %{x:,.2f}<br>' +
                              '% do total: %{customdata:.1f}%<br>' +
                              'Impactos: %{customdata[1]:,.0f}<br>' +
                              '<extra></extra>',
                customdata=np.column_stack((
                    df_invest_camp['percentual_investimento'],
                    df_invest_camp['impactos']
                ))
            ))
            fig_invest_camp.update_layout(
                template=THEME['plotly_template'],
                title=dict(
                    text='Investimento Total por Campanha',
                    font=dict(
                        size=18, 
                        color=THEME['text'],
                        family='Segoe UI'
                    ),
                    x=0.5, xanchor='center'
                ),
                xaxis=dict(
                    title=dict(
                        text='Investimento (R$)',
                        font=dict(color=THEME['text'])
                    ),
                    gridcolor='rgba(255,255,255,0.1)' if THEME['is_dark'] else 'rgba(0,0,0,0.1)',
                    tickfont=dict(color=THEME['text'])
                ),
                yaxis=dict(
                    title=dict(
                        text='Campanha',
                        font=dict(color=THEME['text'])
                    ),
                    tickfont=dict(size=12, color=THEME['text'])
                ),
                plot_bgcolor=THEME['sbg'],
                paper_bgcolor=THEME['bg'],
                hovermode='y unified',
                height=400,
                margin=dict(t=60, b=80, l=200, r=40)
            )
            st.plotly_chart(fig_invest_camp, use_container_width=True)
            
            # Gráfico 2: Impactos por Campanha (Barras Horizontais)
            st.markdown(f"""
            <h4 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; margin-top: 20px;">
                📈 Comparativo de Impactos por Campanha
            </h4>
            """, unsafe_allow_html=True)
            
            df_impactos_camp = df_campanhas_comparacao.sort_values('impactos', ascending=True)
            fig_impactos_camp = go.Figure()
            fig_impactos_camp.add_trace(go.Bar(
                y=df_impactos_camp['campanha'],
                x=df_impactos_camp['impactos'],
                name='Impactos',
                orientation='h',
                marker_color=CORES_GRAFICOS[1],
                marker_line_color=COCRED_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_impactos_camp['impactos'].apply(lambda x: f'{x/1000000:.1f}M' if x > 1000000 else f'{x/1000:.0f}K'),
                textposition='outside',
                textfont=dict(
                    size=12, 
                    color=THEME['text'] if THEME['is_dark'] else COCRED_COLORS['cinza_escuro'], 
                    family='Segoe UI'
                ),
                hovertemplate='<b>%{y}</b><br>' +
                              'Impactos: %{x:,}<br>' +
                              '% do total: %{customdata:.1f}%<br>' +
                              'Investimento: R$ %{customdata[1]:,.2f}<br>' +
                              '<extra></extra>',
                customdata=np.column_stack((
                    df_impactos_camp['percentual_impactos'],
                    df_impactos_camp['Investimento']
                ))
            ))
            fig_impactos_camp.update_layout(
                template=THEME['plotly_template'],
                title=dict(
                    text='Impactos Totais por Campanha',
                    font=dict(
                        size=18, 
                        color=THEME['text'],
                        family='Segoe UI'
                    ),
                    x=0.5, xanchor='center'
                ),
                xaxis=dict(
                    title=dict(
                        text='Número de Impactos',
                        font=dict(color=THEME['text'])
                    ),
                    gridcolor='rgba(255,255,255,0.1)' if THEME['is_dark'] else 'rgba(0,0,0,0.1)',
                    tickfont=dict(color=THEME['text'])
                ),
                yaxis=dict(
                    title=dict(
                        text='Campanha',
                        font=dict(color=THEME['text'])
                    ),
                    tickfont=dict(size=12, color=THEME['text'])
                ),
                plot_bgcolor=THEME['sbg'],
                paper_bgcolor=THEME['bg'],
                hovermode='y unified',
                height=400,
                margin=dict(t=60, b=80, l=200, r=40)
            )
            st.plotly_chart(fig_impactos_camp, use_container_width=True)
            
            # Gráfico 3: CPM Médio por Campanha (Barras Horizontais)
            st.markdown(f"""
            <h4 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; margin-top: 20px;">
                💰 Custo-Efetividade (CPM Médio) por Campanha
            </h4>
            """, unsafe_allow_html=True)
            
            df_cpm_camp = df_campanhas_comparacao.sort_values('cpm_medio', ascending=True)
            fig_cpm_camp = go.Figure()
            fig_cpm_camp.add_trace(go.Bar(
                y=df_cpm_camp['campanha'],
                x=df_cpm_camp['cpm_medio'],
                name='CPM Médio',
                orientation='h',
                marker_color=CORES_GRAFICOS[2],
                marker_line_color=COCRED_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_cpm_camp['cpm_medio'].apply(lambda x: f'R$ {x:.2f}'),
                textposition='outside',
                textfont=dict(
                    size=12, 
                    color=THEME['text'] if THEME['is_dark'] else COCRED_COLORS['cinza_escuro'], 
                    family='Segoe UI'
                ),
                hovertemplate='<b>%{y}</b><br>' +
                              'CPM Médio: R$ %{x:.2f}<br>' +
                              'Investimento: R$ %{customdata[0]:,.2f}<br>' +
                              'Impactos: %{customdata[1]:,.0f}<br>' +
                              '<extra></extra>',
                customdata=np.column_stack((
                    df_cpm_camp['Investimento'],
                    df_cpm_camp['impactos']
                ))
            ))
            fig_cpm_camp.update_layout(
                template=THEME['plotly_template'],
                title=dict(
                    text='Custo por Mil Impressões (CPM) por Campanha',
                    font=dict(
                        size=18, 
                        color=THEME['text'],
                        family='Segoe UI'
                    ),
                    x=0.5, xanchor='center'
                ),
                xaxis=dict(
                    title=dict(
                        text='CPM (R$)',
                        font=dict(color=THEME['text'])
                    ),
                    gridcolor='rgba(255,255,255,0.1)' if THEME['is_dark'] else 'rgba(0,0,0,0.1)',
                    tickfont=dict(color=THEME['text'])
                ),
                yaxis=dict(
                    title=dict(
                        text='Campanha',
                        font=dict(color=THEME['text'])
                    ),
                    tickfont=dict(size=12, color=THEME['text'])
                ),
                plot_bgcolor=THEME['sbg'],
                paper_bgcolor=THEME['bg'],
                hovermode='y unified',
                height=400,
                margin=dict(t=60, b=80, l=200, r=40)
            )
            st.plotly_chart(fig_cpm_camp, use_container_width=True)
            
            # Gráfico 4: Eficiência (Impactos/Investimento) por Campanha
            st.markdown(f"""
            <h4 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; margin-top: 20px;">
                ⚡ Eficiência por Campanha (Impactos por R$ 1,00)
            </h4>
            """, unsafe_allow_html=True)
            
            df_eficiencia_camp = df_campanhas_comparacao.sort_values('eficiencia', ascending=True)
            fig_eficiencia_camp = go.Figure()
            fig_eficiencia_camp.add_trace(go.Bar(
                y=df_eficiencia_camp['campanha'],
                x=df_eficiencia_camp['eficiencia'],
                name='Eficiência',
                orientation='h',
                marker_color=CORES_GRAFICOS[3],
                marker_line_color=COCRED_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_eficiencia_camp['eficiencia'].apply(lambda x: f'{x:,.0f}'),
                textposition='outside',
                textfont=dict(
                    size=12, 
                    color=THEME['text'] if THEME['is_dark'] else COCRED_COLORS['cinza_escuro'], 
                    family='Segoe UI'
                ),
                hovertemplate='<b>%{y}</b><br>' +
                              'Eficiência: %{x:,.0f} impactos/R$<br>' +
                              'Investimento: R$ %{customdata[0]:,.2f}<br>' +
                              'Impactos: %{customdata[1]:,.0f}<br>' +
                              '<extra></extra>',
                customdata=np.column_stack((
                    df_eficiencia_camp['Investimento'],
                    df_eficiencia_camp['impactos']
                ))
            ))
            fig_eficiencia_camp.update_layout(
                template=THEME['plotly_template'],
                title=dict(
                    text='Eficiência por Campanha (Impactos gerados por R$ 1,00 investido)',
                    font=dict(
                        size=18, 
                        color=THEME['text'],
                        family='Segoe UI'
                    ),
                    x=0.5, xanchor='center'
                ),
                xaxis=dict(
                    title=dict(
                        text='Impactos por R$ 1,00',
                        font=dict(color=THEME['text'])
                    ),
                    gridcolor='rgba(255,255,255,0.1)' if THEME['is_dark'] else 'rgba(0,0,0,0.1)',
                    tickfont=dict(color=THEME['text'])
                ),
                yaxis=dict(
                    title=dict(
                        text='Campanha',
                        font=dict(color=THEME['text'])
                    ),
                    tickfont=dict(size=12, color=THEME['text'])
                ),
                plot_bgcolor=THEME['sbg'],
                paper_bgcolor=THEME['bg'],
                hovermode='y unified',
                height=400,
                margin=dict(t=60, b=80, l=200, r=40)
            )
            st.plotly_chart(fig_eficiencia_camp, use_container_width=True)
            
            # Tabela Comparativa
            st.markdown(f"""
            <h4 style="color: {COCRED_COLORS['verde_escuro'] if not THEME['is_dark'] else THEME['text']}; margin-top: 20px;">
                📋 Resumo Comparativo entre Campanhas
            </h4>
            """, unsafe_allow_html=True)
            
            df_resumo = df_campanhas_comparacao.copy()
            df_resumo['Investimento_fmt'] = df_resumo['Investimento'].apply(lambda x: f"R$ {x:,.2f}")
            df_resumo['impactos_fmt'] = df_resumo['impactos'].apply(lambda x: f"{x:,}")
            df_resumo['cpm_medio_fmt'] = df_resumo['cpm_medio'].apply(lambda x: f"R$ {x:.2f}")
            df_resumo['eficiencia_fmt'] = df_resumo['eficiencia'].apply(lambda x: f"{x:,.0f}")
            df_resumo['percentual_investimento_fmt'] = df_resumo['percentual_investimento'].apply(lambda x: f"{x:.1f}%")
            df_resumo['percentual_impactos_fmt'] = df_resumo['percentual_impactos'].apply(lambda x: f"{x:.1f}%")
            
            df_resumo_display = df_resumo[[
                'campanha', 'Investimento_fmt', 'percentual_investimento_fmt',
                'impactos_fmt', 'percentual_impactos_fmt', 'cpm_medio_fmt', 'eficiencia_fmt'
            ]]
            
            st.dataframe(
                df_resumo_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "campanha": st.column_config.TextColumn("Campanha", width="medium"),
                    "Investimento_fmt": st.column_config.TextColumn("Investimento", width="medium"),
                    "percentual_investimento_fmt": st.column_config.TextColumn("% Invest.", width="small"),
                    "impactos_fmt": st.column_config.TextColumn("Impactos", width="medium"),
                    "percentual_impactos_fmt": st.column_config.TextColumn("% Impactos", width="small"),
                    "cpm_medio_fmt": st.column_config.TextColumn("CPM Médio", width="small"),
                    "eficiencia_fmt": st.column_config.TextColumn("Eficiência", width="small", 
                                                                 help="Impactos por R$ 1,00 investido")
                }
            )
            
            # Exportar dados comparativos
            csv_comparacao = df_campanhas_comparacao.to_csv(index=False).encode('utf-8')
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                st.download_button(
                    label="📥 Exportar Dados Comparativos para CSV",
                    data=csv_comparacao,
                    file_name=f"comparacao_campanhas_cocred_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("⚠️ É necessário selecionar 'Todas as Campanhas' para ver a comparação entre campanhas.")
# ============================================
# RODAPÉ DO DASHBOARD
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COCRED_COLORS['cinza_medio']}; font-size: 0.9rem; padding: 20px;">
    <p> <strong style="color: {COCRED_COLORS['verde_escuro']};">COCRED Dashboard</strong> - Plataforma de Análise de Campanhas</p>
    <p>👤 Usuário: {st.session_state['username'].capitalize()} | 📅 Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
    <p style="font-size: 0.8rem;">© 2025 Ideatore Americas - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)