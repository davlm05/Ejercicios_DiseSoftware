const AWS = require('aws-sdk');

// Configuracion para emulador local de DynamoDB
const buildDynamoDbClient = () => {
  if (process.env.IS_OFFLINE) {
    return new AWS.DynamoDB.DocumentClient({
      region: 'localhost',
      endpoint: 'http://localhost:8000',
      accessKeyId: 'DEFAULT_ACCESS_KEY', 
      secretAccessKey: 'DEFAULT_SECRET' 
    });
  }
  return new AWS.DynamoDB.DocumentClient();
};

const dynamoDb = buildDynamoDbClient();
const TableName = process.env.PARTES_TABLE;

class ParteRepository {
  async save(parte) {
    const params = {
      TableName,
      Item: parte
    };
    await dynamoDb.put(params).promise();
    return parte;
  }

  async findByTipo(tipo) {
    const params = {
      TableName,
      IndexName: 'TipoIndex',
      KeyConditionExpression: 'tipo = :tipo',
      ExpressionAttributeValues: {
        ':tipo': tipo,
      },
    };
    
    const result = await dynamoDb.query(params).promise();
    return result.Items;
  }
}

module.exports = new ParteRepository();
