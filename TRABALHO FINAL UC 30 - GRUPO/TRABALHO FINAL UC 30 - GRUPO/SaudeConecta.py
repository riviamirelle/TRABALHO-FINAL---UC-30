"""
Sistema da Clínica Social SaudeConecta
Médicos voluntários atendem pessoas de baixa renda.
Implementa:
- Cadastro de médicos (com CRM)
- Cadastro de pacientes (com prioridade e cor da pulseira)
- Listagem de atendimentos
- Busca de paciente por nome
- Validações de dados
- Relação com ODS 3 (Saúde e Bem-Estar)
- Acessibilidade: textos claros, uso de upper() para evitar erro de digitação
"""

# Constantes para validação
ESPECIALIDADES_VALIDAS = ["clinico geral", "pediatria", "ginecologista", "odontologia", "dermatologista", "psicologia"]
CORES_PULSEIRA = ["normal", "medio", "grave"]
PREFERENCIAL_VALIDO = ["idoso", "adulto", "crianca"]

# Listas para armazenar os dados
medicos = []        # Cada médico será um dicionário
pacientes = []      # Cada paciente será um dicionário
atendimentos = []   # Relaciona médico + paciente + data

# ==================== FUNÇÕES DE VALIDAÇÃO ====================

def validar_crm(crm):
    """Valida se o CRM é um número inteiro positivo"""
    if crm.isdigit() and int(crm) > 0:
        return True
    return False

def validar_data(data):
    """Validação simples de data no formato DD/MM/AAAA"""
    partes = data.split("/")
    if len(partes) != 3:
        return False
    dia, mes, ano = partes
    if dia.isdigit() and mes.isdigit() and ano.isdigit():
        if 1 <= int(dia) <= 31 and 1 <= int(mes) <= 12 and int(ano) > 1900:
            return True
    return False

def validar_nome(nome):
    """Valida se o nome não está vazio e tem pelo menos 3 caracteres"""
    return nome.strip() != "" and len(nome.strip()) >= 3

# ==================== FUNÇÕES PRINCIPAIS ====================

def cadastrar_medico():
    """Cadastra um médico voluntário"""
    print("\n--- Cadastro de Médico Voluntário ---")
    nome = input("Nome do médico: ").strip()
    while not validar_nome(nome):
        print("Nome inválido (mínimo 3 caracteres).")
        nome = input("Nome do médico: ").strip()
    
    especialidade = input("Especialidade (clinico geral, pediatria, ginecologista, odontologia, dermatologista, psicologia): ").strip().lower()
    while especialidade not in ESPECIALIDADES_VALIDAS:
        print("Especialidade inválida. Opções: " + ", ".join(ESPECIALIDADES_VALIDAS))
        especialidade = input("Especialidade: ").strip().lower()
    
    crm = input("CRM (apenas números): ").strip()
    while not validar_crm(crm):
        print("CRM inválido (apenas números positivos).")
        crm = input("CRM: ").strip()
    
    medico = {
        "nome": nome,
        "especialidade": especialidade,
        "crm": crm
    }
    medicos.append(medico)
    print(f"Médico {nome} cadastrado com sucesso!")

