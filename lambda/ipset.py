import boto3
import time
client = boto3.client('wafv2', region_name='us-east-1')

ipsetName = 'intern-ip-set'
ipsetId = 'db7069b7-5982-41f9-ba60-b9b73a448467'
ipAddress = '10.0.0.1/32'

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

print(wafv2_update_ip_set(ipsetName,ipsetId,ipAddress))
time.sleep(10)
print(wafv2_delete_ip_set(ipsetName,ipsetId,ipAddress))