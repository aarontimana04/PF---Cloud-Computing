import json
import random
from datetime import datetime
import boto3

def lambda_handler(event, context):
    # Generar datos aleatorios para la tarea ficticia
    task_id = str(random.randint(2505, 2510))  # Generar un ID de tarea aleatorio de 4 dígitos
    tenant_id = "CS" + task_id
    tarea_id = "T-"+str(random.randint(1, 10))
    now = datetime.now()
    descripcion = f"Tarea Final del curso {tenant_id}."
    task_status = random.choice(['Pendiente', 'En Progreso', 'Completada'])  # Estado aleatorio para la tarea
    fecha_hora = str(now.date()) + "." + str(now.time())

    asignacion = {
        'tenant_id': tenant_id,
        'tarea_id': tarea_id,
        'fecha_creacion': fecha_hora,
        'descripcion': descripcion,
        'status': task_status
    }
    
    print(asignacion)  # Para logs en Cloud Watch

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:864755325173:NuevaTarea',
        Subject='Nueva Tarea Creada',
        Message=json.dumps(asignacion),
        MessageAttributes={
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id},
            'tarea_id': {'DataType': 'String', 'StringValue': tarea_id},
            'fecha_creacion': {'DataType': 'String', 'StringValue': fecha_hora},
            'descripcion': {'DataType': 'String', 'StringValue': descripcion},
            'status': {'DataType': 'String', 'StringValue': task_status}
        }
    )
    
    return {
        'statusCode': 200,
        'body': response_sns
    }
