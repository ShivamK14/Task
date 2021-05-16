import time
from wsgiref.util import FileWrapper
import json
from django.http import HttpResponse
from datetime import datetime
from .serializers import InputImageSerializer, OutputImageSerializer
from .models import InputImage, OutputImage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os, csv
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


def xml_to_txt(xml_path, image_path, image_name):

    in_file = open(xml_path)
    tree = ET.parse(in_file)
    root = tree.getroot()
    jpg = image_path
    dict = {}
    jpg2 = ''

    for obj in root.iter('object'):
        current = list()
        name = obj.find('name').text
        name = name.upper()
        coordinates = []
        xmlbox = obj.find('bndbox')
        xn = int(xmlbox.find('xmin').text)
        xx1 = int(xmlbox.find('xmax').text)
        yn = int(xmlbox.find('ymin').text)
        yx1 = int(xmlbox.find('ymax').text)


        coordinates = [xn, xx1, yn, yx1]

        shape = [(xn, yn), (xx1, yx1)]
        dict[name] = coordinates

        img = Image.open(jpg)

        img1 = ImageDraw.Draw(img)
        img1.rectangle(shape, width=2, outline="red")
        img1.text((xn, yn-20), name, font=ImageFont.truetype("./media/arial.ttf", 25))
        try:
            os.mkdir("./media/output/")
        except OSError as e:
            print("Directory exists")
        img.save('./media/output/processed_'+str(image_name))
        jpg= './media/output/processed_'+str(image_name)
        jpg2 = 'processed_'+str(image_name)

    file = 'http://127.0.0.1:8000/media/output/processed_'+str(image_name)
    queryset = OutputImage.objects.create(image_name=jpg2, coordinates=dict)
    print(queryset)
    return file


class InputImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = InputImageSerializer

    def get(self, request, *args, **kwargs):
        posts = InputImage.objects.all()
        serializer = InputImageSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = InputImageSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()

            queryset = posts_serializer.data.get('id', '')
            queryset = InputImage.objects.get(id=queryset)

            image_path = queryset.image.path
            image_name = queryset.image.name.split("/")
            imgname = image_name[len(image_name)-1]
            print(imgname)
            xml_path = queryset.xml.path
            file_handle = xml_to_txt(xml_path, image_path, imgname)
            print(file_handle)

            return Response(file_handle, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def to_csv(csv_file, dict_data):
    csv_columns = ['image_name', 'object_name', 'x_min', 'y_min', 'x_max', 'y_max', 'timestamp']
    try:
        os.mkdir("./media/csv/")
    except OSError as e:
        print("Directory exists")
    with open("./media/csv/"+csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
        return csvfile


class InfoCsv(APIView):
    serializer_class = OutputImageSerializer

    def post(self, request):
        start_date = request.data.get("start_date", "")
        end_date = request.data.get("end_date", "")
        list = OutputImage.objects.filter(timestamp__range=(start_date, end_date))
        dict_data = []
        for i in range(len(list)):
            son_acceptable_string = list[i].coordinates.replace("'", "\"")
            dictionary = json.loads(son_acceptable_string)
            for x, y in dictionary.items():

                dict_data.append({
                    "image_name": list[i].image_name,
                    "object_name": x,
                    "x_min": y[0],
                    "y_min": y[1],
                    "x_max": y[2],
                    "y_max": y[3],
                    "timestamp": list[i].timestamp
                })
        csv_file = "output_" + str(time.time())+".csv"

        file_handle = to_csv(csv_file, dict_data)
        file_handle = file_handle.name.split(".")
        file = 'http://127.0.0.1:8000' + file_handle[1]+'.' + file_handle[2]+'.csv'
        print(file)
        return Response(file, status=status.HTTP_201_CREATED)




