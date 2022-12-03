import string, re
import streamlit as st
from nltk.tokenize import word_tokenize, sent_tokenize
from TurkishStemmer import TurkishStemmer
from nltk.corpus import stopwords
import zeyrek
from tqdm import tqdm

st.set_page_config(page_title="Normalizasyon", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; '>Normalizasyon</h1>", unsafe_allow_html=True)
st.sidebar.header("Normalizasyon")

st.info("""
Metin normalleştirme, metnin kalitesini artırmayı ve makinelerin işlemesine uygun hale getirmeyi amaçlayan bir ön işleme adımıdır . Metin normalleştirmedeki dört ana adım, büyük/küçük harf normalleştirme, simgeleştirme ve durdurma sözcüğü kaldırma, Konuşma Bölümleri (POS) etiketleme ve kök çıkarmadır.""")
# st.info("Stemming ve lemmatization, bir kelimenin arkasındaki anlamı analiz etmek için kullanılan yöntemlerdir . Stemming kelimenin kökünü kullanırken, lemmatizasyon kelimenin kullanıldığı bağlamı kullanır.")


def preprocess(text: str):
    text = text.lower()
    text = text.replace('\n', ' ')
    srcWords = text.split(' ')
    trgWords = []
    analyzer = zeyrek.MorphAnalyzer()
    for word in tqdm(srcWords):
        if len(word) == 0:
            continue

        lastPunc = ''
        if word[-1] in string.punctuation:
            lastPunc = word[-1]

        word = word.translate(str.maketrans('', '', string.punctuation))
        if word in stopwords.words("turkish"):
            continue
        word = analyzer.lemmatize(word)[0][1][0] + lastPunc
        trgWords.append(word)
    return " ".join(trgWords)


cols = st.columns(2)
with cols[0]:
    text = st.text_area(label="",value="""Maaş müşterisi olmam       halinde halen daha ek hesap veya kredi kartı alamıyorum... 'Diğer bankalar' kart verirken QNB Finansbank hiç umursamıyor. Başvuru yaptığım zaman beni şubelere yönlendiriyorlar..!
Daha önceden yaşamış olduğum bazı banka sıkıntıları yüzünden kart verilmediğini belirtiyorlar.""", height=300)
    button = st.button("Normalize")

with cols[1]:
    if button:
        process_text = preprocess(text)
        st.text_area(label = "", value=process_text, height=300)
