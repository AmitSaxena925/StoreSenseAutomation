import hashlib
import requests
import datetime
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from SSHUB.datafile import *
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def mongodb_connects_image_validation(chs):
    mongoClient = MongoClient(mongo_db)
    db = mongoClient.instoreai_storesense
    ch = {checksum : chs}
    images = db['images'].find_one(ch)
    print(images)
    print("CheckSum:",images["checksum"])
    a =images['_id']
    isid={'_id':ObjectId(a)}
    images1 = db['images'].find_one(isid)
    print(images1['_id'])
    print(images1)


def mongodb_connects_visitior_validation(vid,ord):
    mongoClient = MongoClient(mongo_db)
    db = mongoClient.instoreai_storesense
    orgId =int(ord)
    a = {"visitor": ObjectId(vid)}
    orgs= db['orgs'].find_one({'orgId':orgId})
    print("Org Name:",orgs)
    print("Inference Type List --->",orgs['inferenceTypeList'])
    inference_type=orgs['inferenceTypeList']
    if inference_type ==["DP"]:
        demographies = db["demographies"].find_one(a)
        print(demographies)
        print("Status of inference--->",demographies["status"])

    elif  inference_type ==[ "FP", "DP", "DT", "ISS" ]:
        fashions = db["fashions"].find_one(a)
        print(fashions)
        print("Status of inference--->", fashions["status"])
        demographies = db["demographies"].find_one(a)
        print(demographies)
        print("Status of inference--->", demographies["status"])
        dwelltimes = db['dwelltimes'].find_one(a)
        print(dwelltimes)
        print("Status of inference--->", dwelltimes["status"])

    elif inference_type ==["FP"]:
        fashions = db["fashions"].find_one(a)
        print(fashions)
        print("Status of inference--->", fashions["status"])

    elif inference_type ==["DW"]:
        dwelltimes = db['dwelltimes'].find_one(a)
        print(dwelltimes)
        print("Status of inference--->", dwelltimes["status"])
    elif inference_type ==["CR"]:
        customerrecognitions = db["customerrecognitions"].find_one(a)
        print(customerrecognitions)
        print("Status of inference--->", customerrecognitions["status"])
    elif inference_type == ["ISS"]:
        pass
        #print("Status of inference--->", demographies["status"])
    elif inference_type ==[ "FP", "DP", "DT", "CR", "ISS" ]:
        fashions = db["fashions"].find_one(a)
        print(fashions)
        print("Status of inference--->", fashions["status"])
        demographies = db["demographies"].find_one(a)
        print(demographies)
        print("Status of inference--->", demographies["status"])
        dwelltimes = db['dwelltimes'].find_one(a)
        print(dwelltimes)
        customerrecognitions = db["customerrecognitions"].find_one(a)
        print(customerrecognitions)

    else:
        print("something went wrong")

def calculate_checksum(filename):
    with open(filename, 'rb') as open_file:
        content = open_file.read()
        hasher = hashlib.md5()
        hasher.update(content)
        return (hasher.hexdigest())

def time_module():
    local_time = time.mktime(datetime.datetime.now().timetuple())
    return int(local_time)
with_out_mili =time_module()

def time_module_mili():
    millis = int(round(time.time() * 1000))
    return int(millis)

va = time_module_mili()

temp=[]

# Image Scenario
def image_upload_data():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': var, 'frameTime': var2, 'score': '80'}
        print("Checksum:",var)
        print("\n")
        req = requests.post(urlss,data=datas,files=files,auth=auth_id)
        temp.append(req.json()['body']['imageId'])
        response = json.dumps(req.json(), indent=4)
        print("\n")
        print("Response of code:",response)
        re = req.json()
        print("\n")
        dumps(mongodb_connects_image_validation(var))
        #print(abb["checksum"])
        body=re['body']['imageId']
        status_code = re['status']['code']
        status_message = re['status']['message']
        print("ImageID:", body)
        expected_code =200
        expected_message ="success"
        assert status_code == expected_code,"Actaul_Status_code_is_'{}'but Expected Status_Code_is'{}'".format(status_code,expected_code)
        assert status_message == expected_message,"Actaul_Status_message_is_'{}'but Expected Status_message_is'{}'".format(status_code,expected_message)
        assert body !='',"Actaul_body_is_'{}'".format(body)
        print("Status_Code::",status_code)
        print("Status_Message::", status_message)
        print("One Iteration Is COMPLETED")
    print(temp)

