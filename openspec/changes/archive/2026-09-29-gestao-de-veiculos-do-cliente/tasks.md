# Tasks

## 1. Backend (Xano) - Tabela e Endpoints

- [x] 1.1 Criar tabela `vehicle` no Xano com campos (`id`, `created_at`, `user_id`, `plate`, `brand`, `model`, `color`, `year`) e verificar sucesso no schema
- [x] 1.2 Criar endpoint POST `/vehicle` para cadastro de veículo, garantindo a atribuição e validação automática de `user_id = auth.id` vinculado ao usuário autenticado, e verificar resposta de sucesso
- [x] 1.3 Criar endpoint GET `/vehicle` para listagem dos veículos, assegurando que a query filtra estritamente por `user_id = auth.id` para retornar apenas os veículos do usuário autenticado e nunca de terceiros
- [x] 1.4 Criar endpoints PUT `/vehicle/{id}` e DELETE `/vehicle/{id}` para edição e exclusão de veículos, validando obrigatoriamente que o registro pertence ao usuário autenticado (`user_id = auth.id`), rejeitando com 403/404 em caso de tentativa de acesso a veículos de terceiros
- [x] 1.5 Realizar teste de verificação final de isolamento entre usuários: criar dois usuários de teste distintos e confirmar empiricamente que nenhum consegue acessar, listar, editar ou excluir os veículos do outro

## 2. Frontend (Reflex) - Módulo de Veículos

- [x] 2.1 Criar estado `VehicleState` no Reflex com lógica para listar, adicionar, editar e excluir veículos consumindo a API do Xano
- [x] 2.2 Criar componente/página de gerenciamento de veículos no Reflex com formulário de cadastro e tabela de listagem, verificando renderização visual correta
- [x] 2.3 Integrar o módulo de veículos ao dashboard principal do usuário logado e verificar navegação e interatividade
