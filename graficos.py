import pandas as pd
import plotly.graph_objects as go

def df_previsao_5dias(previsoes, cidade):
    """
    Converte o dict de previsões em DataFrame para gráficos
    """
    df = pd.DataFrame([
        {"data": dia, 
         "desc": info["desc"], 
         "temp_min": info["temp_min"], 
         "temp_max": info["temp_max"]}
        for dia, info in list(previsoes.items())[:5]
    ])
    df['cidade'] = cidade
    return df

def plot_temp_5dias(df):
    fig = go.Figure()

    # Linha Temp Máx
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['temp_max'],
        mode='lines+markers',
        name='Temp Máx',
        line=dict(color='#ff914d', width=3)
    ))

    # Linha Temp Mín
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['temp_min'],
        mode='lines+markers',
        name='Temp Mín',
        line=dict(color='#0097b2', width=3)
    ))

    # Layout com fundo transparente e responsivo
    fig.update_layout(
        title=f"Temperaturas em {df['cidade'].iloc[0]}",
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        width=None,  # responsivo
    )

    return fig

def analises_5dias_graficos(df):
    figs = []

    # 1. Dia mais quente
    df_max = df.loc[df['temp_max'].idxmax()]
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df_max['temp_max'],
        title={"text": f"Dia mais quente: {df_max['data']}"},
        gauge={'axis': {'range': [0, max(df['temp_max']) + 5]},
               'bar': {'color': "#ff914d"},
               'bgcolor': "#0097b2",
               'borderwidth': 3,
               'bordercolor': "#ff914d"}
    ))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=50, l=50, r=50),
        autosize=True,
        width=None,
    )
    figs.append(fig1)

    # 2. Dia mais frio
    df_min = df.loc[df['temp_min'].idxmin()]
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df_min['temp_min'],
        title={"text": f"Dia mais frio: {df_min['data']}"},
        gauge={'axis': {'range': [min(df['temp_min']) - 5, max(df['temp_max']) + 5]},
               'bar': {'color': "#0097b2"},
               'bgcolor': "#ff914d",
               'borderwidth': 3,
               'bordercolor': "#0097b2"}
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=50, l=50, r=50),
        autosize=True,
        width=None,
    )
    figs.append(fig2)

    # 3. Temperatura média da semana
    temp_min_media = df['temp_min'].mean()
    temp_max_media = df['temp_max'].mean()
    fig3 = go.Figure(go.Bar(
        x=['Mínima Média', 'Máxima Média'],
        y=[temp_min_media, temp_max_media],
        marker_color=["#ff914d", "#0097b2"],
        marker_line_color="#ffffff",
        marker_line_width=2
    ))
    fig3.update_layout(
        title="Temperatura média nos próximos 5 dias",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=50, l=50, r=50),
        autosize=True,
        width=None,
    )
    figs.append(fig3)

    return figs
