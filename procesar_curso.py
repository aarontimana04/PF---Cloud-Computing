import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    table_name = 't_cursos'

    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            message = json.loads(body['Message'])
            action = message['action']
            tenant_id = message['tenant_id']
            curso_id = message['curso_id']
            curso_data = message.get('curso_data', {})

            table = dynamodb.Table(f'{table_name}')

            if action == 'post':
                # Crear un nuevo curso
                curso = {
                    'tenant_id': tenant_id,
                    'curso_id': curso_id,
                    'curso_data': curso_data
                }
                response = table.put_item(Item=curso)
                message_subject = f'Procesado Nuevo Curso: {curso_data["nombre"]}'
                message_body = (
                    f"Tenant ID: {tenant_id}\n"
                    f"Curso ID: {curso_id}\n"
                    f"Nombre del Curso: {curso_data['nombre']}\n"
                    f"Profesor: {curso_data.get('profesor', '')}\n"
                    f"Sección: {curso_data.get('seccion', '')}\n"
                    f"ACL: {curso_data.get('ACL', '')}\n"
                    f"Nota: {curso_data.get('Nota', '')}"
                )

            elif action == 'put':
                # Actualizar un curso existente
                # Verificar si el curso existe antes de actualizar
                response_get = table.get_item(
                    Key={
                        'tenant_id': tenant_id,
                        'curso_id': curso_id
                    }
                )
                if 'Item' not in response_get:
                    raise ValueError(f'Curso {curso_id} not found.')

                response = table.update_item(
                    Key={
                        'tenant_id': tenant_id,
                        'curso_id': curso_id
                    },
                    UpdateExpression="set curso_data=:curso_data",
                    ExpressionAttributeValues={
                        ':curso_data': curso_data
                    },
                    ReturnValues="UPDATED_NEW"
                )
                message_subject = f'Procesado Curso a Actualizar: {curso_data["nombre"]}'
                message_body = (
                    f"Tenant ID: {tenant_id}\n"
                    f"Curso ID: {curso_id}\n"
                    f"Nombre del Curso: {curso_data['nombre']}\n"
                    f"Profesor: {curso_data.get('profesor', '')}\n"
                    f"Sección: {curso_data.get('seccion', '')}\n"
                    f"ACL: {curso_data.get('ACL', '')}\n"
                    f"Nota: {curso_data.get('Nota', '')}"
                )

            elif action == 'delete':
                # Eliminar un curso
                # Verificar si el curso existe antes de eliminar
                response_get = table.get_item(
                    Key={
                        'tenant_id': tenant_id,
                        'curso_id': curso_id
                    }
                )
                if 'Item' not in response_get:
                    raise ValueError(f'Curso {curso_id} not found.')

                response = table.delete_item(
                    Key={
                        'tenant_id': tenant_id,
                        'curso_id': curso_id
                    }
                )
                message_subject = f'Procesado Curso a Eliminar: {curso_id}'
                message_body = (
                    f"Tenant ID: {tenant_id}\n"
                    f"Curso ID: {curso_id}\n"
                    f"Nombre del Curso: {curso_data.get('nombre', '')}"
                )

            else:
                return {
                    'statusCode': 400,
                    'message': 'Invalid action'
                }

            # Publicar en SNS DetallesCursoProcesado
            response_sns = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:864755325173:DetallesCursoProcesado',
                Subject=message_subject,
                Message=message_body,
                MessageAttributes={
                    'tenant_id': {'DataType': 'String', 'StringValue': tenant_id}
                }
            )
            print(response_sns)

        except ClientError as e:
            print(f'Error processing record: {e}')
            return {
                'statusCode': 500,
                'message': str(e)
            }
        except ValueError as ve:
            print(f'Error: {ve}')
            return {
                'statusCode': 404,
                'message': str(ve)
            }

    return {
        'statusCode': 200,
        'message': 'Curso processed successfully'
    }
