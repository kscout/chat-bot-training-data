import ibm_watson
import os
import logging

# Configuring IBM-Watson Assistant
service = ibm_watson.AssistantV1(
    version='2019-02-28',
    iam_apikey=os.environ['API_KEY'],
)
