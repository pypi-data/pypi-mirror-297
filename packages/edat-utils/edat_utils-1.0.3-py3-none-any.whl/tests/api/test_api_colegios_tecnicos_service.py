from typing import List, Union
from edat_utils.api.api_colegios_service.service import ApiColegiosTecnicosService
from edat_utils.api.models import Usuario


def test_get_alunos_colegios(get_api_colegios_tecnicos_service: ApiColegiosTecnicosService):
    query = f'notNull: {{nome_aluno: {None}}}'
    funcionarios: Union[List[Usuario], None] = get_api_colegios_tecnicos_service.get(query=query)

    if not funcionarios:
        assert False

    assert len(funcionarios) > 0
    assert funcionarios[0].model_dump() is not None
