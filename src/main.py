# para rodar esse arquivo: 
# python -m streamlit run src/main.py

"""
Dashboard principal para visualização de dados das estações meteorológicas
"""
import streamlit as st
import pandas as pd
from src.config.settings import PERIOD_OPTIONS
from src.data.timestream_client import init_timestream_client, get_all_stations_latest_data, get_station_details
from src.visualization.cards import render_weather_cards
from src.visualization.gauges import render_gauge_indicators
from src.visualization.charts import create_dual_axis_chart

# --- Configuração da página Streamlit (deve ser o primeiro comando Streamlit) ---
st.set_page_config(page_title="Dashboard Estações Meteorológicas", layout="wide")

# --- Estilos CSS para os cards ---
st.markdown("""
<style>
.metric-card {
    background-color:#0e1117;
    border-radius:10px;
    padding:24px;
    text-align:center;
    height:100%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    box-shadow:0 0 12px rgba(141, 141, 141, 0.1);
}
.metric-label_small  {font-size:0.7rem; color:#d0d0d0; margin-bottom:4px;}
.metric-value_small  {font-size:2.0rem;  font-weight:600; color:#ffffff; margin:0;}
.metric-label_big  {font-size:1.05rem; color:#d0d0d0; margin-bottom:4px;}
.metric-value_big  {font-size:3.0rem;  font-weight:600; color:#ffffff; margin:0;}
.big-card   {min-height:255px;}   /* ocupa a coluna toda (≈2×small + gap) */
.small-card {min-height:100px;}
</style>
""", unsafe_allow_html=True)

def main():
    # Inicializa o cliente Timestream
    ts_query_client = init_timestream_client()
    st.title("🛰️ Dashboard de Estações Meteorológicas")

    stations_df = get_all_stations_latest_data(ts_query_client)
    selected_device_id = None

    if ts_query_client is None:
        st.error("Cliente Timestream não inicializado. O dashboard não pode funcionar.")
    elif stations_df.empty:
        st.warning("Nenhuma estação com dados de localização recentes (último dia) encontrada. Verifique a conexão e se há dados no Timestream.")
    else:
        st.sidebar.header("Selecionar Estação")
        if "selected_device_id" not in st.session_state or st.session_state.selected_device_id not in stations_df["device_id"].unique():
            st.session_state.selected_device_id = stations_df["device_id"].unique()[0]

        selected_device_id = st.sidebar.selectbox(
            "Escolha uma estação pelo ID:", 
            options=stations_df["device_id"].unique(),
            key="station_select_box_main_v10",
            index=list(stations_df["device_id"].unique()).index(st.session_state.selected_device_id)
        )
        st.session_state.selected_device_id = selected_device_id

        st.subheader("Localização das Estações")
        st.map(stations_df[["latitude", "longitude"]])
        st.caption(f"Fonte da Localização: {(get_station_details(ts_query_client, selected_device_id).iloc[0]).get('fonte_localizacao', 'N/A')}")

    if selected_device_id:
        st.subheader(f"Dados da Estação: {selected_device_id} (Período Selecionado)")
        
        # Seleção do período de dados
        selected_period = st.sidebar.selectbox(
            "Selecione o período de dados:",
            options=list(PERIOD_OPTIONS.keys()),
            key="period_select_box"
        )
        period_hours = PERIOD_OPTIONS[selected_period]
        
        station_details_df = get_station_details(ts_query_client, selected_device_id, period_hours)

        if station_details_df.empty:
            st.warning(f"Nenhum dado detalhado encontrado para a estação {selected_device_id} no período selecionado. Verifique se a estação está enviando dados.")
        else:
            latest_data = station_details_df.iloc[0]
            
            # Extrair dados para cards
            current_temp = latest_data.get("temperatura")
            current_humidity = latest_data.get("umidade")
            max_temp = pd.NA
            min_temp = pd.NA

            if "temperatura" in station_details_df.columns and not station_details_df["temperatura"].dropna().empty:
                max_temp = station_details_df["temperatura"].max()
                min_temp = station_details_df["temperatura"].min()

            if "umidade" in station_details_df.columns and not station_details_df["umidade"].dropna().empty:
                max_humidity = station_details_df["umidade"].max()
                min_humidity = station_details_df["umidade"].min()

            # Renderizar cards meteorológicos
            render_weather_cards(
                current_temp, max_temp, min_temp, 
                current_humidity, max_humidity, min_humidity,
                selected_period
            )
            
            # Renderizar indicadores gauge
            render_gauge_indicators(latest_data)

            # Mostrar timestamp da última atualização
            hora_local = latest_data.get('time', pd.NaT)
            if pd.notna(hora_local):
                # Garante que está no timezone correto
                if hora_local.tz is None:
                    hora_local = hora_local.tz_localize('UTC').tz_convert('America/Sao_Paulo')
                else:
                    hora_local = hora_local.tz_convert('America/Sao_Paulo')
                st.caption(f"Última atualização da estação: {hora_local.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.caption("Última atualização da estação: N/A")
            
            # Mostrar gráfico histórico
            st.subheader(f"Histórico de {selected_period} (Temperatura, Umidade, Pressão)")
            display_cols = ["time", "temperatura", "umidade", "pressao"]
            chart_data_cols = [col for col in display_cols if col in station_details_df.columns]
            
            if "time" in chart_data_cols and any(col in chart_data_cols for col in ["temperatura", "umidade", "pressao"]):
                # Criar e exibir o gráfico de eixos duplos
                dual_axis_fig = create_dual_axis_chart(station_details_df, time_col="time")
                if dual_axis_fig:
                    st.plotly_chart(dual_axis_fig, use_container_width=True)
                else:
                    st.info("Não há dados de histórico suficientes para exibir o gráfico.")
            else:
                st.info("Coluna 'time' ou dados insuficientes para o gráfico de histórico.")
    else:
        if ts_query_client and not stations_df.empty:
            st.info("Selecione uma estação na barra lateral para ver os detalhes.")

    st.sidebar.markdown("_Desenvolvido por Vitor e Jerônimo_ \n"
                        "_IoT 2025.1_")

if __name__ == "__main__":
    main() 