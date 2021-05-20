#!/usr/bin/python
import requests
import time
import sys

TIMEOUT = 1200
INTERVAL = 5


def check_alert(am_url):
    timeout = TIMEOUT
    am_header = {'Accept': 'application/json'}

    while True:
        response = requests.get(am_url, headers=am_header).json()
        if response['status'] != "success":
            return sys.exit("Get alert Error !!!")

        for data in response['data']:
            if data['labels']['alertname'] == 'PrometheusNodeExportDown':
                print('fingerprint', data['fingerprint'], 'startsAt', data['startsAt'])
                print("*****************************************************")
                print("**** Alert success !!! ****")
                return {'fingerprint': data['fingerprint'], 'startsAt': data['startsAt']}
            else:
                print(data['labels'])
        time.sleep(INTERVAL)
        timeout = timeout - INTERVAL
        print(timeout)
        if timeout <= 0:
            sys.exit("Alert is not fired. Timeout !!!")


def check_push_slack_message(alert_dict, token):
    timeout = TIMEOUT

    slack_url = 'https://slack.com/api/conversations.history'
    slack_header = {
        'Authorization': token,
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }

    params = {
        "channel": "C01R18S4RTM",
        "inclusive": True,
        "limit": 10
    }

    while True:
        response = requests.get(slack_url, headers=slack_header, params=params).json()
        if not response['ok']:
            print("Get slack messages error !!!")
            return False

        for mess in response['messages']:
            print("mess ", mess)
            if 'attachments' in mess:
                for attach in mess['attachments']:
                    print('attach', attach)
                    if 'title' in attach:
                        print('title', attach['title'])
                        slack_dict = get_fingerprint_EndsAt(attach['title'])
                        print('slack_dict', slack_dict)
                        print('alert_dict', alert_dict)
                        alert_endat = time.strptime(alert_dict['startsAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        if alert_dict['fingerprint'] == slack_dict['fingerprint'] and alert_endat == slack_dict['startsAt']:
                            print("*****************************************************")
                            print("**** Push slack message success !!! ****")
                            return True
            else:
                continue
        time.sleep(INTERVAL)
        timeout = timeout - INTERVAL
        print(timeout)
        if timeout <= 0:
            sys.exit("Retrieve message. Timeout !!!")


def get_fingerprint_EndsAt(title):
    fp = 'c72a9773a07090db'
    slack_startsat = '2021-05-20 02:55:47.083 +0000 UTC'
    time_startsat = time.strptime(slack_startsat, '%Y-%m-%d %H:%M:%S.%f +0000 UTC')

    str_list = title.split("[")
    if len(str_list) > 1:
        str_list = str_list[1].split("]")
        if len(str_list) > 1:
            str_list = str_list[0].split(",")
            if len(str_list) > 1:
                fp = str_list[0].split(":")[1]
                slack_startsat = str_list[1].split(":", 1)[1].rstrip()

    try:
        time_startsat = time.strptime(slack_startsat, '%Y-%m-%d %H:%M:%S.%f +0000 UTC')
    except ValueError:
        pass

    return {
        'fingerprint': fp,
        'startsAt': time_startsat
    }


def main(argv):
    am_url = argv[0]
    token = "Bearer " + argv[1]

    alert_dict = check_alert(am_url)

    check_push_slack_message(alert_dict, token)


if __name__ == "__main__":
    main(sys.argv[1:])