# image_upload_data()
# Visitor Scenarios
def upload_visitor_data():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(orgId))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    as_ip =str((visitor_id_val))
    print(as_ip)
    org_id = int(orgId)
    print(mongodb_connects_visitior_validation("5d10af0d1feea626d5c89535",org_id))
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

#upload_visitor_data()

def create_aws_certificate():

    try:           #'https://nightly.capillary.in/instoreai/storesense/storesense-hub/device/iot/50015469/certificate?deviceType=CE'
        urlss = url + str(aws_endpoint)
        res = requests.get(urlss,data=None,json=None,auth=auth_id)
        response_code = res.status_code
        print(json.dumps(res.json(), indent=4))
        assert response_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
            response_code, 400)

    except Exception as error:
        print(error)

#print("Create AWS_Certificate",create_aws_certificate())
def set_config():
    urlss = url + endpoint_set_config
    res = requests.get(urlss+scid1+'/'+scid2+'?'+se_cfig_parm+'&'+stro+'&'+org+'&'+ device_type,auth=auth_id)
    print("Request URL:",res.url)
    response = json.dumps(res.json(), indent=4)
    print(response)
    re = res.json()
    status_code = re["status"]["code"]
    print("Code of response",status_code)
    status_message = re["body"]["status"]
    print("Message of response",status_message)
    print("Body of response:",re['body'])
    print("JOB ID:",re['body']['jobId'])
    print("Status of response",re['body']['status'])
    assert status_code == 202,"Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(status_code, 200)
    assert status_message == 'InProgress'


def image_upload_data_score_invalid():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': var, 'frameTime': with_out_mili, 'score': '-90'}
        req = requests.post(urlss, data=datas, files=files, auth=auth_id)
        #temp.append(req.json()['body']['imageId'])
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        print(re)
        status_code = re["status"]["code"]
        print("Status of the response",re['status'])
        print("code of the response",re['status']['code'])
        assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(status_code, 500)

def image_upload_data_score_empty():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': var, 'frameTime': with_out_mili, 'score': ''}
        req = requests.post(urlss, data=datas, files=files, auth=auth_id)
        # temp.append(req.json()['body']['imageId'])
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        print(re)
        status_code = re["status"]["code"]
        print("Status of the response", re['status'])
        print("code of the response", re['status']['code'])
        assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(status_code, 500)

def image_upload_data_frameTime_invalid():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': var, 'frameTime': '1234567890', 'score': '80'}
        req = requests.post(urlss, data=datas, files=files, auth=auth_id)
        temp.append(req.json()['body']['imageId'])
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        body = re['body']['imageId']
        status_code = re['status']['code']
        status_message = re['status']['message']
        print("ImageID:", body)
        expected_code = 200
        expected_message = "success"
        assert status_code == expected_code, "Actaul_Status_code_is_'{}'but Expected Status_Code_is'{}'".format(
            status_code, expected_code)
        assert status_message == expected_message, "Actaul_Status_message_is_'{}'but Expected Status_message_is'{}'".format(status_code, expected_message)
        assert body != '', "Actaul_body_is_'{}'".format(body)
        print("Status_Code::", status_code)
        print("Status_Message::", status_message)
        print("One Iteration Is COMPLETED")

def image_upload_data_frameTime_null():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': var, 'frameTime': '', 'score': '80'}
        req = requests.post(urlss, data=datas, files=files, auth=auth_id)
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        print(re)
        status_code = re["status"]["code"]
        print("Status of the response", re['status'])
        print("code of the response", re['status']['code'])
        assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
            status_code, 500)

def image_upload_data_checksum_null():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': '', 'frameTime': with_out_mili, 'score': '80'}
        req = requests.post(urlss,data=datas,files=files,auth=auth_id)
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        print(re)
        status_code = re["status"]["code"]
        print("Status of the response", re['status'])
        print("code of the response", re['status']['code'])
        assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
            status_code, 500)

def image_upload_data_checksum_invalid():

    for i in path_of_file:
        var = calculate_checksum(i)
        var2 = time_module_mili()
        urlss = str(url) + str(end_iu)
        files = {'image': open(i, 'rb')}
        datas = {'checksum': 12344444, 'frameTime': with_out_mili, 'score': '80'}
        req = requests.post(urlss, data=datas, files=files, auth=auth_id)
        response = json.dumps(req.json(), indent=4)
        print(response)
        re = req.json()
        print(re)
        status_code = re["status"]["code"]
        print("Status of the response", re['status'])
        print("code of the response", re['status']['code'])
        assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
            status_code, 500)


