# Tasks

## 1. Backend (Xano) - Ajuste de Papéis e Autenticação

- [x] 1.1 Atualizar o schema da tabela `user.xs` para que o enum `role` suporte `["admin", "cliente"]`, e ajustar `signup_POST.xs` para atribuir o papel `"cliente"` por padrão, verificando a sintaxe correta via Xano Developer MCP ou validação.
- [x] 1.2 Verificar e testar os endpoints `/auth/signup`, `/auth/login` e `/auth/me` para garantir o correto retorno do token JWT e dos dados do usuário.

## 2. Frontend (Reflex) - Estado e Telas de Autenticação

- [x] 2.1 Implementar a classe `AuthState` em Reflex para gerenciar o token de autenticação, o estado de login, usuário atual e chamadas HTTP para o Xano.
- [x] 2.2 Criar componentes e páginas de Login e Cadastro em Reflex com formulários e tratamento de erros (e-mail duplicado, credenciais inválidas), verificando a renderização correta.
- [x] 2.3 Implementar proteção de rotas e redirecionamento automático com base no estado de autenticação do usuário.

## 3. Verificação e Validação

- [x] 3.1 Executar testes de integração simulando o fluxo completo de cadastro, login e consulta de perfil `/auth/me`, validando os densos cenários descritos na spec `user-auth`.
