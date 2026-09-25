import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Base de Dados Interna (Carregamento via Cache para Performance)
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    dados = [
        {"Item": "Aço e Plástico", "Categoria": "Matéria-Prima", "Valor (R$)": 6500.00, "Prioridade": "Alta"},
        {"Item": "Embalagens Recicláveis", "Categoria": "Matéria-Prima", "Valor (R$)": 1800.00, "Prioridade": "Média"},
        {"Item": "Equipe de Desenvolvimento", "Categoria": "Mão de Obra", "Valor (R$)": 8500.00, "Prioridade": "Alta"},
        {"Item": "Consultoria Técnica", "Categoria": "Mão de Obra", "Valor (R$)": 3200.00, "Prioridade": "Baixa"},
        {"Item": "Transporte Rodoviário", "Categoria": "Logística", "Valor (R$)": 2400.00, "Prioridade": "Alta"},
        {"Item": "Armazenamento Terceirizado", "Categoria": "Logística", "Valor (R$)": 1200.00, "Prioridade": "Média"},
        {"Item": "Conta de Luz Industrial", "Categoria": "Energia", "Valor (R$)": 1900.00, "Prioridade": "Alta"},
        {"Item": "Licenças de Software CAD", "Categoria": "Ferramentas", "Valor (R$)": 1500.00, "Prioridade": "Média"},
        {"Item": "Manutenção de Maquinário", "Categoria": "Ferramentas", "Valor (R$)": 950.00, "Prioridade": "Baixa"},
        {"Item": "Gerador de Emergência", "Categoria": "Energia", "Valor (R$)": 800.00, "Prioridade": "Baixa"},
    ]
    return pd.DataFrame(dados)

df_despesas = carregar_dados()

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Configurações do Orçamento")

orcamento_total = st.sidebar.slider(
    "Orçamento Total Disponível (R$)",
    min_value=5000,
    max_value=50000,
    value=20000,
    step=500,
    format="R$ %d"
)

categorias_disponiveis = df_despesas["Categoria"].unique().tolist()

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

# -----------------------------------------------------------------------------
# Processamento dos Dados Filtrados
# -----------------------------------------------------------------------------
df_filtrado = df_despesas[df_despesas["Categoria"].isin(categorias_selecionadas)]

gasto_total = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_total

# -----------------------------------------------------------------------------
# Área Principal
# -----------------------------------------------------------------------------
st.title("💰 Simulador de Custos e Orçamento")
st.caption("Painel interativo para monitoramento de despesas, análise por categoria e saúde financeira do projeto.")

st.divider()

# Painel de Métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Orçamento Definido",
    value=f"R$ {orcamento_total:,.2f}"
)

col2.metric(
    label="Gasto Filtrado Total",
    value=f"R$ {gasto_total:,.2f}"
)

col3.metric(
    label="Saldo Restante",
    value=f"R$ {saldo_restante:,.2f}",
    delta=f"R$ {saldo_restante:,.2f}",
    delta_color="normal"  # Verde se positivo, vermelho se negativo
)

st.divider()

# Alerta Visual Condicional
if saldo_restante >= 0:
    st.success(f"✅ **Projeto dentro da meta!** Você ainda possui **R$ {saldo_restante:,.2f}** disponíveis no orçamento.")
else:
    excedente = abs(saldo_restante)
    st.error(f"⚠️ **Atenção: Orçamento Estourado!** Os custos selecionados ultrapassam o limite em **R$ {excedente:,.2f}**.")

st.write("")

# Layout em duas colunas para Gráfico e Tabela
col_grafico, col_tabela = st.columns([1, 1.2])

with col_grafico:
    st.subheader("📊 Gastos por Categoria")
    if not df_filtrado.empty:
        # Agrupamento nativo via Pandas
        df_agrupado = (
            df_filtrado.groupby("Categoria")["Valor (R$)"]
            .sum()
            .reset_index()
            .sort_values(by="Valor (R$)", ascending=True)
        )
        # Renderização usando o motor gráfico embutido do Streamlit (sem Plotly/Matplotlib)
        st.bar_chart(
            data=df_agrupado,
            x="Categoria",
            y="Valor (R$)",
            horizontal=True
        )
    else:
        st.info("Nenhuma categoria selecionada para exibir o gráfico.")

with col_tabela:
    st.subheader("📋 Detalhamento dos Itens")
    if not df_filtrado.empty:
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor (R$)": st.column_config.NumberColumn(
                    "Valor",
                    format="R$ %.2f"
                )
            }
        )
    else:
        st.warning("Selecione ao menos uma categoria na barra lateral.")
