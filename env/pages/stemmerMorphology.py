import pandas as pd
import streamlit as st
from Deasciifier import NGramDeasciifier, SimpleDeasciifier
import test,text2sentences
from nltk.tokenize import word_tokenize
from Deasciifier.Deasciifier import Deasciifier
import string
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from Corpus.Sentence import Sentence


st.set_page_config(page_title="Stemmer: Morfolojik Anlam", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; '>Stemmer: Morfolojik Anlam</h1>", unsafe_allow_html=True)
st.sidebar.header("Stemmer: Morfolojik Anlam")
# st.info("""Türkçe karakterler (ş, ı, ö, ç, ğ, ü) kullanmadan yazılmış yazıları doğru Türkçe karakter karşılıkları ile düzeltmeye denir.""")  # DEASCIIFIER
st.info("""Bir kelimenin doğru morfolojik analizini seçmek için bir morfolojik ayırıcı kullanılır .
 Morfolojik anlam ayrımı, genellikle doğal dil işlemenin ilk adımlarından biri olduğu ve performansı sonraki analizleri etkilediği için önemlidir.""")

cols = st.columns(2)
with cols[0]:
    text = st.text_area(label="",value="""Maaş müşterisi olmam       halinde halen daha ek hesap veya kredi kartı alamıyorum... 'Diğer bankalar' kart verirken QNB Finansbank hiç umursamıyor. Başvuru yaptığım zaman beni şubelere yönlendiriyorlar..!
Daha önceden yaşamış olduğum bazı banka sıkıntıları yüzünden kart verilmediğini belirtiyorlar.""", height=300)
    button = st.button("Analyse")
with cols[1]:
    tokenizerList = []
    if button:
        fsm = FsmMorphologicalAnalyzer()
        parseLists = fsm.morphologicalAnalysis(Sentence(text))
        cleanList = [word.lower() for word in text.split() if word not in string.punctuation]
        wordList = []
        for word in cleanList:
            wordList.append(word[:2])
        stemList, morpList, morphologList = [], [], []
        totalList = []
        for i in range(len(parseLists)):
            for j in range(parseLists[i].size()):
                morphologList = list(str(parseLists[i].getFsmParse(-1)).split("+"))
                totalList.append(str(parseLists[i].getFsmParse(-1)).split())
                if wordList[i] == morphologList[0][:2]:
                    stemList.append(cleanList[i])
                    morpList.append(parseLists[i].getFsmParse(-1))
                break
        st.text_area(label="",value=totalList, height=300)
        dfStem = pd.DataFrame(stemList, columns=["Stem"])
        dfMorpholog = pd.DataFrame(morpList, columns=["Morphological Tags"])
        df = pd.concat([dfStem,dfMorpholog], axis=1)
        st.dataframe(df, width=600)

