import pandas as pd
import spacy
import pandas as pd

movie_name = 'ultraman'

# 使用する単語の品詞とストップワードの指定
include_pos = ('NOUN', 'PROPN', 'VERB', 'ADJ')
stopwords = ('する', 'ある', 'ない', 'いう', 'もの', 'こと', 'よう',
             'なる', 'ほう', 'いる', 'くる', 'お', 'つ', 'おる', 'とき', 'しまう',
             'いく', 'みる', 'ため', 'ところ', '際', '他', '時', '中', '方', '目', 
             '回', '年', '点', '前', '後', '思う', '行く')

# レビューデータの読み込み
df = pd.read_csv(f'dataframe/filmarks_review_{movie_name}.csv', encoding='utf-8', usecols=[1,2]).values.tolist()
df_review = []
df_date = []
for s in df:
    df_review.append(s[0])
    df_date.append(s[1])

result = ' '.join(map(str, df_review))
text_file = open(f'text/review_in_{movie_name}.txt', 'w')
text_file.write(result)
text_file.close()