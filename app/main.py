"""Ponto de entrada da aplicação FastAPI."""

from fastapi import FastAPI

from app.rotas import router

app = FastAPI(
    title="API do Acervo da Biblioteca",
    description="Consulta ao acervo de livros (Atividade 4 - Arquitetura de Software).",
    version="1.0.0",
)

app.include_router(router)
