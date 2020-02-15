from bs4 import BeautifulSoup
import cv2
import os
import requests
import shutil
import urllib


# 環境整備
shutil.rmtree('image')
os.mkdir('image')
os.mkdir('image/faces')


class ImageDownloader(object):
    def __init__(self, keyword):
        session = requests.session()
        session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
             Gecko/20100101 Firefox/10.0'})
        params = urllib.parse.urlencode(
            {'q': keyword, 'tbm': 'isch', 'ijn': '1'})
        query = "https://www.google.co.jp/search" + '?' + params
        self._bs = BeautifulSoup(session.get(query).text, 'html.parser')

    def go(self):
        downloads = []
        for img in self._bs.find_all('img'):
            try:
                url = img['data-iurl']
                downloads.append('image/image_{}.jpg'.format(len(downloads) + 1))
                urllib.request.urlretrieve(url, downloads[-1])
            except KeyError:
                print('failed to get url : {}'.format(img))
        return downloads


class FaceDetector(object):

    # 学習済モデル
    FACE_CASCADE = '/home/websoler/anaconda3/lib/python3.7/site-packages/cv2/data/lbpcascade_animeface.xml'

    def __init__(self, fname):
        self._img = cv2.imread(fname)

    def cutout_faces(self, fname):
        gray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        classifier = cv2.CascadeClassifier(FaceDetector.FACE_CASCADE)
        faces = classifier.detectMultiScale(gray, scaleFactor=1.2, minSize=(30, 30))
        if len(faces):
            for (x, y, w, h) in faces:
                region = self._img[y:y + h, x:x + w]
                region_resized = cv2.resize(region, (128, 128))
                cv2.imwrite(fname, region_resized)
                break  #TODO とりあえず最初の一件だけとする。

if __name__ == '__main__':

    downloads = ImageDownloader('アンジェ・カトリーナ').go()
    for i, d in enumerate(downloads):
        FaceDetector(d).cutout_faces('image/faces/faces_{}.jpg'.format(i + 1))
