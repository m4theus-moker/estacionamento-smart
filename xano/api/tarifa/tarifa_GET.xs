query "tarifa" verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
  }

  stack {
    db.query tarifa {
      return = {type: "list"}
    } as $tarifas
  }

  response = $tarifas
  tags = ["parking-management"]
  guid = "tarifa-get-guid-001"
}
