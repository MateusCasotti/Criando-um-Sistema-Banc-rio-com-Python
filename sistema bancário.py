# 🎯 Variáveis principais
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# 🚀 Início do menu interativo
while True:
    print("""
╔════════════════════════════╗
║      🏦 MENU BANCÁRIO      ║
╠════════════════════════════╣
║ [d] 💰 Depositar           ║
║ [s] 💸 Sacar               ║
║ [e] 📄 Extrato             ║
║ [q] ❌ Sair                ║
╚════════════════════════════╝
    """)
    opcao = input("👉 Escolha uma opção: ").lower()

    if opcao == "d":
        valor = float(input("🔢 Valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato += f"📥 Depósito: R$ {valor:.2f}\n"
            print("✅ Depósito realizado com sucesso!")
        else:
            print("⚠️ Valor inválido! Digite um valor positivo.")

    elif opcao == "s":
        valor = float(input("🔢 Valor do saque: R$ "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

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

    elif opcao == "e":
        print("\n📄 ===== EXTRATO =====")
        print(extrato if extrato else "📭 Não foram realizadas movimentações.")
        print(f"\n💰 Saldo atual: R$ {saldo:.2f}")
        print("========================\n")

    elif opcao == "q":
        print("👋 Saindo do sistema... Até logo!")
        break

    else:
        print("❌ Opção inválida! Tente novamente.")
