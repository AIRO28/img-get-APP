# coding:utf-8
import requests as rq
import re
import datetime
from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path


class Conachan():
    def __init__(self):
        super().__init__()
        self._SERACH_URL = "https://konachan.com"
        self.__session = rq.session()
        self.__session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        })
        self.__get_img_num = 0
        self.__get_img_max = 0
    
    def search_conachan(self, keyword: str, num: int) -> None:
        # 保存先ディレクトリを生成(result/year-month-day/)
        output_dir = Path("./result/" + str(datetime.date.today()) + "_" + keyword)
        output_dir.mkdir(exist_ok=True, parents=True)
        self.__get_img_max = num

        # 検索結果にアクセス
        if (keyword == "new"):
            res = self.__session.get(self._SERACH_URL + "/post")
        else:
            res = self.__session.get(self._SERACH_URL + "/post?tags=" + keyword)
        soup = BeautifulSoup(res.text, "html.parser")
        # 画像リンクを取得
        img_links = self._get_image_links(soup)
        if 0 >= len(img_links):
            return
        # 画像リンクから画像の保存を実行
        self._save_img(img_links, output_dir)
        if self.__get_img_max <= self.__get_img_num:
            return

        # 次のページへ遷移
        while(True):
            i_page = soup.find("div", id="paginator")
            n_page = i_page.find("a", class_= "next_page")
            n_page_link = n_page.get("href")
            res = self.__session.get(self._SERACH_URL + n_page_link)
            soup = BeautifulSoup(res.text, "html.parser")
            img_links = self._get_image_links(soup)
            if 0 >= len(img_links):
                return
            self._save_img(img_links, output_dir)
            if self.__get_img_max <= self.__get_img_num:
                return
        return

    def _get_image_links(self, text_elem:BeautifulSoup):
        i_con = text_elem.find("div", id="content")
        c_con = i_con.find("div", class_="content")
        largeimg_link = []
        try:
            i_plist = c_con.find("ul", id="post-list-posts")
            post_list_links = i_plist.find_all("a", class_="directlink largeimg")
            for post_list_link in post_list_links:
                largeimg_link.append(post_list_link.get("href"))
                self.__get_img_num += 1
                if self.__get_img_max <= self.__get_img_num:
                    break
        except Exception as e:
            print("No results found!")
        return largeimg_link
    
    def _save_img(self, img_links, save_dir:Path):
        for img_link in img_links:
            img = img = self.__session.get(img_link)
            sleep(1)
            filename = re.search(".*\/(.*png|.*jpg|.*jpeg)$", img_link)
            save_imgname = save_dir.joinpath(filename.group(1))
            print(filename.group(1))
            with open(save_imgname, 'wb') as f:
                f.write(img.content)
