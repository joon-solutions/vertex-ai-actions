import requests
import json
import os
import base64
import utils
import re

from datetime import datetime
from flask import request, Response, redirect
from dotenv import load_dotenv

load_dotenv()



BASE_DOMAIN = f"https://{os.environ.get('REGION')}-{os.environ.get('PROJECT')}.cloudfunctions.net/{os.environ.get('ACTION_NAME')}-"

# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint
def salesforce_action_list(request):
    """Return action hub list endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth

    response = {
        'label': 'POC Action Hub',
        'integrations': [
            {
                'name': os.environ.get('ACTION_NAME'),
                'label': os.environ.get('ACTION_LABEL'),
                'supported_action_types': ['query', 'cell', 'dashboard'],
                "icon_data_uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVQ4jaXTL0vDURjF8c/zQ0RETCJG2RbE4GsYJjGbDT+LwVdgFLOYBfcCjGI2GUxiMI2tGERERERERHwMczD/4rYDF275nuce7nkiM8MQKoaBYaR7if3WCFERWSGauJQIE+RLlrWnnwwiMyMa7VFsYQPjeEQDk1jEFXZwiFE8Z1l97TVYko7En5HucYIpNGXu5lrtvGuwjc0+41+j3p141ycMM1gvotGe1ck+gHK+wApmBzOIiwJjg8FusFfgCA//hG5xjgNyOctqs/sLdZRY+Di9usZrB85N4hSPn3oAsd8qUBFxiLmeias40ynPt5fG12WKRnsaSzqNPEYry+rbb5m+GfSrobfxHWu4YtTFW9MMAAAAAElFTkSuQmCC",
                'form_url': BASE_DOMAIN + 'form',
                'url': BASE_DOMAIN + 'execute',
                'supported_formats': ['json', 'csv_zip'],
                'required_fields': [{"any_tag": ["sfdc_lead_id"]}],
                'supported_formattings': ['formatted'],
                'supported_visualization_formattings': ['noapply'],
                'params': [
                    {
                        'description': "Salesforce domain name, e.g. https://MyDomainName.my.salesforce.com",
                        'label': "Salesforce domain",
                        'name': "salesforce_domain",
                        'required': True,
                        'sensitive': False
                    }
                ],
                'uses_oauth': True
            },
            {
                'name': 'salesforce-post-creator-poc',
                'label': 'Post',
                'supported_action_types': ['query', 'cell', 'dashboard'],
                "icon_data_uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVQ4jaXTL0vDURjF8c/zQ0RETCJG2RbE4GsYJjGbDT+LwVdgFLOYBfcCjGI2GUxiMI2tGERERERERHwMczD/4rYDF275nuce7nkiM8MQKoaBYaR7if3WCFERWSGauJQIE+RLlrWnnwwiMyMa7VFsYQPjeEQDk1jEFXZwiFE8Z1l97TVYko7En5HucYIpNGXu5lrtvGuwjc0+41+j3p141ycMM1gvotGe1ck+gHK+wApmBzOIiwJjg8FusFfgCA//hG5xjgNyOctqs/sLdZRY+Di9usZrB85N4hSPn3oAsd8qUBFxiLmeias40ynPt5fG12WKRnsaSzqNPEYry+rbb5m+GfSrobfxHWu4YtTFW9MMAAAAAElFTkSuQmCC",
                'form_url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-post-creator-poc-form',
                'url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-post-creator-poc-execute',
                'supported_formats': ['json', 'csv_zip'],
                'required_fields': [{"any_tag": ["sfdc_lead_id"]}],
                'supported_formattings': ['formatted'],
                'supported_visualization_formattings': ['noapply'],
                'params': [
                    {
                        'description': "Salesforce domain name, e.g. https://MyDomainName.my.salesforce.com",
                        'label': "Salesforce domain",
                        'name': "salesforce_domain",
                        'required': True,
                        'sensitive': False
                    }
                ],
                'uses_oauth': True
            },
            {
                'name': 'salesforce-question-creator-poc',
                'label': 'Question',
                'supported_action_types': ['query', 'cell', 'dashboard'],
                "icon_data_uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVQ4jaXTL0vDURjF8c/zQ0RETCJG2RbE4GsYJjGbDT+LwVdgFLOYBfcCjGI2GUxiMI2tGERERERERHwMczD/4rYDF275nuce7nkiM8MQKoaBYaR7if3WCFERWSGauJQIE+RLlrWnnwwiMyMa7VFsYQPjeEQDk1jEFXZwiFE8Z1l97TVYko7En5HucYIpNGXu5lrtvGuwjc0+41+j3p141ycMM1gvotGe1ck+gHK+wApmBzOIiwJjg8FusFfgCA//hG5xjgNyOctqs/sLdZRY+Di9usZrB85N4hSPn3oAsd8qUBFxiLmeias40ynPt5fG12WKRnsaSzqNPEYry+rbb5m+GfSrobfxHWu4YtTFW9MMAAAAAElFTkSuQmCC",
                'form_url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-question-creator-poc-form',
                'url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-question-creator-poc-execute',
                'supported_formats': ['json', 'csv_zip'],
                'required_fields': [{"any_tag": ["sfdc_lead_id"]}],
                'supported_formattings': ['formatted'],
                'supported_visualization_formattings': ['noapply'],
                'params': [
                    {
                        'description': "Salesforce domain name, e.g. https://MyDomainName.my.salesforce.com",
                        'label': "Salesforce domain",
                        'name': "salesforce_domain",
                        'required': True,
                        'sensitive': False
                    }
                ],
                'uses_oauth': True
            },
            {
                'name': 'salesforce-poll-creator-poc',
                'label': 'Poll',
                'supported_action_types': ['query', 'cell', 'dashboard'],
                "icon_data_uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVQ4jaXTL0vDURjF8c/zQ0RETCJG2RbE4GsYJjGbDT+LwVdgFLOYBfcCjGI2GUxiMI2tGERERERERHwMczD/4rYDF275nuce7nkiM8MQKoaBYaR7if3WCFERWSGauJQIE+RLlrWnnwwiMyMa7VFsYQPjeEQDk1jEFXZwiFE8Z1l97TVYko7En5HucYIpNGXu5lrtvGuwjc0+41+j3p141ycMM1gvotGe1ck+gHK+wApmBzOIiwJjg8FusFfgCA//hG5xjgNyOctqs/sLdZRY+Di9usZrB85N4hSPn3oAsd8qUBFxiLmeias40ynPt5fG12WKRnsaSzqNPEYry+rbb5m+GfSrobfxHWu4YtTFW9MMAAAAAElFTkSuQmCC",
                'form_url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-poll-creator-poc-form',
                'url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-poll-creator-poc-execute',
                'supported_formats': ['json', 'csv_zip'],
                'required_fields': [{"any_tag": ["sfdc_lead_id"]}],
                'supported_formattings': ['formatted'],
                'supported_visualization_formattings': ['noapply'],
                'params': [
                    {
                        'description': "Salesforce domain name, e.g. https://MyDomainName.my.salesforce.com",
                        'label': "Salesforce domain",
                        'name': "salesforce_domain",
                        'required': True,
                        'sensitive': False
                    }
                ],
                'uses_oauth': True
            },
            {
                'name': 'salesforce-task-creator-poc',
                'label': 'New Task',
                'supported_action_types': ['query', 'cell', 'dashboard'],
                "icon_data_uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVQ4jaXTL0vDURjF8c/zQ0RETCJG2RbE4GsYJjGbDT+LwVdgFLOYBfcCjGI2GUxiMI2tGERERERERHwMczD/4rYDF275nuce7nkiM8MQKoaBYaR7if3WCFERWSGauJQIE+RLlrWnnwwiMyMa7VFsYQPjeEQDk1jEFXZwiFE8Z1l97TVYko7En5HucYIpNGXu5lrtvGuwjc0+41+j3p141ycMM1gvotGe1ck+gHK+wApmBzOIiwJjg8FusFfgCA//hG5xjgNyOctqs/sLdZRY+Di9usZrB85N4hSPn3oAsd8qUBFxiLmeias40ynPt5fG12WKRnsaSzqNPEYry+rbb5m+GfSrobfxHWu4YtTFW9MMAAAAAElFTkSuQmCC",
                'form_url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-task-creator-poc-form',
                'url': 'https://asia-southeast1-joon-sandbox.cloudfunctions.net/salesforce-task-creator-poc-execute',
                'supported_formats': ['json', 'csv_zip'],
                'required_fields': [{"any_tag": ["sfdc_lead_id"]}],
                'supported_formattings': ['formatted'],
                'supported_visualization_formattings': ['noapply'],
                'params': [
                    {
                        'description': "Salesforce domain name, e.g. https://MyDomainName.my.salesforce.com",
                        'label': "Salesforce domain",
                        'name': "salesforce_domain",
                        'required': True,
                        'sensitive': False
                    }
                ],
                'uses_oauth': True
            }
        ]
    }

    print('returning integrations json')
    return Response(json.dumps(response), status=200, mimetype='application/json')

# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def campaign_form(request):
    """Return form endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    
    request_json = request.get_json()
    data = request_json['data']
    print(data)
    
    field_value = ''

    if 'value' in data:
        field_value = data['value']

    response = [{
            'name': 'campaign_name',
            'label': 'Campaign Name',
            'description': 'Identifying name of the campaign',
            'type': 'text',
            'default': field_value,
            'required': True
        },
            {
            'name': 'start_date',
            'label': 'Start Date',
            'description': "Start date of the campaign (YYYY-MM-DD)",
            'type': 'date',
            'default':  datetime.today().strftime('%Y-%m-%d'),
            'required': True
        },
            {
            'name': 'end_date',
            'label': 'End Date',
            'description': "End date of the campaign (YYYY-MM-DD)",
            'type': 'date',
            'required': True
        },
            {
            'name': 'campaign_status',
            'label': 'Campaign Status',
            'description': "Status of the campaign",
            'type': 'select',
            'required': True,
            'options': [
                {'name': 'planned', 'label': 'Planned'},
                {'name': 'in_progress', 'label': 'In Progress'},
                {'name': 'completed', 'label': 'Completed'}
            ]
        },
            {
            'name': 'campaign_type',
            'label': 'Campaign Type',
            'description': "Type of the campaign",
            'type': 'select',
            'required': True,
            'options': [
                {'name': 'webinar', 'label': 'Webinar'},
                {'name': 'advertisement', 'label': 'Advertisement'},
                {'name': 'email', 'label': 'Email'}
            ]
        }
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')


# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-execute-endpoint
def campaign_execute(request):
    """Process form input and send data to Salesforce to create a new campaign"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    request_json = request.get_json()
    form_params = request_json['form_params']
    print(form_params)

    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    validation_errors = {}
    # form params error handling
    try:
        campaign_name = form_params['campaign_name']
        start_date = form_params['start_date']
        end_date = form_params['end_date']
        campaign_status = form_params['campaign_status']
        campaign_type = form_params['campaign_type']
    except KeyError as e:
        validation_errors[str(e).strip("'")] = "Missing required parameter"
        response = {
                "looker": {
                    "success": False,
                    "validation_errors": {
                    str(e).strip("'"): "Missing required parameter"
                    }
                }
            }
    
    if not bool(re.match(r"^\d{4}-\d{2}-\d{2}$", end_date)):
        validation_errors['end_date'] = "Invalid date format. Please use YYYY-MM-DD format"
    if not bool(re.match(r"^\d{4}-\d{2}-\d{2}$", start_date)):
        validation_errors['start_date'] = "Invalid date format. Please use YYYY-MM-DD format"
    if validation_errors:
        response = {
            "looker": {
                "success": False,
                "validation_errors": validation_errors
            }
        }
        return Response(status=400, mimetype="application/json", response=json.dumps(response))


    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']

    # create campaign via api
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/composite/sobjects"
    payload = json.dumps({
        "allOrNone": False,
        "records": [
            {
                "attributes": {"type": "Campaign"},
                "Name": campaign_name,
                "StartDate" : start_date,
                "EndDate" : end_date,
                "Status" : campaign_status,
                "Type" : campaign_type
            }
        ]
    })

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f'create campaign payload: {payload}')
    print(f'create campaign headers: {headers}')
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    print(f'create campaign response: {response.json()}')
    print(f'create campaign response status: {response.status_code}')
    if response.status_code in [200, 201] and response.json()[0]['success']:
        return Response(status=200, mimetype="application/json")
    else:
        return Response(status=response.status_code, mimetype="application/json", response=json.dumps(response.json()))
    
# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def poll_form(request):
    """Return form endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth

    response = [{
            'name': 'question',
            'label': 'Question',
            'description': "What would you like to add?",
            'type': 'textarea',
            'required': True
        },
            {
            'name': 'choice_1',
            'label': 'Choice 1',
            'type': 'text',
            'required': True
        },
            {
            'name': 'choice_2',
            'label': 'Choice 2',
            'type': 'text',
            'required': True
        }
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')




# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-execute-endpoint
def poll_execute(request):
    """Process form input and send data to Salesforce to create a new campaign"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    request_json = request.get_json()
    form_params = request_json['form_params']
    data = request_json['data']
    
    cell_value = ''

    if 'value' in data:
        cell_value = data['value']
    
    print(form_params)
    print(data)


    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    validation_errors = {}
    # form params error handling
    try:
        question = form_params['question']
        choice_1 = form_params['choice_1']
        choice_2 = form_params['choice_2']
    except KeyError as e:
        validation_errors[str(e).strip("'")] = "Missing required parameter"
        response = {
                "looker": {
                    "success": False,
                    "validation_errors": {
                    str(e).strip("'"): "Missing required parameter"
                    }
                }
            }
    
    if validation_errors:
        response = {
            "looker": {
                "success": False,
                "validation_errors": validation_errors
            }
        }
        return Response(status=400, mimetype="application/json", response=json.dumps(response))


    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']
    
    # create chatter via api
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/chatter/feed-elements/"
    payload = json.dumps(
        {
           "body":{
              "messageSegments":[
                 {
                    "type": "Text",
                    "text": question
                 }
              ]
           },
           "capabilities":{
              "poll":{
                 "choices":[
                    choice_1,
                    choice_2
                 ]
              }
           },
           "feedElementType": "FeedItem",
           "subjectId": cell_value
        }
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f'create chatter payload: {payload}')
    print(f'create chatter headers: {headers}')
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    print(f'create chatter response: {response.json()}')
    print(f'create chatter response status: {response.status_code}')
    if response.status_code in [200, 201]:
        return Response(status=200, mimetype="application/json")
    else:
        return Response(status=response.status_code, mimetype="application/json", response=json.dumps(response.json()))
    
# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def post_form(request):
    """Return form endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth    

    response = [{
            'name': 'content',
            'label': 'Content',
            'description': "Share an update",
            'type': 'textarea',
            'required': True
        }
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')




# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-execute-endpoint
def post_execute(request):
    """Process form input and send data to Salesforce to create a new campaign"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    request_json = request.get_json()
    form_params = request_json['form_params']
    data = request_json['data']
    
    print(form_params)
    print(data)
    
    cell_value = ''

    if 'value' in data:
        cell_value = data['value']
    

    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    validation_errors = {}
    # form params error handling
    try:
        content = form_params['content']
    except KeyError as e:
        validation_errors[str(e).strip("'")] = "Missing required parameter"
        response = {
                "looker": {
                    "success": False,
                    "validation_errors": {
                    str(e).strip("'"): "Missing required parameter"
                    }
                }
            }
    
    if validation_errors:
        response = {
            "looker": {
                "success": False,
                "validation_errors": validation_errors
            }
        }
        return Response(status=400, mimetype="application/json", response=json.dumps(response))


    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']
    
    # create chatter via api
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/chatter/feed-elements/"
    payload = json.dumps(
        { 
           "body" : {
              "messageSegments" : [
                 {
                    "type" : "Text",
                    "text" : content
                 }]
               },
           "feedElementType" : "FeedItem",
           "subjectId" : cell_value
        }
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f'create chatter payload: {payload}')
    print(f'create chatter headers: {headers}')
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    print(f'create chatter response: {response.json()}')
    print(f'create chatter response status: {response.status_code}')
    if response.status_code in [200, 201]:
        return Response(status=200, mimetype="application/json")
    else:
        return Response(status=response.status_code, mimetype="application/json", response=json.dumps(response.json()))
    
# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def question_form(request):
    """Return form endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth

    response = [{
            'name': 'question',
            'label': 'Question',
            'description': "What would you like to know?",
            'type': 'textarea',
            'required': True
        },
            {
            'name': 'detail',
            'label': 'Detail',
            'description': "If you have more to say, add detail here",
            'type': 'textarea',
            'required': True
        },
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')




# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-execute-endpoint
def question_execute(request):
    """Process form input and send data to Salesforce to create a new campaign"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    request_json = request.get_json()
    form_params = request_json['form_params']
    data = request_json['data']
    print(form_params)
    print(data)
    
    cell_value = ''

    if 'value' in data:
        cell_value = data['value']
    

    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    validation_errors = {}
    # form params error handling
    try:
        question = form_params['question']
        detail = form_params['detail']
    except KeyError as e:
        validation_errors[str(e).strip("'")] = "Missing required parameter"
        response = {
                "looker": {
                    "success": False,
                    "validation_errors": {
                    str(e).strip("'"): "Missing required parameter"
                    }
                }
            }
    
    if validation_errors:
        response = {
            "looker": {
                "success": False,
                "validation_errors": validation_errors
            }
        }
        return Response(status=400, mimetype="application/json", response=json.dumps(response))


    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']
    
    # create chatter via api
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/chatter/feed-elements/"
    payload = json.dumps(
        {
           "body":{
              "messageSegments":[
                 {
                    "type":"Text",
                    "text":detail
                 }
              ]
           },
           "capabilities":{
              "questionAndAnswers" : {
                  "questionTitle" : question
                }

           },
           "feedElementType": "FeedItem",
           "subjectId": cell_value
        }
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f'create chatter payload: {payload}')
    print(f'create chatter headers: {headers}')
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    print(f'create chatter response: {response.json()}')
    print(f'create chatter response status: {response.status_code}')
    if response.status_code in [200, 201]:
        return Response(status=200, mimetype="application/json")
    else:
        return Response(status=response.status_code, mimetype="application/json", response=json.dumps(response.json()))
    
# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-form-endpoint
def task_form(request):
    """Return form endpoint data for action"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    
    request_json = request.get_json()
    data = request_json['data']
    print(data)
    
    cell_value = ''

    if 'value' in data:
        cell_value = data['value']
    
    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']

    # get category list
    query = "SELECT Category__c FROM Task WHERE CreatedDate >= LAST_N_MONTHS:3 GROUP BY Category__c"
    url = f"https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/query/?q={query}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_category = requests.request("GET", url, headers=headers)
    if get_category.status_code in [200, 201]:
        category_data = get_category.json()
        category_list = [
            {'name': category['Category__c'], 'label': category['Category__c']}
            for category in category_data['records']
        ]
    else:
        print(f"Error {get_category.status_code}: {get_category.text}")

    #get default name for related object
    query = f"SELECT Name FROM Customer_Group__c WHERE Id = '{cell_value}'"
    url = f"https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/query/?q={query}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_related_object_name = requests.request("GET", url, headers=headers)
    if get_related_object_name.status_code in [200, 201]:
        object_name_record = get_related_object_name.json()
        object_name_data = object_name_record['records']
        object_name = object_name_data[0]['Name']
        default_object_list = [{ "name": cell_value, "label": object_name }]
    else:
        print(f"Error {get_category.status_code}: {get_category.text}")

    #get other object data list
    query = f"SELECT Id, Name FROM Customer_Group__c LIMIT 25"
    url = f"https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/query/?q={query}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_all_object = requests.request("GET", url, headers=headers)
    if get_all_object.status_code in [200, 201]:
        object_data = get_all_object.json()
        object_list = [
            {'name': object['Id'], 'label': object['Name']}
            for object in object_data['records']
        ]
    else:
        print(f"Error {get_all_object.status_code}: {get_all_object.text}")

    #get own user info
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/userinfo"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_user_info = requests.request("GET", url, headers=headers)
    if get_user_info.status_code in [200, 201]:
        user_data = get_user_info.json()
        user_name = user_data['name']
        user_id = user_data['user_id']
        default_owner_list = [{ "name": user_id, "label": user_name }]
    else:
        print(f"Error {get_user_info.status_code}: {get_user_info.text}")

    #get all user info
    query = f"SELECT Id, Name FROM User LIMIT 25"
    url = f"https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/query/?q={query}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_all_user = requests.request("GET", url, headers=headers)
    if get_all_user.status_code in [200, 201]:
        all_user_data = get_all_user.json()
        user_list = [
            {'name': user['Id'], 'label': user['Name']}
            for user in all_user_data['records']
        ]
    else:
        print(f"Error {get_all_user.status_code}: {get_all_user.text}")

    #form configuration
    response = [{
            'name': 'subject',
            'label': 'Subject',
            'type': 'select',
            'required': True,
            'options': [
                {'name': 'Call', 'label': 'Call'},
                {'name': 'Send Letter', 'label': 'Send Letter'},
                {'name': 'Send Quote', 'label': 'Send Quote'},
                {'name': 'Other', 'label': 'Other'}
            ]
        },
            {
            'name': 'category',
            'label': 'Category',
            'type': 'select',
            'required': True,
            'options': category_list
        },
            {
            'name': 'due_date',
            'label': 'Due Date',
            'description': "Format YYYY-MM-DD",
            'type': 'date',
            'required': True
        },
            {
            'name': 'description',
            'label': 'Description',
            'description': "Tip: Type Command + period to insert quick text.",
            'type': 'textarea',
            'required': True
        },
            {
            'name': 'related_to',
            'label': 'Related To',
            'type': 'select',
            'required': True,
            'options': default_object_list + object_list,
            'default': cell_value   
        },
            {
            'name': 'assigned_to',
            'label': 'Assigned To',
            'type': 'select',
            'required': True,
            'options': default_owner_list + user_list,
            'default': user_id
        }
    ]
    print(f'returning form json: {json.dumps(response)}')
    return Response(json.dumps(response), status=200, mimetype='application/json')




# https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#action-execute-endpoint
def task_execute(request):
    """Process form input and send data to Salesforce to create a new campaign"""
    auth = utils.authenticate(request)
    if auth.status_code != 200:
        return auth
    request_json = request.get_json()
    form_params = request_json['form_params']
    print(form_params)

    # get token using username/password
    url = 'https://one-line--ofuat.sandbox.my.salesforce.com/services/oauth2/token'
    client_id = os.environ.get('SALESFORCE_CLIENT_ID')
    client_secret = os.environ.get('SALESFORCE_CLIENT_SECRET')
    username = os.environ.get('SALESFORCE_USERNAME')
    password = os.environ.get('SALESFORCE_PASSWORD')

    validation_errors = {}
    # form params error handling
    try:
        subject = form_params['subject']
        category = form_params['category']
        due_date = form_params['due_date']
        description = form_params['description']
        related_to = form_params['related_to']
        assigned_to = form_params['assigned_to']
    except KeyError as e:
        validation_errors[str(e).strip("'")] = "Missing required parameter"
        response = {
                "looker": {
                    "success": False,
                    "validation_errors": {
                    str(e).strip("'"): "Missing required parameter"
                    }
                }
            }
        
    if not bool(re.match(r"^\d{4}-\d{2}-\d{2}$", due_date)):
        validation_errors['due_date'] = "Invalid date format. Please use YYYY-MM-DD format" 
    if validation_errors:
        response = {
            "looker": {
                "success": False,
                "validation_errors": validation_errors
            }
        }
        return Response(status=400, mimetype="application/json", response=json.dumps(response))


    payload = {'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password}
    headers = {}

    print(f'payload: {payload}')
    response = requests.request("POST", url, headers=headers, data=payload, timeout = 10)
    print(f'response: {response.json()}')
    token = response.json()['access_token']
 
    # create task via api
    url = "https://one-line--ofuat.sandbox.my.salesforce.com/services/data/v63.0/composite/sobjects"
    payload = json.dumps({
        "allOrNone": False,
        "records": [
            {
                "attributes": {"type": "Task"},
                "Subject" : subject,
                "Category__c" : category,
                "ActivityDate":  due_date,
                "Description" : description,
                "WhatId" : related_to,
                "OwnerId" : assigned_to,
                "RecordTypeId":"0122w000001MHouAAG"
            }
        ]
    })

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f'create task payload: {payload}')
    print(f'create task headers: {headers}')
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    print(f'create task response: {response.json()}')
    print(f'create task response status: {response.status_code}')
    if response.status_code in [200, 201] and response.json()[0]['success']:
        return Response(status=200, mimetype="application/json")
    else:
        return Response(status=response.status_code, mimetype="application/json", response=json.dumps(response.json()))