def cadastrar_atendimento():
    """Cadastra um paciente que será atendido (baseado no fluxograma)"""
    print("\n--- Cadastro de Atendimento (Paciente) ---")
    
    # Nome do paciente
    nome_paciente = input("Nome do paciente: ").strip()
    while not validar_nome(nome_paciente):
        print("Nome inválido (mínimo 3 caracteres).")
        nome_paciente = input("Nome do paciente: ").strip()
    
    # Tipo de atendimento (especialidade desejada)
    print("Especialidades disponíveis: " + ", ".join(ESPECIALIDADES_VALIDAS))
    tipo = input("Tipo de atendimento (especialidade desejada): ").strip().lower()
    while tipo not in ESPECIALIDADES_VALIDAS:
        print("Especialidade inválida.")
        tipo = input("Tipo de atendimento: ").strip().lower()
    
    # Data do atendimento
    data = input("Data do atendimento (DD/MM/AAAA): ").strip()
    while not validar_data(data):
        print("Data inválida. Use o formato DD/MM/AAAA.")
        data = input("Data do atendimento: ").strip()
    
    # Profissional (médico) - listar médicos disponíveis com aquela especialidade
    medicos_disponiveis = [m for m in medicos if m["especialidade"] == tipo]
    if not medicos_disponiveis:
        print(f"Nenhum médico disponível para a especialidade {tipo}. Cadastre um médico primeiro.")
        return
    
    print("\nMédicos disponíveis para esta especialidade:")
    for i, m in enumerate(medicos_disponiveis):
        print(f"{i+1} - {m['nome']} (CRM: {m['crm']})")
    
    escolha = input("Escolha o médico (número): ").strip()
    while not (escolha.isdigit() and 1 <= int(escolha) <= len(medicos_disponiveis)):
        print("Opção inválida.")
        escolha = input("Escolha o médico (número): ").strip()
    
    medico_escolhido = medicos_disponiveis[int(escolha)-1]
    
    # DADOS ADICIONAIS DO PACIENTE (cor da pulseira e preferencial)
    print("\n--- Classificação do Paciente ---")
    cor_pulseira = input("Cor da pulseira (normal, medio, grave): ").strip().lower()
    while cor_pulseira not in CORES_PULSEIRA:
        print("Opção inválida. Use: normal, medio, grave")
        cor_pulseira = input("Cor da pulseira: ").strip().lower()
    
    preferencial = input("Preferencial (idoso, adulto, crianca): ").strip().lower()
    while preferencial not in PREFERENCIAL_VALIDO:
        print("Opção inválida. Use: idoso, adulto, crianca")
        preferencial = input("Preferencial: ").strip().lower()
    
    # Criar dicionário do paciente
    paciente = {
        "nome": nome_paciente,
        "tipo_atendimento": tipo,
        "data": data,
        "profissional": medico_escolhido["nome"],
        "crm_medico": medico_escolhido["crm"],
        "cor_pulseira": cor_pulseira,
        "preferencial": preferencial
    }
    pacientes.append(paciente)
    atendimentos.append(paciente)  # para manter compatibilidade com fluxograma
    
    print(f"\nAtendimento cadastrado com sucesso!\nPaciente: {nome_paciente} | Pulseira: {cor_pulseira} | Preferencial: {preferencial}")

def listar_atendimentos():
    """Lista todos os atendimentos cadastrados"""
    print("\n--- Lista de Atendimentos ---")
    if not atendimentos:
        print("Nenhum atendimento cadastrado.")
    else:
        for i, at in enumerate(atendimentos, 1):
            print(f"{i}. Paciente: {at['nome']} | Especialidade: {at['tipo_atendimento']} | Data: {at['data']} | Médico: {at['profissional']} | Pulseira: {at['cor_pulseira']} | Preferencial: {at['preferencial']}")
    input("\nPressione Enter para voltar ao menu...")

def buscar_paciente():
    """Busca paciente pelo nome"""
    print("\n--- Buscar Paciente ---")
    nome_busca = input("Digite o nome do paciente: ").strip().lower()
    encontrados = [p for p in pacientes if nome_busca in p['nome'].lower()]
    
    if not encontrados:
        print("Paciente não encontrado.")
    else:
        print(f"\nEncontrado(s) {len(encontrados)} paciente(s):")
        for p in encontrados:
            print(f"Nome: {p['nome']} | Data: {p['data']} | Médico: {p['profissional']} | Pulseira: {p['cor_pulseira']} | Preferencial: {p['preferencial']}")
    input("\nPressione Enter para voltar ao menu...")

def mostrar_menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("        CLÍNICA SAUDECONECTA")
    print("        Médicos Voluntários - Atendimento Social")
    print("="*50)
    print("1 - Cadastrar Médico")
    print("2 - Cadastrar Atendimento (Paciente)")
    print("3 - Listar Atendimentos")
    print("4 - Buscar Paciente")
    print("5 - Sair")
    print("="*50)

# ==================== PROGRAMA PRINCIPAL ====================

def main():
    print("Bem-vindo ao sistema da Clínica SaudeConecta!")
    print("Relação com ODS 3 (Saúde e Bem-Estar): Promovendo acesso gratuito à saúde para pessoas de baixa renda.")
    print("Acessibilidade: Textos claros e validação de dados para evitar erros.")
    
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_medico()
        elif opcao == "2":
            if not medicos:
                print("\nÉ necessário cadastrar pelo menos um médico antes de cadastrar um atendimento.")
                continue
            cadastrar_atendimento()
        elif opcao == "3":
            listar_atendimentos()
        elif opcao == "4":
            buscar_paciente()
        elif opcao == "5":
            print("\nEncerrando o sistema. Obrigado por usar o SaudeConecta!")
            break
        else:
            print("\nOpção inválida. Digite um número de 1 a 5.")

# Execução do programa
if __name__ == "__main__":
    main()