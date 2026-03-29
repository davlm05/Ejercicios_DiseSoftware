const { v4: uuidv4 } = require('uuid');

class Parte {
  constructor({ id, nombre, tipo, precio }) {
    this.id = id || uuidv4();
    this.nombre = nombre;
    this.tipo = tipo;
    this.precio = precio;
  }
}

module.exports = Parte;
