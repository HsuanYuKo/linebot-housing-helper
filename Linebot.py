# -*- coding: utf-8 -*-
"""
Created on Sun May 22 18:05:15 2022

@author: elain
"""

from flask import Flask
app=Flask(__name__)

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, 
    LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, TemplateSendMessage,
    ButtonsTemplate, MessageTemplateAction,
    CarouselTemplate, CarouselColumn, URIAction, ConfirmTemplate, PostbackAction
)
import re

import json, ssl, urllib.request
import requests
import numpy as np
import heapq

line_bot_api=LineBotApi('YvMQz75cE7GVJ/kdX35gh+WOquJaRDCW8hFGQb8YprRtI1mVe9BiwxYh6/blloyJq9yaqRospC3oIfwjTrFf665fr3Gj+s89dgVvLeZQQSZl2Duc8sGDNTbmq8JohHBLaQxS/6Gd/NMx16xs45j5kwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('2b8a873987cf6189f2606a26ca1697d1')


url = 'https://data.kcg.gov.tw/dataset/0315a1e8-7138-4f86-90ea-d2cc82b4d9ec/resource/435fe041-e5ce-45ca-bef7-37fbdea05216/download/-.json'
context = ssl._create_unverified_context()

lat = 22.706173
lng = 120.344779
result = []

def Haversine(lat1, long1, lat2, long2):
    R = 6371
    LAT = (float(lat2) - float(lat1)) * np.pi / 180
    LONG = (float(long2) - float(long1)) * np.pi / 180
    temp = np.sin(LAT / 2) ** 2 + np.cos(float(lat1) * np.pi / 180) * np.cos(float(lat2) * np.pi / 180) * np.sin(LONG / 2) ** 2
    temp1 = 2 * np.arctan2(np.sqrt(temp), np.sqrt(1 - temp))
    d = R * temp1
    return d

def findPlace(data):
    list = []
    index = []
    for i in range(len(data)):
        list.append(Haversine(lat, lng, data[i]['lat'], data[i]['lng']))
    num = heapq.nsmallest(3, list)
    for j in num:
        t = list.index(j)
        index.append(t)
        list[t] = 1000
    return index

with urllib.request.urlopen(url, context=context) as jsondata:
    p = json.loads(jsondata.read().decode('utf-8-sig'))
    p = p["orgs"]['frg']['org']
    result = findPlace(p)
    

# ??????????????????
def earth_quake():
    msg = ['????????????????????????','https://example.com/demo.jpg']
    try:
        code = 'CWB-0A6C8F8C-91B2-4FCE-BFEE-2EFEBAB0DB73'
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={code}'
        e_data = requests.get(url)       # ????????????????????????      
        e_data_json = e_data.json()      # json ?????????????????????
        eq = e_data_json['records']['earthquake']  # ??????????????????
        for i in eq:
            shakearea = i["intensity"]["shakingArea"] # ??????????????????
            for j in shakearea:
                name_of_area = j["areaName"] # ??????????????????
                area_val = j["areaIntensity"]["value"] # ??????????????????
                if(name_of_area == '?????????'):
                #if(name_of_area == '?????????' and area_val>=4):
                    loc = i['earthquakeInfo']['epiCenter']['location']       # ????????????
                    val = i['earthquakeInfo']['magnitude']['magnitudeValue'] # ????????????
                    dep = i['earthquakeInfo']['depth']['value']              # ????????????
                    eq_time = i['earthquakeInfo']['originTime']              # ????????????
                    #img = i['reportImageURI']                                # ?????????
                    msg = '[????????????]'+str(eq_time)+'??????'+str(loc)+'?????????????????? '+str(val)+' ????????????\n\n'+str(name_of_area)+'????????????'+str(area_val)+'??????'
                    # msg2 = str(name_of_area)+'????????????'+str(area_val)+'??????'
                    break     # ??????????????????????????? break
        return msg, area_val    # ?????? msg
    except:
        return msg     # ????????????????????????????????????????????? msg


@app.route("/callback", methods=['POST'])
def callback():
    signature=request.headers['X-Line-Signature']
    body=request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext=event.message.text
    msg, area_val = earth_quake()
    if mtext == '@????????????':
        voom_url="https://sheets.googleapis.com/v4/spreadsheets/14fDd1ZL_K5gctCqF1eSqYCNAt950uuWUMynSx415h8Q?key=AIzaSyBKDnSOUAJ5hdlD9q94J0HzONYeQTzKUDI&includeGridData=true"
        voom_html=requests.get(voom_url).text
        voom_json=json.loads(voom_html)
        
        news=''
        i=0
        while True:
            try:
                response=voom_json['sheets'][0]['data'][0]['rowData'][i]['values']
                news_url=response[0]['formattedValue']
                i=i+1
                news=news_url
            except:
                break
        try:
            message=TextSendMessage(
                text=news
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
    
    if mtext == '@????????????':
        try:
            message=ImageSendMessage(
                original_content_url="https://drive.google.com/open?id=1qdzyZl0D5dzkgfmFsGIcLicGLIsB_rEG",
                preview_image_url="https://drive.google.com/open?id=1qdzyZl0D5dzkgfmFsGIcLicGLIsB_rEG"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
            
    elif mtext=='@????????????':
        try:
            message=TextSendMessage(
                text="???????????????",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="2F", text="@2F")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="3F", text="@3F")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="4F", text="@4F")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
            
    elif mtext=='@????????????':
        try:
            message=TextSendMessage(
                text="???????????????????????????",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="?????????", text="@?????????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="?????????", text="@?????????")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
            
    elif mtext=='@????????????':
        try:
            message=TextSendMessage(
                text="??????????????????AWS???????????????"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
    
    elif mtext=='@????????????':
        try:
            message=TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text='????????????????????????',
                    actions=[
                        MessageAction(
                            label='??????',
                            text='@??????????????????'
                        ),
                        MessageAction(
                            label='??????',
                            text='@????????????????????????'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
            
    elif mtext=='@??????????????????':
        try:
            message=TextSendMessage(
                text="https://forms.gle/zHHeC7fspwovLM2Q9"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
    
    elif mtext=='@????????????????????????':
        try:
            furniture_url = "https://sheets.googleapis.com/v4/spreadsheets/1YNJ96VD-Tjy79tg14NQI05Xd-Z1nSEL-NBMrLaxjCzI?key=AIzaSyBKDnSOUAJ5hdlD9q94J0HzONYeQTzKUDI&includeGridData=true"
            html=requests.get(furniture_url).text
            jsonFile=json.loads(html)
            
            """????????????"""
            user=[]
            i=0
            while True:
                try:
                    response=jsonFile['sheets'][0]['data'][0]['rowData'][i]['values']
                    reg=response[0]['formattedValue']
                    person=response[1]['formattedValue']
                    contact=response[2]['formattedValue']
                    furniture=response[3]['formattedValue']
                    form=response[4]['formattedValue']
                    price=response[5]['formattedValue']
                    size=response[6]['formattedValue']
                    image=response[7]['formattedValue']
                    user.append([reg,person,contact,furniture,form,price,size,image])
                    i=i+1
                except:
                    break
            
            message=TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title=user[i-1][3],
                            text="??????: "+user[i-1][4]+" /??????: "+user[i-1][5]+"\n??????: "+user[i-1][6]+"\n??????: "+user[i-1][1]+" / "+user[i-1][2],
                            actions=[
                                URIAction(
                                    label='????????????',
                                    uri=user[i-1][7]
                                ),
                                URIAction(
                                    label='See More',
                                    uri='https://docs.google.com/spreadsheets/d/1YNJ96VD-Tjy79tg14NQI05Xd-Z1nSEL-NBMrLaxjCzI/edit?usp=sharing'
                                )
                            ]
                        ),
                        CarouselColumn(
                            title=user[i-2][3],
                            text="??????: "+user[i-2][4]+" /??????: "+user[i-2][5]+"\n??????: "+user[i-2][6]+"\n??????: "+user[i-2][1]+" / "+user[i-2][2],
                            actions=[
                                URIAction(
                                    label='????????????',
                                    uri=user[i-2][7]
                                ),
                                URIAction(
                                    label='See More',
                                    uri='https://docs.google.com/spreadsheets/d/1YNJ96VD-Tjy79tg14NQI05Xd-Z1nSEL-NBMrLaxjCzI/edit?usp=sharing'
                                )
                            ]
                        )
                    ]
                ),
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))        
    
    elif mtext=='@?????????':
        try:
            message=TextSendMessage(
                text="???????????????7~9??? 8:00~18:00"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
    
    elif mtext=='@?????????':
        try:
            message=TextSendMessage(
                text="???????????????????????????",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="??????????????????", text="@???????????????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="???????????????", text="@???????????????")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????'))
    
    elif mtext=='@????????????':
        location_message = [
            LocationSendMessage(
                title='????????????????????????',
                address=p[result[0]]['text'],
                latitude=p[result[0]]['lat'],
                longitude=p[result[0]]['lng']
            ),
            LocationSendMessage(
                title='????????????????????????',
                address=p[result[1]]['text'],
                latitude=p[result[1]]['lat'],
                longitude=p[result[1]]['lng']
            ),
            LocationSendMessage(
                title='????????????????????????',
                address=p[result[2]]['text'],
                latitude=p[result[2]]['lat'],
                longitude=p[result[2]]['lng']
            ),
            TextSendMessage(str(msg))]
            # TextSendMessage(msg2)]
        line_bot_api.reply_message(event.reply_token, location_message)

            
    
if __name__ == '__main__':
    app.run()