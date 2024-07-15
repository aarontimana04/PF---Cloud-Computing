import json
import boto3

def lambda_handler(event, context):
    # Obtener el tenant_id y archivo_id del response de Rekognition
    client = boto3.client("rekognition")
    response = client.detect_labels(
        Image={"S3Object": {"Bucket": "archivos-aaron04", "Name": "A2.jpg"}}, #cambiar en cada ejecucion
        MaxLabels=3,
        MinConfidence=80
    )
    
    # Extraer los valores necesarios del response de Rekognition
    name = response['Labels'][0]['Name']  # Tomar el nombre de la primera etiqueta
    confidence = response['Labels'][0]['Confidence']  # Tomar la confianza de la primera etiqueta
    
    # Preparar el mensaje para enviar al SNS
    sns_message = {
        "tenant_id": name,
        "archivo_id": confidence
    }
    
    # Enviar el mensaje al SNS
    sns_client = boto3.client('sns')
    sns_response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:864755325173:DetallesArchivos',
        Message=json.dumps({'default': json.dumps(sns_message)}),
        MessageStructure='json'
    )
    
    # Si se quiere verificar la respuesta del SNS
    print("Mensaje enviado al SNS:", sns_response)
    
    # Retornar una respuesta HTTP 200
    return {
        'statusCode': 200,
        'body': json.dumps("Correcto")
    }
