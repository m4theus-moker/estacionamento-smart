# parking-management Specification

## Purpose
Gerenciar o cadastro, os tipos, os status e as tarifas das vagas do estacionamento, permitindo que administradores configurem a infraestrutura física e clientes consultem a disponibilidade com atualização sob demanda.

## Requirements

### Requirement: Cadastro e Gestão de Vagas
O sistema SHALL permitir que o administrador cadastre, edite e remova vagas informando o número de identificação e o tipo da vaga (Carro, Moto, PCD, Elétrico). O número da vaga deve ser único, rejeitando tentativas de cadastro com número duplicado.

#### Scenario: Administrador cadastra nova vaga com sucesso
- **WHEN** o administrador preenche o número da vaga e seleciona o tipo "Carro" e submete o formulário
- **THEN** a vaga é criada com status inicial "Livre" e aparece na listagem de vagas

#### Scenario: Administrador edita vaga existente
- **WHEN** o administrador altera o tipo ou status de uma vaga existente e salva
- **THEN** os dados da vaga são atualizados com sucesso no sistema

#### Scenario: Administrador remove vaga existente
- **WHEN** o administrador seleciona uma vaga existente e solicita sua remoção
- **THEN** a vaga é removida do cadastro do estacionamento

#### Scenario: Tentativa de cadastro de vaga com número duplicado é rejeitada
- **WHEN** o administrador tenta cadastrar uma nova vaga com um número que já existe no sistema
- **THEN** o sistema rejeita a operação com erro indicando duplicidade de número

### Requirement: Controle de Acesso para Gestão de Vagas e Tarifas
O sistema SHALL garantir que a consulta de vagas e tarifas seja permitida a qualquer usuário autenticado (cliente ou admin), enquanto operações de criação, edição e remoção sejam restritas exclusivamente a administradores. Clientes sem perfil admin tentando mutar dados devem receber acesso negado.

#### Scenario: Cliente consulta vagas e tarifas com sucesso
- **WHEN** um usuário autenticado com perfil de cliente solicita a consulta de vagas ou tarifas
- **THEN** o sistema retorna os dados solicitados com sucesso

#### Scenario: Cliente tenta criar, editar ou remover vaga ou tarifa
- **WHEN** um usuário autenticado com perfil de cliente tenta executar operações de criação, edição ou remoção em vagas ou tarifas
- **THEN** o sistema retorna erro de acesso negado (Unauthorized/Forbidden)

### Requirement: Gestão de Tarifas por Tipo de Vaga
O sistema SHALL permitir que o administrador defina e atualize o valor da tarifa por hora para cada `tipo_vaga`, garantindo que exista apenas uma tarifa única por tipo de vaga. Tentativas de cadastrar tarifas duplicadas para o mesmo tipo são rejeitadas.

#### Scenario: Administrador define tarifa única para o tipo Carro
- **WHEN** o administrador define o valor por hora para a categoria "Carro"
- **THEN** a tarifa é salva com sucesso para aquele tipo

#### Scenario: Administrador atualiza o valor de uma tarifa existente
- **WHEN** o administrador altera o valor por hora de uma tarifa já cadastrada para determinado tipo e salva
- **THEN** o novo valor da tarifa é atualizado com sucesso

#### Scenario: Tentativa de cadastrar tarifa duplicada para o mesmo tipo é rejeitada
- **WHEN** o administrador tenta criar uma nova tarifa para um tipo de vaga que já possui tarifa cadastrada
- **THEN** o sistema rejeita a operação indicando que já existe tarifa para o tipo especificado

### Requirement: Consulta de Vagas sob Demanda para Clientes e Administradores
O sistema SHALL permitir que os usuários consultem a disponibilidade de vagas do estacionamento com atualização sob demanda (ao abrir a tela e após cada ação de mutação).

#### Scenario: Usuário consulta vagas disponíveis sob demanda
- **WHEN** o usuário abre a tela de consulta de vagas ou executa uma ação de atualização
- **THEN** o sistema carrega e exibe todas as vagas cadastradas com seus respectivos números, tipos e status atuais
