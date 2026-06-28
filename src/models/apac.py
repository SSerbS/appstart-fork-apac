from sqlalchemy import Column, String, Date, Text, Integer
from src.resources.database import Base

class ApacProcessamento(Base):
    __tablename__ = "apac_processamento"

    id_apac = Column(String, primary_key=True) # UUID gerado no backend
    cns_paciente = Column(String, nullable=False)
    nome_paciente = Column(String, nullable=False)
    data_atendimento = Column(Date, nullable=False)
    texto_evolucao = Column(Text, nullable=False)
    status = Column(String, nullable=False)

class DicionarioTermo(Base):
    __tablename__ = "dicionario_termos"

    id_termo = Column(Integer, primary_key=True, autoincrement=True)
    jargao_medico = Column(String, nullable=False, unique=True)
    categoria = Column(String, nullable=False) # 'diagnostico' ou 'tratamento'
    codigo_procedimento = Column(String, nullable=True)
    cid_principal = Column(String, nullable=True)
    cid_secundario = Column(String, nullable=True)
