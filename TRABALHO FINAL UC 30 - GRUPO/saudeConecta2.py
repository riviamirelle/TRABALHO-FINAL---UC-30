"""
Sistema da Clínica Social SaudeConecta
Médicos voluntários atendem pessoas de baixa renda.
Implementa:
- Cadastro de médicos (com CRM de 6 dígitos)
- Cadastro de pacientes (com prioridade e cor da pulseira colorida)
- Listagem de médicos disponíveis com Dr.(a) antes do nome
- Especialidades com seleção numérica
- Tipos de atendimento: normal, preferencial, infantil
- Validações de dados
- Relação com ODS 3 (Saúde e Bem-Estar)
- Acessibilidade: textos claros, uso de cores no terminal
"""

# Import para cores no terminal (funciona em Windows, Mac, Linux)
import sys
if sys.platform == "win32":
    import os
    os.system("color")  # Habilita cores no Windows

# Constantes para cores (ANSI escape codes)
class Cores:
    VERDE = '\033[92m'      # Verde - Normal
    AMARELO = '\033[93m'    # Amarelo - Grave
    VERMELHO = '\033[91m'   # Vermelho - Emergência
    RESET = '\033[0m'       # Reseta cor
    AZUL = '\033[94m'       # Azul para menus
    CIANO = '\033[96m'      # Ciano para destaques
    MAGENTA = '\033[95m'    # Magenta para títulos

# Constantes para validação
ESPECIALIDADES_VALIDAS = [
    "clinico geral", 
    "pediatria", 
    "ginecologista", 
    "odontologia", 
    "dermatologista", 
    "psicologia",
    "cardiologia",
    "neurologia",
    "ortopedia",
    "oftalmologia",
    "nutrologia",
    "fisioterapia"
]

# Mapeamento de cores das pulseiras
CORES_PULSEIRA = {
    "normal": Cores.VERDE + "VERDE (Normal)" + Cores.RESET,
    "grave": Cores.AMARELO + "AMARELO (Grave)" + Cores.RESET,
    "emergencia": Cores.VERMELHO + "VERMELHO (Emergência)" + Cores.RESET
}

# Opções de tipo de atendimento
TIPOS_ATENDIMENTO = {
    1: {"nome": "Atendimento Normal", "categorias": ["adulto"]},
    2: {"nome": "Atendimento Preferencial", "categorias": ["idoso", "gestante", "comorbidades"]},
    3: {"nome": "Atendimento Infantil", "categorias": ["crianca"]}
}

# Listas para armazenar os dados
medicos = []        # Cada médico será um dicionário
pacientes = []      # Cada paciente será um dicionário
atendimentos = []   # Relaciona médico + paciente + data

# ==================== FUNÇÕES DE VALIDAÇÃO ====================

def validar_crm(crm):
    """
    Valida se o CRM tem exatamente 6 dígitos numéricos
    Formato: XXXXXX (6 números)
    """
    # Remove espaços em branco
    crm = crm.strip()
    # Verifica se tem exatamente 6 caracteres e se todos são dígitos
    if len(crm) == 6 and crm.isdigit():
        return True
    return False

def formatar_crm(crm):
    """Formata o CRM para exibição com pontos (ex: 123456 -> 123.456)"""
    crm = crm.strip()
    if len(crm) == 6:
        return f"{crm[:3]}.{crm[3:]}"
    return crm

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

def formatar_nome_medico(nome, pronome="o"):
    """
    Formata o nome do médico com Dr.(a) baseado no gênero inferido
    pronome: "o" para masculino, "a" para feminino (padrão: neutro)
    """
    nome = nome.strip()
    # Tenta inferir gênero pelo último caractere do primeiro nome
    primeiro_nome = nome.split()[0] if nome.split() else nome
    if primeiro_nome.endswith('a'):
        return f"Dra. {nome}"
    elif primeiro_nome.endswith('o'):
        return f"Dr. {nome}"
    else:
        # Caso não consiga inferir, usa "Dr.(a)" como forma neutra
        return f"Dr.(a) {nome}"

