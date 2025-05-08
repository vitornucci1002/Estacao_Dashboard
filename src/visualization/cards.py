"""
Módulo para renderização dos cards do dashboard
"""
import streamlit as st

def render_weather_cards(current_temp, max_temp, min_temp, current_humidity, max_humidity, min_humidity, selected_period):
    """Renderiza os cards com dados meteorológicos"""
    col_temp1, col_temp2, col_temp3, col_temp4 = st.columns(4)

    # Temperatura Atual  ▸ coluna 1 (cartão grande)
    with col_temp1:
        st.markdown(
            f"""
            <div class="metric-card big-card">
                <div class="metric-label_big">Temperatura Atual</div>
                <div class="metric-value_big">{current_temp:.1f} °C</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Temperatura Máx / Mín  ▸ coluna 2 (dois cartões pequenos empilhados)
    with col_temp2:
        st.markdown(
            f"""
            <div class="metric-card small-card">
                <div class="metric-label_small">Temp. Máx ({selected_period})</div>
                <div class="metric-value_small">{max_temp:.1f} °C</div>
            </div>
            <div style="height:12px;"></div>  <!-- espaçamento -->
            <div class="metric-card small-card">
                <div class="metric-label_small">Temp. Mín ({selected_period})</div>
                <div class="metric-value_small">{min_temp:.1f} °C</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Umidade Atual  ▸ coluna 3 (cartão grande)
    with col_temp3:
        st.markdown(
            f"""
            <div class="metric-card big-card">
                <div class="metric-label_big">Umidade Atual</div>
                <div class="metric-value_big">{current_humidity:.1f} %</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Umidade Máx / Mín  ▸ coluna 4 (dois cartões pequenos empilhados)
    with col_temp4:
        st.markdown(
            f"""
            <div class="metric-card small-card">
                <div class="metric-label_small">Umidade Máx ({selected_period})</div>
                <div class="metric-value_small">{max_humidity:.1f} %</div>
            </div>
            <div style="height:12px;"></div>  <!-- espaçamento -->
            <div class="metric-card small-card">
                <div class="metric-label_small">Umidade Mín ({selected_period})</div>
                <div class="metric-value_small">{min_humidity:.1f} %</div>
            </div>
            """,
            unsafe_allow_html=True
        ) 