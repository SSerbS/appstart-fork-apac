import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..interfaces.paciente_provider_interface import PacienteProviderInterface

# Índices das colunas do CSV (ajuste conforme necessário)
INDEX_ID = 0
INDEX_CNS = 1
INDEX_NOME = 5
INDEX_DATA = 2
INDEX_TEXTO = 6

class PacienteCsvProvider(PacienteProviderInterface):
    def __init__(self, csv_path: str = 'data/pacientes.csv'):
        self.csv_path = csv_path

    async def listar_pacientes(self) -> List[Dict[str, Any]]:
        pacientes = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Ignorar linhas vazias ou muito curtas
                    if not row or len(row) <= max(INDEX_ID, INDEX_CNS, INDEX_NOME, INDEX_DATA, INDEX_TEXTO):
                        continue
                    
                    # Ignorar se as colunas essenciais ou a evolução clínica estiverem vazias
                    raw_id = row[INDEX_ID].strip() if row[INDEX_ID] else ""
                    raw_cns = row[INDEX_CNS].strip() if row[INDEX_CNS] else ""
                    raw_texto = row[INDEX_TEXTO].strip() if row[INDEX_TEXTO] else ""
                    if not raw_id or not raw_cns or not raw_texto:
                        continue
                    
                    try:
                        seq_atendimento = int(row[INDEX_ID])
                    except ValueError:
                        seq_atendimento = row[INDEX_ID]

                    pacientes.append({
                        "seq_atendimento": seq_atendimento,
                        "cns_paciente": row[INDEX_CNS].strip() if row[INDEX_CNS] else "",
                        "nome_paciente": row[INDEX_NOME].strip() if row[INDEX_NOME] else "",
                        "data_atendimento": row[INDEX_DATA].strip() if row[INDEX_DATA] else "",
                        "texto_evolucao": row[INDEX_TEXTO].strip() if row[INDEX_TEXTO] else ""
                    })
        except FileNotFoundError:
            print(f"Arquivo CSV de pacientes não encontrado em: {self.csv_path}")
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")
        return pacientes

    async def obter_paciente_por_codigo(self, codigo: int) -> Dict[str, Any]:
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) <= max(INDEX_ID, INDEX_CNS, INDEX_NOME, INDEX_DATA, INDEX_TEXTO):
                        continue
                    
                    # Ignorar se as colunas essenciais ou a evolução clínica estiverem vazias
                    raw_id = row[INDEX_ID].strip() if row[INDEX_ID] else ""
                    raw_cns = row[INDEX_CNS].strip() if row[INDEX_CNS] else ""
                    raw_texto = row[INDEX_TEXTO].strip() if row[INDEX_TEXTO] else ""
                    if not raw_id or not raw_cns or not raw_texto:
                        continue
                    
                    try:
                        current_codigo = int(row[INDEX_ID])
                    except ValueError:
                        current_codigo = row[INDEX_ID]
                        
                    if str(current_codigo) == str(codigo):
                        return {
                            "seq_atendimento": current_codigo,
                            "cns_paciente": row[INDEX_CNS].strip() if row[INDEX_CNS] else "",
                            "nome_paciente": row[INDEX_NOME].strip() if row[INDEX_NOME] else "",
                            "data_atendimento": row[INDEX_DATA].strip() if row[INDEX_DATA] else "",
                            "texto_evolucao": row[INDEX_TEXTO].strip() if row[INDEX_TEXTO] else ""
                        }
        except FileNotFoundError:
            print(f"Arquivo CSV de pacientes não encontrado em: {self.csv_path}")
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado no CSV")
