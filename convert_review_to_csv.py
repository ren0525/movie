# Filmarksのスクレイピング
# 対象映画は「」
from bs4 import BeautifulSoup
from urllib import request
import pandas as pd

df_list = []
sep = ' '
pages = range(11)
movie_name = 'ultraman'
movie_index = '85555'

url = f'https://filmarks.com/movies/{movie_index}/'
response = request.urlopen(url)

# ページのソースコードを取得
soup = BeautifulSoup(response)
response.close()

for page in pages:
    url = f'https://filmarks.com/movies/{movie_index}?page='+str(page)+''

    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    response.close()

    # レビューゾーンのスクレイピング
    # class属性が「p-main-area p-timeline」のdivタグを検索する
    p_main_area = soup.find('div', class_='p-main-area p-timeline')

    # class属性が「p-mark__review」であるdivタグを検索する
    score = p_main_area.find_all('div', class_='c-rating__score')
    review = p_main_area.find_all('div', class_='p-mark__review')
    date = p_main_area.find_all('time', class_='c-media__date')


    for i in range(len(score)):
        data_text = date[i].text.split(sep)
        _df = pd.DataFrame({'score': [score[i].text],
                            'review': [review[i].text],
                            'date': data_text[0]})
        df_list.append(_df)
        
    print("page%s is over"%page )

del df_list[0:10]

# 一つのデータフレームにまとめる
df_review = pd.concat(df_list).reset_index(drop=True)
print(df_review.shape)
df_review.head()

# スコアがない場合は０を入れる
df_review['score'].replace("-", 0 ,inplace=True)

# スコアを数値化
df_review['score'] = df_review['score'].astype(float)

# スクレイピングしたデータフレームをcsv形式で保存
df_review.to_csv(f'dataframe/filmarks_review_{movie_name}.csv', index=False, encoding='utf_8_sig')