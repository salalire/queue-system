from apps.queues.models import QueueEntry
import json
import http.client
from django.conf import settings
import re
from infobip_api_client.api.sms_api import SmsApi
from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.models import SmsRequest, SmsMessage, SmsDestination, SmsTextContent, SmsMessageContent

def clean_phone_number(phone):
    clean_number = re.sub(r'\D', '', str(phone))
    
    if clean_number.startswith('0'):
        clean_number = '251' + clean_number[1:]
    elif len(clean_number) == 9:
        clean_number = '251' + clean_number
        
    return clean_number

def calculate_wait_time(service, position):
    completed = QueueEntry.objects.filter(
        service=service,
        status='done',
        completed_at__isnull=False,
        started_at__isnull=False
    ).order_by('-completed_at')[:5]

    if completed.exists():
        total_time = 0
        for entry in completed:
            duration = (entry.completed_at - entry.started_at).total_seconds() / 60
            total_time += duration

        avg_time = total_time / len(completed)
    else:
        avg_time = service.avg_service_time

    return int(position * avg_time)

def send_sms(phone_number, message_text):
    
    client_config = Configuration(
        host = settings.INFOBIP_BASE_URL.replace("https://", ""),
        api_key = {"APIKeyHeader": f"App {settings.INFOBIP_API_KEY}"}
    )
    api_client = ApiClient(client_config)
    sms_api = SmsApi(api_client)

    destination = SmsDestination(to=clean_phone_number(phone_number))
    message = SmsMessage(
        destinations=[destination],
        sender="QueueApp",
        content=SmsMessageContent(
            actual_instance=SmsTextContent(text=message_text)
        )
    )
    request = SmsRequest(messages=[message])
   
    try:
        response = sms_api.send_sms_messages(sms_request=request)
        return True
    except Exception as e:
        print(f"Global SMS Error: {e}")
        return False