from fastapi import APIRouter, Depends, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth import auth_handler
from ..dependencies import get_paciente_provider
from ..resources.database import get_app_db_session
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..controllers import apac_controller

STRATEGY = "csv"

class TermoCreate(BaseModel):
    jargao_medico: str
    categoria: str
    codigo_procedimento: Optional[str] = None
    cid_principal: Optional[str] = None
    cid_secundario: Optional[str] = None

class TermoResponse(TermoCreate):
    id_termo: int

router = APIRouter(
    prefix="/api/apac",
    tags=["APAC"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.get("/pacientes", response_model=List[Dict[str, Any]])
async def listar_pacientes_apac(
    provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY)),
    session: AsyncSession = Depends(get_app_db_session)
):
    """
    Lê os pacientes do CSV, passa os textos de evolução para o ApacController
    fazer a varredura contra o dicionário local e retorna a lista mapeada.
    """
    # 1. Obter pacientes do CSV
    pacientes = await provider.listar_pacientes()
    
    # 2. Obter dicionário do banco local
    dicionario = await apac_controller.obter_dicionario(session)
    
    # 3. Mapear termos em cada evolução
    for paciente in pacientes:
        texto = paciente.get("texto_evolucao", "")
        paciente["termos_encontrados"] = apac_controller.mapear_termos(texto, dicionario)
        
    return pacientes

@router.post("/dicionario", response_model=TermoResponse)
async def adicionar_termo(
    dados: TermoCreate = Body(...),
    session: AsyncSession = Depends(get_app_db_session)
):
    """
    Adiciona novos termos ao banco transacional.
    """
    return await apac_controller.adicionar_termo_dicionario(session, dados.dict())

@router.get("/exportar")
async def exportar_apac():
    """
    Simula o arquivo TXT do SUS.
    """
    return "MOCK_TXT_SUS_LINE_1\nMOCK_TXT_SUS_LINE_2\n"
