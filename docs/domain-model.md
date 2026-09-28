# Domain Model — Estacionamento Smart

Este documento descreve os conceitos fundamentais do domínio e como eles se relacionam. Ele é conceitual: não define tabelas nem colunas — isso é responsabilidade da implementação física de cada change.

## Visão geral dos relacionamentos

```text
Usuario
   │
   ├── Veiculo
   │
   └── Reserva ──── Veiculo
           │
           ├── Vaga
           │
           └── Estacionamento (registro de uso real)

Vaga ──── Tarifa (por tipo de vaga/veículo)
```

## Usuário

Representa qualquer pessoa que acessa o sistema — cliente ou administrador.

**Responsabilidade:** autenticação e identificação de quem realiza cada ação (reserva, cadastro, gestão).

**Principais informações conceituais:** nome, e-mail, credencial de acesso, tipo (cliente ou administrador).

**Relacionamentos:** um usuário pode possuir vários veículos; um usuário (cliente) pode fazer várias reservas.

## Veículo

Representa um veículo pertencente a um usuário.

**Responsabilidade:** identificar o que será estacionado e vinculá-lo a um dono.

**Principais informações conceituais:** placa, modelo, cor.

**Relacionamentos:** um veículo pertence a um único usuário; um veículo pode estar associado a várias reservas ao longo do tempo.

## Vaga

Representa um espaço físico do estacionamento.

**Responsabilidade:** representar disponibilidade e características do espaço (tipo, status).

**Principais informações conceituais:** número/identificação, tipo (carro, moto, PCD, elétrico), status (livre, ocupada, reservada).

**Relacionamentos:** uma vaga pode ter várias reservas ao longo do tempo (nunca duas simultâneas para o mesmo período); uma vaga está associada a uma tarifa conforme seu tipo.

## Reserva

Representa a intenção de uso de uma vaga por um usuário, em um período determinado.

**Responsabilidade:** conectar usuário, veículo e vaga para um intervalo de tempo, evitando conflitos entre reservas.

**Principais informações conceituais:** período previsto de entrada e saída, status (ativa, concluída, cancelada).

**Relacionamentos:** uma reserva pertence a um usuário, refere-se a um veículo e a uma vaga; uma reserva concluída origina um registro em Estacionamento.

**Regra estrutural importante:** duas reservas não podem se sobrepor para a mesma vaga no mesmo intervalo de tempo.

## Estacionamento (uso real)

Representa o uso efetivo de uma vaga — o que de fato aconteceu, em contraste com o que foi reservado.

**Responsabilidade:** registrar entrada e saída reais e o valor final cobrado.

**Principais informações conceituais:** horário real de entrada, horário real de saída, valor cobrado.

**Relacionamentos:** um registro de Estacionamento está associado a uma Reserva (quando existente) ou pode ser originado diretamente de uma entrada sem reserva prévia, dependendo da funcionalidade implementada.

**Regra estrutural importante:** o valor cobrado é sempre calculado a partir do tempo de permanência real, nunca do tempo reservado.

## Tarifa

Representa o valor cobrado por tipo de vaga/veículo.

**Responsabilidade:** fornecer a base de cálculo para o valor do Estacionamento.

**Principais informações conceituais:** tipo de veículo/vaga associado, valor por hora (podendo evoluir para regras como primeira hora, hora adicional e diária).

**Relacionamentos:** uma tarifa se aplica a um tipo de vaga; um tipo de vaga tem uma tarifa vigente por vez.

## Conceitos previstos para etapas futuras (fora do MVP)

- **Mensalista**: plano recorrente (mensal, semestral, anual) associado a um usuário, podendo garantir vaga reservada ou acesso preferencial.
- **Previsão de lotação**: estimativa de ocupação futura derivada do histórico de Estacionamento.

Esses conceitos não devem ser implementados no MVP, mas o modelo já os reconhece para evitar decisões incompatíveis mais adiante.
