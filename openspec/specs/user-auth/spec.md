# user-auth Specification

## Purpose
Gerencia o cadastro, autenticação e sessão de usuários (clientes e administradores) no sistema Estacionamento Smart, garantindo a segurança e o controle de acesso por papéis em todas as interações.

## Requirements

### Requirement: Cadastro de Usuário
O sistema SHALL permitir que novos usuários se cadastrem informando nome, e-mail único e senha válida, atribuindo o papel padrão de cliente.

#### Scenario: Cadastro bem-sucedido
- **WHEN** um novo usuário submete nome, e-mail válido e senha que atende aos requisitos mínimos
- **THEN** o sistema cria o registro do usuário no backend, atribui o papel de cliente e retorna um token de autenticação válido

#### Scenario: Tentativa de cadastro com e-mail duplicado
- **WHEN** um usuário tenta se cadastrar com um e-mail já cadastrado
- **THEN** o sistema rejeita a operação com erro de e-mail já cadastrado (conflito) e não cria um novo registro

### Requirement: Autenticação e Login
O sistema SHALL autenticar usuários cadastrados por meio de e-mail e senha, emitindo um token de acesso válido por tempo determinado.

#### Scenario: Login bem-sucedido
- **WHEN** o usuário fornece credenciais corretas (e-mail e senha)
- **THEN** o sistema valida as credenciais e retorna um token de autenticação JWT e o identificador do usuário

#### Scenario: Login com credenciais inválidas
- **WHEN** o usuário fornece e-mail inexistente ou senha incorreta
- **THEN** o sistema rejeita o acesso com erro de credenciais inválidas

### Requirement: Sessão e Obtenção de Dados do Usuário
O sistema SHALL permitir que o usuário autenticado obtenha seus dados de perfil e papel utilizando seu token de acesso.

#### Scenario: Consulta de perfil autenticado
- **WHEN** uma requisição válida contendo o token de autenticação é enviada ao endpoint de dados do usuário
- **THEN** o sistema retorna os dados do usuário, incluindo seu papel (`cliente` ou `administrador`)

#### Scenario: Consulta de perfil sem autenticação
- **WHEN** uma requisição sem token ou com token inválido/expirado é realizada
- **THEN** o sistema nega o acesso com erro de autenticação
