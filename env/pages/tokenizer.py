import streamlit as st
from nltk.tokenize import word_tokenize


st.set_page_config(page_title="Tokenizer", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; '>Word Tokenizer</h1>", unsafe_allow_html=True)
st.sidebar.header("Word Tokenizasyon")
st.info("""Metin içindeki kelimeleri anlamlı küçük birim parçacıklarına ayırma işlemidir.""")

cols = st.columns(2)
with cols[0]:
    text = st.text_area(label="",value="""Maaş müşterisi olmam       halinde halen daha ek hesap veya kredi kartı alamıyorum... 'Diğer bankalar' kart verirken QNB Finansbank hiç umursamıyor. Başvuru yaptığım zaman beni şubelere yönlendiriyorlar..!
Daha önceden yaşamış olduğum bazı banka sıkıntıları yüzünden kart verilmediğini belirtiyorlar.""", height=300)
    button = st.button("Tokenize")
with cols[1]:
    tokenizerList = []
    if button:
        for word in word_tokenize(text):
            tokenizerList.append(str(word))
        st.text_area(label="",value="\n".join(tokenizerList), height=300)
