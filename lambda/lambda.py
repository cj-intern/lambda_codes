import urllib3
import json

http = urllib3.PoolManager()


def lambda_handler(event, context):
    url = "https://hooks.slack.com/services/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"
    data = json.loads(event["Records"][0]["Sns"]["Message"])
    instanceID = data["detail"]["resource"]["instanceDetails"]["instanceId"]
    findingDescription = data["detail"]["description"]
    attackers_id = data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"]
    severity = data["detail"]["severity"] 
    attacked_resouce = data["detail"]["service"]["action"]["networkConnectionAction"]["localIpDetails"]["ipAddressV4"]
    region = data["region"]
    time = data["time"]
    type = data["detail"]["resource"]["instanceDetails"]["instanceType"]

    guard_duty_info = f"""Guard Duty 공격 탐지 \n
    Description: {findingDescription}\n  
    Region: {region}\n
    Instance ID: {instanceID}\n
    Instance Type: {type}\n
    Date: {time}\n
    Severity: {severity}\n
    Attacked IP: {attacked_resouce}\n
    Attacker's IP: {attackers_id}:
    """
    
    msg = {
        "channel": "#guardduty-alert",
        "username": "김기정",
        "text": guard_duty_info,  
        "icon_emoji": "",
    }

    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)