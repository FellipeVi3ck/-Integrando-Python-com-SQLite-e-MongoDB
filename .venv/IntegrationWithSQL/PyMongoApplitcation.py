import sqlalchemy

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()

class Client(Base):
    __tablename__ = "client_account"
    id = Column(Integer, primary_key=True)
    nome = Column(String(15))
    cpf = Column(String(9))
    endereço = Column(String(15))

    account_type = relationship("Conta", back_populates="client_account")\

    def __repr__(self):
        return f"Client(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereço={self.endereço})"


class Conta(Base):
    __tablename__ = "account_type"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    saldo = Column(Float)
    id_cliente = Column(Integer, ForeignKey("client_account.id"), nullable=False)

    client_account = relationship("Client", back_populates="account_type")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


#conexão com o banco de dados
engine = create_engine("sqlite://")

#criando classes como tabelas no banco de dados
Base.metadata.create_all(engine)

#interface para obter informações sobre um banco de dados existente
insp = inspect(engine)

#Retorna se o valor inserido existe ou não como tabela
print(insp.has_table("client_account"))

#Retorna o nome das tebelas(class) criadas
print(insp.get_table_names())

with (Session(engine) as session):
    Fellipe = Client(
        nome = 'Fellipe',
        cpf = '156.456.546-00',
        endereço = 'Rua das Bananeiras, 888',
        account_type = [Conta(tipo='Conta Corrente', agencia='6868', num='12345-6', saldo=0.0)]
    )

    Diego = Client(
        nome = 'Diego',
        cpf = '101.466.344-78',
        endereço = 'Rua das Maças, 999',
        account_type = [Conta(tipo='Conta Corrente', agencia='7565', num='84622-8', saldo=0.0)]
    )

    Nalanda = Client(
        nome = 'Nalanda',
        cpf = '127.676.656-14',
        endereço = 'Rua das Rosas, 22',
        account_type=[Conta(tipo='Conta Corrente', agencia='4556', num='54321-0', saldo=0.0)]
    )

    #enviando para o banco de dados(Persistência de dados)
    session.add_all([Fellipe, Diego, Nalanda])

    session.commit()

stmt = select(Client).where(Client.nome.in_(["Fellipe","Nalanda"]))
print("\nRecuperando usuários a partir de uma condição de filtragem")
for client_account in session.scalars(stmt):
    print(client_account)

# Aqui esta retornando apenas o email do usuario na posição 2, assim como solicitado abaixo
stmt_agencia = select(Conta.agencia).join_from(Conta, Client).where(Client.nome == "Diego")

print("\nRecuperando a agência de Diego")
for agencia in session.scalars(stmt_agencia):
    print(agencia)

stmt_ordenar = select(Client).order_by(Client.cpf.desc())
print("\nRecuperando informações de maneira ordenada")
for result in session.scalars(stmt_ordenar):
    print(result)

stmt_join = select(Client.cpf, Conta.agencia).join_from(Conta, Client)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

print("\n",select(Client.cpf, Conta.agencia).join_from(Conta, Client))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count("*")).select_from(Client)
print("\nTotal de instâncias em Client")
for result in session.scalars(stmt_count):
    print(result)