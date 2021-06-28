# プロジェクト名
**img-get-APP**<br>  


# 概要
画像投稿サイト(https://konachan.com)から`指定キーワード`もしくは`新着`の画像を取得するスクレイピングプログラムです。  
<br>

# 使い方
取得したい画像のキーワードと取得枚数を指定することで、検索結果から画像を取得し保存します。  
取得結果はプロジェクトのルートディレクトリの`./result/日付_検索キーワード`以下に保存されます。  

```python
# 新着投稿を30件取得する場合
$ pyhton3 main.py new 30

# 指定キーワードで30枚取得する場合
$ python3 <キーワード> 30
```

# 作成者
- AIRO
- "https://twitter.com/AIRO28_"

# ライセンス
This repository is Free.

