#import the Python packages for Lambda to use
import boto3
import json
import os
from boto3.dynamodb.conditions import Key, Attr

#start our Lambda runtime here
def lambda_handler(event,context):

    #Retrieve the customer phone number from the trigger Event
    callerID = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]

    #Establish connection to dynamoDB and retrieve table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    #KeyConditionExpression looks for number that equals ANI of inbound call from a dynamoDB table and saves it to response
    response = table.query(
        KeyConditionExpression=Key('PhoneNumber').eq(callerID)
    )

    #Required when troubleshooting
    #print("============================")
    #print(json.dumps(response, indent=4))
    #print("============================")

    #Check for u'Count' existing with a 1 value within the DynamoDB indicating a blocked record exists
    if 1 in response.values():
        #Sets Key:Value Pair needed for proper Connect handling
        userReturn = {
            "customerContactFlow": response['Items'][0]['contactFlow']
        }
        print(json.dumps(userReturn, indent=4))
    else:
        #Sets Key:Value Pair needed for proper Connect handling
        userReturn = {
            "customerContactFlow": "arn:arn:arn"
        }

    #Return to Connect our key/value combo
    return userReturn


def addTags(tts):
    if tts.startswith("<speak>"):
        return tts
    else:
        return "<speak>" + tts + "</speak>"
