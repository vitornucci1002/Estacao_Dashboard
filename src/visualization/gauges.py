"""
Módulo para renderização dos gauges do dashboard
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.config.settings import PRESSURE_STEPS, AIR_QUALITY_STEPS
from src.utils.helpers import classify_air_quality_from_analog

def create_gauge_chart(
        value,
        title_text,
        min_val,
        max_val,
        steps_config: list | None = None,
        bar_color: str = "#1f77b4",
        display_text: str | None = None,
        hide_ticks: bool = False
    ):
    """Cria um gráfico de gauge com estilo consistente"""
    gauge_value = value if pd.notna(value) and isinstance(value, (int, float)) else min_val

    axis_cfg = {"range": [min_val, max_val]}
    if hide_ticks:
        # Em vez de desligar os ticks, pintamos tudo de transparente
        axis_cfg.update({
            "tickwidth": 0,                          # sem traço
            "ticklen": 0,                            # sem comprimento
            "tickcolor": "rgba(0,0,0,0)",            # cor invisível
            "tickfont": {"color": "rgba(0,0,0,0)"},  # rótulos invisíveis
            "showticklabels": True                   # continua 'True' (importante)
        })
    else:
        axis_cfg.update({
            "tickwidth": 1.5,
            "tickcolor": "gray",
            "showticklabels": True
        })

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            title={"text": title_text,
                   "font": {"size": 16, "color": "white"},
                   "align": "center"},
            number={"suffix": "",
                    "font": {"size": 1, "color": "rgba(0,0,0,0)"}},
            gauge={
                "axis": axis_cfg,
                "bar": {"color": bar_color, "thickness": 0.3},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": steps_config or [],
            },
            domain={"x": [0, 1], "y": [0, 1]}
        )
    )

    # texto central
    fig.add_annotation(
        x=0.5, y=0.15, xref="paper", yref="paper",
        text=display_text,
        showarrow=False,
        font={"size": 22, "color": "white"},
        xanchor="center"
    )

    fig.update_layout(
        height=200,
        margin={"t": 50, "b": 20, "l": 35, "r": 35},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"}
    )
    return fig

def render_gauge_indicators(latest_data):
    """Renderiza os indicadores gauge"""
    st.markdown("---_Indicadores Detalhados_---")
    col_gauge1, col_gauge2, col_gauge3 = st.columns(3)
    
    with col_gauge1:
        pressao_val = latest_data.get("pressao")
        press_gauge = create_gauge_chart(
            value=pressao_val, 
            title_text="Pressão", 
            min_val=900, 
            max_val=1100, 
            steps_config=PRESSURE_STEPS, 
            bar_color="#4682B4",
            display_text=f"{pressao_val:.1f} hPa" if pd.notna(pressao_val) else None,
        )
        st.plotly_chart(press_gauge, use_container_width=True)

    with col_gauge2:
        altitude_val = latest_data.get("altitude")
        alt_max_range = max(1000, altitude_val + 200) if pd.notna(altitude_val) and isinstance(altitude_val, (int,float)) else 1000
        alt_gauge = create_gauge_chart(
            value=altitude_val, 
            title_text="Altitude", 
            min_val=0, 
            max_val=alt_max_range, 
            bar_color="#2CA02C",
            display_text=f"{altitude_val:.1f} m" if pd.notna(altitude_val) else None,
        )
        st.plotly_chart(alt_gauge, use_container_width=True)

    with col_gauge3:
        mq135_analog_val = latest_data.get("mq135_analog")
        air_quality_category = classify_air_quality_from_analog(mq135_analog_val)
        
        air_qual_gauge_max = 3500 
        
        # Para manter o mesmo estilo dos outros gauges mas ainda mostrar a categoria
        air_qual_gauge_fig = create_gauge_chart(
            value=mq135_analog_val, 
            title_text="Qualidade do Ar", 
            min_val=0, 
            max_val=air_qual_gauge_max, 
            steps_config=AIR_QUALITY_STEPS, 
            bar_color="#7F7F7F",
            display_text=air_quality_category,
            hide_ticks = True 
        )
        st.plotly_chart(air_qual_gauge_fig, use_container_width=True) 