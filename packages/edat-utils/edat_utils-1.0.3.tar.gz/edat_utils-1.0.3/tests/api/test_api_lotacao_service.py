from typing import List, Union

from edat_utils.api.api_lotacao_service.service import ApiLotacaoService
from edat_utils.api.models import UnidadeSchema


def test_get_lotacoes(get_api_lotacao_service: ApiLotacaoService):
    query = ''
    unidades: Union[List[UnidadeSchema], None] = get_api_lotacao_service.get(query=query)

    if not unidades:
        assert False

    assert len(unidades) > 0
    assert unidades[0].model_dump() is not None
