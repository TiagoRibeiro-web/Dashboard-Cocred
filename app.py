# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
            color: #2E7D32;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .login-title {
            color: #2E7D32;
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
            background: linear-gradient(135deg, #3FA110 0%, #2E7D32 100%);
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
            box-shadow: 0 6px 20px rgba(63, 161, 16, 0.3);
        }
        .stTextInput > div > div > input {
            padding: 14px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            transition: border 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #3FA110;
            box-shadow: 0 0 0 3px rgba(63, 161, 16, 0.1);
        }
        .credential-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #3FA110;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Container de login
    st.markdown("""
    <div class="login-container">
        <div class="sicredi-logo">🌾</div>
        <h1 class="login-title">Cocred Dashboard</h1>
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
            # st.markdown("""
            # <div class="credential-box">
            #     <h4 style="color: #2E7D32; margin-top: 0;">🔐 Credenciais de Teste</h4>
            #     <p style="margin: 5px 0;"><strong>👤 admin</strong> / 🔐 admin123</p>
            #     <p style="margin: 5px 0;"><strong>👤 gerente</strong> / 🔐 gerente123</p>
            #     <p style="margin: 5px 0;"><strong>👤 analista</strong> / 🔐 analista123</p>
            # </div>
            # """, unsafe_allow_html=True)
    
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
# CONFIGURAÇÕES DA MARCA SICREDI - VERSÃO AGRÍCOLA
# ============================================
SICREDI_COLORS = {
    'verde_impresso': '#00B140',        # Pantone 361 C
    'verde_digital': '#3FA110',          # Verde Sicredi Digital
    'verde_agricola': '#2E7D32',         # Verde mais escuro para melhor contraste
    'terra': '#8D6E63',                  # Cor de terra - referência agrícola
    'ouro': '#FFB300',                   # Dourado - referência a colheita
    'laranja': '#F57C00',                # Laranja para destaques
    'branco': '#FFFFFF',
    'cinza_claro': '#F5F5F5',
    'cinza_medio': '#9E9E9E',
    'cinza_escuro': '#424242',
    'verde_claro': '#C8E6C9',
    'verde_medio': '#4CAF50',
    'verde_escuro': '#1B5E20'
}

# Configuração da página Cocred Agrícola
st.set_page_config(
    page_title="Dashboard de Campanhas - Cocred",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS PERSONALIZADO - TEMA SICREDI AGRÍCOLA
# ============================================
st.markdown(f"""
<style>
    /* Fundo geral com textura sutil */
    .stApp {{
        background: linear-gradient(135deg, {SICREDI_COLORS['branco']} 0%, #F9F9F9 100%);
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }}
    
    /* Sidebar com gradiente */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SICREDI_COLORS['verde_agricola']} 0%, {SICREDI_COLORS['verde_impresso']} 100%);
        padding: 20px;
    }}
    
        
    /* Títulos com sombra para melhor legibilidade */
    h1, h2, h3, .st-emotion-cache-10trblm {{
        color: {SICREDI_COLORS['verde_agricola']} !important;
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
        border: 2px solid {SICREDI_COLORS['verde_medio']};
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    
    .stMetric label {{
        font-weight: 700 !important;
        color: {SICREDI_COLORS['verde_agricola']} !important;
        font-size: 14px !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {SICREDI_COLORS['verde_impresso']} !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    
        
    .main .stMetric {{
        background: linear-gradient(135deg, #C8E6C9, white) !important;  /* Verde clarinho */
        padding: 20px !important;
        border-radius: 12px !important;
        border: 2px solid #4CAF50 !important;  /* Verde médio */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }}
    
    [data-testid="stSidebar"] .stMetric {{
        background: rgba(255,255,255,0.1) !important;  /* Transparente branco */
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}
    
            
    /* Botões com gradiente agrícola */
    .stButton button {{
        background: linear-gradient(135deg, {SICREDI_COLORS['verde_digital']} 0%, {SICREDI_COLORS['verde_agricola']} 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 700;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, {SICREDI_COLORS['verde_agricola']} 0%, {SICREDI_COLORS['verde_impresso']} 100%) !important;
    }}
    
    /* Tabs com cores contrastantes */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {SICREDI_COLORS['cinza_claro']};
        padding: 8px;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        color: {SICREDI_COLORS['cinza_escuro']};
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid {SICREDI_COLORS['cinza_claro']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {SICREDI_COLORS['verde_digital']} 0%, {SICREDI_COLORS['verde_agricola']} 100%) !important;
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
        color: {SICREDI_COLORS['ouro']} !important;
    }}
    
    .stMetric [data-testid="stMetricDelta"] {{
        color: green !important;
    }}
    
    .stMetric [data-testid="stMarkdownContainer"] {{
        color: green !important;
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
        color: {SICREDI_COLORS['terra']};
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
            <div style="display: inline-block; background: rgba(46, 125, 50, 0.1); padding: 8px 16px; border-radius: 20px;">
                <span style="color: {SICREDI_COLORS['verde_agricola']}; font-weight: bold;">
                    👤 {st.session_state['username'].capitalize()}
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Separador decorativo
st.markdown(f"""
<div style="height: 4px; background: linear-gradient(90deg, {SICREDI_COLORS['verde_digital']}, {SICREDI_COLORS['ouro']}, {SICREDI_COLORS['verde_impresso']}); 
            border-radius: 2px; margin: 20px 0;"></div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR COM INFORMAÇÕES DO USUÁRIO E LOGOUT
# ============================================
with st.sidebar:
    # Informações do usuário
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 50px; color: white;">🌾</div>
            <h3 style="color: white; margin-bottom: 5px; text-align: center;">Cocred Dashboard</h3>
            <div style="background: rgba(255, 255, 255, 0.2); padding: 10px; border-radius: 10px; margin: 10px 0;">
                <p style="margin: 0; font-weight: bold;">👤 {st.session_state['username'].capitalize()}</p>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Usuário logado</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de logout
    if st.button("🚪 Sair do Sistema", use_container_width=True, type="secondary"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()
    
    # st.markdown("---")
    
    # # Seção de ajuda/contato
    # st.markdown("### 📞 Suporte")
    # st.markdown("**Email:** suporte@sicredi.com")
    # st.markdown("**Telefone:** (11) 99999-9999")
    # st.markdown("**Horário:** 9h às 18h")

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
# FUNÇÃO DE AGREGAÇÃO PARA "TODAS AS CAMPANHAS" - VERSÃO CORRIGIDA
# ============================================

def agregar_dados_contextuais(df, campanha_selecionada, canal_selecionado):
    """
    Agrega dados de forma inteligente:
    - Se 'Todas as Campanhas': agrega por canal (soma investimentos, cálculo correto de CPM)
    - Se campanha específica: mantém dados originais daquela campanha
    
    CORREÇÃO: A função agora mantém as colunas originais e calcula os percentuais corretamente
    """
    
    # Aplicar filtro de canal primeiro (se houver)
    df_filtrado = df.copy()
    if canal_selecionado:
        df_filtrado = df_filtrado[df_filtrado['canal'].isin(canal_selecionado)]
    
    # Se selecionou TODAS as campanhas, agregar por canal
    if campanha_selecionada == 'Todas as Campanhas':
        # Criar DataFrame agregado por canal mantendo CPM original quando disponível
        df_agregado = df_filtrado.groupby('canal').agg({
            'Investimento': 'sum',
            'impactos': 'sum'
        }).reset_index()
        
        # Calcular CPM correto para dados agregados
        df_agregado['cpm'] = df_agregado.apply(
            lambda row: (row['Investimento'] / row['impactos'] * 1000) if row['impactos'] > 0 else 0,
            axis=1
        )
        
        # Calcular porcentagens baseadas no TOTAL AGREGADO
        total_invest_agregado = df_agregado['Investimento'].sum()
        total_impactos_agregado = df_agregado['impactos'].sum()
        
        if total_invest_agregado > 0:
            df_agregado['porcentagem_investimento'] = df_agregado['Investimento'] / total_invest_agregado
        else:
            df_agregado['porcentagem_investimento'] = 0
            
        if total_impactos_agregado > 0:
            df_agregado['porcentagem_impactos'] = df_agregado['impactos'] / total_impactos_agregado
        else:
            df_agregado['porcentagem_impactos'] = 0
        
        # Adicionar coluna de campanha para consistência
        df_agregado['campanha'] = 'Todas as Campanhas'
        
        # Reordenar colunas para corresponder à estrutura original
        df_agregado = df_agregado[['campanha', 'canal', 'Investimento', 'porcentagem_investimento', 
                                  'impactos', 'porcentagem_impactos', 'cpm']]
        
        return df_agregado
    
    else:
        # Se selecionou campanha específica, filtrar
        df_filtrado = df_filtrado[df_filtrado['campanha'] == campanha_selecionada]
        
        # Recalcular porcentagens baseadas apenas na campanha selecionada
        if not df_filtrado.empty:
            total_invest_campanha = df_filtrado['Investimento'].sum()
            total_impactos_campanha = df_filtrado['impactos'].sum()
            
            if total_invest_campanha > 0:
                df_filtrado['porcentagem_investimento'] = df_filtrado['Investimento'] / total_invest_campanha
            else:
                df_filtrado['porcentagem_investimento'] = 0
                
            if total_impactos_campanha > 0:
                df_filtrado['porcentagem_impactos'] = df_filtrado['impactos'] / total_impactos_campanha
            else:
                df_filtrado['porcentagem_impactos'] = 0
        
        return df_filtrado

# ============================================
# SIDEBAR - FILTROS
# ============================================
with st.sidebar:
    # Filtros de análise (após a seção do usuário)
    st.markdown("### 🔍 Filtros de Análise")
    
    # Filtro de campanha
    campanhas = df['campanha'].unique()
    campanha_selecionada = st.selectbox(
        "Selecione a Campanha:",
        options=['Todas as Campanhas'] + list(campanhas),
        key="campanha_filter"
    )
    
    # Filtro por canal
    canais = df['canal'].unique()
    canal_selecionado = st.multiselect(
        "Filtrar por Canal:",
        options=canais,
        default=[],
        key="canal_filter"
    )
    
    # Filtrar dados baseados nos filtros usando função de agregação
    df_filtrado = agregar_dados_contextuais(
        df, 
        campanha_selecionada, 
        canal_selecionado if canal_selecionado else None
    )
    
    # Métricas na sidebar
    st.markdown("---")
    st.markdown("### ⚡ Métricas Rápidas")
    
    total_investimento = df_filtrado['Investimento'].sum()
    total_impactos = df_filtrado['impactos'].sum()
    
    # CPM médio CORRETO (ponderado pelos impactos)
    df_cpm_valido = df_filtrado[df_filtrado['cpm'] > 0]
    if not df_cpm_valido.empty and df_cpm_valido['impactos'].sum() > 0:
        # Cálculo correto: média ponderada pelos impactos
        media_cpm = (df_cpm_valido['impactos'] * df_cpm_valido['cpm']).sum() / df_cpm_valido['impactos'].sum()
    else:
        media_cpm = 0
    
    # Exibir métricas na sidebar
    st.metric("💰 Total Investido", f"R$ {total_investimento:,.2f}")
    st.metric("👁️ Total Impactos", f"{total_impactos:,}")
    st.metric("📈 CPM Médio", f"R$ {media_cpm:.2f}")

# ============================================
# KPIs PRINCIPAIS - COM DESTAQUES
# ============================================
st.subheader("📈 KPIs de Performance")

# Calcular métricas avançadas
df_kpi = df_filtrado.copy()
total_invest_kpi = df_kpi['Investimento'].sum()
total_impactos_kpi = df_kpi['impactos'].sum()

# Layout dos KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Investimento Total",
        f"R$ {total_invest_kpi:,.2f}",
        delta=f"{len(df_kpi)} canais",
        delta_color="off",
        help="Valor total investido nos canais selecionados"
    )

with col2:
    if total_impactos_kpi > 0:
        st.metric(
            "👁️ Impactos Totais",
            f"{total_impactos_kpi:,}",
            delta_color="off",
            help="Total de impressões alcançadas"
        )
    else:
        st.metric("👁️ Impactos Totais", "0", help="Total de impressões alcançadas")

with col3:
    df_cpm_kpi = df_kpi[df_kpi['cpm'] > 0]
    # Cálculo CORRETO do CPM médio
    if not df_cpm_kpi.empty and df_cpm_kpi['impactos'].sum() > 0:
        media_cpm_kpi = (df_cpm_kpi['impactos'] * df_cpm_kpi['cpm']).sum() / df_cpm_kpi['impactos'].sum()
    else:
        media_cpm_kpi = 0
        
    st.metric(
        "🎯 CPM Médio", 
        f"R$ {media_cpm_kpi:.2f}",
        help="Custo médio por mil impressões (ponderado pelos impactos)"
    )

with col4:
    if total_impactos_kpi > 0:
        eficiencia = total_impactos_kpi / total_invest_kpi
        
        # Usando HTML para mais controle
        st.markdown(f"""
        <div class="stMetric">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 8px;">⚡</span>
                <label style="color: {SICREDI_COLORS['verde_agricola']} !important; font-weight: 700; font-size: 16px;">
                    Eficiência
                    <span title="Indica quantas impressões são geradas por cada R$ 1,00 investido">[?]</span>
                </label>
            </div>
            <div data-testid="stMetricValue" style="color: {SICREDI_COLORS['verde_impresso']} !important; font-size: 28px; font-weight: 800; margin-bottom: 4px;">
                {eficiencia:,.1f}
            </div>
            <div style="color: {SICREDI_COLORS['cinza_medio']} !important; font-size: 14px; margin-top: 4px;">
                impressões por R$ 1,00
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.metric("⚡ Eficiência", "R$ 0.0000")

# Separador
st.markdown(f"""
<div style="height: 3px; background: linear-gradient(90deg, {SICREDI_COLORS['verde_digital']}, {SICREDI_COLORS['ouro']}); 
            border-radius: 2px; margin: 30px 0;"></div>
""", unsafe_allow_html=True)

# ============================================
# VISUALIZAÇÕES PRINCIPAIS - COM CORES FORTES
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Análise por Canal", 
    "📈 Distribuição (Investimento)", 
    "📈 Distribuição (Impacto)",
    "💰 Eficiência (CPM)", 
    "📋 Dados Detalhados"
])

# Paleta de cores contrastantes para gráficos
CORES_GRAFICOS = [
    SICREDI_COLORS['verde_agricola'],   # Verde escuro - melhor contraste
    SICREDI_COLORS['ouro'],             # Dourado - ótimo contraste
    SICREDI_COLORS['laranja'],          # Laranja - muito visível
    SICREDI_COLORS['terra'],            # Marrom/terra - bom contraste
    SICREDI_COLORS['verde_impresso'],   # Verde original
    '#D32F2F',                          # Vermelho - excelente contraste
    '#1976D2',                          # Azul - ótima visibilidade
    '#7B1FA2'                           # Roxo - destaque
]

with tab1:
    st.markdown(f"""
    <h3 style="color: {SICREDI_COLORS['verde_agricola']}; border-left: 6px solid {SICREDI_COLORS['ouro']}; padding-left: 15px;">
        📊 Análise de Desempenho por Canal
    </h3>
    """, unsafe_allow_html=True)
    
    # Adicionar contexto sobre os dados
    contexto = "agregados de todas as campanhas" if campanha_selecionada == 'Todas as Campanhas' else f"da campanha {campanha_selecionada}"
    st.markdown(f"<p style='color: {SICREDI_COLORS['cinza_medio']}; font-size: 14px; margin-bottom: 20px;'>Dados {contexto}</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de investimento por canal
        if not df_filtrado.empty:
            df_invest = df_filtrado.sort_values('Investimento', ascending=False)
            
            fig_invest = go.Figure()
            
            fig_invest.add_trace(go.Bar(
                x=df_invest['canal'],
                y=df_invest['Investimento'],
                name='Investimento',
                marker_color=CORES_GRAFICOS[0],
                marker_line_color=SICREDI_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_invest['Investimento'].apply(lambda x: f'R$ {x:,.0f}'),
                textposition='outside',
                textfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro'], family='Segoe UI'),
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
                    font=dict(size=20, color=SICREDI_COLORS['verde_agricola'], family='Segoe UI'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text='Canal', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                    tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                    tickangle=45
                ),
                yaxis=dict(
                    title=dict(text='Investimento (R$)', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                    tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                height=500,
                margin=dict(t=80, b=120, l=80, r=40)
            )
            
            st.plotly_chart(fig_invest, use_container_width=True)
    
    with col2:
        # Gráfico de impactos por canal
        if not df_filtrado.empty:
            df_impactos = df_filtrado.sort_values('impactos', ascending=False)
            
            fig_impactos = go.Figure()
            
            fig_impactos.add_trace(go.Bar(
                x=df_impactos['canal'],
                y=df_impactos['impactos'],
                name='Impactos',
                marker_color=CORES_GRAFICOS[1],  # Dourado
                marker_line_color=SICREDI_COLORS['cinza_escuro'],
                marker_line_width=2,
                text=df_impactos['impactos'].apply(lambda x: f'{x/1000000:.1f}M' if x > 1000000 else f'{x/1000:.0f}K'),
                textposition='outside',
                textfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro'], family='Segoe UI'),
                hovertemplate='<b>%{x}</b><br>' +
                              'Impactos: %{y:,}<br>' +
                              '% do total: %{customdata:.1%}<br>' +
                              'Campanha: ' + ('Todas' if campanha_selecionada == 'Todas as Campanhas' else campanha_selecionada) + 
                              '<extra></extra>',
                customdata=df_impactos['porcentagem_impactos']
            ))
            
            fig_impactos.update_layout(
                title=dict(
                    text=f'Impactos por Canal ({campanha_selecionada})',
                    font=dict(size=20, color=SICREDI_COLORS['verde_agricola'], family='Segoe UI'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text='Canal', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                    tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                    tickangle=45
                ),
                yaxis=dict(
                    title=dict(text='Número de Impactos', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                    tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                height=500,
                margin=dict(t=80, b=120, l=80, r=40)
            )
            
            st.plotly_chart(fig_impactos, use_container_width=True)

with tab2:
    st.markdown(f"""
    <h3 style="color: {SICREDI_COLORS['verde_agricola']}; border-left: 6px solid {SICREDI_COLORS['laranja']}; padding-left: 15px;">
        📈 Distribuição de Recursos (Investimento)
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Treemap para investimento (mantido como solicitado)
        if not df_filtrado.empty:
            # Filtrar apenas canais com investimento positivo
            df_treemap_invest = df_filtrado[df_filtrado['Investimento'] > 0]
            
            if not df_treemap_invest.empty:
                # Para "Todas as Campanhas", manter a estrutura original com campanhas e canais
                if campanha_selecionada == 'Todas as Campanhas':
                    # Usar dados completos para ver todas as campanhas
                    fig_treemap = px.treemap(
                        df,
                        path=['campanha', 'canal'],
                        values='Investimento',
                        color='cpm',
                        color_continuous_scale=["#6AB06D", SICREDI_COLORS['verde_agricola']],
                        title='Mapa de Investimento por Campanha e Canal'
                    )
                    
                    fig_treemap.update_traces(
                        textinfo='label+value',
                        textfont=dict(size=14, color='white'),
                        hovertemplate='<b>%{label}</b><br>Investimento: R$ %{value:,.2f}<br>CPM: R$ %{color:.2f}<extra></extra>'
                    )
                else:
                    # Para campanha específica, mostrar apenas os canais dessa campanha
                    fig_treemap = px.treemap(
                        df_treemap_invest,
                        path=['canal'],
                        values='Investimento',
                        color='cpm',
                        color_continuous_scale=["#6AB06D", SICREDI_COLORS['verde_agricola']],
                        title=f'Mapa de Investimento - {campanha_selecionada}'
                    )
                    
                    fig_treemap.update_traces(
                        textinfo='label+percent entry',
                        textfont=dict(size=14, color='white'),
                        hovertemplate='<b>%{label}</b><br>Investimento: R$ %{value:,.2f}<br>CPM: R$ %{color:.2f}<extra></extra>'
                    )
                
                fig_treemap.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI"),
                    height=500,
                    margin=dict(t=50, b=50, l=50, r=50)
                )
                
                st.plotly_chart(fig_treemap, use_container_width=True)
    
    with col2:
        # Gráfico de pizza para investimento (voltando ao original)
        if not df_filtrado.empty:
            df_pie_invest = df_filtrado[df_filtrado['Investimento'] > 0]
            if not df_pie_invest.empty:
                fig_pie_invest = px.pie(
                    df_pie_invest,
                    values='Investimento',
                    names='canal',
                    title=f'Distribuição do Investimento por Canal ({campanha_selecionada})',
                    color_discrete_sequence=CORES_GRAFICOS[:len(df_pie_invest)]
                )
                
                fig_pie_invest.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont=dict(size=14, color='white', family='Segoe UI'),
                    marker=dict(line=dict(color='white', width=3)),
                    hovertemplate='<b>%{label}</b><br>Investimento: R$ %{value:,.2f}<br>Porcentagem: %{percent}<extra></extra>'
                )
                
                fig_pie_invest.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI", size=14),
                    height=500,
                    legend=dict(
                        font=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor=SICREDI_COLORS['cinza_claro'],
                        borderwidth=2
                    ),
                    title=dict(
                        font=dict(size=18, color=SICREDI_COLORS['verde_agricola']),
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig_pie_invest, use_container_width=True)

with tab3:
    st.markdown(f"""
    <h3 style="color: {SICREDI_COLORS['verde_agricola']}; border-left: 6px solid {SICREDI_COLORS['ouro']}; padding-left: 15px;">
        📈 Distribuição de Recursos (Impacto)
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Treemap para impactos (mantido como solicitado)
        if not df_filtrado.empty:
            # Filtrar apenas canais com impactos positivos
            df_treemap_impact = df_filtrado[df_filtrado['impactos'] > 0]
            
            if not df_treemap_impact.empty:
                # Para "Todas as Campanhas"
                if campanha_selecionada == 'Todas as Campanhas':
                    fig_treemap_impact = px.treemap(
                        df,
                        path=['campanha', 'canal'],
                        values='impactos',
                        color='cpm',
                        color_continuous_scale=["#FFB300", SICREDI_COLORS['ouro']],
                        title='Mapa de Impactos por Campanha e Canal'
                    )
                    
                    fig_treemap_impact.update_traces(
                        textinfo='label+value',
                        textfont=dict(size=14, color='white'),
                        hovertemplate='<b>%{label}</b><br>Impactos: %{value:,}<br>CPM: R$ %{color:.2f}<extra></extra>'
                    )
                else:
                    # Para campanha específica
                    fig_treemap_impact = px.treemap(
                        df_treemap_impact,
                        path=['canal'],
                        values='impactos',
                        color='cpm',
                        color_continuous_scale=["#FFB300", SICREDI_COLORS['ouro']],
                        title=f'Mapa de Impactos - {campanha_selecionada}'
                    )
                    
                    fig_treemap_impact.update_traces(
                        textinfo='label+percent entry',
                        textfont=dict(size=14, color='white'),
                        hovertemplate='<b>%{label}</b><br>Impactos: %{value:,}<br>CPM: R$ %{color:.2f}<extra></extra>'
                    )
                
                fig_treemap_impact.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI"),
                    height=500,
                    margin=dict(t=50, b=50, l=50, r=50)
                )
                
                st.plotly_chart(fig_treemap_impact, use_container_width=True)
    
    with col2:
        # Gráfico de pizza para impactos (voltando ao original)
        if not df_filtrado.empty:
            df_pie_impact = df_filtrado[df_filtrado['impactos'] > 0]
            if not df_pie_impact.empty:
                fig_pie_impact = px.pie(
                    df_pie_impact,
                    values='impactos',
                    names='canal',
                    title=f'Distribuição de Impactos por Canal ({campanha_selecionada})',
                    color_discrete_sequence=CORES_GRAFICOS[:len(df_pie_impact)]
                )
                
                fig_pie_impact.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont=dict(size=14, color='white', family='Segoe UI'),
                    marker=dict(line=dict(color='white', width=3)),
                    hovertemplate='<b>%{label}</b><br>Impactos: %{value:,}<br>Porcentagem: %{percent}<extra></extra>'
                )
                
                fig_pie_impact.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI", size=14),
                    height=500,
                    legend=dict(
                        font=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor=SICREDI_COLORS['cinza_claro'],
                        borderwidth=2
                    ),
                    title=dict(
                        font=dict(size=18, color=SICREDI_COLORS['verde_agricola']),
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig_pie_impact, use_container_width=True)

with tab4:
    st.markdown(f"""
    <h3 style="color: {SICREDI_COLORS['verde_agricola']}; border-left: 6px solid {SICREDI_COLORS['terra']}; padding-left: 15px;">
        💰 Análise de Eficiência (CPM)
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de CPM - Barras horizontais para melhor leitura
        if not df_filtrado.empty:
            df_cpm = df_filtrado[df_filtrado['cpm'] > 0]
            if not df_cpm.empty:
                df_cpm = df_cpm.sort_values('cpm', ascending=True)  # Ordenar do menor para maior
                
                fig_cpm = go.Figure()
                
                fig_cpm.add_trace(go.Bar(
                    y=df_cpm['canal'],
                    x=df_cpm['cpm'],
                    name='CPM',
                    orientation='h',
                    marker_color=CORES_GRAFICOS[2],  # Laranja
                    marker_line_color=SICREDI_COLORS['cinza_escuro'],
                    marker_line_width=2,
                    text=df_cpm['cpm'].apply(lambda x: f'R$ {x:.2f}'),
                    textposition='outside',
                    textfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro'], family='Segoe UI'),
                    hovertemplate='<b>%{y}</b><br>' +
                                  'CPM: R$ %{x:.2f}<br>' +
                                  'Investimento: R$ %{customdata:,.2f}<br>' +
                                  'Campanha: ' + ('Todas' if campanha_selecionada == 'Todas as Campanhas' else campanha_selecionada) + 
                                  '<extra></extra>',
                    customdata=df_cpm['Investimento']
                ))
                
                fig_cpm.update_layout(
                    title=dict(
                        text=f'Custo por Mil Impressões (CPM) por Canal ({campanha_selecionada})',
                        font=dict(size=18, color=SICREDI_COLORS['verde_agricola'], family='Segoe UI'),
                        x=0.5
                    ),
                    yaxis=dict(
                        title=dict(text='Canal', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                        tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro'])
                    ),
                    xaxis=dict(
                        title=dict(text='CPM (R$)', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                        tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                        gridcolor='rgba(0,0,0,0.1)'
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    hovermode='y unified',
                    height=500,
                    margin=dict(t=80, b=80, l=150, r=40)
                )
                
                st.plotly_chart(fig_cpm, use_container_width=True)
    
    with col2:
        # Scatter plot com cores fortes
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
                    xaxis=dict(
                        title=dict(text='Investimento (R$)', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                        tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                        gridcolor='rgba(0,0,0,0.1)'
                    ),
                    yaxis=dict(
                        title=dict(text='Impactos', font=dict(size=14, color=SICREDI_COLORS['cinza_escuro'])),
                        tickfont=dict(size=12, color=SICREDI_COLORS['cinza_escuro']),
                        gridcolor='rgba(0,0,0,0.1)'
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI"),
                    height=500,
                    legend=dict(
                        font=dict(size=11, color=SICREDI_COLORS['cinza_escuro']),
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor=SICREDI_COLORS['cinza_claro'],
                        borderwidth=2
                    )
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)

with tab5:
    st.markdown(f"""
    <h3 style="color: {SICREDI_COLORS['verde_agricola']}; border-left: 6px solid {SICREDI_COLORS['verde_digital']}; padding-left: 15px;">
        📋 Dados Detalhados
    </h3>
    """, unsafe_allow_html=True)
    
    # Tabela detalhada com formatação condicional
    df_display = df_filtrado.copy()
    
    # Formatar valores
    df_display['Investimento_fmt'] = df_display['Investimento'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['porcentagem_investimento_fmt'] = df_display['porcentagem_investimento'].apply(lambda x: f"{x*100:.2f}%")
    df_display['impactos_fmt'] = df_display['impactos'].apply(lambda x: f"{x:,}")
    df_display['porcentagem_impactos_fmt'] = df_display['porcentagem_impactos'].apply(lambda x: f"{x*100:.2f}%")
    df_display['cpm_fmt'] = df_display['cpm'].apply(lambda x: f"R$ {x:.2f}" if x > 0 else "R$ 0.00")
    
    # Calcular eficiência (impactos por R$ investido)
    df_display['eficiencia'] = df_display.apply(
        lambda row: row['impactos'] / row['Investimento'] if row['Investimento'] > 0 else 0,
        axis=1
    )
    df_display['eficiencia_fmt'] = df_display['eficiencia'].apply(lambda x: f"{x:.2f}")
    
    # Reordenar colunas
    df_display = df_display[[
        'campanha', 'canal', 'Investimento_fmt', 'porcentagem_investimento_fmt',
        'impactos_fmt', 'porcentagem_impactos_fmt', 'cpm_fmt', 'eficiencia_fmt'
    ]]
    
    # Exibir tabela
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
    
    # Botão de download
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

# ============================================
# RODAPÉ DO DASHBOARD
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {SICREDI_COLORS['cinza_medio']}; font-size: 0.9rem; padding: 20px;">
    <p>🌾 <strong>Cocred Dashboard</strong> - Plataforma de Análise de Campanhas</p>
    <p>👤 Usuário: {st.session_state['username'].capitalize()} | 📅 Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
    <p style="font-size: 0.8rem;">© 2025 Cocred Cooperativa - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)