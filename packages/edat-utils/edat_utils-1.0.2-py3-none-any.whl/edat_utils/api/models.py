from datetime import date, datetime
from enum import Enum
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, TypeAdapter, model_validator

class TipoUsuario(str, Enum):
    """ Classe enum de tipo de usuário """
    DOCENTE = 'faculty'
    FUNCIONARIO = 'staff'
    ALUNO = 'student'
    ALUNO_COTIL = 'ALUNO COTIL'
    ALUNO_COTUCA = 'ALUNO COTUCA'
    FUNCAMP = 'funcamp'

    def __str__(self) -> str:
        return str(self.value)

class Usuario(BaseModel):
    nome: str = Field(..., description='Nome do usuário')
    identificador: int = Field(..., description='Identificador do usuário, matricula ou ra')
    email: str = Field(..., description='Nome do usuário')
    unidade: str = Field(..., description='Unidade, Centro, Instituto ou Faculdade do usuário')
    cargo: str = Field(..., description='cargo ou curso do usuário')
    nomeSindicato: Union[str, None] = Field(default=None, alias='nome_sindicato', description='Tipo de sindicato do usuário')
    telefone: Optional[Union[str, int]] = Field(default=None, description='telefone/ ramal do usuário')
    username: Optional[str] = Field(default=None, description='username do usuário')
    tipo_usuario: Union[TipoUsuario, None]= Field(default=None, alias='TipoUsuario', description='Tipo de Membro do usuário')

    
    @model_validator(mode='before')
    def antes(cls, values):
        if 'email' in values and isinstance(values['email'], int):
            values['email'] = 'email não informado'
        return values

    @model_validator(mode='after')
    def ajustar_campos(self):
        if self.nomeSindicato:
            # ajustar o tipo de usuário
            match self.nomeSindicato:
                case 'Funcamp':
                    self.tipo_usuario = TipoUsuario.FUNCAMP
                case 'ESU, Docente':
                    self.tipo_usuario = TipoUsuario.DOCENTE
                case 'ESU, Não Docente':
                    self.tipo_usuario = TipoUsuario.FUNCIONARIO
                case 'CLT, Não Docente':
                    self.tipo_usuario = TipoUsuario.FUNCIONARIO
                case _ :
                    self.tipo_usuario = TipoUsuario.ALUNO
        else:
            self.tipo_usuario = TipoUsuario.ALUNO

        # ajustar o username
        if self.email != 'EMAIL NAO ATIVO':
            self.username = str(self.email).split('@')[0]
        else:
            self.username = None

        # remover o campo desnecessário
        delattr(self, 'nomeSindicato')

        return self


class UnidadeSchema(BaseModel):
    numeroLotacao: int = Field(..., description='Número da lotação da unidade')
    unidade: str = Field(..., description='Sigla da unidade')
    nomeUnidade: str = Field(..., description='Nome da unidade em caixa alta sem acentuação')
    lotacao: str = Field(..., description='Código da lotação da unidade')
    nomeUnidadeAcentuada: Optional[str] = Field(..., description='Nome da unidade formatado e acentuado')
    tipoUnidade: Optional[str] = Field(..., description='Tipo da unidade')
    categoriaUnidade: Optional[str] = Field(..., description='Categoria da Unidade')
    siglaArea: Optional[str] = Field(..., description='Sigla da área da unidade')
    descricaoArea: Optional[str] = Field(..., description='Descrição da unidade')

    @model_validator(mode='before')
    def antes(cls, values):
        if 'siglaArea' in values and values['siglaArea'] in ['', ' ', '  ', 'null']:
            values['siglaArea'] = None
        
        if 'lotacao' not in values:
            values['lotacao'] = values.get('codigoLocal', 'não informado')

        if 'descricaoArea' not in values:
            values['descricaoArea'] = None

        if 'numeroLotacao' not in values:
            values['numeroLotacao'] = values.get('numeroUnidade', 0)

        return values

class CursoSchema(BaseModel):
    dataGeracao: datetime = Field(..., description='Data de quanto o registro foi processado pelo sistema de importação de tabelas')
    ultimoCatalogoVigente: int = Field(..., description='Último ano do catálogo vigente')
    siglaOrgao: str = Field(..., description='Sigla do orgão ao qual o curso pertence')
    codigoCurso: int = Field(..., description='Código do curso')
    nomeCurso: str = Field(..., description='Nome do curso')
    nomeUnidade: str = Field(..., description='Nome da unidade ao qual o curso pertence')


class CursoDacSchema(CursoSchema):
    siglaOrgaoCatalogo: str = Field(str, description='Sigla do órgão do catálogo')
    nivelCurso: str = Field(..., description='Nível do curso')
    descAreaCurso: str = Field(..., description='Descrição da área do curso')
    tipoTurnoCurso: str = Field(..., description='Tipo de turno do curso')
    nomeUnidadeAcentuada: str = Field(..., description='Nome da unidade com acentuação ao qual o curso pertence')
    coordenadoria: str = Field(..., description='Nome da coordenadoria ao qual o curso pertence')
    classificacaoCurso: Optional[str] = Field(..., description='Classificação do curso')
    nomeCursoAnuario: Optional[str] = Field(default=None, description='Nome do curso do anuário')
    especialidadeAnuario: Optional[str] = Field(default=None, description='Especialidade do anuário')
    siglaOrgaoAnuario: Optional[str] = Field(..., description='Sigla do orgão do anuário')


class CursoTecnicoSchema(BaseModel):
    totalDeMatriculadosCurso: Optional[int] = Field(default=None, description='Quantidade de alunos matriculados')


# Tipo de lista de usuário para facilitar o parse do pydantic
UsuarioList = TypeAdapter(List[Usuario])

# Tipo de lista de unidade para facilitar o parse do pydantic
UnidadeSchemaList = TypeAdapter(List[UnidadeSchema])

# Tipo de lista de cursos academicos para facilitar o parse do pydantic
CursoList = TypeAdapter(List[CursoDacSchema])

# Tipo de lista de cursos técnicos para facilitar o parse do pydantic
CursoTecnicoList = TypeAdapter(List[CursoTecnicoSchema])
