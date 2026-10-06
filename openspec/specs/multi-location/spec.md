# multi-location Specification

## Purpose
Gerenciar múltiplos locais ou filiais de estacionamento, permitindo que administradores cadastrem unidades e que vagas, tarifas e operações sejam segmentadas por localidade com controle estrito de acesso e unicidade composta.

## Requirements

### Requirement: Cadastro e Gestão de Locais de Estacionamento
O sistema SHALL permitir que administradores cadastrem, editem e removam locais (filiais/unidades) informando nome, endereço e descrição. O nome do local deve ser único, rejeitando tentativas de cadastro com nome duplicado.

#### Scenario: Administrador cadastra novo local com sucesso
- **WHEN** o administrador preenche o nome, endereço e descrição de uma nova unidade e submete o formulário
- **THEN** o local é cadastrado com sucesso e fica disponível no sistema

#### Scenario: Administrador edita informações de um local
- **WHEN** o administrador atualiza os dados de um local existente e salva
- **THEN** as alterações são refletidas corretamente no sistema

#### Scenario: Administrador remove local existente
- **WHEN** o administrador seleciona um local existente e solicita sua remoção
- **THEN** o local é removido do sistema

#### Scenario: Tentativa de cadastro de local com nome duplicado é rejeitada
- **WHEN** o administrador tenta cadastrar um novo local com um nome que já existe no sistema
- **THEN** o sistema rejeita a operação com erro indicando duplicidade de nome

### Requirement: Controle de Acesso para Gestão de Locais
O sistema SHALL garantir que a consulta de locais seja permitida a qualquer usuário autenticado (cliente ou admin), enquanto operações de criação, edição e remoção sejam restritas exclusivamente a administradores. Clientes sem perfil admin tentando mutar dados devem receber acesso negado.

#### Scenario: Cliente consulta locais com sucesso
- **WHEN** um usuário autenticado com perfil de cliente solicita a consulta de locais cadastrados
- **THEN** o sistema retorna a lista de locais com sucesso

#### Scenario: Cliente tenta criar, editar ou remover local
- **WHEN** um usuário autenticado com perfil de cliente tenta executar operações de criação, edição ou remoção de locais
- **THEN** o sistema retorna erro de acesso negado (Unauthorized/Forbidden)

### Requirement: Segmentação de Vagas por Local
O sistema SHALL vincular cada vaga a um local específico (`location_id`), garantindo que o gerenciamento e a listagem de vagas ocorram estritamente no escopo do local selecionado.

#### Scenario: Vaga associada a um local específico
- **WHEN** uma vaga é cadastrada informando a qual local ela pertence
- **THEN** a vaga fica associada exclusivamente àquele local no sistema

### Requirement: Gestão de Tarifas por Local e Tipo de Vaga
O sistema SHALL permitir que o administrador defina e atualize o valor da tarifa por hora para cada combinação de `(location_id + tipo_vaga)`, garantindo que exista apenas uma tarifa única para o mesmo tipo de vaga em um mesmo local. O mesmo tipo de vaga pode possuir tarifas diferentes em locais distintos, mas tentativas de cadastrar tarifas duplicadas para o mesmo tipo no MESMO local devem ser rejeitadas.

#### Scenario: Administrador define tarifa para o tipo Carro em um local específico
- **WHEN** o administrador define o valor por hora para a categoria "Carro" no local A
- **THEN** a tarifa é salva com sucesso para aquele tipo no local A

#### Scenario: Mesma tarifa cadastrada em dois locais diferentes com sucesso
- **WHEN** o administrador cadastra uma tarifa para o tipo "Carro" no local A e posteriormente cadastra outra tarifa para o tipo "Carro" no local B
- **THEN** ambas as tarifas são cadastradas com sucesso, mantendo valores independentes por local

#### Scenario: Tentativa de cadastrar tarifa duplicada para o mesmo tipo no mesmo local é rejeitada
- **WHEN** o administrador tenta criar uma nova tarifa para o tipo "Carro" em um local que já possui tarifa cadastrada para esse mesmo tipo
- **THEN** o sistema rejeita a operação indicando duplicidade de tarifa para o local especificado

### Requirement: Seleção de Local Ativo e Isolamento de Dados
O sistema SHALL permitir que o usuário selecione o local ativo na interface para visualizar vagas e tarifas, garantindo isolamento estrito de forma que dados de um local não apareçam ao consultar outro.

#### Scenario: Usuário seleciona local ativo no painel e visualiza dados segmentados
- **WHEN** o usuário seleciona uma unidade específica no seletor de locais
- **THEN** o sistema carrega e exibe exclusivamente as vagas e tarifas pertencentes àquele local, sem exibir dados de outras unidades
