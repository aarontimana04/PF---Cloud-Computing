import json
import random
from datetime import datetime
import boto3

def lambda_handler(event, context):
    # Generar datos aleatorios para la tarea ficticia
    task_id = str(random.randint(1000, 9999))  # Generar un ID de tarea aleatorio de 4 dígitos
    task_name = f"Tarea {task_id}"  # Nombre de la tarea basado en el ID generado
    task_description = f"Descripción de la Tarea {task_id}"  # Descripción de la tarea basada en el ID generado
    task_status = random.choice(['Pendiente', 'En Progreso', 'Completada'])  # Estado aleatorio para la tarea
    
    # Generar una marca de tiempo para la creación de la tarea
    now = datetime.now()
    created_at = str(now.date()) + "." + str(now.time())
    
    # Crear el objeto de tarea
    task_object = {
        'task_id': task_id,
        'task_name': task_name,
        'task_description': task_description,
        'task_status': task_status,
        'created_at': created_at
    }
    
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:864755325173:NuevaTarea',  # ARN del tema SNS para tareas
        Subject='Nueva Tarea Creada',
        Message=json.dumps(task_object),
        MessageAttributes={
            'task_id': {'DataType': 'String', 'StringValue': task_id},
            'task_name': {'DataType': 'String', 'StringValue': task_name},
            'task_status': {'DataType': 'String', 'StringValue': task_status}
        }
    )
    
    # Retornar la respuesta
    return {
        'statusCode': 200,
        'body': response_sns
    }
