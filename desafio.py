menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input('\nDigite o valor do depósito: '))
        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f}\n'
        else:
            print("O valor informado é menor ou igual a zero, falha na operação de depósito")
    elif opcao == "s":
        valor = float(input('\nDigite o valor do saque: '))
        if numero_saques>=LIMITE_SAQUES:
            print('\n Excedeu o limite de 3 saques diários')
            continue
        if valor>LIMITE:
            print('\nValor excede o limite de R$ 500 reais por saque')
            continue
        if valor <= saldo and valor>0:
            saldo -= valor
            numero_saques += 1
            extrato += f'Saque: R$ {valor:.2f}\n'
        else:
            print("O valor informado não pode ser sacado (maior que o saldo ou igual/menor que zero), falha na operaçdão de saque")
    elif opcao == "e":
        print(f'EXTRATRO BANCÁRIO: \n\n   SALDO:{saldo}\n\n OPERAÇÕES: \n{extrato}')
    elif opcao == "q":
        break
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
    