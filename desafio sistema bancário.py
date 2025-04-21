import textwrap
from abc import ABC, abstractmethod
from datetime import date

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor <= 0 or valor > self.saldo:
            print("\n@@@ Saque inválido ou saldo insuficiente. @@@")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Depósito inválido. @@@")
            return False

        self.saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if valor > self.limite:
            print("\n@@@ Valor excede o limite de saque. @@@")
            return False

        if self.saques_realizados >= self.limite_saques:
            print("\n@@@ Limite de saques diários excedido. @@@")
            return False

        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": date.today().strftime("%d-%m-%Y")
        })


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f} em {transacao['data']}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    data_nasc = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append(PessoaFisica(nome, cpf, data_nasc, endereco))
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    for u in usuarios:
        if isinstance(u, PessoaFisica) and u.cpf == cpf:
            return u
    return None


def criar_conta(numero_conta, usuarios):
    cpf = input("CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return

    conta = ContaCorrente(numero_conta, usuario)
    usuario.adicionar_conta(conta)
    print("=== Conta criada com sucesso! ===")
    return conta


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(f"Agência: {conta.agencia} | C/C: {conta.numero} | Titular: {conta.cliente.nome}")


def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao in ["d", "s", "e"]:
            cpf = input("CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if not usuario:
                print("\n@@@ Usuário não encontrado! @@@")
                continue

            if not usuario.contas:
                print("\n@@@ Usuário não possui contas. @@@")
                continue

            conta = usuario.contas[0]  # Simplesmente pega a primeira conta

            if opcao == "d":
                valor = float(input("Valor do depósito: "))
                transacao = Deposito(valor)

            elif opcao == "s":
                valor = float(input("Valor do saque: "))
                transacao = Saque(valor)

            elif opcao == "e":
                exibir_extrato(conta)
                continue

            usuario.realizar_transacao(conta, transacao)

        elif opcao == "q":
            break

        else:
            print("@@@ Opção inválida. Tente novamente. @@@")


main()
