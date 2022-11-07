from tf_idf import TfIdf
from mlask import MLAsk
emotion_analyzer = MLAsk()
print(emotion_analyzer.analyze("ウルトラマンの題名に引かれて見てしまったお子様達とそのお母さん達は残念。そしてかるーい暇つぶしに見た俺。まず子供の時に見たウルトラマンとは違うね。人類の生存と人愛を好きになったウルトラマンの覚悟と決死。題材として子供にはわかんないと思うが幼年期、ウルトラマンを見ていたおっちゃん達にはたまらなかった。ゼットンもゾフィーも居た。キャストも良かった。特に長澤まさみの匂いを嗅がれた所、おっちゃんたまらん。"))

# tf = TfIdf()
# tf.add_file('シンゴジラ','text/review_in_godzila.txt')
# tf.add_file('トップガン','text/review_in_topgun.txt')
# tf.create()
# print(tf.top_words())
# print(tf.word_count())