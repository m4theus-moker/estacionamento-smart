# AGENTS.md — Estacionamento Smart

Este arquivo contém as regras de como o agente de IA deve trabalhar neste projeto. Ele não repete o conteúdo de `docs/project-overview.md` nem de `docs/domain-model.md` — consulte esses documentos quando precisar de contexto sobre o que o projeto é ou quais são seus conceitos.

## Documentação

Antes de propor ou implementar qualquer mudança significativa, consultar `docs/project-overview.md` e `docs/domain-model.md`. Não presumir funcionalidades, entidades ou regras que não estejam documentadas ali ou em uma spec já aprovada.

## Frontend

O frontend do projeto deve ser implementado exclusivamente com Reflex. Utilize os mecanismos próprios do Reflex para componentes, estado (`State`), eventos, páginas e interação. Não introduza outra tecnologia de frontend para substituir ou complementar o Reflex, salvo quando houver uma alteração arquitetural explicitamente aprovada.

## Backend

O backend do projeto deve ser implementado exclusivamente com Xano, usando XanoScript (arquivos `.xs`). Não escreva um backend alternativo (NestJS, Express, Django, etc.) para substituir ou complementar o Xano. Antes de implementar ou alterar lógica de backend, consulte o Xano Developer MCP para documentação e validação de sintaxe — não presuma sintaxe de XanoScript de memória.

## Arquitetura

O frontend (Reflex) consome os endpoints REST expostos pelo backend (Xano) — a comunicação entre as camadas nunca deve pressupor acesso direto a um banco de dados fora do Xano. Reutilizar entidades e estruturas já definidas no `domain-model.md` em vez de recriá-las por funcionalidade. Não modificar funcionalidades fora do escopo da change atual sem justificativa.

## Segurança

Toda regra de autorização (o que cliente e administrador podem fazer) deve ser aplicada no backend (Xano) — o frontend Reflex nunca é mecanismo de segurança. O valor cobrado em `Estacionamento` deve sempre ser recalculado no backend a partir dos horários reais de entrada e saída, nunca aceito diretamente do frontend. Nunca coloque tokens ou credenciais do Xano em arquivos versionados.

## Desenvolvimento

Mudanças devem seguir o fluxo OpenSpec: explore → propose → review → apply → archive. Seguir a ordem definida nos três níveis do projeto (MVP → Intermediário → Avançado) descrita em `docs/project-overview.md`, evitando implementar funcionalidades de um nível posterior antes das dependências do nível anterior estarem prontas.

## Testes

Toda mudança funcional deve possuir uma estratégia de verificação mínima (cenários de sucesso e de erro), especialmente para: conflito de reservas na mesma vaga/período, cálculo do valor a partir do tempo real de permanência, e regras de autorização entre cliente e administrador.

## Idioma

Escrever os artefatos do OpenSpec (proposal, specs, design, tasks) em português brasileiro.