from typing import List, Union
from edat_utils.api import ApiFuncionarioService
from edat_utils.api.models import Usuario


def test_get_funcionarios(get_api_funcionario_service: ApiFuncionarioService):
    query = f'in: {{matricula: {[260703, 319884, 314937, 299025]}}}'
    funcionarios: Union[List[Usuario], None] = get_api_funcionario_service.get(query=query)

    if not funcionarios:
        assert False

    assert len(funcionarios) > 0
    assert funcionarios[0].model_dump() is not None
