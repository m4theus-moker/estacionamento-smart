query "tarifa" verb=POST {
  api_group = "Parking Management"
  auth = "user"

  input {
    enum tipo_vaga {
      values = ["carro", "moto", "pcd", "eletrico"]
    }
    decimal valor_hora
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record

    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem gerenciar tarifas."
    }

    db.get tarifa {
      field_name = "tipo_vaga"
      field_value = $input.tipo_vaga
    } as $existing

    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Já existe uma tarifa cadastrada para este tipo de vaga."
    }

    db.add tarifa {
      data = {
        created_at: "now"
        tipo_vaga : $input.tipo_vaga
        valor_hora: $input.valor_hora
      }
    } as $tarifa
  }

  response = $tarifa
  tags = ["parking-management"]
  guid = "tarifa-post-guid-001"
}
