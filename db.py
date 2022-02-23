from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

NOME_BANCO = "banco"

engine = create_engine(f"sqlite:///./{NOME_BANCO}.sqlite", echo=True)
Base = declarative_base()

# Declaracao das classes
class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    def __repr__(self):
        return f"Cliente {self.nome}"


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"))
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Produto {self.nome}"


class Carrinho(Base):
    __tablename__ = "carrinho"
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produto.id"))


class Troca(Base):

    __tablename__ = "troca"

    id = Column(Integer, primary_key=True)
    de_cliente = Column(Integer, ForeignKey("cliente.id"))
    para_cliente = Column(Integer, ForeignKey("cliente.id"))


# fim da declaracao
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()