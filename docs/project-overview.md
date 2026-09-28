# Project Overview — Estacionamento Smart

## 1. Visão geral

O Estacionamento Smart é um sistema web para gerenciamento de estacionamentos. Ele conecta dois perfis de uso: o cliente, que consulta vagas, reserva um espaço e acompanha seu uso do estacionamento; e o administrador, que controla vagas, veículos, tarifas, entradas/saídas e a operação geral do estabelecimento.

## 2. Problema

A gestão manual de estacionamentos (planilhas, cadernos, controle visual) dificulta saber em tempo real quais vagas estão livres, gera conflitos de reserva, torna o cálculo de cobrança sujeito a erro e não deixa histórico útil para decisões (ex.: previsão de lotação).

## 3. Objetivos

- Permitir que o cliente veja e reserve vagas disponíveis sem conflitos.
- Automatizar o cálculo do valor devido a partir do tempo de permanência.
- Dar ao administrador uma visão em tempo real da ocupação do estacionamento.
- Registrar histórico de uso para relatórios e, futuramente, previsão de lotação.
- Entregar um MVP funcional primeiro, evoluindo depois com recursos intermediários e avançados.

## 4. Público-alvo / usuários

- **Cliente**: pessoa que estaciona o veículo — cria conta, cadastra veículos, reserva e paga pelo uso.
- **Administrador**: responsável pela operação do estacionamento — gerencia vagas, tarifas, entradas/saídas e relatórios.

## 5. Escopo

**Dentro do escopo (MVP):** login, cadastro de veículos, consulta de vagas, reservas, registro de entrada/saída, cálculo automático do valor.

**Fora do escopo do MVP** (planejado para etapas seguintes): dashboard administrativo completo, QR Code, relatórios, múltiplos tipos de vaga, sistema de mensalistas, previsão de lotação, notificações e distribuição otimizada de vagas.

## 6. Principais funcionalidades

**Cliente:** conta e login; cadastro de veículos; consulta de vagas; reserva de vaga; histórico; entrada/saída; consulta de valor e comprovante.

**Administrador:** gestão de vagas (criar, editar, remover, definir tipo); visão em tempo real do estacionamento; gestão de tarifas; registro de entradas/saídas; relatórios; gestão de usuários e veículos.

Tipos de vaga previstos: Carro, Moto, PCD, Elétrico.

## 7. Requisitos e restrições importantes

- Uma vaga não pode ser reservada para dois usuários no mesmo intervalo de tempo (reserva inteligente por período).
- O valor cobrado deve refletir o tempo de permanência real (entrada x saída), não apenas o período reservado.
- Regras de autorização (o que cada perfil pode fazer) devem ser aplicadas no backend (Xano), nunca apenas no frontend.
- O sistema deve continuar funcional com o escopo do MVP mesmo antes de qualquer funcionalidade diferencial existir.

## 8. Arquitetura tecnológica

- **Frontend**: Reflex (Python). Reflex é a tecnologia exclusiva para implementação do frontend da aplicação — não deve ser substituído ou complementado por React, Vue, Angular ou outro framework, salvo mudança arquitetural explicitamente aprovada.
- **Backend**: Xano. A lógica de negócio, os endpoints de API e as regras de autorização são implementados em XanoScript (arquivos `.xs`) e sincronizados com o repositório local através do Xano CLI (`xano workspace pull` / `push`).
- **Banco de dados**: interno do Xano — as tabelas do domínio (Usuário, Veículo, Vaga, Reserva, Estacionamento, Tarifa) são gerenciadas dentro do workspace Xano, não em um banco relacional administrado separadamente pelo projeto.
- **Autenticação**: mecanismos nativos de autenticação do Xano.
- **Documentação de API**: gerada automaticamente pelo Xano para os grupos de endpoints.
- **Controle de versão**: Git + GitHub.
- **Editor**: Visual Studio Code, com XanoScript Language Server (suporte aos arquivos `.xs`) e as Agent Skills do Reflex (`reflex-docs`, `setup-python-env`, `reflex-process-management`).
- **Assistência de IA**: GitHub Copilot ou Gemini CLI, apoiados pelo Xano Developer MCP (documentação e validação de XanoScript) para o trabalho no backend.
- **Especificação e documentação viva**: OpenSpec.

## 9. Princípios de desenvolvimento

- Desenvolvimento incremental: MVP primeiro, depois nível intermediário, depois avançado.
- Mudanças conduzidas via OpenSpec (spec-driven), uma capability/feature por vez.
- Não introduzir tecnologia de frontend ou backend fora da stack definida (Reflex / Xano) sem uma mudança arquitetural explicitamente registrada e aprovada.
- Reutilizar estruturas já definidas (modelo de dados, entidades) em vez de recriá-las por funcionalidade.

## 10. Segurança e integridade

- Autenticação via mecanismos nativos do Xano; sem essa autenticação, nenhum endpoint de reserva, cadastro de veículo ou administração deve responder.
- Toda regra de autorização (cliente x administrador) é validada no backend (Xano), nunca apenas no frontend Reflex.
- O valor cobrado é sempre recalculado no backend a partir de `entrada_real` e `saida_real`, nunca aceito diretamente do frontend.
- Tokens e credenciais do Xano nunca são versionados em arquivos do repositório.

## 11. Estratégia de desenvolvimento

O projeto segue três níveis:

1. **MVP**: login → cadastro de veículos → consulta de vagas → reservas → entrada e saída → cálculo do preço.
2. **Intermediário**: dashboard, QR Code, relatórios, múltiplos tipos de vaga, sistema de mensalistas.
3. **Avançado**: distribuição otimizada de vagas, previsão de lotação, notificações, análise de dados.

Cada funcionalidade nova é conduzida como uma change no OpenSpec: explore → propose → review → apply → archive.

## 12. Fonte de verdade e documentação

- `docs/project-overview.md` (este documento): visão geral e estável do projeto.
- `docs/domain-model.md`: conceitos do domínio e seus relacionamentos.
- `AGENTS.md`: regras de como o agente de IA deve trabalhar neste projeto.
- `openspec/specs/`: comportamento consolidado do sistema, atualizado a cada change arquivada.
- `openspec/changes/`: mudanças em planejamento ou implementação no momento.
