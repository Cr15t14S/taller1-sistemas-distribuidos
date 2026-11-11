// Inicializacion del Replica Set de 3 miembros con Write Concern majority
rs.initiate({
  _id: "rs-taller",
  members: [
    { _id: 0, host: "100.124.175.89:27017" },
    { _id: 1, host: "100.98.174.25:27017" },
    { _id: 2, host: "100.72.188.70:27017" }
  ]
});
