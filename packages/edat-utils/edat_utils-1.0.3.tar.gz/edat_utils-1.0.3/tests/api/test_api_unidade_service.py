from typing import List, Union

from edat_utils.api.api_unidade_service.service import ApiUnidadeService
from edat_utils.api.models import UnidadeSchema


def test_get_unidades(get_api_unidade_service: ApiUnidadeService):
    query = 'gt: {numero_lotacao: 0}'
    unidades: Union[List[UnidadeSchema], None] = get_api_unidade_service.get(query=query)

    if not unidades:
        assert False

    assert len(unidades) > 0
    assert unidades[0].model_dump() is not None
