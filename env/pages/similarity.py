import streamlit as st
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
import string
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import zeyrek


st.set_page_config(page_title="Similarity", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; '>Similarity</h1>", unsafe_allow_html=True)
st.sidebar.header("Similarity")
st.info("""Metin benzerliği, iki kelimenin/cümlenin/belgenin birbirine ne kadar yakın olduğunu hesaplamaktır . Bu yakınlık sözcüksel veya anlamsal olabilir.""")

from tqdm import tqdm
def preprocessText(text: str):
    sentTokenizerList = [sentence.strip() for sentence in text.split(".") if sentence != '']
    print(sentTokenizerList)
    sentenceSeries = pd.Series(sentTokenizerList)
    df = pd.DataFrame(sentenceSeries, columns=["sentence"])
    sentenceList = []
    # wordFreq = pd.Series(" ".join(df.sentence).split()).value_counts()[-4:]
    analyzer = zeyrek.MorphAnalyzer()
    for sentence in df.sentence:
        wordList = []
        for word in tqdm(sentence.split()):
            if len(word) == 0:
                continue
            realWord, lemmatizeWord = analyzer.lemmatize(word)[0]
            word = lemmatizeWord[-1].lower()
            lastPunc = ""
            if word[-1] in string.punctuation:
                lastPunc = word[-1]
            word = word.translate(str.maketrans("", "", string.punctuation))
            if word not in stopwords.words("turkish"): #  and word not in wordFreq
                word = word + lastPunc
                wordList.append(word)
        sentenceList.append(" ".join(wordList))
    df = pd.DataFrame(pd.Series([sentence for sentence in sentenceList if sentence != '']), columns=["sentence"])
    return df

def cosineSimilarity(text1:str, text2: str):
    text1_set = {w.lower() for w in text1.split()}
    text2_set = {w.lower() for w in text2.split()}
    l1 =[];l2 =[]
    rvector = text1_set.union(text2_set) # a birlesim b
    for w in rvector:
          if w in text1_set: l1.append(1)
          else: l1.append(0)
          if w in text2_set: l2.append(1)
          else: l2.append(0)
    c = 0
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine


cols = st.columns(2)
with cols[0]:
    text = st.text_area(label="",value="""Maaş müşterisi olmam       halinde halen daha ek hesap veya kredi kartı alamıyorum... 'Diğer bankalar' kart verirken QNB Finansbank hiç umursamıyor. Başvuru yaptığım zaman beni şubelere yönlendiriyorlar..!
Daha önceden yaşamış olduğum bazı banka sıkıntıları yüzünden kart verilmediğini belirtiyorlar.İş Bankası altıyol şubesini arıyorum ulaşamıyorum mesaj atıyorum ulaşamıyorum beni arayın diyorum arayan yok bireysel bankacılıkla görüşme yapacağım görüşemiyorum
bir çok kez aradım şikayet etmek istemezdim başka yol bırakmadılar müşteri seçiyorlar sanırım""", height=300)
    button = st.button("Similarity")
with cols[1]:
    tokenizerList = []
    if button:
        cleanDataFrame = preprocessText(text)
        text1, text2, similarityCos = [], [], []
        for i in range(len(cleanDataFrame) - 1):  # 0       1
            first = cleanDataFrame.iloc[i, 0]
            for j in range(i + 1, len(cleanDataFrame)):  # 1 - 2 - 3       2 - 3
                second = cleanDataFrame.iloc[j, 0]
                cosine = cosineSimilarity(first, second)
                text1.append(first)
                text2.append(second)
                similarityCos.append(cosine)
                # print(f"first: {first}\tsecond: {second}\tcosine similarity: {cosine}")
        resultDf = pd.concat([pd.DataFrame(text1, columns=["text1"]), pd.DataFrame(text2, columns=["text2"]),
                              pd.DataFrame(similarityCos, columns=["similarity"])], axis=1)
        resultDf = resultDf.sort_values("similarity", ascending=False)
        st.dataframe(resultDf, height=300)

