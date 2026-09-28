# Proposal: Autenticação & Sessão

## Why

O Estacionamento Smart precisa de um mecanismo confiável de autenticação e controle de sessão para distinguir clientes e administradores, protegendo todas as operações subsequentes (cadastro de veículos, consulta de vagas, reservas e controle de entradas/saídas). Esta é a fundação de segurança exigida pelo domínio.

## What Changes

- **Backend (Xano)**: Ajuste do enum de papéis (`role`) na tabela `user.xs` para suportar explicitamente `cliente` e `administrador` (mapeando o padrão anterior `member` para `cliente`). Garantia de que os endpoints de cadastro (`POST /auth/signup`), login (`POST /auth/login`) e dados do usuário (`GET /auth/me`) atendam aos requisitos do domínio.
- **Frontend (Reflex)**: Implementação do `AuthState` em Python para gerenciar o token de autenticação JWT, estado de login, dados do usuário autenticado (`cliente` ou `administrador`), além das páginas/componentes de Login e Cadastro com tratamento de erros.
- **Segurança**: Validação de que todas as rotas protegidas exigem token válido e verificação de papéis no backend.

## Capabilities

### New Capabilities
- `user-auth`: Gerenciamento de usuários, autenticação baseada em token JWT, sessão no Reflex e controle de acesso por papel (`cliente` e `administrador`).

### Modified Capabilities
- Nenhum (capability inaugural).

## Impact

- **Backend**: Atualização em `xano/table/user.xs` para o enum de `role` e verificação nos endpoints de autenticação.
- **Frontend**: Criação de lógica de estado (`AuthState`), páginas de autenticação e proteção de rotas no aplicativo Reflex (`estacionamento_smart/`).
- **Dependências**: Nenhuma (fatia inicial do MVP).
