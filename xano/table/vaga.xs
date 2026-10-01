table vaga {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text numero filters=trim
    enum tipo {
      values = ["carro", "moto", "pcd", "eletrico"]
    }
    enum status {
      values = ["livre", "ocupada", "reservada"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "numero", op: "asc"}]}
  ]

  tags = ["parking-management"]
  guid = "vaga-table-guid-001"
}
