# Proposal

## Why

O sistema atual de gerenciamento de estacionamento precisa implementar a gestão completa de vagas e tarifas para viabilizar o MVP. Sem o controle estruturado de vagas (por tipo: carro, moto, PCD, elétrico) e tarifas associadas, não é possível realizar reservas inteligentes nem calcular automaticamente os valores devidos pelo tempo de permanência real dos veículos. O modelo de usuário no Xano já possui o campo `role` (admin/cliente), permitindo aplicar corretamente o controle de acesso.

## What Changes

- Implementar o modelo de dados e endpoints no Xano para o cadastro e gestão de Vagas (número único, tipo, status inicial "livre", editável pelo admin), com restrição de duplicidade de número de vaga.
- Implementar o modelo de dados e endpoints no Xano para a gestão de Tarifas (valor por hora único por `tipo_vaga`), com restrição de duplicidade de tarifa para o mesmo tipo.
- Aplicar validação de controle de acesso nos endpoints para garantir que apenas administradores possam criar, editar ou remover vagas e tarifas (clientes recebem acesso negado).
- Criar as telas e componentes no Reflex (frontend) para o Administrador gerenciar vagas e tarifas com atualização sob demanda (ao abrir a tela e após cada ação).
- Criar a interface no Reflex para o Cliente consultar a disponibilidade de vagas (atualização sob demanda).

## Capabilities

### New Capabilities
- `parking-management`: Gerenciamento de vagas e tarifas do estacionamento, abrangendo cadastro de vagas por tipo, controle de status (livre, ocupada, reservada - editável pelo admin nesta change), e definição de tarifa única por hora para cada `tipo_vaga`.

### Modified Capabilities
- 

## Impact

- Banco de dados Xano: adição/atualização das tabelas de vagas e tarifas.
- Endpoints de API Xano para CRUD de vagas e tarifas com validação de perfil (admin/cliente) e restrições de duplicidade.
- Frontend Reflex: novas páginas e componentes administrativos e de consulta para clientes com atualização sob demanda.
