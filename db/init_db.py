from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    saldo = Column(Numeric(10, 2), nullable=False)


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)


class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    data = Column(DateTime(timezone=True), server_default=func.now())

def criar_banco():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def popular_dados():
    Session = sessionmaker(bind=engine)
    session = Session()

    clientes = [
        Cliente(nome="João Silva", email="joao@email.com", saldo=2500.00),
        Cliente(nome="Maria Oliveira", email="maria@email.com", saldo=3500.00),
        Cliente(nome="Carlos Lima", email="carlos@email.com", saldo=1200.00),
        Cliente(nome="Ana Costa", email="ana@email.com", saldo=4200.00),
        Cliente(nome="Pedro Santos", email="pedro@email.com", saldo=1800.00),
        Cliente(nome="Luiza Ferreira", email="luiza@email.com", saldo=3100.00),
        Cliente(nome="Ricardo Alves", email="ricardo@email.com", saldo=2700.00),
        Cliente(nome="Fernanda Rocha", email="fernanda@email.com", saldo=1950.00),
        Cliente(nome="Gabriel Martins", email="gabriel@email.com", saldo=3800.00),
        Cliente(nome="Juliana Pereira", email="juliana@email.com", saldo=2200.00),
        Cliente(nome="Marcos Andrade", email="marcos@email.com", saldo=1600.00),
        Cliente(nome="Beatriz Lopes", email="beatriz@email.com", saldo=4500.00),
        Cliente(nome="Thiago Sousa", email="thiago@email.com", saldo=2900.00),
        Cliente(nome="Camila Barbosa", email="camila@email.com", saldo=3300.00),
        Cliente(nome="Rafael Dias", email="rafael@email.com", saldo=2100.00),
    ]

    produtos = [
        Produto(nome="notebook", preco=2200.00),
        Produto(nome="smartphone", preco=1800.00),
        Produto(nome="fone de ouvido", preco=200.00),
        Produto(nome="monitor", preco=800.00),
        Produto(nome="teclado mecânico", preco=350.00),
        Produto(nome="mouse gamer", preco=150.00),
        Produto(nome="ssd 1tb", preco=400.00),
        Produto(nome="placa de vídeo", preco=1500.00),
        Produto(nome="memória ram 16gb", preco=600.00),
        Produto(nome="webcam", preco=180.00),
        Produto(nome="impressora", preco=450.00),
        Produto(nome="tablet", preco=900.00),
        Produto(nome="carregador portátil", preco=120.00),
        Produto(nome="caixa de som", preco=250.00),
        Produto(nome="smartwatch", preco=700.00),
    ]

    session.add_all(clientes + produtos)
    session.commit()

    transacoes = [
        Transacao(cliente_id=1, produto_id=1),
        Transacao(cliente_id=1, produto_id=3),
        Transacao(cliente_id=2, produto_id=2),
        Transacao(cliente_id=3, produto_id=3),
        Transacao(cliente_id=2, produto_id=4),
        Transacao(cliente_id=4, produto_id=5),
        Transacao(cliente_id=5, produto_id=6),
        Transacao(cliente_id=6, produto_id=7),
        Transacao(cliente_id=7, produto_id=8),
        Transacao(cliente_id=8, produto_id=9),
        Transacao(cliente_id=9, produto_id=10),
        Transacao(cliente_id=10, produto_id=11),
        Transacao(cliente_id=11, produto_id=12),
        Transacao(cliente_id=12, produto_id=13),
        Transacao(cliente_id=13, produto_id=14),
        Transacao(cliente_id=14, produto_id=15),
        Transacao(cliente_id=15, produto_id=1),
        Transacao(cliente_id=1, produto_id=5),
        Transacao(cliente_id=3, produto_id=8),
        Transacao(cliente_id=5, produto_id=12),
    ]

    session.add_all(transacoes)
    session.commit()
    session.close()
    print("Dados inseridos com sucesso.")

if __name__ == "__main__":
    criar_banco()
    popular_dados()
