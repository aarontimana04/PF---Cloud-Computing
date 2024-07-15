import json
import boto3

def lambda_handler(event, context):
    # Verificar si hay registros en el evento
    if 'Records' in event and len(event['Records']) > 0:
        # Extraer el mensaje del evento SNS
        sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        
        # Obtener tenant_id y archivo_id del mensaje
        tenant_id = sns_message.get('tenant_id', '')
        archivo_id = sns_message.get('archivo_id', '')

        # Si se obtienen los valores necesarios
        if tenant_id and archivo_id:
            # Conectar con DynamoDB y escribir en la tabla t_archivos
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('t_archivos')
            
            # Preparar el item a insertar
            archivo = {
                'tenant_id': tenant_id,
                'archivo_id': str(archivo_id)  # Convertir archivo_id a string si es necesario
            }
            
            # Insertar el registro en la tabla t_archivos
            response = table.put_item(Item=archivo)
            
            # Imprimir la respuesta (opcional)
            print("Registro insertado en la tabla t_archivos:", response)
            
            # Retornar una respuesta de éxito
            return {
                'statusCode': 200,
                'body': json.dumps("Registro insertado correctamente en t_archivos")
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("Faltan datos necesarios en el mensaje SNS")
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("No se encontraron registros en el evento SNS")
        }
