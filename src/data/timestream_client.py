"""
Módulo para interação com o AWS Timestream
"""
import streamlit as st
import boto3
import pandas as pd
from src.config.settings import DATABASE_NAME, TABLE_NAME, AWS_REGION

@st.cache_resource
def init_timestream_client():
    """Inicializa o cliente Timestream"""
    try:
        session = boto3.Session()
        return session.client("timestream-query", region_name=AWS_REGION)
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Timestream: {e}. Verifique as credenciais da AWS e a região.")
        return None

@st.cache_data(ttl=10)
def parse_query_response(_response, query_origin="Unknown"):
    """Parseia a resposta da consulta Timestream"""
    column_info = _response["ColumnInfo"]
    rows = _response["Rows"]
    data = []
    for row_idx, row in enumerate(rows):
        record = {}
        for i, item in enumerate(row["Data"]):
            col_name = column_info[i]["Name"]
            if "ScalarValue" in item:
                scalar_type = column_info[i].get("Type", {}).get("ScalarType")
                value = item["ScalarValue"]
                if scalar_type == "TIMESTAMP":
                    record[col_name] = pd.to_datetime(value, errors="coerce", utc=True)
                elif scalar_type in ["DOUBLE", "BIGINT", "INTEGER"]:
                    record[col_name] = pd.to_numeric(value, errors="coerce")
                else:  # VARCHAR and others
                    record[col_name] = value            
            elif "NullValue" in item and item["NullValue"]:
                record[col_name] = pd.NA
        data.append(record)
    df = pd.DataFrame(data)
    
    # Ajusta coluna de tempo para o timezone local se existir
    if "time" in df.columns:
        try:
            df["time"] = df["time"].dt.tz_convert('America/Sao_Paulo')
        except Exception:
            pass
    return df

@st.cache_data(ttl=60)
def get_all_stations_latest_data(_ts_query_client):
    """Obtém os últimos dados de todas as estações ativas"""
    if not _ts_query_client:
        return pd.DataFrame()
    query_simplified = f"""
    WITH ranked_by_time AS (
        SELECT 
            device_id, 
            latitude, 
            longitude, 
            time,
            ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY time DESC) as rn
        FROM \"{DATABASE_NAME}\".\"{TABLE_NAME}\"
        WHERE time >= ago(1d) AND TRY_CAST(latitude AS VARCHAR) IS NOT NULL AND TRY_CAST(longitude AS VARCHAR) IS NOT NULL
    )
    SELECT 
        device_id, 
        TRY_CAST(latitude AS DOUBLE) as latitude, 
        TRY_CAST(longitude AS DOUBLE) as longitude, 
        time as last_seen 
    FROM ranked_by_time 
    WHERE rn = 1
    """
    try:
        response = _ts_query_client.query(QueryString=query_simplified)
        df = parse_query_response(response, "all_stations")
        if not df.empty:
            df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
            df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
            df = df.dropna(subset=["latitude", "longitude"])
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados das estações: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=10)
def get_station_details(_ts_query_client, device_id, period_hours=24):
    """Obtém dados detalhados para uma estação específica"""
    if not _ts_query_client:
        return pd.DataFrame()
    query_flat_table = f"""
    SELECT 
        time, 
        device_id,
        TRY_CAST(temperatura AS DOUBLE) as temperatura,
        TRY_CAST(umidade AS DOUBLE) as umidade,
        TRY_CAST(pressao AS DOUBLE) as pressao,
        TRY_CAST(altitude AS DOUBLE) as altitude,
        TRY_CAST(mq135_analog AS DOUBLE) as mq135_analog, 
        fonte_localizacao
    FROM \"{DATABASE_NAME}\".\"{TABLE_NAME}\"
    WHERE device_id = \'{device_id}\' AND time >= ago({period_hours}h)
    ORDER BY time DESC
    """
    try:
        response = _ts_query_client.query(QueryString=query_flat_table)
        df = parse_query_response(response, f"station_details_{device_id}_{period_hours}")
        if not df.empty:
            numeric_cols = ["temperatura", "umidade", "pressao", "altitude", "mq135_analog"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "time" in df.columns:
                 df["time"] = pd.to_datetime(df["time"], errors="coerce")
                 df = df.sort_values(by="time", ascending=False)
        return df
    except Exception as e:
        st.error(f"Erro ao buscar detalhes da estação {device_id}: {e}")
        return pd.DataFrame() 