import boto3
import json
import logging
from collections import defaultdict

client = boto3.client('dynamodb')

def getAllMysfits():
    
    #retrieve Mysfits from DynamoDB
    response = client.scan(
        TableName='MysfitsTable'
    )
    
    logging.info(response["Items"])
    
    mysfitList = defaultdict(list)
    for item in response["Items"]:
        mysfit = {}
        mysfit["mysfitId"] = item["MysfitId"]["S"] 
        mysfit["name"] = item["Name"]["S"]
        mysfit["age"] = int(item["Age"]["N"])
        mysfit["alignment"] = item["Alignment"]["S"]
        mysfit["species"] = item["Species"]["S"]
        mysfit["description"] = item["Description"]["S"]
        mysfit["thumbImageUri"] = item["ThumbImageUri"]["S"]
        mysfit["profileImageUri"] = item["ProfileImageUri"]["S"]
        mysfitList["mysfits"].append(mysfit)
        
    return json.dumps(mysfitList)
    
def queryMysfits(queryParam):
    
    logging.info("Here.")
    logging.info(json.dumps(queryParam))
    
    response = client.query(
        TableName='MysfitsTable',
        IndexName=queryParam['filter']+'Index',
        KeyConditions={
            queryParam['filter']: {
                'AttributeValueList': [
                    {
                        'S': queryParam['value']    
                    }
                ],
                'ComparisonOperator': "EQ"
            }
        }
    )
    
    mysfitList = defaultdict(list)
    for item in response["Items"]:
        mysfit = {}
        mysfit["mysfitId"] = item["MysfitId"]["S"] 
        mysfit["name"] = item["Name"]["S"]
        mysfit["age"] = int(item["Age"]["N"])
        mysfit["alignment"] = item["Alignment"]["S"]
        mysfit["species"] = item["Species"]["S"]
        mysfit["description"] = item["Description"]["S"]
        mysfit["thumbImageUri"] = item["ThumbImageUri"]["S"]
        mysfit["profileImageUri"] = item["ProfileImageUri"]["S"]
        mysfitList["mysfits"].append(mysfit)
        
    return json.dumps(mysfitList)
    