def mostrar_especialidades():
    """Exibe a lista numerada de especialidades disponíveis"""
    print(f"\n{Cores.CIANO}Especialidades disponíveis:{Cores.RESET}")
    for i, esp in enumerate(ESPECIALIDADES_VALIDAS, 1):
        print(f"  {i} - {esp.title()}")
    return len(ESPECIALIDADES_VALIDAS)

def escolher_especialidade():
    """Permite ao usuário escolher uma especialidade pelo número"""
    total = mostrar_especialidades()
    while True:
        try:
            opcao = int(input(f"\nDigite o número da especialidade (1-{total}): "))
            if 1 <= opcao <= total:
                return ESPECIALIDADES_VALIDAS[opcao - 1]
            else:
                print(f"{Cores.VERMELHO}Opção inválida. Digite um número entre 1 e {total}.{Cores.RESET}")
        except ValueError:
            print(f"{Cores.VERMELHO}Entrada inválida. Digite um número.{Cores.RESET}")

def listar_medicos_disponiveis(especialidade=None):
    """
    Lista todos os médicos ou filtra por especialidade
    Exibe Dr.(a) antes do nome e CRM formatado com 6 dígitos
    Retorna a lista de médicos disponíveis
    """
    if especialidade:
        medicos_filtrados = [m for m in medicos if m["especialidade"] == especialidade]
    else:
        medicos_filtrados = medicos.copy()
    
    if not medicos_filtrados:
        if especialidade:
            print(f"\n{Cores.VERMELHO}❌ Nenhum médico disponível para a especialidade: {especialidade.title()}{Cores.RESET}")
        else:
            print(f"\n{Cores.AMARELO}⚠️ Nenhum médico cadastrado no sistema.{Cores.RESET}")
        return []
    
    print(f"\n{Cores.MAGENTA}{'='*55}{Cores.RESET}")
    print(f"{Cores.AZUL}========== MÉDICOS DISPONÍVEIS =========={Cores.RESET}")
    print(f"{Cores.MAGENTA}{'='*55}{Cores.RESET}")
    for i, m in enumerate(medicos_filtrados, 1):
        # Nome formatado com Dr.(a)
        nome_formatado = formatar_nome_medico(m['nome'])
        # CRM formatado (ex: 123456 -> 123.456)
        crm_formatado = formatar_crm(m['crm'])
        print(f"{i}. {nome_formatado}")
        print(f"   Especialidade: {m['especialidade'].title()}")
        print(f"   CRM: {crm_formatado}")
        print(f"{Cores.CIANO}{'-'*55}{Cores.RESET}")
    print(f"{Cores.MAGENTA}{'='*55}{Cores.RESET}")
    
    return medicos_filtrados

def escolher_cor_pulseira():
    """Exibe opções de cores das pulseiras com cores visuais"""
    print(f"\n{Cores.CIANO}Classificação da Pulseira por Gravidade:{Cores.RESET}")
    print(f"1 - {CORES_PULSEIRA['normal']}")
    print(f"2 - {CORES_PULSEIRA['grave']}")
    print(f"3 - {CORES_PULSEIRA['emergencia']}")
    
    while True:
        try:
            opcao = int(input("\nEscolha a cor da pulseira (1-3): "))
            if opcao == 1:
                return "normal", CORES_PULSEIRA["normal"]
            elif opcao == 2:
                return "grave", CORES_PULSEIRA["grave"]
            elif opcao == 3:
                return "emergencia", CORES_PULSEIRA["emergencia"]
            else:
                print(f"{Cores.VERMELHO}Opção inválida. Escolha 1, 2 ou 3.{Cores.RESET}")
        except ValueError:
            print(f"{Cores.VERMELHO}Entrada inválida. Digite um número.{Cores.RESET}")

