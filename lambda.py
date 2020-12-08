import boto3
import os
import json
import datetime

minutes = os.environ['Period']


iam = boto3.client('iam')

period = datetime.timedelta(minutes=int(minutes))
now = datetime.datetime.now(datetime.timezone.utc)
end = now + period

# Change DateTime format
start_time = now.isoformat('T','seconds').replace('+00:00', 'Z')
end_time = end.isoformat('T','seconds').replace('+00:00', 'Z')

# Create a policy
iam_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "DateGreaterThan": {"aws:CurrentTime": start_time},
                "DateLessThan": {"aws:CurrentTime": end_time}
            }
        }
    ]
}

def lambda_handler(event, context):

  user = event["user"]
  
  iam.put_user_policy(
    UserName=user,
    PolicyName='prd-access-policy',
    PolicyDocument=json.dumps(iam_policy)
  )
  
  response = 'End time is ' + end_time
  
  return response