import json
import random

# Global variable to hold the value
value = 100.0

def lambda_handler(event, context):
    global value
    # Update value by +/-1%
    value = value * (1 + random.uniform(-0.01, 0.01))
    
    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "updated_value": value
        })
    }
    return response
