"""
Configurações do projeto
"""

# Configuração AWS Timestream
DATABASE_NAME = "Estacao_ESP32_database"
TABLE_NAME = "telemetria"
AWS_REGION = "us-east-1"

# Configurações de período
PERIOD_OPTIONS = {
    "1 hora": 1,
    "4 horas": 4,
    "12 horas": 12,
    "1 dia": 24,
    "1 semana": 168,
    "1 mês": 720
}

# Configurações de qualidade do ar
AIR_QUALITY_THRESHOLDS = {
    "Ótima": 800,
    "Boa": 1200,
    "Moderada": 2000,
    "Ruim": 2800,
    "Muito Ruim": float('inf')
}

# Configurações de pressão
PRESSURE_STEPS = [
    {"range": [900, 950], "color": "#E0E0E0"},
    {"range": [950, 1000], "color": "#ADD8E6"},
    {"range": [1000, 1050], "color": "#87CEEB"},
    {"range": [1050, 1100], "color": "#ADD8E6"}
]

# Configurações de qualidade do ar
AIR_QUALITY_STEPS = [
    {"range": [0, 800], "color": "#90EE90"},     # Ótima
    {"range": [800, 1200], "color": "#FFFF00"},  # Boa
    {"range": [1200, 2000], "color": "#FFA500"}, # Moderada
    {"range": [2000, 2800], "color": "#FF0000"}, # Ruim
    {"range": [2800, 3500], "color": "#800000"}  # Muito Ruim
]

# Configurações de cores para gráficos
CHART_COLORS = {
    "temperatura": "#FFA500",
    "umidade": "#1E90FF",
    "pressao": "#7209B7"
} 