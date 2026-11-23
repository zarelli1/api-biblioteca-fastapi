# 10482522284 - Leonardo Zarelli - API do Acervo da Biblioteca

Atividade 4 de Arquitetura de Software (Unoeste EAD): API em Python e FastAPI para consultar o acervo de uma biblioteca.

## Como executar

Na pasta do projeto:

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate.bat          # Windows
source .venv/bin/activate           # Linux ou Mac

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Subir a API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Documentação interativa: http://127.0.0.1:8001/docs

## Rotas

| Método | Rota | Resposta |
|---|---|---|
| GET | `/livros` | 200 e lista de livros (lista vazia se o acervo estiver vazio) |
| GET | `/livros/{livro_id}` | 200 livro encontrado, 404 sem livro com esse id, 422 id inválido (zero, negativo ou texto) |

Exemplos:

```bash
curl http://127.0.0.1:8001/livros
curl http://127.0.0.1:8001/livros/1      # 200
curl http://127.0.0.1:8001/livros/999    # 404
curl http://127.0.0.1:8001/livros/0      # 422
curl http://127.0.0.1:8001/livros/abc    # 422
```

## Organização do código

```
app/
  main.py         cria a aplicação FastAPI
  rotas.py        camada da API: rotas, validação do id e conversão da exceção em 404
  servico.py      regras de consulta do acervo
  repositorio.py  único acesso à coleção de livros em memória (5 livros de exemplo)
  modelos.py      modelo Livro com validação dos campos (Pydantic)
  excecoes.py     LivroNaoEncontradoError
tests/
  test_api.py     testes de 200, 404, 422 e acervo vazio
```

Fluxo de uma consulta: `rotas` chama `servico`, que chama `repositorio`. Se o livro não existe, o repositório lança `LivroNaoEncontradoError`, que não conhece HTTP. Só a camada `rotas` a converte em `404`.

## Validações

- `id` e `ano_publicacao`: inteiros maiores que zero.
- `titulo` e `autor`: texto não vazio (espaços nas pontas são removidos antes da checagem).
- `livro_id` na URL: `int` com `gt=0`, o que gera 422 automaticamente para zero, negativos e texto.

## Testes

```bash
python -m pytest
```
