"""Camada da API: rotas HTTP.

Responsabilidade: receber a requisição, validar parâmetros, chamar o serviço
e traduzir exceções de domínio em códigos HTTP. Não acessa a lista de livros.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.excecoes import LivroNaoEncontradoError
from app.modelos import Livro
from app.repositorio import criar_acervo_inicial
from app.servico import ServicoLivros

router = APIRouter(prefix="/livros", tags=["Livros"])

# Uma única instância do repositório vive enquanto a aplicação estiver de pé;
# sem isso cada requisição enxergaria um acervo novo.
_repositorio = criar_acervo_inicial()


def obter_servico() -> ServicoLivros:
    """Dependência do FastAPI. Nos testes pode ser trocada via dependency_overrides."""
    return ServicoLivros(_repositorio)


@router.get("", response_model=list[Livro], summary="Listar o acervo")
def listar_livros(servico: ServicoLivros = Depends(obter_servico)) -> list[Livro]:
    """Retorna 200 e a lista de livros (lista vazia se não houver nenhum)."""
    return servico.listar_livros()


@router.get(
    "/{livro_id}",
    response_model=Livro,
    summary="Consultar livro por identificador",
    responses={404: {"description": "Livro não encontrado"}},
)
def obter_livro(
    # gt=0 recusa zero e negativos; o tipo int recusa texto. Ambos geram 422
    # automaticamente, antes de a função rodar.
    livro_id: int = Path(gt=0, description="Identificador do livro (inteiro maior que zero)"),
    servico: ServicoLivros = Depends(obter_servico),
) -> Livro:
    try:
        return servico.obter_livro(livro_id)
    except LivroNaoEncontradoError as erro:
        # Id válido, mas sem livro: a exceção de domínio vira 404 aqui, na API.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
