# Design

## Context

O projeto utiliza Xano como backend (com sincronização via Xano CLI) e Reflex (Python) no frontend. O gerenciamento de veículos requer a criação de uma nova tabela `vehicle` vinculada ao usuário autenticado e a exposição de endpoints REST no Xano, além de componentes e páginas no Reflex.

## Goals / Non-Goals

**Goals:**
- Criar modelo de dados `vehicle` no Xano com associação ao usuário (`user_id`).
- Implementar endpoints de API REST no Xano para operações de CRUD de veículos com validação de propriedade.
- Desenvolver interface em Reflex para o cliente gerenciar seus veículos.

**Non-Goals:**
- Gestão de veículos por administradores (foco atual no autosserviço do cliente).
- Associação automática de vagas nesta fase.

## Decisions

- **Armazenamento no Xano**: Criação da tabela `vehicle` com campos: `id`, `created_at`, `user_id` (foreign key para `user`), `plate` (string/placa), `brand`, `model`, `color`, `year`.
- **Autenticação e Segurança**: Uso do token JWT do Xano nos requests HTTP (`httpx`) do Reflex para garantir que cada usuário gerencie apenas seus próprios veículos.
- **Frontend Reflex**: Criação de estado (`VehicleState`) e componentes de formulário/tabela em Python/Reflex seguindo o padrão de design estabelecido.

## Risks / Trade-offs

- **Validação de Placa**: Risco de formato de placa inválido. 
  - *Mitigação*: Aplicar filtros de formatação e validação básica no frontend e backend.
