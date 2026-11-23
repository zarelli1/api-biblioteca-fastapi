import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositorio import RepositorioLivros
from app.rotas import obter_servico
from app.servico import ServicoLivros

cliente = TestClient(app)


def test_listar_retorna_200_e_ao_menos_cinco_livros() -> None:
    resposta = cliente.get("/livros")
    assert resposta.status_code == 200
    assert len(resposta.json()) >= 5


def test_listar_acervo_vazio_retorna_lista_vazia() -> None:
    app.dependency_overrides[obter_servico] = lambda: ServicoLivros(RepositorioLivros([]))
    try:
        resposta = cliente.get("/livros")
    finally:
        app.dependency_overrides.clear()
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_buscar_livro_existente_retorna_200() -> None:
    resposta = cliente.get("/livros/1")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert set(corpo) == {"id", "titulo", "autor", "ano_publicacao", "disponivel"}


def test_buscar_livro_inexistente_retorna_404() -> None:
    resposta = cliente.get("/livros/999")
    assert resposta.status_code == 404


@pytest.mark.parametrize("identificador", ["0", "-1", "abc"])
def test_identificador_invalido_retorna_422(identificador: str) -> None:
    resposta = cliente.get(f"/livros/{identificador}")
    assert resposta.status_code == 422
