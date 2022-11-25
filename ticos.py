import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer
import demoji
from sklearn.feature_extraction.text import CountVectorizer
import MeCab
from mlask import MLAsk
import pandas as pd

movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', 'マイフェアレディ', 'ウエストサイドストーリー',
              'テリファー', 'レプリカズ', 'デイシフト', 'バーフバリ', 'スケートキッチン', 'ユーザに入力されたテキスト']
filenames=['text/popular/review_in_godzilla.txt','text/popular/review_in_forrestgump.txt','text/popular/review_in_topgun.txt', 'text/popular/review_in_parasite.txt', 'text/popular/review_in_titanic.txt', 'text/review.txt',
            'text/standard/review_in_ultraman.txt', 'text/standard/review_in_godfather.txt', 'text/standard/review_in_rocky.txt', 'text/standard/review_in_myfairlady.txt', 'text/standard/review_in_westsidestory.txt',
            'text/unpopular/review_in_terrifier.txt', 'text/unpopular/review_in_replicas.txt', 'text/unpopular/review_in_baahubali.txt', 'text/unpopular/review_in_dayshift.txt', 'text/unpopular/review_in_skatekitchen.txt']
wakati_list = []
for filename in filenames: # テキストファイルを読み出しtextに代入 
    with open(filename,'r',encoding='utf-8') as f:
        text = f.read()
        word_list = ""
    text_1 = demoji.replace(string=text, repl="")  
    m=MeCab.Tagger()
    m1=m.parse(text_1)
    for row in m1.split("\n"):
        word =row.split("\t")[0]#タブ区切りになっている１つ目を取り出す。ここには形態素が格納されている
        if word == "EOS":
            break
        else:
            pos = row.split("\t")[1].split(',')#タブ区切りになっている2つ目を取り出す。ここには品詞が格納されている
            if ("名詞" in pos and '一般' in pos and '非自立' not in pos) or ("名詞" in pos and '固有名詞' in pos and '非自立' not in pos) in pos:
                word_list = word_list + ' ' + word 
    wakati_list.append(word_list)
wakati_list_np = np.array(wakati_list) # リストをndarrayに変換

# vectorizerの生成。token_pattern=u'\\b\\w+\\b'で1文字の語を含む設定
vectorizer = CountVectorizer(token_pattern=u'\\b\\w+\\b')
# transformerの生成。TF-IDFを使用
transformer = TfidfTransformer()
tf = vectorizer.fit_transform(wakati_list_np) # ベクトル化
tfidf = transformer.fit_transform(tf) # TF-IDF
tfidf_array = tfidf.toarray()
cos = cosine_similarity(tfidf_array,tfidf_array)  # cos類似度計算
df_cos = pd.DataFrame(cos, index=movie_name, columns=movie_name)
df_cos.to_excel('dataframe/filmarks_review_cos.xlsx', index=movie_name, columns=movie_name)