def escolher_tipo_atendimento():
    """Exibe opções de tipo de atendimento e retorna a categoria"""
    print(f"\n{Cores.CIANO}Tipos de Atendimento:{Cores.RESET}")
    for num, tipo in TIPOS_ATENDIMENTO.items():
        print(f"{num} - {tipo['nome']} ({', '.join(tipo['categorias']).title()})")
    
    while True:
        try:
            opcao = int(input("\nEscolha o tipo de atendimento (1-3): "))
            if opcao in TIPOS_ATENDIMENTO:
                # Retorna a primeira categoria do tipo escolhido
                categoria = TIPOS_ATENDIMENTO[opcao]["categorias"][0]
                nome_tipo = TIPOS_ATENDIMENTO[opcao]["nome"]
                return categoria, nome_tipo
            else:
                print(f"{Cores.VERMELHO}Opção inválida. Escolha 1, 2 ou 3.{Cores.RESET}")
        except ValueError:
            print(f"{Cores.VERMELHO}Entrada inválida. Digite um número.{Cores.RESET}")

# ==================== FUNÇÕES PRINCIPAIS ====================

def cadastrar_medico():
    """Cadastra um médico voluntário com CRM de 6 dígitos"""
    print(f"\n{Cores.AZUL}{'='*50}{Cores.RESET}")
    print(f"{Cores.VERDE}--- Cadastro de Médico Voluntário ---{Cores.RESET}")
    print(f"{Cores.AZUL}{'='*50}{Cores.RESET}")
    
    nome = input("Nome completo do médico: ").strip()
    while not validar_nome(nome):
        print(f"{Cores.VERMELHO}Nome inválido (mínimo 3 caracteres).{Cores.RESET}")
        nome = input("Nome completo do médico: ").strip()
    
    # Usar o novo sistema de escolha numerada de especialidades
    especialidade = escolher_especialidade()
    
    print(f"\n{Cores.CIANO}O CRM deve ter exatamente 6 dígitos numéricos (ex: 123456){Cores.RESET}")
    crm = input("CRM (6 dígitos): ").strip()
    while not validar_crm(crm):
        print(f"{Cores.VERMELHO}CRM inválido! Deve ter exatamente 6 dígitos numéricos (ex: 123456).{Cores.RESET}")
        crm = input("CRM (6 dígitos): ").strip()
    
    medico = {
        "nome": nome,
        "especialidade": especialidade,
        "crm": crm,  # Armazena como string de 6 dígitos
        "nome_formatado": formatar_nome_medico(nome),  # Já formata para uso futuro
        "crm_formatado": formatar_crm(crm)
    }
    medicos.append(medico)
    
    print(f"\n{Cores.VERDE}{'='*50}{Cores.RESET}")
    print(f"{Cores.VERDE}✅ Médico cadastrado com sucesso!{Cores.RESET}")
    print(f"{Cores.CIANO}   {medico['nome_formatado']}{Cores.RESET}")
    print(f"{Cores.CIANO}   Especialidade: {medico['especialidade'].title()}{Cores.RESET}")
    print(f"{Cores.CIANO}   CRM: {medico['crm_formatado']}{Cores.RESET}")
    print(f"{Cores.VERDE}{'='*50}{Cores.RESET}")

