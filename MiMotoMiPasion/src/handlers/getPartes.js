const parteService = require('../business/parte.service');

module.exports.handler = async (event) => {
  try {
    const tipo = event.queryStringParameters && event.queryStringParameters.tipo;
    const partes = await parteService.obtenerPartesPorTipo(tipo);
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        partes
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
