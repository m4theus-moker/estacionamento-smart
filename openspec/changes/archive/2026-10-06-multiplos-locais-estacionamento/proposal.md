# Proposal: Suporte a Múltiplos Locais de Estacionamento

## Why

Atualmente, o Estacionamento Smart opera em um único local. Para expandir o negócio e permitir a gestão centralizada de diferentes unidades ou filiais (por exemplo, estacionamento Centro, Shopping, Aeroporto), é necessário introduzir o suporte a múltiplos locais de estacionamento, segmentando vagas, tarifas e operações por localidade.

## What Changes

- **Backend (Xano)**: Criação da tabela `location` (local/filial) e associação do campo `location_id` às tabelas existentes de vagas (`vaga`/`vehicle` ou `parking`) e tarifas para isolar os dados por local.
- **Frontend (Reflex)**: Adição de seletor de local ativo na interface do usuário e adaptação dos painéis de administração e cliente para filtrar e gerenciar recursos por local selecionado.
- **Segurança e Isolamento**: Garantir que consultas e operações respeitem o local selecionado ou vinculado.

## Capabilities

### New Capabilities
- `multi-location`: Gerenciamento de múltiplos locais/filiais de estacionamento, permitindo cadastro de locais e segmentação de vagas e tarifas por unidade.

### Modified Capabilities
- (Nenhuma nova modificação em spec existente nesta fase inicial, embora `parking-management` possa ser estendida futuramente se necessário).

## Impact

- **Backend (Xano)**: Nova tabela `location` e atualização das chaves estrangeiras em tabelas dependentes (`vaga`, `tarifa`, etc.).
- **Frontend (Reflex)**: Novo estado e componentes de seleção de localidade e telas de administração de locais.
- **Banco de Dados**: Migração/atualização do schema Xano.