def cadastrar_atendimento():
    """Cadastra um paciente que será atendido com verificação de médicos disponíveis"""
    print(f"\n{Cores.AZUL}{'='*50}{Cores.RESET}")
    print(f"{Cores.VERDE}--- Cadastro de Atendimento (Paciente) ---{Cores.RESET}")
    print(f"{Cores.AZUL}{'='*50}{Cores.RESET}")
    
    # Nome do paciente
    nome_paciente = input("Nome completo do paciente: ").strip()
    while not validar_nome(nome_paciente):
        print(f"{Cores.VERMELHO}Nome inválido (mínimo 3 caracteres).{Cores.RESET}")
        nome_paciente = input("Nome completo do paciente: ").strip()
    
    # Tipo de atendimento (criança, adulto, preferencial)
    categoria_preferencial, nome_tipo_atendimento = escolher_tipo_atendimento()
    
    # Escolher especialidade desejada (com números)
    print(f"\n{Cores.CIANO}Para o {nome_tipo_atendimento}, qual especialidade você precisa?{Cores.RESET}")
    especialidade_desejada = escolher_especialidade()
    
    # VERIFICAR SE EXISTE MÉDICO DISPONÍVEL COM ESSA ESPECIALIDADE
    print(f"\n{Cores.AZUL}Verificando médicos disponíveis para {especialidade_desejada.title()}...{Cores.RESET}")
    medicos_disponiveis = listar_medicos_disponiveis(especialidade_desejada)
    
    if not medicos_disponiveis:
        print(f"\n{Cores.VERMELHO}❌ Não há médicos disponíveis para a especialidade {especialidade_desejada.title()}.{Cores.RESET}")
        print(f"{Cores.AMARELO}Por favor, cadastre um médico com essa especialidade ou tente outra especialidade.{Cores.RESET}")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    # Escolher médico específico (já está listado com Dr.(a) e CRM formatado)
    print(f"\n{Cores.CIANO}Escolha o médico para o atendimento:{Cores.RESET}")
    for i, m in enumerate(medicos_disponiveis, 1):
        nome_formatado = formatar_nome_medico(m['nome'])
        crm_formatado = formatar_crm(m['crm'])
        print(f"{i} - {nome_formatado} (CRM: {crm_formatado}) - {m['especialidade'].title()}")
    
    escolha = input("\nDigite o número do médico: ").strip()
    while not (escolha.isdigit() and 1 <= int(escolha) <= len(medicos_disponiveis)):
        print(f"{Cores.VERMELHO}Opção inválida.{Cores.RESET}")
        escolha = input("Digite o número do médico: ").strip()
    
    medico_escolhido = medicos_disponiveis[int(escolha)-1]
    
    # Data do atendimento
    data = input("Data do atendimento (DD/MM/AAAA): ").strip()
    while not validar_data(data):
        print(f"{Cores.VERMELHO}Data inválida. Use o formato DD/MM/AAAA.{Cores.RESET}")
        data = input("Data do atendimento: ").strip()
    
    # Cor da pulseira com cores visuais
    cor_key, cor_exibida = escolher_cor_pulseira()
    
    # Criar dicionário do paciente
    paciente = {
        "nome": nome_paciente,
        "tipo_atendimento": nome_tipo_atendimento,
        "categoria_preferencial": categoria_preferencial,
        "especialidade": especialidade_desejada,
        "data": data,
        "profissional": medico_escolhido["nome"],
        "profissional_formatado": formatar_nome_medico(medico_escolhido["nome"]),
        "crm_medico": medico_escolhido["crm"],
        "crm_medico_formatado": formatar_crm(medico_escolhido["crm"]),
        "cor_pulseira_key": cor_key,
        "cor_pulseira_exibida": cor_exibida
    }
    pacientes.append(paciente)
    atendimentos.append(paciente)
    
    print(f"\n{Cores.VERDE}{'='*55}{Cores.RESET}")
    print(f"{Cores.VERDE}✅ ATENDIMENTO CADASTRADO COM SUCESSO!{Cores.RESET}")
    print(f"{Cores.VERDE}{'='*55}{Cores.RESET}")
    print(f"{Cores.CIANO}📋 RESUMO DO ATENDIMENTO:{Cores.RESET}")
    print(f"  {'Paciente:':<20} {nome_paciente}")
    print(f"  {'Tipo:':<20} {nome_tipo_atendimento}")
    print(f"  {'Especialidade:':<20} {especialidade_desejada.title()}")
    print(f"  {'Médico:':<20} {paciente['profissional_formatado']}")
    print(f"  {'CRM:':<20} {paciente['crm_medico_formatado']}")
    print(f"  {'Data:':<20} {data}")
    print(f"  {'Pulseira:':<20} {cor_exibida}")
    print(f"{Cores.VERDE}{'='*55}{Cores.RESET}")

