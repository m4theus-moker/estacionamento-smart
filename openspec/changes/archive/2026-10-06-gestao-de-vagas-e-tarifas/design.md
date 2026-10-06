# Design

## Context

See proposal.md for motivation. O sistema utiliza Reflex (Python) no frontend e Xano (backend e banco de dados relacional interno) para persistência e regras de negócio. O modelo de usuário no Xano já possui o campo `role` (`admin` / `cliente`), que será utilizado para autorização. Esta change introduz as entidades de Vaga e Tarifa, estruturando o domínio físico e de cobrança do estacionamento.

## Goals / Non-Goals

**Goals:**
- Definir tabelas no Xano para `vaga` (número único, tipo, status inicial "livre", editável pelo admin) e `tarifa` (`tipo_vaga` único, `valor_hora`).
- Criar endpoints REST no Xano para operações CRUD completas de vagas e tarifas (criar, listar, editar, remover), protegidos por autenticação, com consulta permitida a qualquer usuário autenticado e mutação restrita a administradores (`role == 'admin'`), retornando erro adequado (`error_type` válidos) em caso de acesso negado ou duplicidade.
- Desenvolver componentes e páginas no Reflex para o painel do administrador (gestão de vagas e tarifas) e para a interface do cliente (consulta de disponibilidade com atualização sob demanda: ao abrir a tela e após cada ação).

**Non-Goals:**
- Implementar regras complexas de mensalistas ou descontos dinâmicos nesta etapa (reservado para fases futuras).
- Transição automática de status de vaga por reserva (ficará para a change de Reservas; nesta change o status é gerenciado diretamente pelo admin).

## Decisions

- **Modelo de Dados no Xano**: 
  - `vaga`: `id`, `numero` (único, indexado), `tipo` (carro, moto, pcd, eletrico), `status` (livre, ocupada, reservada).
  - `tarifa`: `id`, `tipo_vaga` (único, indexado), `valor_hora`.
- **Validação e Segurança**: Consulta permitida a qualquer usuário autenticado; rotas de mutação exigem autenticação e verificação explícita do campo `role` do usuário no Xano (`admin`), rejeitando clientes com erro de acesso negado.
- **Tratamento de Erros e Xano**: Uso exclusivo de `error_type` válidos do Xano. Sempre confirmar o push do Xano (`xano workspace push`) após alterar arquivos `.xs`.
- **Atualização sob Demanda**: Os dados no Reflex são buscados ao carregar a página/componente e recarregados após qualquer ação de mutação (criação, edição, exclusão).

## Risks / Trade-offs

- [Consistência de Acesso] → Mitigação: Verificação rigorosa do `role` no backend Xano em todas as rotas administrativas, enquanto consultas são abertas a usuários autenticados.
- [Duplicidade de Dados] → Mitigação: Índices únicos no banco de dados Xano para `numero` de vaga e `tipo_vaga` de tarifa.
- [Latência de Rede / Chamadas Xano no Reflex] → Mitigação: Tratamento de estados de carregamento (loading states) e feedback visual claro no Reflex durante a atualização sob demanda.
- [Validação de Erros de API] → Mitigação: Mapeamento padronizado de códigos de status HTTP e `error_type` do Xano no cliente Reflex para exibir mensagens amigáveis (ex: duplicidade ou acesso negado).
