# -*- coding: utf-8 -*-

from urllib.parse import urljoin
import re

import requests

from util import TimeManager


class KmuMenu:
    _session = None
    root_uri = 'https://kmucoop.kookmin.ac.kr'

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': '*/*'})
        return self._session

    @property
    def today(self):
        dt = TimeManager.get_now_datetime(utc=True).astimezone(TimeManager.TIMEZONE_KR)
        return dt.strftime("%Y-%m-%d")

    def request(self, sdate: str, edate: str):
        self.session.post(urljoin(self.root_uri, '/___verify'))
        data = self.session.get(urljoin(self.root_uri, '/menu/menujson.php'),
                                params=dict(sdate=sdate, edate=edate, today=self.today)).json()
        return KmuMenu.parse(data)

    def get_today(self):
        return self.request(self.today, self.today)

    @staticmethod
    def parse(data: dict):
        result = {}

        # 아침:4 점심:2 저녁:1 점심저녁:3
        for restaurant in data.keys():
            for _data in data[restaurant].values():
                for sub_name, __data in _data.items():
                    if restaurant not in result:
                        result[restaurant] = []

                    item = {}

                    # item['sub'] = sub_name

                    if '중석식' in sub_name:
                        item['part'] = 3
                    elif '조식' in sub_name:
                        item['part'] = 4
                    elif '중식' in sub_name:
                        item['part'] = 2
                    elif '석식' in sub_name:
                        item['part'] = 1
                    else:
                        item['part'] = 3

                    if '\\' in __data['메뉴']:
                        for menu_name, price in re.findall('(.+?)\r\n\\\\([\\d/]+)', __data['메뉴']):
                            _item = item.copy()
                            _item['name'] = menu_name
                            _item['price'] = price
                            result[restaurant].append(_item)
                    else:
                        if '생활관' in restaurant:
                            item['name'] = sub_name
                        else:
                            item['name'] = __data['메뉴']
                        item['price'] = __data['가격']
                        result[restaurant].append(item)
        return result


if __name__ == '__main__':
    from pprint import pprint

    pprint(KmuMenu().request('2018-10-26', '2018-10-26'))

    # pprint(KmuMenu().request('2018-10-26', '2018-10-26').json())
