const parteService = require('../business/parte.service');

module.exports.handler = async (event) => {
  try {
    const data = JSON.parse(event.body);
    const parte = await parteService.crearParte(data);
    
    return {
      statusCode: 201,
      body: JSON.stringify({
        message: 'Parte de motocicleta registrada exitosamente',
        parte
      }),
    };
  } catch (error) {
    return {
      statusCode: 400,
      body: JSON.stringify({
        message: error.message
      }),
    };
  }
};
