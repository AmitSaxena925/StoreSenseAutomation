*** Settings ***

Library  RequestsLibrary
Library  Collections
Library  String
Library  JSONLibrary
Resource   ../SSHUB/keywrd.robot

*** Test Cases ***
device platform verifcation
    [Tags]  Device
    [Documentation]  Device Platform Registration
    device platform verifcation

#Add Device
    #[Tags]  Device
    #add device

Detach Device Using DeviceId
     [Tags]  Device
     [Documentation]  Detach Device Using DeviceId
     detach device using deviceId

Detach Device By TillId and DeviceType
     [Tags]  Device
     [Documentation]  Detach Device By TillId and DeviceType
     detach device by tillId and deviceType

Upload Image
     [Tags]  IMAGE
     [Documentation]  Upload Image
     IMAGES

visitor data
     [Tags]  VISITOR
     [Documentation]  Visitor Data
     upload_visitor

create aws
     [Tags]  CERTIFICATE
     [Documentation]  CREATE AWS CERTIFICATE

    create aws cert

set_config_triger
    [Tags]  MQTT
    [Documentation]  Set Config Trigger
    set_con

Image_invalid_scre
    [Tags]  IMAGE  NEGATIVE
    [Documentation]  Image Invalid Score

    Image_INVALID_SCORE

negative_null
    [Tags]  VISITOR  NEGATIVE
    [Documentation]  VISITOR Event Time is Null
    eventime_null


image_empty_Scr
    [Tags]  IMAGE  NEGATIVE
    [Documentation]  IMAGE Score is Null

    image_empty_score

Image_frame_time_invalid
    [Tags]  IMAGE  NEGATIVE
    [Documentation]   FrameTime is invalid

    Image_fra_time_invalid

Image_checksum_is_null
     [Tags]  IMAGE  NEGATIVE
     [Documentation]   Checksum  is Null
     Image_checksum_null

Image_checksum_invalid
    [Tags]  IMAGE  NEGATIVE
    [Documentation]   Checksum  is Invalid
    checksum_Invalid

Visitor_Invalid_Till_Id
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Till id  is Invalid
    visitor_invalid_till_id

Visitor_Invalid_Event_Time
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Event Time is Invalid
    visitor_invalid_event_time

Visitor_Invalid_Track_Id
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Track Id is Invalid
    visitor_invalid_track_id
Visitor_Invalid_Org_Id
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Org Id is Invalid
    visitor_invalid_org_id

Visitor_Invalid_Device_Id
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Device Id is Invalid
    visitor_invalid_device_id

Visitor_Invalid_Image_List
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Image List is Invalid
    visitor_invalid_image_list

Visitor_Invalid_Start_Time
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Start Time is Invalid
    visitor_invalid_start_time

Visitor_null_store_id
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Store Id is Null
    Visitor_null_sto_id

Visitor_till_ID_Null
    [Tags]  VISITOR  NEGATIVE
    [Documentation]   Till Id is Null
    visitor_till_id_null

Visitor_store_id_null
     [Tags]  VISITOR  NEGATIVE
     [Documentation]   Store Id is Null
     Visitor_null_sto_id

frameTime_null
     [Tags]  VISITOR  NEGATIVE
     [Documentation]   FRAMETIME is Null
     fra_time_null


Send_Email_Test_Report
    [Tags]  Mail
    send_email























