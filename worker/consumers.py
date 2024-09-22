import json
from random import randint
from time import sleep
import base64
import numpy as np
import cv2
import torch
from asgiref.sync import sync_to_async

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from ultralytics import YOLO
from master.databaseWork import DatabaseWork
from master.models import *



class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        torch.cuda.set_device(0)
        self.model = YOLO("AiVision/yolo_weights/t-profile_640_16.pt")
        self.task_id = -1
        self.max_id_profile = 0
        self.amount_profile = 0
        

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):        
        data = json.loads(text_data)                
        if data['isFs'] ==  1:  
            print('Первая отправка сообщения')          
            self.task_id = data['task_id']
            self.amount_profile = await self.get_start_profile_amount()
        elif data['chgVal'] ==  1:
            print('Изменение количества профиля')
            self.amount_profile = data['value']
            await self.change_profile_amount_in_db()            
        else:                 
            image_data = data['image']

        # Декодирование изображения
            image_data = base64.b64decode(image_data)
            np_image = np.frombuffer(image_data, np.uint8)

        # Преобразование в изображение OpenCV
            frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Обработка изображения с помощью YOLO
            processed_frame = self.process_frame(frame)

        # Дополнительная обработка или отправка результата обратно клиенту
        # закодировать обратно в base64 и отправить клиенту
        
            _, buffer = cv2.imencode('.jpg', processed_frame)
            processed_image_data = base64.b64encode(buffer).decode('utf-8')

            await self.send(text_data=json.dumps({
                'processed_image': processed_image_data,
                'max_id_profile': self.amount_profile
            }))

    def process_frame(self, frame):
    # Логика обработки изображения
    # Предобученная модель Yolov8      
        results = self.model.track(frame, stream=True, persist=True, iou=0.50, conf=0.88,
                                        tracker="botsort.yaml", imgsz=640, classes=0, verbose=False)
        for result in results:
            res_plotted = result.plot()
            if result.boxes.id != None:
                for id_item in result.boxes.id:
                    id_item = int(id_item.item())                    
                    if id_item > self.max_id_profile:
                        self.amount_profile = self.amount_profile + (id_item - self.max_id_profile)
                        self.max_id_profile = id_item
                        
                        
        res_plotted = cv2.resize(res_plotted, (res_plotted.shape[1]//2, res_plotted.shape[0]//2))
        image = res_plotted        
        return image
    
    @sync_to_async
    def get_start_profile_amount(self):
        return Tasks.objects.get(id=self.task_id).profile_amount_now
    
    @sync_to_async
    def change_profile_amount_in_db(self):
        data_task = DatabaseWork({'id_task':self.task_id})    
        result = data_task.change_profile_amount(self.task_id, self.amount_profile)
        print(result)
      
      
      
  