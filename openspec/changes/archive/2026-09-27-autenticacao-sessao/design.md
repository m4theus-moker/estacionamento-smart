# Design: Autenticação & Sessão

## Context

Ver proposal.md - Why. O backend Xano já possui suporte a autenticação por token e tabela `user` com o campo `role`. O frontend Reflex precisa integrar-se a esses endpoints (`/auth/signup`, `/auth/login`, `/auth/me`) armazenando o token no estado reativo (`AuthState`) e controlando o acesso às páginas.

## Goals / Non-Goals

**Goals:**
- Garantir que o enum de papéis no Xano utilize `cliente` e `administrador` (atualizando o padrão `member` para `cliente`).
- Criar a classe `AuthState` em Reflex para gerenciar tokens e requisições HTTP autenticadas via `httpx`.
- Implementar telas e componentes de Login, Cadastro e Painel inicial com redirecionamento baseado no estado de autenticação.

**Non-Goals:**
- Implementar recuperação de senha por e-mail (fora do escopo do MVP).
- Autenticação OAuth/Social (Google, GitHub, etc.).

## Decisions

- **Armazenamento do Token no Reflex**: O token JWT será mantido no `AuthState` (variável de estado do Reflex). Para persistência entre recarregamentos de página sem dependência externa complexa no MVP, será utilizado o armazenamento em memória do estado Reflex e opcionalmente `rx.LocalStorage` se suportado nativamente pelo Reflex.
- **Enum de Papéis no Xano**: Atualizar a tabela `user.xs` para aceitar `["admin", "cliente"]` nos valores do enum `role`, garantindo alinhamento direto com o modelo de domínio (`docs/domain-model.md`).

## Risks / Trade-offs

- [Expiração de Token] → Tratamento automático de erro 401 (Unauthorized) no cliente Reflex redirecionando para a tela de login.
