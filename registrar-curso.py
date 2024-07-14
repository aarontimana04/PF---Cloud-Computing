import json
import boto3

def lambda_handler(event, context):
    try:
        action = event['action']
        tenant_id = event['tenant_id']
        curso_id = event['curso_id']
        curso_data = event['curso_data']

        # Lógica para manejar las acciones (post, put, delete)
        if action == 'post':
            message_subject = f'Registrado Nuevo Curso: {curso_data["nombre"]}'
            message_action = 'post'
        elif action == 'put':
            message_subject = f'Registrado Curso a Actualizar: {curso_data["nombre"]}'
            message_action = 'put'
        elif action == 'delete':
            message_subject = f'Registrado Curso a Eliminar: {curso_id}'
            message_action = 'delete'
        else:
            return {
                'statusCode': 400,
                'message': 'Invalid action'
            }

        # Publicar en SNS
        sns_client = boto3.client('sns')
        message = {
            'action': message_action,
            'tenant_id': tenant_id,
            'curso_id': curso_id,
            'curso_data': curso_data
        }
        response_sns = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:864755325173:DetallesCursoRegistrado',
            Subject=message_subject,
            Message=json.dumps(message),
            MessageAttributes={
                'tenant_id': {'DataType': 'String', 'StringValue': tenant_id }
            }
        )
        print(response_sns)

        return {
            'statusCode': 200,
            'message': f'Curso {action} processed successfully',
            'snsResponse': response_sns
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }
