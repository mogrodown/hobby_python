import chromedriver_binary
from selenium import webdriver

import os
import requests
import shutil
import time


IMAGE_FOLDER = './images/ange'


class YahooImagePicker:
    def __init__(self, keyword, count):
        self._keyword = keyword
        self._count = count
        self._driver = webdriver.Chrome()

    def jump(self):
        # yahooページへ遷移
        self._driver.get('http://yahoo.co.jp')

        # 検索キーワード入力/実行
        query = self._driver.find_element_by_name('p')
        query.send_keys(self._keyword)
        query.submit()
        time.sleep(3)

        # 画像リンクページへ遷移
        self._driver.find_element_by_link_text('画像').click()
        time.sleep(3)

        # 最初の画像イメージをクリック
        self._driver.find_element_by_tag_name('img').click()
        time.sleep(3)

    def image_urls(self):
        while True:
            # イメージリンク取得
            c = self._driver.find_element_by_id('imgContainer')
            c.find_element_by_id('imgInner')
            i = c.find_element_by_id('imgInner')
            i.find_element_by_tag_name('img')
            i2 = i.find_element_by_tag_name('img')
            i2.get_attribute('src')
            u = i2.get_attribute('src')

            # 次のイメージへ移動
            self._driver.find_element_by_class_name('next').click()
            time.sleep(3)

            print('count = {}'.format(self._count))
            self._count -= 1
            if self._count > 0:
                yield u
            else:
                return u


if __name__ == '__main__':

    try:
        shutil.rmtree(IMAGE_FOLDER)
    except (FileNotFoundError):
        pass
    os.makedirs(IMAGE_FOLDER)

    picker = YahooImagePicker('アンジュ・カトリーナ', 150)
    picker.jump()
    for i, u in enumerate(picker.image_urls()):
        r = requests.get(u)
        with open(os.path.join(IMAGE_FOLDER, 'ange_{}.jpg'.format(i)), 'wb') as f:
            f.write(r.content)
