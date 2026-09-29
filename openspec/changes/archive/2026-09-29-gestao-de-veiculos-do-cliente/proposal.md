# Proposal

## Why

Atualmente o sistema possui autenticação de usuários, mas carece de um módulo onde o cliente possa cadastrar, visualizar, editar e gerenciar seus próprios veículos vinculados à sua conta no estacionamento. Isso é fundamental para permitir a associação de veículos a futuras reservas e vagas.

## What Changes

- **Novo Módulo de Veículos**: Adicionar funcionalidade para que o cliente cadastre seus veículos informando placa, modelo, marca, cor e ano.
- **Backend (Xano)**: Criar tabela `vehicle` (com relação ao usuário autenticado) e endpoints de API para CRUD de veículos (`GET /vehicle`, `POST /vehicle`, `PUT /vehicle/{id}`, `DELETE /vehicle/{id}`).
- **Frontend (Reflex)**: Desenvolver a tela/componente de gerenciamento de veículos no painel do usuário.

## Capabilities

### New Capabilities
- `vehicle-management`: Gerenciamento completo de veículos do cliente (cadastro, listagem, edição e exclusão).

### Modified Capabilities
- (Nenhuma)

## Impact

- **Banco de Dados (Xano)**: Nova tabela `vehicle` com chave estrangeira para `user`.
- **API (Xano)**: Novos endpoints REST autenticados para gestão de veículos.
- **Frontend (Reflex)**: Nova página/visão de veículos integrada ao estado de autenticação (`AuthState`).
