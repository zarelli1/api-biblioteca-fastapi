"""Modelo de dados do livro.

O mesmo modelo é usado para validar os dados do acervo e para descrever
a resposta das rotas (response_model), o que também alimenta o /docs.
"""

from pydantic import BaseModel, ConfigDict, Field


class Livro(BaseModel):
    # Remove espaços nas pontas antes de validar: "   " vira "" e é rejeitado
    # pelo min_length=1, garantindo que título e autor não sejam vazios.
    model_config = ConfigDict(str_strip_whitespace=True)

    id: int = Field(gt=0, description="Identificador do livro (maior que zero)")
    titulo: str = Field(min_length=1, description="Título do livro")
    autor: str = Field(min_length=1, description="Autor do livro")
    ano_publicacao: int = Field(gt=0, description="Ano de publicação (maior que zero)")
    disponivel: bool = Field(description="Indica se está disponível para empréstimo")
