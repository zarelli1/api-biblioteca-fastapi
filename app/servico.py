"""Serviço de livros: regras de consulta do acervo.

Recebe o repositório por construtor (inversão de dependência), então não
depende de onde os dados são guardados nem de nada relacionado a HTTP.
"""

from app.modelos import Livro
from app.repositorio import RepositorioLivros


class ServicoLivros:
    def __init__(self, repositorio: RepositorioLivros) -> None:
        self._repositorio = repositorio

    def listar_livros(self) -> list[Livro]:
        return self._repositorio.listar()

    def obter_livro(self, livro_id: int) -> Livro:
        # A LivroNaoEncontradoError sobe daqui até a camada da API.
        return self._repositorio.buscar_por_id(livro_id)
