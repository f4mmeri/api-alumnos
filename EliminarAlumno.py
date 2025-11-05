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

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    result = table.delete_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
        ConditionExpression=Attr('alumno_id').exists(),
        ReturnValues="ALL_OLD"
    )

    if 'Attributes' not in result:
        return {'statusCode': 404, 'error': 'Alumno no encontrado'}

    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'deleted': result['Attributes']
    }
