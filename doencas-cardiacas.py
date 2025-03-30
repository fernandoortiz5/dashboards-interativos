def carregar_dados():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    colunas = [
        'idade', 'sexo', 'tipo_dor', 'pressao_repouso', 'colesterol',
        'glicemia', 'eletrocardiograma', 'freq_maxima', 'angina_induzida',
        'depressao_st', 'inclinacao_st', 'vasos_col', 'talassemia', 'diagnostico'
    ]

    df = (
        pd.read_csv(url, names=colunas, na_values='?')
        .dropna()
        .assign(
            diagnostico = lambda x: x['diagnostico'].gt(0).map({True: 'Doença', False: 'Saudável'}),
            sexo = lambda x: x['sexo'].map({0: 'Feminino', 1: 'Masculino'}),
            faixa_etaria = lambda x: pd.cut(x['idade'],
                                          bins=[20, 40, 60, 100],
                                          labels=['20-40', '41-60', '60+'])
        )
    )
    return df

df = carregar_dados()
print("\n🔍 Dataset totalmente processado:")
display(df.head(2))

from google.colab import output
output.enable_custom_widget_manager()

def config_viz():
    import plotly.io as pio
    pio.renderers.default = 'colab'
    pio.templates.default = 'plotly_white'

config_viz()
print("⚙️ Renderização configurada para o Colab!")

@interact
def analise_interativa(
    faixa=widgets.Dropdown(options=df['faixa_etaria'].cat.categories.tolist(), description='Faixa Etária:'),
    sexo=widgets.SelectMultiple(options=df['sexo'].unique(), description='Sexo:', value=['Masculino'])
):
    # Aplicar filtros
    dados = df[(df['faixa_etaria'] == faixa) & (df['sexo'].isin(sexo))]

    # Layout dinâmico
    clear_output(wait=True)

    # Visualização 1: Distribuição de Diagnósticos
    fig1 = px.histogram(
        dados, x='idade', color='diagnostico',
        title=f'Distribuição por Idade - {faixa}',
        labels={'idade': 'Idade (anos)', 'count': 'Pacientes'},
        color_discrete_map={'Saudável': '#2ecc71', 'Doença': '#e74c3c'}
    )

    # Visualização 2: Relação Clínica
    fig2 = px.scatter(
        dados, x='pressao_repouso', y='colesterol',
        color='diagnostico', size='idade',
        title='Relação Pressão Arterial x Colesterol',
        labels={'pressao_repouso': 'Pressão (mmHg)', 'colesterol': 'Colesterol (mg/dl)'}
    )

    # Visualização 3: Correlações
    corr = dados[['idade', 'pressao_repouso', 'colesterol', 'freq_maxima']].corr()
    fig3 = px.imshow(
        corr.round(2), text_auto=True,
        title='Mapa de Calor de Correlações',
        color_continuous_scale='RdBu', zmin=-1, zmax=1
    )

    # Exibição organizada
    display(fig1)
    display(fig2)
    display(fig3)

    # Dados relevantes
    print(f"\n📌 Resumo Estatístico ({len(dados)} pacientes):")
    display(dados[['pressao_repouso', 'colesterol']].describe())
