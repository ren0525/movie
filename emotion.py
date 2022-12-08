#必要なモジュールをインポート
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
import demoji
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import MeCab
from mlask import MLAsk


#pandasライブラリで読み込み。自動的にカラム名設定。
df = pd.read_excel("dataframe/review_data.xlsx", usecols="B:K").values.tolist()

wakati_list = []
cos_list = []
adjustment_cosine_similarity = []
df_list = []
emotion_list = ['suki', 'iya', 'none', 'yorokobi', 'aware', 'takaburi', 'yasu', 'kowa', 'ikari', 'haji', 'odoroki']

movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', '2001年宇宙の旅', 'ウエストサイドストーリー',
              'マリグナント', 'イコライザー', 'グレムリン', '孤狼の血', '羊たちの沈黙' ]

            
for review in df:
    word_list = ''
    result = ' '.join(map(str, review))
    text_1 = demoji.replace(string=result, repl="")
    m=MeCab.Tagger()
    m1=m.parse(text_1)
    for row in m1.split("\n"):
        word =row.split("\t")[0]#タブ区切りになっている１つ目を取り出す。ここには形態素が格納されている
        if word == "EOS":
            break
        elif word == 'nan':
            continue
        else:
            pos = row.split("\t")[1].split(',')#タブ区切りになっている2つ目を取り出す。ここには品詞が格納されている
            if ("名詞" in pos and '一般' in pos and '非自立' not in pos) or ("名詞" in pos and '固有名詞' in pos and '非自立' not in pos) in pos:
                word_list = word_list + ' ' + word 
    wakati_list.append(word_list)
wakati_list_np = np.array(wakati_list) # リストをndarrayに変換

emotion_analyzer = MLAsk()

for filename in wakati_list_np:
    emotion_count1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    emotion = emotion_analyzer.analyze(filename)
    if emotion['emotion'] is not None:
        #kに感情名、vに対象となった単語が入る。
        for k,v in emotion['emotion'].items():
            index = emotion_list.index(k)
            emotion_count1[index] += len(v) #　複数の単語がある場合、その数だけ感情値としてカウントする。
    else:
        emotion_count1[2] += 1
    emotion_ave1 = sum(emotion_count1)/11
    num1 = 0
    for i in emotion_count1:
        emotion_count1[num1] = i - emotion_ave1
        num1 += 1
    emo_np1 = np.array([emotion_count1])
    #感情値のコサイン類似度を出力
    df_list.append(emo_np1[0])
cs = cosine_similarity(df_list, df_list)
print(np.round(cs, decimals=3))