def listar_atendimentos():
    """Lista todos os atendimentos cadastrados com Dr.(a) e CRM formatado"""
    print(f"\n{Cores.AZUL}{'='*60}{Cores.RESET}")
    print(f"{Cores.VERDE}--- LISTA DE ATENDIMENTOS ---{Cores.RESET}")
    print(f"{Cores.AZUL}{'='*60}{Cores.RESET}")
    
    if not atendimentos:
        print(f"{Cores.AMARELO}Nenhum atendimento cadastrado.{Cores.RESET}")
    else:
        for i, at in enumerate(atendimentos, 1):
            print(f"\n{Cores.MAGENTA}📌 ATENDIMENTO #{i}{Cores.RESET}")
            print(f"{Cores.CIANO}{'-'*50}{Cores.RESET}")
            print(f"  Paciente:     {at['nome']}")
            print(f"  Tipo:         {at['tipo_atendimento']}")
            print(f"  Especialidade: {at['especialidade'].title()}")
            print(f"  Data:         {at['data']}")
            print(f"  Médico:       {at.get('profissional_formatado', formatar_nome_medico(at['profissional']))}")
            print(f"  CRM:          {at.get('crm_medico_formatado', formatar_crm(at['crm_medico']))}")
            print(f"  Pulseira:     {at['cor_pulseira_exibida']}")
            print(f"{Cores.CIANO}{'-'*50}{Cores.RESET}")
    
    input(f"\n{Cores.AZUL}Pressione Enter para voltar ao menu...{Cores.RESET}")

def buscar_paciente():
    """Busca paciente pelo nome com informações formatadas"""
    print(f"\n{Cores.AZUL}{'='*50}{Cores.RESET}")
    print(f"{Cores.VERDE}--- BUSCAR PACIENTE ---{Cores.RESET}")
    print(f"{Cores.AZUL}{'='*50}{Cores.RESET}")
    
    nome_busca = input("Digite o nome do paciente: ").strip().lower()
    encontrados = [p for p in pacientes if nome_busca in p['nome'].lower()]
    
    if not encontrados:
        print(f"{Cores.VERMELHO}❌ Paciente não encontrado.{Cores.RESET}")
    else:
        print(f"\n{Cores.VERDE}✅ Encontrado(s) {len(encontrados)} paciente(s):{Cores.RESET}")
        for p in encontrados:
            print(f"\n{Cores.CIANO}{'─'*45}{Cores.RESET}")
            print(f"  Nome:         {p['nome']}")
            print(f"  Tipo:         {p['tipo_atendimento']}")
            print(f"  Especialidade: {p['especialidade'].title()}")
            print(f"  Data:         {p['data']}")
            print(f"  Médico:       {p.get('profissional_formatado', formatar_nome_medico(p['profissional']))}")
            print(f"  CRM:          {p.get('crm_medico_formatado', formatar_crm(p['crm_medico']))}")
            print(f"  Pulseira:     {p['cor_pulseira_exibida']}")
            print(f"{Cores.CIANO}{'─'*45}{Cores.RESET}")
    
    input(f"\n{Cores.AZUL}Pressione Enter para voltar ao menu...{Cores.RESET}")

