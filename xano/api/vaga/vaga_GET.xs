query "vaga" verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
  }

  stack {
    db.query vaga {
      return = {type: "list"}
    } as $vagas
  }

  response = $vagas
  tags = ["parking-management"]
  guid = "vaga-get-guid-001"
}
