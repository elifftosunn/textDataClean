import streamlit as st
import pandas as pd
from io import StringIO
from tqdm import tqdm
import zeyrek,string, nltk
nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords

st.set_page_config(
    page_title="Veri Temizleme",
    page_icon="📊",
)

st.write("#  📊  Veri Temizleme Aracı")

st.sidebar.success("Yapmak istediginiz işlemi seçin.")

st.markdown("""    <style> .backgroundColor {
            background-color: #8185A8;
            padding: 10px 10px 10px 10px;
            margin: 0px;
    }""", unsafe_allow_html=True)

st.markdown(""" 
    <p class="backgroundColor"; style="color:black;"> Uyarı: </p>
    <p class="backgroundColor"> Temizlenecek veri (csv,xlsx,json) formatlarında olmalıdır. </p>
    <p class="backgroundColor"; style="bottom:10px"> Temizle&İndir butonuna basılarak verinin temizlenmesi sağlanır. </p>
    <p class="backgroundColor";> Sadece bir dosya yükleyebilirsiniz.</p>
    <p class="backgroundColor";> Veri boyutu 200 MB'tan büyük olmamalıdır.</p>
""",unsafe_allow_html=True)


def preprocess(df):
    sentenceList = []
    analyzer = zeyrek.MorphAnalyzer()
    df = df[df.text.notnull()]
    for sentence in df.text:
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
            if word not in stopwords.words("turkish"):  # and word not in wordFreq
                word = word + lastPunc
                wordList.append(word)
        sentenceList.append(" ".join(wordList))
    dfText = pd.DataFrame(pd.Series([sentence.lower() for sentence in sentenceList if sentence != '']),
                            columns=["text"])
    dfText = dfText[dfText.text.notnull()]
    df = pd.concat([df.drop("text", axis=1), dfText], axis=1)
    return df

def upload_file():
    cols = st.columns([3,1])
    with cols[0]:
        uploaded_file = st.file_uploader(label="Dosyanızı yükleyiniz.", type={"csv","xlsx","json"}, key="Yukle")
        def dataCreate():
            if uploaded_file is not None:
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                    return df
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    df = pd.read_excel(uploaded_file)
                    return df
                elif uploaded_file.type == "text/json":
                    df = pd.read_json(uploaded_file)
                    return df
                else:
                    st.warning("Hatalı Format!!!")

    with cols[1]:
        st.text("")
        st.text("")
        st.text("")
        df = dataCreate()
        emptyButton = st.empty()
        cleanButton = emptyButton.button(label="Temizle&İndir")
        if cleanButton:
            if df is not None:
                df = preprocess(df)
                emptyButton.empty()
                st.download_button(
                        label="İndir",
                        data=df.to_csv(index=False).encode("utf-8"),
                        file_name='cleanBankData.csv',
                        mime='text/csv'
                )
            else:
                st.warning("Dosya yüklenmedi..!")

upload_file()