def upload_visitor_data_invalid_till_id():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":invalid_till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur,data=(json_string),auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id",visitor_id_val)
    print("Status_code",status_code)
    print("status_message;",status_message)

def upload_visitor_data_invalid_event_time():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":till_id,"eventTime":invalid_event_time, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)


def upload_visitor_data_invalid_track_id():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":invalid_track_id,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur,data=(json_string),auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

def upload_visitor_data_invalid_org_id():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":invalid_org_id,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

def upload_visitor_data_invalid_device_id():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)

    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":invalid_device_id,"startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

def upload_visitor_data_invalid_image_list():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)

    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,"startTime": va,"eventType": eventType,"imageList":invalid_img_lst} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

def upload_visitor_data_invalid_start_time():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)

    json_string = {"tillId":till_id,"eventTime":with_out_mili, "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":deviceId,invalid_start_time: va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)

def upload_visitor_data_event_time_is_null():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    #print(trackId)
    json_string = {"tillId":till_id,"eventTime":"", "trackId":trackId,"storeId":storeId,"orgId":orgId," deviceId":"","startime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 500, "Actual Status Code is '{}'  but expected is '{}' since Event Time is Null !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message =="Cannot read property 'length' of undefined"

def upload_visitor_data_till_id_is_null():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":"","eventTime":"", "trackId":trackId,"storeId":storeId,"orgId":orgId,"deviceId":"","startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)


def upload_visitor_data_storeId_is_null():
    ur = str(url)+str( end_point_vud)
    trackId = str(with_out_mili)+'-'+str(va)
    print(trackId)
    json_string = {"tillId":"","eventTime":"", "trackId":trackId,"storeId":'',"orgId":orgId,"deviceId":"","startTime": va,"eventType": eventType,"imageList":temp} # ['5df2196440f1dd488ebf9707','5df21f4e40f1dd488ebf993b','5df21fed40f1dd488ebf9984','5df2203140f1dd488ebf99a5','5df22069ce2d4648bbf8129d']
    print(type(json_string))
    req = requests.post(ur, data=(json_string), auth=auth_id)
    response = json.dumps(req.json(), indent=4)
    print(response)
    re = req.json()
    status_code = re['status']['code']
    status_message = re['status']['message']
    assert status_code == 200, "Actual Status Code is '{}'  but expected is '{}' !!!!!!!!!!!!!!!!!!!!!!!!. ".format(
        status_code, 500)
    assert status_message == "created new visitor doc"
    visitor_id_val = re['body']['visitor']['_id']
    print("Visitor_id", visitor_id_val)
    print("Status_code", status_code)
    print("status_message;", status_message)


def send_test_report():
    dir_path = "/home/amit.saxena@capdomain.com/StoreSenseAutomation/Tests"
    files = ["/home/amit.saxena@capdomain.com/StoreSenseAutomation/Tests/report.html","/home/amit.saxena@capdomain.com/StoreSenseAutomation/Tests/log.html","/home/amit.saxena@capdomain.com/StoreSenseAutomation/Tests/output.xml"]
    msg = MIMEMultipart()
    fromaddr="amit.saxena@capilaarytech.com"
    receivers="subrat.panda@capillarytech.com","divya.dias@capillarytech.com","saurav.behera@capillarytech.com","arun.vijay@capillarytech.com"
    msg['To'] = "amitsaxena9225@gmail.com"
    #ccaddrs = "subrat.panda@capillarytech.com","divya.dias@capillarytech.com","saurav.behera@capillarytech.com","arun.vijay@capillarytech.com"
    msg['Subject'] = "SSHUB_Sanity_Test_Report_Result_Nightly"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(receivers)
    #msg['CC'] = ", ".join(ccaddrs)

    body = '''
            <h1>Test Report for Nightly Cluster</h1>              
            <p><b>Hi All,</b></p>
            <p>SSHUB Sanity is passed.</p>
            <p>Please find the attached files for more Details</p>
            <p>Thanks,</p>
            <p>Amit Saxena</p>
           '''

    msg.attach(MIMEText(body, 'html'))  # add message body (text or html)

    for f in files:  # add files to the message
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("amitsaxena9225@gmail.com", "capillary@123")
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    print ('done!')
    s.close()

send_test_report()