def listar_todos_medicos():
    """Lista todos os médicos cadastrados com Dr.(a) e CRM formatado"""
    print(f"\n{Cores.AZUL}{'='*55}{Cores.RESET}")
    print(f"{Cores.VERDE}--- MÉDICOS VOLUNTÁRIOS CADASTRADOS ---{Cores.RESET}")
    print(f"{Cores.AZUL}{'='*55}{Cores.RESET}")
    
    if not medicos:
        print(f"{Cores.AMARELO}⚠️ Nenhum médico cadastrado no sistema.{Cores.RESET}")
    else:
        print(f"\n{Cores.CIANO}Total de médicos: {len(medicos)}{Cores.RESET}")
        print(f"{Cores.MAGENTA}{'─'*50}{Cores.RESET}")
        for i, m in enumerate(medicos, 1):
            nome_formatado = formatar_nome_medico(m['nome'])
            crm_formatado = formatar_crm(m['crm'])
            print(f"{i}. {nome_formatado}")
            print(f"   Especialidade: {m['especialidade'].title()}")
            print(f"   CRM: {crm_formatado}")
            if i < len(medicos):
                print(f"{Cores.CIANO}{'─'*50}{Cores.RESET}")
        print(f"{Cores.MAGENTA}{'─'*50}{Cores.RESET}")
    
    input(f"\n{Cores.AZUL}Pressione Enter para voltar ao menu...{Cores.RESET}")

def mostrar_menu():
    """Exibe o menu principal"""
    print(f"\n{Cores.MAGENTA}{'='*55}{Cores.RESET}")
    print(f"{Cores.VERDE}        🏥 CLÍNICA SAUDECONECTA 🏥{Cores.RESET}")
    print(f"{Cores.CIANO}        Médicos Voluntários - Atendimento Social{Cores.RESET}")
    print(f"{Cores.MAGENTA}{'='*55}{Cores.RESET}")
    print(" 1 - Cadastrar Médico")
    print(" 2 - Cadastrar Atendimento (Paciente)")
    print(" 3 - Listar Atendimentos")
    print(" 4 - Buscar Paciente")
    print(" 5 - Listar Médicos Disponíveis")
    print(" 6 - Sair")
    print(f"{Cores.MAGENTA}{'='*55}{Cores.RESET}")

# ==================== PROGRAMA PRINCIPAL ====================

def main():
    print(f"\n{Cores.VERDE}{'='*60}{Cores.RESET}")
    print(f"{Cores.VERDE}🌟 Bem-vindo ao sistema da Clínica SaudeConecta! 🌟{Cores.RESET}")
    print(f"{Cores.VERDE}{'='*60}{Cores.RESET}")
    print(f"{Cores.CIANO}📌 ODS 3 - Saúde e Bem-Estar:{Cores.RESET} Promovendo acesso gratuito à saúde para pessoas de baixa renda.")
    print(f"{Cores.AMARELO}♿ Acessibilidade:{Cores.RESET} Textos claros, cores no terminal, validação de dados para evitar erros.")
    print(f"{Cores.CIANO}📋 CRM:{Cores.RESET} Deve ter exatamente 6 dígitos (ex: 123456)")
    print(f"{Cores.VERDE}{'='*60}{Cores.RESET}")
    
    while True:
        mostrar_menu()
        opcao = input("🎯 Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_medico()
        elif opcao == "2":
            if not medicos:
                print(f"\n{Cores.VERMELHO}❌ É necessário cadastrar pelo menos um médico antes de cadastrar um atendimento.{Cores.RESET}")
                input("Pressione Enter para continuar...")
                continue
            cadastrar_atendimento()
        elif opcao == "3":
            listar_atendimentos()
        elif opcao == "4":
            buscar_paciente()
        elif opcao == "5":
            listar_todos_medicos()
        elif opcao == "6":
            print(f"\n{Cores.VERDE}{'='*50}{Cores.RESET}")
            print(f"{Cores.VERDE}✅ Encerrando o sistema. Obrigado por usar o SaudeConecta!{Cores.RESET}")
            print(f"{Cores.CIANO}   Até logo! 🏥{Cores.RESET}")
            print(f"{Cores.VERDE}{'='*50}{Cores.RESET}")
            break
        else:
            print(f"\n{Cores.VERMELHO}❌ Opção inválida. Digite um número de 1 a 6.{Cores.RESET}")

# Execução do programa
if __name__ == "__main__":
    main()
