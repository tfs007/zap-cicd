import time 
import requests 
from zapv2 import ZAPv2

# ZAP Setup 
ZAP_API_KEY = 'zapkey'
ZAP_HOST = 'http://localhost:8080'
TARGET = 'http://localhost:8000'
LOGIN_URL = f'{TARGET}/token'
PROTECTED_URL = f'{TARGET}/protected'
HTML_REPORT_PATH = 'zap_report.html'

# Oauth2 Login 
def get_token():
    response = requests.post(
        LOGIN_URL,
        data = {'username':'demo', 'password':'secret'},
        headers= {'Content-Type': 'application/x-www-form-urlencoded'}
    )


    response.raise_for_status()
    token = response.json().get('access_token')
    print(f">> Got token : {token}")
    return token 

def main():
    # Set up ZAP proxy 
    ZAP = ZAPv2(apikey=ZAP_API_KEY, proxies={'http': ZAP_HOST, 'https': ZAP_HOST})

    # 1. Get Access token 
    token = get_token()
    print(f"token: {token}")

    #2 Access the protected route with bearer token so that ZAP sees it 
    print(">> visiting protected route with token...")
    response = requests.get(PROTECTED_URL, headers={"Authorization":f"Bearer {token}"})
    print(f"[+] Status Code : {response.status_code}, Response: {response.text}")

    # 3 Access target to let ZAP see the routes
    print("[*] Accessing target to populate the site tree..")
    ZAP.urlopen(TARGET)
    time.sleep(2)

    #4 Ensure ZAP is only scanning target 
    print(">>> Scanning...")
    ZAP.spider.scan(TARGET)
    time.sleep(5) # Allow time for the spider to start 

    #5 Start the Active Scan 
    print("[*] Starting Active scan...")
    scan_id = ZAP.spider.scan(TARGET)
    print(f"type: {ZAP.spider.status(scan_id)}")
    while int(ZAP.spider.status(scan_id)) < 100:
        print(f"Spider progress: {ZAP.spider.status(scan_id)}%")
        time.sleep(2)

    print("Scan complete")

    # 6 HTML reports 
    print(">>> Generating HTML report ")
    report = ZAP.core.htmlreport()
    with open(HTML_REPORT_PATH,"w") as report_file:
        report_file.write(report)
    print(f">> Report saved to {HTML_REPORT_PATH}")

    # 7 Print alerts (optional)
    alerts = ZAP.core.alerts(baseurl=TARGET)
    print(f"[+] Found {len(alerts)} alerts.")
    for alert in alerts:
        print(f"[!] {alert['alert']} - Risk : {alert['risk']}, URL: {alert['url']}")


if __name__ == '__main__':
    main()