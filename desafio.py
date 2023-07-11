# No código não há validação dos valores de CPF, endereço e etc

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques>=limite_saques:
        print('\n Excedeu o limite de 3 saques diários')
    if valor>limite:
        print('\nValor excede o limite de R$ 500 reais por saque')
    if valor <= saldo and valor>0:
        saldo -= valor
        numero_saques += 1
        extrato += f'Saque: R$ {valor:.2f}\n'
    else:
        print("O valor informado não pode ser sacado (maior que o saldo ou igual/menor que zero), falha na operaçdão de saque")
    return  extrato, saldo, numero_saques

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
    else:
        print("O valor informado é menor ou igual a zero, falha na operação de depósito")
    return extrato, saldo
     
def menu_nao_logado():
    return """
        [u] Cadastrar usuário
        [lu] Listar usuários
        [c] Cadastrar conta
        [lc] Listar contas de um usuário
        [e] Entrar na conta
        [s] Sair do aplicativo
    =>"""

def menu_logado():
     
    return  """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair da conta

    => """

def cadastrar_usuario(usuarios):
    cpf = input('Informe seu CPF(somente os números) \n=>')
    nome = input('Informe seu nome completo\n=>')
    data_nascimento = input('Informe sua data de nascimento (dd-mm-aaaa)\n=>')
    endereco = input('Informe seu endereço (logradouro, nr - bairro - cidade/sigla estado) \n=>')
    usuario = {'dados':{'cpf':cpf,'nome':nome,'data_nascimento':data_nascimento,'endereco':endereco}}
    if usuario['dados']['cpf'] in usuarios:
        print('CPF já cadastrado, operação anulada, selecione novamente a opção desejada\n')
    else:
        usuarios.append(usuario)
    return usuarios

def filtrar_usuario_por_cpf(cpf, usuarios):
    for usuario in usuarios:
        if usuario['dados']['cpf'] == cpf:
            return usuario
    return 0
            
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario_por_cpf(cpf=cpf, usuarios=usuarios)
    if usuario == 0:
        print('Usuário não encontrado, cadastre-o e tente novamente\n')
        return 0
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario":usuario['dados']['cpf'], 'saldo':0, 'saques':0, 'extrato': ''}

def listar_usuarios(usuarios):
    string_return = ''
    print("LISTA DE USUÁRIOS:\n")
    for id, usuario in enumerate(usuarios):
                    string_return += (f"""USUÁRIO {id}:\n 
                           \nNome: {usuario['dados']['nome']}
                           \nCPF: {usuario['dados']['cpf']}
                           \nData de nascimento: {usuario['dados']['data_nascimento']}
                           \nEndereco: {usuario['dados']['endereco']}\n"""
                          )
    if string_return == '':
        string_return = 'Nenhum usuário cadastrado\n'
    return string_return

def entrar_na_conta(conta_desejada, contas):
    resultado = 'Não encontrado'
    for id, conta in enumerate(contas):
        if conta['numero_conta'] == int(conta_desejada):
            resultado = 'Encontrado'
            return id, resultado
    return None, resultado
def listar_contas_cpf(cpf, contas):
    print(f'\nContas do usuário com CPF {cpf}:\n')
    string_return = ''
    for conta in contas:
        if conta['usuario'] == cpf:
            string_return += f"""ID CONTA:{conta['numero_conta']}\nAGENCIA:{conta['agencia']}\nSALDO:{conta['saldo']}\nSAQUES DISPONÍVEIS:{3-conta['saques']}\nEXTRATO: {conta['extrato']}"""
    if string_return == '':
        string_return = 'Nenhuma conta identificada para o usuário\n'
    return string_return

def extrato(saldo, /, *, extrato):
    return f'EXTRATRO BANCÁRIO: \n\n   SALDO:{saldo}\n\n OPERAÇÕES: \n{extrato}'

def main():
    usuarios = []
    contas = []
    conta_atual = None
    LIMITE = 500
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    numero_conta = 1
    while True:
        if conta_atual == None :
            opcao = input(menu_nao_logado())
            if opcao == "u":
                # cadastro de usuários 
                usuarios = cadastrar_usuario(usuarios)
            elif opcao == "c":
                # criação de contas
                conta = criar_conta(agencia=AGENCIA,numero_conta=numero_conta, usuarios=usuarios)
                if conta != 0:
                    contas.append(conta)
                    numero_conta += 1
            elif opcao == "e":
                # login na conta
                conta_desejada = input('Digite o número da conta desejada\n=>')
                conta_atual, resultado = entrar_na_conta(conta_desejada, contas)
                if resultado == 'Não encontrado':
                    print('Conta não encontrada\n')
            elif opcao == "lc":
                # listar contas cadastradas em um CPF
                cpf = input('Digite o CPF do usuário que deseja ver as contas\n=>')
                print(listar_contas_cpf(cpf,contas))
            elif opcao == "lu":
                # listar todos os usuários cadastrados
                print(listar_usuarios(usuarios=usuarios))
            elif opcao == "s":
                break
            else:
                print('Operação inválida, por favor selecione novamente a operação desejada.')
        else:
            opcao = input(menu_logado())
            if opcao == "d":
                valor = float(input('Digite o valor do depósito\n=>'))
                contas[conta_atual]['extrato'], contas[conta_atual]['saldo'] = depositar(contas[conta_atual]['saldo'],valor,contas[conta_atual]['extrato'],)
            elif opcao == "s":
                valor = float(input('Digite o valor para sacar\n=>'))
                contas[conta_atual]['extrato'], contas[conta_atual]['saldo'], contas[conta_atual]['saques'] = saque(saldo=contas[conta_atual]['saldo'],
                                                                                                                    valor=valor,extrato=contas[conta_atual]['extrato'],
                                                                                                                    limite=LIMITE,
                                                                                                                    numero_saques=contas[conta_atual]['saques'],
                                                                                                                    limite_saques=LIMITE_SAQUES)
            elif opcao == "e":
                print(extrato(contas[conta_atual]['saldo'], extrato=contas[conta_atual]['extrato']))
            elif opcao == "q":
                conta_atual = None
            else:
                print('Operação inválida, por favor selecione novamente a operação desejada.')
        
if __name__ == '__main__':
     main()