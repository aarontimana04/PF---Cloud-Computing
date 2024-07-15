import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    asignacion = json.loads(body['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_tareas')
    response = table.put_item(Item=asignacion)
    print(asignacion) # Para logs en Cloud Watch
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
