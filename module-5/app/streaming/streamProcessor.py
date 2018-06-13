from __future__ import print_function

import base64

import json

import requests

def retrieveMysfit(mysfitId):
    apiEndpoint = 'REPLACE_ME' + str(mysfitId)
    mysfit = requests.get(apiEndpoint).json()
    return mysfit

def processRecord(event, context):
    output = []

    for record in event['records']:
        print('Processing record: ' + record['recordId'])
        click = json.loads(base64.b64decode(record['data']))

        mysfitId = click['mysfitId']
        mysfit = retrieveMysfit(mysfitId)

        enrichedClick = {
                'userId': click['userId'],
                'mysfitId': mysfitId,
                'alignment': mysfit['alignment'],
                'species': mysfit['species']
            }

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(enrichedClick).encode('utf-8') + b'\n').decode('utf-8')
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
