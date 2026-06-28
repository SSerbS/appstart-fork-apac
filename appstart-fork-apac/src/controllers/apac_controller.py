import re
from typing import List, Dict, Any

def mapear_termos(texto: str, dicionario: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Busca termos do dicionário no texto da evolução de forma eficiente.
    Retorna uma lista de dicionários contendo os termos encontrados, 
    seus códigos (CID e procedimento) e os índices de início e fim no texto original.
    """
    if not texto or not dicionario:
        return []

    resultados = []
    
    # Ordenar o dicionário pelo tamanho do jargão (decrescente) evita 
    # que palavras menores dentro de maiores (ex: 'qt colon' dentro de 'qt colon 1l')
    # causem dupla marcação e sobreposição indevida.
    dicionario_ordenado = sorted(dicionario, key=lambda x: len(x['jargao_medico']), reverse=True)
    
    # Set para controlar os intervalos que já receberam marcação
    intervalos_mapeados = set()

    for item in dicionario_ordenado:
        jargao = item['jargao_medico']
        
        # Ignoramos case para que 'neo de mama' encontre 'NEO DE MAMA'
        pattern = re.compile(re.escape(jargao), re.IGNORECASE)
        
        for match in pattern.finditer(texto):
            inicio, fim = match.span()
            
            # Verifica se os índices conflitam com algo já mapeado
            sobreposicao = False
            for (map_inicio, map_fim) in intervalos_mapeados:
                if (inicio >= map_inicio and inicio < map_fim) or (fim > map_inicio and fim <= map_fim) or (inicio <= map_inicio and fim >= map_fim):
                    sobreposicao = True
                    break
            
            if not sobreposicao:
                intervalos_mapeados.add((inicio, fim))
                resultados.append({
                    "termo": jargao,
                    "codigo_procedimento": item.get('codigo_procedimento'),
                    "cid_principal": item.get('cid_principal'),
                    "cid_secundario": item.get('cid_secundario'),
                    "inicio": inicio,
                    "fim": fim
                })
                
    # Retornar a lista ordenada conforme as palavras aparecem no texto para facilitar uso no front-end
    return sorted(resultados, key=lambda x: x['inicio'])
