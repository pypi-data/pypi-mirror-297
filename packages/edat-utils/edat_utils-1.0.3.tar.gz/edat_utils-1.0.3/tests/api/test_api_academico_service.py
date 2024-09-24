from typing import List, Union
from edat_utils.api import ApiAcademicoService
from edat_utils.api.models import Usuario


def test_get_alunos(get_api_academico_service: ApiAcademicoService):
    query = f'in: {{ra: {[103752, 103750, 104589, 105891, 107921]}}}'
    alunos: Union[List[Usuario], None] = get_api_academico_service.get(query=query)

    if not alunos:
        assert False

    assert len(alunos) > 0
    assert alunos[0].model_dump() is not None
