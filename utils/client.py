import os
import time
import json
import yaml
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-ct", "--check_type", type=str, default="new_one", help="the check type, new_one, demo_inference, demo_inference_url, demo_clean or test")
parser.add_argument("-pu", "--project_uuid", type=str, default="", help="the project uuid")
args = parser.parse_args()

with open('./utils/config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


# b8b63f92-51cc-11ef-94f2-acde48001122
BASE_URL = 'http://127.0.0.1:8000'
headers = {
    'Content-Type': 'application/json'
}

if args.check_type == 'new_one':
    # new one
    data = {
        "account": "qq",
        "password": "bb",
        "token": config['token'],
    }

    response = requests.post(f'{BASE_URL}/registration', headers=headers, data=json.dumps(data))
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

    response = requests.post(f'{BASE_URL}/login', headers=headers, data=json.dumps(data))
    cookies = response.cookies
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

    response = requests.post(f'{BASE_URL}/main', cookies=cookies)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
elif args.check_type == 'demo_inference':
    data = {
        "account": "toby",
        "password": "best",
        "token": config['token'],
    }

    response = requests.post(f'{BASE_URL}/login', headers=headers, data=json.dumps(data))
    cookies = response.cookies
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())


    # 查看版本
    response = requests.post(f'{BASE_URL}/version', cookies=cookies)
    # response = requests.post(f'{BASE_URL}/version')
    # response = requests.post(url, headers=headers, data=json.dumps(data), cookies=cookies)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())


    response = requests.post(f'{BASE_URL}/main', cookies=cookies)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

    # upload file
    print('upload file: ')
    file_path = 'utils/datas/demo_datas/demo_input.zip'
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'application/zip')}
        response = requests.post(f'{BASE_URL}/upload_from_zip', files = files, cookies=cookies)
        # response = requests.post(f'{BASE_URL}/inference_from_zip', files = files)
        print('Status Code:', response.status_code)
        print('Response JSON:', response.json())

    time.sleep(2)

    # inference project
    response = requests.post(f'{BASE_URL}/inference_labels/demo_sample', cookies=cookies)
    project_uuid = response.json()['project_uuid']
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
    
    # get demo data
    response = requests.post(f'{BASE_URL}/main/{project_uuid}', stream = True, cookies=cookies)
    try:
        if 'finish_flag' in response.json():
            print('Status Code:', response.status_code)
            print('Response JSON:', response.json())
        else:
            filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
            if not filename:
                filename = "downloaded_file.zip"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Zip file '{filename}' downloaded successfully.")
    except Exception as e:
        print(f'Error: {e}')
        print(response.text)
        
    # save cookie
    with open('cookies.json', 'w') as f:
        json.dump(cookies.get_dict(), f)
    
elif args.check_type == 'demo_inference_url':
    data = {
        "account": "toby",
        "password": "best",
        "token": config['token'],
    }

    response = requests.post(f'{BASE_URL}/login', headers=headers, data=json.dumps(data))
    cookies = response.cookies
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
    
    
    # upload file
    print('upload file: ')
    file_url = 'drive.google.com/file/d/1aybOEAextTIeYrrp3gfulZt228bOr5i4/view?usp=sharing'
    response = requests.post(f'{BASE_URL}/upload_from_url/{file_url}', cookies=cookies)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

    time.sleep(2)

    # inference project
    response = requests.post(f'{BASE_URL}/inference_labels/demo_sample', cookies=cookies)
    project_uuid = response.json()['project_uuid']
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
    
    # get demo data
    response = requests.post(f'{BASE_URL}/main/{project_uuid}', stream = True, cookies=cookies)
    try:
        if 'finish_flag' in response.json():
            print('Status Code:', response.status_code)
            print('Response JSON:', response.json())
        else:
            filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
            if not filename:
                filename = "downloaded_file.zip"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Zip file '{filename}' downloaded successfully.")
    except Exception as e:
        print(f'Error: {e}')
        print(response.text)
    
elif args.check_type == 'demo_clean':
    project_uuid = args.project_uuid
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    
    # get demo data
    response = requests.post(f'{BASE_URL}/main/{project_uuid}', stream = True, cookies=cookies)
    if 'finish_flag' in response.json():
        print('Status Code:', response.status_code)
        print('Response JSON:', response.json())
    else:
        filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
        if not filename:
            filename = "downloaded_file.zip"
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Zip file '{filename}' downloaded successfully.")
    
    # 清除 demo data
    response = requests.post(f'{BASE_URL}/clean_demo_datas', cookies=cookies)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())


    response = requests.post(f'{BASE_URL}/logout')
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())


    response = requests.post(f'{BASE_URL}/version')
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
    
elif args.check_type == 'test':
    data = {
        "account": "toby",
        "password": "best",
        "token": config['token'],
    }
    session = requests.Session()
    response = session.post(f'{BASE_URL}/login', headers=headers, data=json.dumps(data))
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

    # 查看版本
    response = session.post(f'{BASE_URL}/version')
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())
    
else:
    pass



