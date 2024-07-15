import json
import boto3

def lambda_handler(event, context):
    # Obtener el mensaje del evento de SNS
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    
    # Extraer los datos relevantes del mensaje
    tenant_id = sns_message['tenant_id']
    tarea_id = sns_message['task_id']  # asumiendo que el ID de la tarea es 'task_id' en el mensaje
    
    # Guardar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_tareas')  # Nombre de la tabla DynamoDB
    
    # Crear el objeto de tarea para guardar en DynamoDB
    task_item = {
        'tenant_id': tenant_id,
        'tarea_id': tarea_id
    }
    
    # Escribir en la tabla DynamoDB
    response = table.put_item(Item=task_item)
    
    # Retornar la respuesta
    return {
        'statusCode': 200,
        'body': json.dumps('Tarea guardada en DynamoDB')
    }
