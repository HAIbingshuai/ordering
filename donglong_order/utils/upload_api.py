import requests


def upload_api(data):
    upload_api_url = 'https://third.zhihuilonghu.com/file/api/upload'
    response = requests.post(upload_api_url, data=data)
    if response.status_code == 200:
        response_data = response.json()
        file_data = response_data.get('data', {})
        uploaded_image_url = file_data.get('fileUrl', '') if file_data else ''
        return {'code': 0, 'data': {'url': uploaded_image_url}}
    else:
        return {'code': 1, 'msg': '上传失败'}
