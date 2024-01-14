import cv2
from flask import Flask, request
from flask_restful import Resource, Api
import urllib.error
import urllib.request

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)


class PeopleCounter(Resource):
    def get(self):
        # load image
        image = cv2.imread('nowy-dworzec.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'peopleCount': len(rects)}


class PeopleCounterDynamicUrl(Resource):
    def get(self):
             # here we want to get the value of user (i.e. ?user=some-value)
        user = request.args.get('user')
        # 1. Pobrać zdjęcie z otrzymanego adresu
        # 2. Pobrane zdjęcie można zapisać na dysku lub przetwarzać je w pamięci podręcznej
        # 3. Załadowane zjęcie do zmiennej image przekazać do algorytmu hog.detectMultiScale## i zwrócić z endpointu liczbę wykrytych osób.

        url = request.args.get('url')
        try:
            with urllib.request.urlopen(url) as web_file, open('image.jpg', 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)
        print('url', url)
        image = cv2.imread('image.jpg')
        image = cv2.resize(image, (700, 400))
            # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        return {'peopleCount': len(rects)}


api.add_resource(PeopleCounter, '/')
api.add_resource(PeopleCounterDynamicUrl, '/dynamic')

if __name__ == '__main__':
    app.run(debug=True)

