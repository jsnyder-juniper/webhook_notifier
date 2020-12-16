# webhook_notifier

Webhook Notifier is a docker-compose package design to provide a stateless way to format webhooks from Mist into those consumable by common applications.

Today we support 2 primary targets: Microsoft Teams and Slack.

## Requirements:
- Docker and Docker-Compose
- NGROK auth token (ngrok.com free account is ok)
- Mist Account information (API Token, Org_id)
- Microsoft Teams or Slack incoming webhook URL


To learn how to setup an incoming webhook in slack, please read https://api.slack.com/apps/A01F2AGU89Z/incoming-webhooks?success=1

To learn how to setup a webhook connector in a teams channel, please read https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook



## Getting Started
To start, you should clone this repo.
```
git clone https://github.com/jsnyder-juniper/webhook_notifier.git
```

### Set Environment Variables:<mist api token>
This dockerfile leverages environment variables to populate certain values.  You should set these in the session.
Intend to move this to an environment file in a later release.

```
export MIST_API=<Mist API Token>
export MIST_ORG=<mist_org_id>
export NOTIFY_TYPE=<teams or slack>
export NOTIFY_URL=<incoming webhook url>
export NGROK_AUTH=<ngrok auth token>
export WEBHOOK_SECRET=<secret phrase for simple filtering of requests>
```

### Example:

```
export MIST_API=DqZ5...grymT
export MIST_ORG=exxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx6
export NOTIFY_TYPE=teams
export NOTIFY_URL=https://outlook.office.com/webhook/.../IncomingWebhook/.../...92
export NGROK_AUTH=1c...mC
export WEBHOOK_SECRET=abcdefghijklmnop
```

### Build Containers and run environment

```
cd webhook_notifier
docker-compose build
docker-compose up -d
```

## Container Structure:
### NGROK
The NGROK container provides the URL for the inbound webhook.  This allows us to receive a webhook with a public URL and certificate (HTTPS) without the need to port-forwarding or a public IP and generating our own certificate.
NGROK has a status page configure on that can be exposed on port 4041 (currently commented out in docker-compose)
NGROK forwards to port 80 on the NGINX reverse proxy.

### RPROXY (NGINX)
This takes incoming requests on port 80 and forwards them to the Node-Red container at :1880/mist
This port can be exposed on 5051 (commented out in docker-compose file) if you want to test locally.  Long term will implement filters to restrict to just the mist webhook ip addresses.


### Node-Red
Node Red is running a flow that handles the processing of the inbound webhook.  This is done in a stateless way, as the webhook will pass the `x-notify-type` and `x-notify-url` headers which indicate the info needed for the incoming webhook from teams or slack.
Node red can be configured to listen on the host on port 1882 if you want to inspect it locally (commented out in docker-compose).

![alt text](https://github.com/jsnyder-juniper/webhook_notifier/blob/main/img/NodeRedFlow.png?raw=true)


### mist_receiver_config
This container is responsible for the setup and tear-down of the webhook in mist.  It queries the NGROK container to locate the unique url it is listening on and uses the Mist API to configure an org-level webhook with the appropriate headers and topics (audit and alarms are currently supported).  On termination, it removes the configuration of the webhook.  This is the only container that knows the API token for Mist, and has no ports exposed to any other container. 

## Example Output:
![alt text](https://github.com/jsnyder-juniper/webhook_notifier/blob/main/img/example_teams.png?raw=true)

