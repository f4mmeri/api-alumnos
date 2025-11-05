import boto3
import json
from boto3.dynamodb.conditions import Attr

def _body(event):
    b = event.get("body")
    return b if isinstance(b, dict) else json.loads(b or "{}")

def lambda_handler(event, context):
    print(event)
    body = _body(event)

    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']
    alumno_datos = body['alumno_datos']  # dict con los nuevos datos

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Reemplaza por completo el objeto alumno_datos
    result = table.update_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
        UpdateExpression="SET alumno_datos = :datos",
        ExpressionAttributeValues={":datos": alumno_datos},
        ConditionExpression=Attr('alumno_id').exists(),  # asegura que exista
        ReturnValues="ALL_NEW"
    )

    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'updated': result['Attributes']
    }
