# Sistema de Transações Financeiras (Python)

Este projeto implementa um sistema de **transferências financeiras entre contas**, com foco em **boas práticas de engenharia de software**, incluindo arquitetura desacoplada, testes automatizados e controle de concorrência.

## Objetivo

Simular um ambiente de transações bancárias que:

- Realiza transferências entre contas
- Garante consistência dos dados
- Trata erros de negócio (saldo insuficiente, conta inexistente)
- Suporta execução concorrente (multi-thread)
- Mantém alta testabilidade e baixo acoplamento

## Arquitetura

O projeto segue uma abordagem inspirada em:

- **Clean Architecture**
- **Hexagonal Architecture (Ports and Adapters)**
- **SOLID Principles**

## Estrutura do Projeto
TransacaoFinanceira/
│
├── models/ # Entidades do domínio
│ ├── conta.py
│ ├── transacao.py
│ └── resultado_transacao.py
│
├── repositories/ # Camada de acesso a dados
│ ├── repository_interface.py
│ └── repository_memory.py
│
├── services/ # Regras de negócio
│ └── transacao_service.py
│
├── exceptions/ # Exceções customizadas
│ └── exceptions.py
│
├── tests/ # Testes automatizados
│ ├── test_conta.py
│ ├── test_conta_repository.py
│ ├── test_transacao_service.py
│ └── test_concorrencia.py
│
└── main.py # Execução do sistema

## Descrição da Arquitetura

### Camada de Domínio (models)

Contém as entidades principais:

- Conta: representa uma conta bancária
- Transacao: representa uma transferência (imutável)
- ResultadoTransacao: representa o resultado da operação
- Contém lógica de negócio básica (ex: débito/crédito)

### Camada de Serviço (services)

Responsável pela lógica principal:

- TransacaoService

Funções:
- Validar saldo
- Buscar contas
- Executar transferência
- Garantir consistência

### Camada de Repositório (repositories)

Implementa o padrão **Repository Pattern**:

- Interface: ContaRepositoryInterface
- Implementação: ContaRepositoryMemory

Permite implementações futuras facilmente:
- Banco de dados real (futuro)
- API externa
- Cache

### Camada de Exceções

Define erros de domínio:
- SaldoInsuficienteError
- ContaNaoEncontradaError

  [Transacao]
     ↓
TransacaoService
     ↓
Busca contas no Repository
     ↓
Valida saldo
     ↓
Executa débito/crédito
     ↓
Atualiza repository
     ↓
Retorna ResultadoTransacao

## Concorrência

O sistema suporta execução paralela usando:
python
ThreadPoolExecutor

## Diagrama de Arquitetura Final
                ┌──────────────────────┐
                │      Transacao       │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │  TransacaoService    │
                └─────────┬────────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼                                ▼
┌──────────────────────┐        ┌──────────────────────┐
│ ContaRepository      │        │ Exceptions           │
│ (Interface)          │        │ (Erros de domínio)   │
└─────────┬────────────┘        └──────────────────────┘
          │
          ▼
┌────────────────────────────┐
│ ContaRepositoryMemory      │
└────────────────────────────┘
