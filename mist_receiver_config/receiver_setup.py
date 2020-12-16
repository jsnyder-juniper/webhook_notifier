#!/usr/bin/env python3
import sys
import time
import MistSystems as Mist
import ngrok_wrapper as NGROK
import os
import signal

def cleanup(signalNumber, frame):
    mist_apikey = os.environ['MIST_API']
    mist_org = os.environ['MIST_ORG']
    webhook_id = os.environ['MIST_WEBHOOK_ID']
    delete_response = Mist.DeleteOrgWebhook(mist_org, webhook_id, mist_apikey)
    print(delete_response.json())
    sys.exit(0)


def main():
    time.sleep(10)
    mist_apikey = os.environ['MIST_API']
    mist_org = os.environ['MIST_ORG']
    notify_type = os.environ['NOTIFY_TYPE']
    notify_url = os.environ['NOTIFY_URL']
    secret = os.environ['WEBHOOK_SECRET']
    ngrok_url = NGROK.Get_NGROK_Tunnel()
    webhook = Mist.CreateOrgWebhook(mist_org, ngrok_url, mist_apikey, notify_type=notify_type, notify_url=notify_url, secret=secret)
    webhook_id = webhook.json()['id']
    os.environ['MIST_WEBHOOK_ID'] = webhook_id
    signal.signal(signal.SIGTERM, cleanup)
    x = True
    while x:
        time.sleep(5)


if __name__ == '__main__':
    main()
