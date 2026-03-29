const Parte = require('../model/parte.model');
const parteRepository = require('../repositories/parte.repository');

class ParteService {
  async crearParte(data) {
    if (!data.nombre || !data.tipo || !data.precio) {
      throw new Error('Informacion incompleta. Se requiere nombre, tipo y precio.');
    }
    
    const nuevaParte = new Parte(data);
    await parteRepository.save(nuevaParte);
    return nuevaParte;
  }

  async obtenerPartesPorTipo(tipo) {
    if (!tipo) {
      throw new Error('Se requiere especificar la categoria o tipo mediante param.');
    }
    return await parteRepository.findByTipo(tipo);
  }
}

module.exports = new ParteService();
