# Design: Suporte a Múltiplos Locais de Estacionamento

## Context

Ver proposal.md - Why. O sistema utiliza Xano como backend e Reflex (Python) como frontend. Para suportar múltiplos locais sem quebrar o modelo atual, precisamos introduzir a entidade `location` e relacioná-la às tabelas de infraestrutura (`vaga`, `tarifa`, etc.).

## Goals / Non-Goals

**Goals:**
- Criar a tabela `location` no Xano com campos: `id`, `created_at`, `name`, `address`, `description`.
- Adicionar chave estrangeira/relação `location_id` nas tabelas de vagas e tarifas.
- Expor endpoints CRUD para locais no Xano e implementar estado reativo (`LocationState`) no Reflex.

**Non-Goals:**
- Transferência de veículos entre locais em tempo real (fora do escopo inicial).
- Faturamento consolidado multi-empresa complexo (focado em unidades de uma mesma operação).

## Decisions

- **Modelo de Dados (Xano)**: A tabela `location` será isolada, e cada vaga/tarifa referenciará `location_id`.
- **Gerenciamento de Estado no Frontend (Reflex)**: `LocationState` armazenará a lista de locais disponíveis e o `selected_location_id`, persistindo a seleção na sessão/estado do Reflex para filtrar as consultas subsequentes.

## Risks / Trade-offs

- [Escopo de Consultas] → Se o usuário não selecionar um local, o sistema deve selecionar um padrão (primeiro local cadastrado) para evitar erros de listagem vazia.
- [Migração de Dados Existentes] → Vagas e tarifas criadas anteriormente precisarão ser associadas a um local padrão ("Matriz" ou "Principal").
