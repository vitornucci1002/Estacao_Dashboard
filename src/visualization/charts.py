"""
Módulo para renderização dos gráficos do dashboard
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..config.settings import CHART_COLORS

def create_dual_axis_chart(df, temp_col='temperatura', humid_col='umidade', pressure_col='pressao', time_col='time'):
    """Cria um gráfico de série temporal com eixos duplos"""
    if df.empty or time_col not in df.columns:
        return None
    
    chart_df = df.copy()
    if time_col in chart_df.columns:
        chart_df = chart_df.sort_values(by=time_col, ascending=True)
    
    # Create the figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add temperature trace on left axis if data exists
    if temp_col in chart_df.columns and not chart_df[temp_col].dropna().empty:
        fig.add_trace(
            go.Scatter(
                x=chart_df[time_col], 
                y=chart_df[temp_col], 
                name="Temperatura (°C)",
                line=dict(color=CHART_COLORS["temperatura"], width=2)
            ),
            secondary_y=False
        )
    
    # Add humidity trace on left axis if data exists
    if humid_col in chart_df.columns and not chart_df[humid_col].dropna().empty:
        fig.add_trace(
            go.Scatter(
                x=chart_df[time_col], 
                y=chart_df[humid_col], 
                name="Umidade (%)",
                line=dict(color=CHART_COLORS["umidade"], width=2)
            ),
            secondary_y=False
        )
    
    # Add pressure trace on right axis if data exists
    if pressure_col in chart_df.columns and not chart_df[pressure_col].dropna().empty:
        fig.add_trace(
            go.Scatter(
                x=chart_df[time_col], 
                y=chart_df[pressure_col], 
                name="Pressão (hPa)",
                line=dict(color=CHART_COLORS["pressao"], width=2)
            ),
            secondary_y=True
        )
    
    # Set titles and axis labels
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="white")
        ),
        margin=dict(l=60, r=60, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.05)",
        hovermode="x unified"
    )
    
    # Update x-axis properties
    fig.update_xaxes(
        title_text="Data/Hora",
        title_font=dict(color="white"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="white")
    )
    
    # Update primary y-axis properties (temperature/humidity)
    temp_max = chart_df[temp_col].max() if temp_col in chart_df.columns else 40
    humid_max = chart_df[humid_col].max() if humid_col in chart_df.columns else 100
    left_max = max(temp_max, humid_max) * 1.1  # 10% headroom
    
    fig.update_yaxes(
        title_text="Temperatura (°C) / Umidade (%)",
        title_font=dict(color="white"),
        tickfont=dict(color="white"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)",
        range=[0, left_max],
        secondary_y=False
    )
    
    # Update secondary y-axis properties (pressure)
    if pressure_col in chart_df.columns and not chart_df[pressure_col].dropna().empty:
        pressure_min = chart_df[pressure_col].min() * 0.998
        pressure_max = chart_df[pressure_col].max() * 1.002
        # Make sure we have a reasonable range
        pressure_range = pressure_max - pressure_min
        if pressure_range < 5:
            pressure_mean = (pressure_max + pressure_min) / 2
            pressure_min = pressure_mean - 2.5
            pressure_max = pressure_mean + 2.5
    else:
        pressure_min = 950
        pressure_max = 1050
    
    fig.update_yaxes(
        title_text="Pressão (hPa)",
        title_font=dict(color="white"),
        tickfont=dict(color="white"),
        showgrid=False,
        range=[pressure_min, pressure_max],
        secondary_y=True
    )
    
    return fig 