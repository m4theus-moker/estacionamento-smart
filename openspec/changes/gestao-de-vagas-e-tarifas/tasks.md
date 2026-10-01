# Tasks

## 1. Backend (Xano) - Modelos, Validações e Endpoints

- [x] 1.1 Validar/atualizar a tabela e schema de Vagas (`vaga`) no Xano com índice único para `numero` e campos tipo e status, executando `xano workspace push` e confirmando o sucesso.
- [x] 1.2 Validar/atualizar a tabela e schema de Tarifas (`tarifa`) no Xano com índice único para `tipo_vaga` e campo `valor_hora`, executando `xano workspace push` e confirmando o sucesso.
- [x] 1.3 Implementar endpoints REST de CRUD completo para Vagas e Tarifas no Xano: consulta permitida a qualquer usuário autenticado, e mutações restritas a administradores (`role == 'admin'`), retornando `error_type` válidos em casos de acesso negado ou duplicidade. Executar `xano workspace push` e confirmar.
- [x] 1.4 Criar testes automatizados em Python (`pytest` + `requests`) cobrindo os endpoints do Xano usando tokens de autenticação de admin e de cliente, validando: (a) sucesso do admin em criar, listar, editar e remover vagas e tarifas; (b) acesso negado (Forbidden/Unauthorized com `error_type` válido) quando o cliente tenta executar mutações; (c) rejeição de número de vaga duplicado; (d) rejeição de tarifa duplicada para o mesmo tipo. Validar execução e confirmar com `xano workspace push`.

## 2. Frontend (Reflex) - Interfaces de Gestão e Consulta sob Demanda

- [x] 2.1 Desenvolver componentes e tela de gestão de vagas no Reflex para o administrador com atualização sob demanda (ao abrir e após ações), verificando renderização.
- [x] 2.2 Desenvolver componentes e tela de gestão de tarifas no Reflex para o administrador (uma por `tipo_vaga`, permitindo edição de valor), verificando salvamento e atualização sob demanda.
- [x] 2.3 Desenvolver a tela de consulta de disponibilidade de vagas para clientes e administradores com atualização sob demanda, verificando exibição correta dos status.

## 3. Validação e Integração

- [x] 3.1 Executar testes de integração e suíte de testes automatizados, confirmando o funcionamento completo do fluxo de administradores, restrições de clientes e tratamento de erros.
