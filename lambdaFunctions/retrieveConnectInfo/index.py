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

    #KeyConditionExpression uses customer phone nomber to retrieve information
    #from a DynamoDB table and saves it to response.
    response = table.query(
        KeyConditionExpression=Key('PhoneNumber').eq(callerID)
    )

    #Required when troubleshooting
    #print("============================")
    #print(json.dumps(response, indent=4))
    #print("============================")

    #Check for u'Count' existing with a 1 value within the DynamoDB indicating the
    #resource exists.
    if 1 in response.values():
        #Sets Key:Value Pair needed for proper Connect handling
        #"customerContactFlow": response['Items'][0]['contactFlow']
        userReturn = {
            "customerContactFlow": getDynamoAtt(response, "contactFlow"),
            "firstName": getDynamoAtt(response, "firstName"),
            "lastName": getDynamoAtt(response, "lastName"),
            "sentiment": getDynamoAtt(response, "sentiment"),
            "product": getDynamoAtt(response, "product"),
            "assignedQueue": getDynamoAtt(response, "assignedQueue"),
            "assignedContactFlow": getDynamoAtt(response, "assignedContactFlow")
        }

        print(json.dumps(userReturn, indent=4))
    else:
        # Defaults
        userReturn = {
            "customerContactFlow": "arn:arn:arn",
            "firstName": "",
            "lastName": "",
            "sentiment": "",
            "product": "",
            "assignedQueue": "",
            "assignedContactFlow": ""
        }

    #Return to Connect our key/value combo
    return userReturn


#Helper function to validate the DynamoDB table contains the specific key
def getDynamoAtt(response, attribute):
    shortPath = response['Items'][0]
    if attribute in response['Items'][0]:
        return shortPath[attribute]
    else:
        return ""
