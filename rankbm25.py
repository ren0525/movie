from rank_bm25 import BM25Okapi
import demoji
import MeCab


filenames = ['text/popular/review_in_godzilla.txt','text/popular/review_in_forrestgump.txt','text/popular/review_in_topgun.txt', 'text/popular/review_in_parasite.txt', 'text/popular/review_in_titanic.txt', 'text/review.txt',
            'text/standard/review_in_ultraman.txt', 'text/standard/review_in_godfather.txt', 'text/standard/review_in_rocky.txt', 'text/standard/review_in_myfairlady.txt', 'text/standard/review_in_westsidestory.txt',
            'text/unpopular/review_in_terrifier.txt', 'text/unpopular/review_in_replicas.txt', 'text/unpopular/review_in_baahubali.txt', 'text/unpopular/review_in_dayshift.txt', 'text/unpopular/review_in_skatekitchen.txt']
corpus = []
word_list = []

for filename in filenames: # テキストファイルを読み出しtextに代入 
    with open(filename,'r',encoding='utf-8') as f:
        text = f.read()
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
                word_list.append(word)
    corpus.append(word_list)


bm25 = BM25Okapi(corpus)

query = "ドキドキ 感動 楽しい 石原さとみ 大迫力"
tokenized_query = query.split(" ")

print(bm25.get_scores(tokenized_query))

# print(bm25.get_top_n(tokenized_query, corpus, n=1))
# ['It is quite windy in London']
