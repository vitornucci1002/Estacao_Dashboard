"""
Funções auxiliares para o dashboard
"""
import pandas as pd
from ..config.settings import AIR_QUALITY_THRESHOLDS

def classify_air_quality_from_analog(analog_value):
    """Classifica a qualidade do ar a partir do valor analógico"""
    if pd.isna(analog_value):
        return "N/A"
    try:
        val = float(analog_value)
    except (ValueError, TypeError):
        return "N/A"

    for quality, threshold in AIR_QUALITY_THRESHOLDS.items():
        if val < threshold:
            return quality
    
    return "Muito Ruim" 