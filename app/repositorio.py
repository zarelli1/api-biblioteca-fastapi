"""Repositório de livros: único lugar que conhece a coleção em memória.

Se amanhã o acervo vier de um banco de dados, só este arquivo muda.
"""

from app.excecoes import LivroNaoEncontradoError
from app.modelos import Livro


class RepositorioLivros:
    def __init__(self, livros: list[Livro] | None = None) -> None:
        # Aceitar a lista por parâmetro facilita os testes (inclusive acervo vazio).
        self._livros: list[Livro] = list(livros) if livros is not None else []

    def listar(self) -> list[Livro]:
        """Retorna todos os livros (lista vazia se o acervo estiver vazio)."""
        return list(self._livros)

    def buscar_por_id(self, livro_id: int) -> Livro:
        """Retorna o livro do id informado ou lança LivroNaoEncontradoError."""
        for livro in self._livros:
            if livro.id == livro_id:
                return livro
        raise LivroNaoEncontradoError(livro_id)


def criar_acervo_inicial() -> RepositorioLivros:
    """Monta o repositório com o acervo de exemplo (5 livros em memória)."""
    return RepositorioLivros(
        [
            Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis", ano_publicacao=1899, disponivel=True),
            Livro(id=2, titulo="Memórias Póstumas de Brás Cubas", autor="Machado de Assis", ano_publicacao=1881, disponivel=False),
            Livro(id=3, titulo="O Cortiço", autor="Aluísio Azevedo", ano_publicacao=1890, disponivel=True),
            Livro(id=4, titulo="Grande Sertão: Veredas", autor="João Guimarães Rosa", ano_publicacao=1956, disponivel=True),
            Livro(id=5, titulo="Capitães da Areia", autor="Jorge Amado", ano_publicacao=1937, disponivel=False),
        ]
    )
