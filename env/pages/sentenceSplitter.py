import streamlit as st
from nltk.tokenize import sent_tokenize

st.set_page_config(page_title="Sentence Splitter", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; '>Sentence Splitter</h1>", unsafe_allow_html=True)
st.sidebar.header("Sentence Splitter")
st.info("""Metni cümlelere bölme işlemidir.""")
cols = st.columns(2)

with cols[0]:
    text = st.text_area(label="",value="""Maaş müşterisi olmam       halinde halen daha ek hesap veya kredi kartı alamıyorum... 'Diğer bankalar' kart verirken QNB Finansbank hiç umursamıyor. Başvuru yaptığım zaman beni şubelere yönlendiriyorlar..!
Daha önceden yaşamış olduğum bazı banka sıkıntıları yüzünden kart verilmediğini belirtiyorlar.""", height=300)
    button = st.button("Split")
with cols[1]:
    if button:
        sentenceList = []
        for sentence in sent_tokenize(text):
            sentenceList.append(sentence)
        st.text_area(label="", value="\n".join(sentenceList), height=300)
