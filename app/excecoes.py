"""Exceções de domínio da biblioteca.

Ficam separadas da API de propósito: o repositório e o serviço não sabem
nada de HTTP. Quem traduz a exceção para um status code é a camada da API.
"""


class LivroNaoEncontradoError(Exception):
    """Lançada quando não existe livro com o identificador informado."""

    def __init__(self, livro_id: int) -> None:
        self.livro_id = livro_id
        super().__init__(f"Livro com id {livro_id} não encontrado.")
