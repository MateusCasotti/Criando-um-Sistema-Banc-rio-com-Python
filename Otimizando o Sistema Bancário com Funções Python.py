import textwrap

# 🎯 Variáveis principais
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []

# Usuário ADMIN
usuarios.append({
    "nome": "ADMIN",
    "cpf": "00000000000",
    "nascimento": "",
    "endereco": "",
    "senha": "admn"
})

def menu_acesso():
    print("\n🔐 === MENU DE ACESSO ===")
    cpf = input("CPF: ").replace(".", "").replace("-", "")
    senha = input("Senha: ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            print(f"✅ Bem-vindo(a), {usuario['nome']}!")
            return usuario

    print("❌ CPF ou senha incorretos.")
    return None

def alterar_senha(usuario):
    print("\n🔐 === ALTERAR SENHA ===")
    senha_atual = input("Senha atual: ")
    if senha_atual == usuario["senha"]:
        nova_senha = input("Nova senha: ")
        usuario["senha"] = nova_senha
        print("✅ Senha alterada com sucesso!")
    else:
        print("❌ Senha atual incorreta.")

def criar_usuario():
    print("\n👤 === CRIAR USUÁRIO ===")
    cpf = input("CPF (somente números): ")
    if any(u["cpf"] == cpf for u in usuarios):
        print("⚠️ CPF já cadastrado!")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    senha = cpf[:5]

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "endereco": endereco,
        "senha": senha
    })
    print(f"✅ Usuário criado com sucesso! Senha padrão: {senha}")

def criar_conta(usuario):
    numero_conta = len(contas) + 1
    conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print(f"✅ Conta criada com sucesso! Agência: 0001 | Número: {numero_conta:04d}")

def listar_contas():
    print("\n📋 === LISTA DE CONTAS ===")
    for conta in contas:
        usuario = conta["usuario"]
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']:04d} | Titular: {usuario['nome']} (CPF: {usuario['cpf']})")

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("❌ Operação cancelada! Saldo insuficiente.")
    elif excedeu_limite:
        print(f"❌ Limite excedido! Saques até R$ {limite:.2f}.")
    elif excedeu_saques:
        print("❌ Limite de saques diários atingido (3).")
    elif valor > 0:
        saldo -= valor
        extrato += f"📤 Saque:    R$ {valor:.2f}\n"
        numero_saques += 1
        print("✅ Saque realizado com sucesso!")
    else:
        print("⚠️ Valor inválido! Digite um valor positivo.")

    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"📥 Depósito: R$ {valor:.2f}\n"
        print("✅ Depósito realizado com sucesso!")
    else:
        print("⚠️ Valor inválido! Digite um valor positivo.")
    return saldo, extrato

def exibir_extrato(saldo, *, extrato):
    print("\n📄 ===== EXTRATO =====")
    print(extrato if extrato else "📭 Não foram realizadas movimentações.")
    print(f"\n💰 Saldo atual: R$ {saldo:.2f}")
    print("========================\n")

# 🌐 Acesso ao sistema
usuario_logado = None
while not usuario_logado:
    print("\n💼 Acesse sua conta")
    print("[1] Login")
    print("[2] Criar usuário")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        usuario_logado = menu_acesso()
    elif escolha == "2":
        criar_usuario()
    else:
        print("❌ Opção inválida!")
