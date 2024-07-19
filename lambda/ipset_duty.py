import urllib3
import json
import boto3
import time

http = urllib3.PoolManager()
client = boto3.client('wafv2', region_name='us-east-1')
ipsetName = 'intern-ip-set'
ipsetId = 'db7069b7-5982-41f9-ba60-b9b73a448467'

def wafv2_update_ip_set(n,i,a):

    # ip가 포함되어 있는지 get_ip_set으로 확인
    response = client.get_ip_set(
            Name=n,
            Scope='CLOUDFRONT',
            Id=i)

    if a in response['IPSet']['Addresses']:
        return f"{a} already exists"
        
    else:
        # ip가 포함되어 있지 않으면 기존 IPset IP에 추가
        ipset_ipaddrs = response['IPSet']['Addresses']
        ipset_ipaddrs.append(a)
        
        response = client.update_ip_set(
                Name=n,
                Scope='CLOUDFRONT',
                Id=i,
                Addresses=ipset_ipaddrs,             # list data
                LockToken=response['LockToken'])     # LockToken값은 get_ip_set에서 득한다.
                
        # 응답값 리턴 : 200 정상
        if str(response['ResponseMetadata']['HTTPStatusCode']) == '200':
            return f"{a} is added to ip set"
        else:
            return "error occurred"

def wafv2_delete_ip_set(n,i,a):
    # ip가 포함되어 있는지 get_ip_set으로 확인
    response = client.get_ip_set(
            Name=n,
            Scope='CLOUDFRONT',
            Id=i)

    if a in response['IPSet']['Addresses']:
        ipset_ipaddrs = response['IPSet']['Addresses']
        ipset_ipaddrs.remove(a)
        response = client.update_ip_set(
                Name=n,
                Scope='CLOUDFRONT',
                Id=i,
                Addresses=ipset_ipaddrs,             # list data
                LockToken=response['LockToken'])     # LockToken값은 get_ip_set에서 득한다.
        if str(response['ResponseMetadata']['HTTPStatusCode']):
            return f"{a} is removed from ip set"
        else:
            return "error occurred"
        
    else:
        return f'ip set doesn\'t have {a}'

def lambda_handler(event, context):
    url = "https://hooks.slack.com/services/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"
    data = json.loads(event["Records"][0]["Sns"]["Message"])
    instanceID = data["detail"]["resource"]["instanceDetails"]["instanceId"]
    findingDescription = data["detail"]["description"]
    attackers_id = data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"]
    severity = data["detail"]["severity"] 
    attacked_resouce = data["detail"]["service"]["action"]["networkConnectionAction"]["localIpDetails"]["ipAddressV4"]
    region = data["region"]
    date = data["time"]
    type = data["detail"]["resource"]["instanceDetails"]["instanceType"]

    guard_duty_info = f"""[Guard Duty] Detection \n
    Description: {findingDescription}\n  
    Region: {region}\n
    Instance ID: {instanceID}\n
    Instance Type: {type}\n
    Date: {date}\n
    Severity: {severity}\n
    Attacked IP: {attacked_resouce}\n
    Attacker's IP: {attackers_id}
    """
    
    msg = {
        "channel": "#guardduty-alert",
        "username": "김기정",
        "text": guard_duty_info,  
        "icon_emoji": "",
    }

    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)
    
    prefix = "[Guard Duty] Prevetion\n"
    result = prefix + wafv2_update_ip_set(ipsetName,ipsetId,attackers_id + "/32")
    print(result)
    msg["text"] = result
    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)
    
    time.sleep(10)
    result = prefix + wafv2_delete_ip_set(ipsetName,ipsetId,attackers_id + "/32")
    print(result)
    msg["text"] = result
    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)