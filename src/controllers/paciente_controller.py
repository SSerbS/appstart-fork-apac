from typing import List, Dict, Any

from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface

async def listar_pacientes(
    provider: PacienteProviderInterface,
    search_id: str = None
) -> List[Dict[str, Any]]:
    return await provider.listar_pacientes(search_id)

async def obter_paciente_por_codigo(
    codigo: int,
    provider: PacienteProviderInterface
) -> Dict[str, Any]:
    return await provider.obter_paciente_por_codigo(codigo)