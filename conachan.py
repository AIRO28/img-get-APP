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
    
    def search_conachan(self):
        # TopPageにアクセス
        res = self.__session.get(self._SERACH_URL+"/post")
        soup = BeautifulSoup(res.text, "html.parser")
        # 画像リンクを取得
        img_links = self._get_image_links(soup)

        # 保存先ディレクトリを生成(result/year-month-day/)
        output_dir = Path("./result/" + str(datetime.date.today()))
        output_dir.mkdir(exist_ok=True, parents=True)

        # 画像リンクから画像の保存を実行
        self._save_img(img_links, output_dir)

        # 次のページへ遷移
        i = 0
        while(True):
            i_page = soup.find("div", id="paginator")
            n_page = i_page.find("a", class_= "next_page")
            n_page_link = n_page.get("href")
            res = self.__session.get(self._SERACH_URL + n_page_link)
            soup = BeautifulSoup(res.text, "html.parser")
            img_links = self._get_image_links(soup)
            self._save_img(img_links, output_dir)
            i += 1
            if (i == 10):
                break

        return

    def _get_image_links(self, text_elem:BeautifulSoup):
        i_con = text_elem.find("div", id="content")
        c_con = i_con.find("div", class_="content")
        i_plist = c_con.find("ul", id="post-list-posts")
        post_list_links = i_plist.find_all("a", class_="directlink largeimg")

        largeimg_link = []

        for post_list_link in post_list_links:
            largeimg_link.append(post_list_link.get("href"))

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


# main func
if __name__ == "__main__":
    cona = Conachan()
    cona.search_conachan()

    exit(0)


