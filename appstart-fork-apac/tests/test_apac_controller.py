import pytest
from src.controllers.apac_controller import mapear_termos

def test_mapear_termos_extrai_multiplos_jargoes():
    texto = "Paciente do sexo feminino com diagnóstico de neo de mama avançado. Iniciou ciclo de qt colon 1l. Relata leve dispneia aos esforços."
    
    dicionario_mock = [
        {"jargao_medico": "neo de mama", "codigo_procedimento": "0304020000", "cid_principal": "C50"},
        {"jargao_medico": "qt colon 1l", "codigo_procedimento": "0304020001", "cid_principal": "C18"},
        {"jargao_medico": "dispneia", "codigo_procedimento": "0000000000", "cid_principal": "R06.0"}
    ]
    
    resultados = mapear_termos(texto, dicionario_mock)
    
    assert len(resultados) == 3
    
    # 1. neo de mama
    assert resultados[0]["termo"] == "neo de mama"
    assert resultados[0]["codigo_procedimento"] == "0304020000"
    assert texto[resultados[0]["inicio"]:resultados[0]["fim"]].lower() == "neo de mama"
    
    # 2. qt colon 1l
    assert resultados[1]["termo"] == "qt colon 1l"
    assert resultados[1]["cid_principal"] == "C18"
    assert texto[resultados[1]["inicio"]:resultados[1]["fim"]].lower() == "qt colon 1l"
    
    # 3. dispneia
    assert resultados[2]["termo"] == "dispneia"
    assert texto[resultados[2]["inicio"]:resultados[2]["fim"]].lower() == "dispneia"

def test_mapear_termos_case_insensitive():
    texto = "Tratamento para NEO DE MAMA e DISPNEIA."
    
    dicionario_mock = [
        {"jargao_medico": "neo de mama", "codigo_procedimento": "0304020000", "cid_principal": "C50"},
        {"jargao_medico": "dispneia", "codigo_procedimento": "0000000000", "cid_principal": "R06.0"}
    ]
    
    resultados = mapear_termos(texto, dicionario_mock)
    
    assert len(resultados) == 2
    assert resultados[0]["termo"] == "neo de mama"
    assert resultados[1]["termo"] == "dispneia"

def test_mapear_termos_sobreposicao():
    # 'qt colon 1l' não deve sobrepor e marcar 'qt colon' isoladamente
    texto = "Realizando qt colon 1l hoje."
    
    dicionario_mock = [
        {"jargao_medico": "qt colon 1l", "codigo_procedimento": "0304020001", "cid_principal": "C18"},
        {"jargao_medico": "qt colon", "codigo_procedimento": "9999", "cid_principal": "C99"}
    ]
    
    resultados = mapear_termos(texto, dicionario_mock)
    
    assert len(resultados) == 1
    assert resultados[0]["termo"] == "qt colon 1l"
