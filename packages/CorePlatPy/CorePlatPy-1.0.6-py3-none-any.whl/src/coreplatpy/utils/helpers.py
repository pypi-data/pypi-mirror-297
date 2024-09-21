from jwt import decode
from requests import Response
from ..models import ErrorReport
from typing import Union
import requests



def respond_with_error(response: Response) -> ErrorReport:
    try:
        error = ErrorReport.model_validate(response.json())
    except:
        error = ErrorReport.model_validate({
            'internal_status': None,
            'status': response.status_code,
            'message': None,
            'reason': response.reason
        })
    return error

def preety_print_error(error: ErrorReport):
    print('Something went wrong...')
    print('HTTP Status:', str(error.status))
    print('HTTP Reason:', str(error.reason))
    print('API Status :', str(error.internal_status))
    print('API Message:', str(error.message))

def safe_login(uri: str, data: dict, headers: dict) -> Union[dict, ErrorReport]:
    try:
        response = requests.post(uri, data=data, headers=headers)
    except Exception as e:
        print("Error at request: " + str(e))
        return ErrorReport()
    else:
        if response.status_code >= 300:
            return respond_with_error(response)
        return response.json()

def safe_json_request(request: str, uri: str, data: Union[dict, None], headers: dict) -> Union[dict, ErrorReport, None]:
    if request == 'POST':
        try:
            if data:
                response = requests.post(uri, json=data, headers=headers)
            else:
                response = requests.post(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'GET':
        try:
            if data:
                response = requests.get(uri, json=data, headers=headers)
            else:
                response = requests.get(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'PUT':
        try:
            if data:
                response = requests.put(uri, json=data, headers=headers)
            else:
                response = requests.put(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'DELETE':
        try:
            if data:
                response = requests.delete(uri, json=data, headers=headers)
            else:
                response = requests.delete(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    else:
        print("Not a valid method: " + str(e))
        return ErrorReport()

def safe_data_request(request: str, uri: str, data: Union[dict, None], headers: dict) -> Union[dict, ErrorReport, None]:
    if request == 'POST':
        try:
            if data:
                response = requests.post(uri, data=data, headers=headers)
            else:
                response = requests.post(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'GET':
        try:
            if data:
                response = requests.get(uri, data=data, headers=headers)
            else:
                response = requests.get(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'PUT':
        try:
            if data:
                response = requests.put(uri, data=data, headers=headers)
            else:
                response = requests.put(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    elif request == 'DELETE':
        try:
            if data:
                response = requests.delete(uri, data=data, headers=headers)
            else:
                response = requests.delete(uri, headers=headers)
        except Exception as e:
            print("Error at request: " + str(e))
            return ErrorReport()
        else:
            if response.status_code >= 300:
                return respond_with_error(response)
            if response.content:
                try:
                    return response.json()
                except:
                    return response.content
            else:
                return None
    else:
        print("Not a valid method: " + str(e))
        return ErrorReport()

def split_file_chunks(file_path, num_chunks, chunk_size_mb = 5 * 1024 * 1024 ):
    with open(file_path, 'rb') as f:
        # Read the file in chunks
        for i in range(num_chunks):
            # Seek to the appropriate position in the file
            f.seek(i * chunk_size_mb)
            # Read the chunk
            chunk = f.read(chunk_size_mb)
            # Yield the chunk
            yield chunk