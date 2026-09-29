# Spec Delta

## Purpose

Permite que os clientes cadastrem, visualizem, editem e removam seus veículos associados à conta para uso no sistema de estacionamento, garantindo isolamento estrito de dados entre usuários.

## ADDED Requirements

### Requirement: Cadastro de veículo pelo cliente
O sistema SHALL permitir que o cliente cadastrado adicione um novo veículo informando placa, modelo, marca, cor e ano, vinculando-o automaticamente ao usuário autenticado (`user_id = auth.id`).

#### Scenario: Cadastro bem-sucedido de veículo
- **WHEN** o cliente preenche os dados do veículo (placa válida, modelo, marca, cor, ano) e envia o formulário
- **THEN** o veículo é cadastrado com sucesso e associado à conta do usuário autenticado

#### Scenario: Tentativa de cadastro com placa duplicada ou inválida
- **WHEN** o cliente tenta cadastrar um veículo com placa já existente ou dados incompletos
- **THEN** o sistema rejeita o cadastro e exibe uma mensagem de erro apropriada

### Requirement: Listagem de veículos do usuário
O sistema SHALL exibir para o usuário autenticado a lista de todos os seus veículos cadastrados, filtrando estritamente por ID do usuário autenticado.

#### Scenario: Visualização da lista de veículos
- **WHEN** o usuário acessa a seção de veículos no painel
- **THEN** o sistema exibe a lista contendo placa, modelo, marca, cor e ano de cada veículo pertencente exclusivamente ao usuário

### Requirement: Isolamento estrito de dados e segurança por usuário
O sistema SHALL garantir o isolamento estrito de dados, assegurando que nenhum usuário possa acessar, listar, editar ou excluir veículos pertencentes a outros usuários sob nenhuma hipótese.

#### Scenario: Tentativa de listar veículos de outro usuário
- **WHEN** o usuário autenticado requisita a listagem de veículos
- **THEN** o sistema retorna exclusivamente os veículos vinculados ao seu próprio `user_id = auth.id`, nunca exibindo veículos de terceiros

#### Scenario: Tentativa de acessar, editar ou excluir veículo de outro usuário
- **WHEN** o usuário tenta ler, editar ou excluir um veículo cujo `user_id` pertence a outro usuário (mesmo conhecendo o ID do veículo)
- **THEN** o sistema rejeita a operação com erro de acesso negado ou não encontrado (403/404)

### Requirement: Edição de dados do veículo
O sistema SHALL permitir que o usuário edite as informações de um veículo de sua propriedade, validando a titularidade prévia.

#### Scenario: Atualização bem-sucedida de veículo
- **WHEN** o usuário altera os dados (ex: cor ou modelo) de um veículo existente de sua propriedade e salva
- **THEN** os dados são atualizados corretamente no sistema

### Requirement: Exclusão de veículo
O sistema SHALL permitir que o usuário remova um veículo cadastrado de sua propriedade que não possua reservas ativas.

#### Scenario: Exclusão de veículo
- **WHEN** o usuário solicita a exclusão de um de seus veículos
- **THEN** o veículo é removido do sistema após validação de propriedade
