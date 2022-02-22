from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from .models import Results, InfrenceModels
from django.core.files.base import ContentFile
from .serializers import ResultsSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
import torch
from typing import Optional
import cv2
from PIL import Image
import numpy as np


class Inference:
    def __init__(self):
        self.model = None
        self.load_model()    
        
    def load_model(self):
        model = InfrenceModels.objects.latest('id')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model.file.path) 

inference = Inference()

def results_to_json(results, thresh, img):
    count = 0
    for pred in results.xyxyn[0]:
        if float(pred[4]) > thresh:
            count += 1
  
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    ret, buf = cv2.imencode('.jpg', img) # cropped_image: cv2 / np array
    orignal_img = ContentFile(buf.tobytes())
    
    for box in results.xyxy[0]: 
        if box[5]==0 and float(box[4]) > thresh:
            xB = int(box[2])
            xA = int(box[0])
            yB = int(box[3])
            yA = int(box[1])
            img = cv2.rectangle(img, (xA, yA), (xB, yB), (255, 0, 0), 2)
    
    #add count to image 
    h,w,c = img.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(count), (w-100,h-100), font, 4, (255,255,255), 2, cv2.LINE_AA)
    
    
    result = Results.objects.create(count=count)
    result.image.save('{}.jpg'.format(result.pk), orignal_img)
    result.output.save('{}.jpg'.format(result.pk), img)
    return result

   

@api_view(['GET'])
def reload_model(request):
    inference.load_model()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def inference(request):
    thresh = float(request.GET.get('thresh', 0.5))
    img = Image.open(request.FILES['image'])
    img = np.array(img) 
    img = cv2.resize(img, (960, 960))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # bilateral = cv2.bilateralFilter(img, 16, 150, 150)
    result = results_to_json(inference.model(img), thresh, img)
    data = ResultsSerializer(result, context={'request': request}).data
    return Response(data, status=status.HTTP_202_ACCEPTED)

