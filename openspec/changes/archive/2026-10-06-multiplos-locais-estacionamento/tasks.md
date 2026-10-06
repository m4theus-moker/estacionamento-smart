# Tasks

## 1. Backend (Xano) - Tabela, Migração e Endpoints de Locais

- [x] 1.1 Criar tabela `location` no Xano com campos (`id`, `created_at`, `name`, `address`, `description`) e verificar sucesso no schema
- [x] 1.2 Criar um local padrão denominado "Matriz" e migrar/atualizar registros legados (dados de testes anteriores de desenvolvimento foram limpos e associados a locais estruturados com `location_id`)
- [x] 1.3 Adicionar campo `location_id` com restrição e índice nas tabelas relacionadas (`vaga`, `tarifa`) e configurar a restrição de unicidade composta `(location_id + tipo_vaga)` na tabela de tarifas
- [x] 1.4 Criar endpoints CRUD no Xano para gerenciamento de locais (`GET /location`, `POST /location`, `PUT /location/{id}`, `DELETE /location/{id}`) com validação estrita de papel administrativo e respostas de sucesso

## 2. Frontend (Reflex) - Estado, Isolamento e Interface de Locais

- [x] 2.1 Criar classe `LocationState` no Reflex para gerenciar listagem, seleção de local ativo e persistência da unidade, verificando carregamento correto
- [x] 2.2 Criar componentes de seleção de local e tela de administração de unidades no Reflex, aplicando validação de acesso (apenas admin pode mutar dados de locais)
- [x] 2.3 Integrar o filtro de `location_id` nas consultas de vagas e tarifas no Reflex e verificar interatividade e filtragem por unidade selecionada
- [x] 2.4 Realizar teste de verificação e isolamento por local: confirmar empiricamente que vagas e tarifas cadastradas em um local não aparecem ao consultar outro local
