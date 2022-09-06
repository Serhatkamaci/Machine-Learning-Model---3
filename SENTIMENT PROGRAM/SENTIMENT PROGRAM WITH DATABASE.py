from textblob import TextBlob
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pandas, xgboost, numpy, textblob, string
import pandas as pd
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from textblob import Word
nltk.download('wordnet')
import time
import sqlite3 as sq

con=sq.connect("Sentiment.db")
cursor=con.cursor()

!pip install --trusted-host pypi.org ipython-sql 

%load_ext sql

%sql sqlite:///Sentiment.db
    
def Veri_Tabanı_Tablo_Olusturma():
    
    print("\n-----------  WELCOME  -----------")
    print("CREATING TABLE")
    time.sleep(2)
    cursor.execute("CREATE TABLE IF NOT EXISTS SENTIMENT_PROGRAM(PHRASE TEXT, RESULT TEXT)")
    print("TABLE CREATED\n")
    con.commit()

def Veri_Tabani_Veri_Ekleme(a):

   
    x=a[0]
    
    if a[1]==1:
        print("STARTING INSERTION ...")
        time.sleep(2)
        con.execute("insert into SENTIMENT_PROGRAM values(?,?)",(x,"POSITIVE"))
        con.commit()
        print("ADDING COMPLETED.")
        
    else:
        con.execute("insert into SENTIMENT_PROGRAM values(?,?)",(x,"NEGATIVE"))
        con.commit()
        
        
def Veri_Tabani_Temizleme():
    
    print("\nSTARTING THE CELANUP ...")
    time.sleep(2)
    con.execute("delete from SENTIMENT_PROGRAM")
    con.commit()
    print("CLEANING PROCESS FINISHED.")
    

def Menu():
              
        data=pandas.read_csv("train.tsv",sep="\t")

        df=data.copy()
        df["Sentiment"].replace(0,value="negative",inplace=True)
        df["Sentiment"].replace(1,value="negative",inplace=True)

        df["Sentiment"].replace(3,value="positive",inplace=True)
        df["Sentiment"].replace(4,value="positive",inplace=True)

        df=df[(df.Sentiment=="negative") | (df.Sentiment=="positive")] 

        df.groupby("Sentiment").count() 
        dmf=pandas.DataFrame()

        dmf["text"]=df["Phrase"][56000:]
        dmf["label"]=df["Sentiment"][56000:]

        dmf["text"] = dmf["text"].apply(lambda x: " ".join(x.lower() for x in x.split()))
        dmf["text"] = dmf["text"].str.replace("[^\w\s]","")
        dmf["text"] = dmf["text"].str.replace("\d","")
        
        sw = stopwords.words('english')
        dmf["text"]= dmf["text"].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
        sil = pd.Series(' '.join(dmf["text"]).split()).value_counts()[-1000:]
        dmf["text"] = dmf["text"].apply(lambda x: " ".join(x for x in x.split() if x not in sil))
        dmf["text"] = dmf["text"].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

        x_train,x_test,y_train,y_test=model_selection.train_test_split(dmf["text"],dmf["label"],random_state=1)

        encoder=preprocessing.LabelEncoder()

        y_train=encoder.fit_transform(y_train)
        y_test=encoder.fit_transform(y_test) 

        vectorizer=CountVectorizer()
        vectorizer.fit(x_train)
        x_train_count=vectorizer.transform(x_train) 
        x_test_count=vectorizer.transform(x_test)
        sentence=input("CAN YOU WRITE A SENTECE ?\n --> ")
        k=sentence
        sentence=pd.Series(sentence)   
        print("\nMY PROGRAMME PROCESSES THIS SENTENCE.")
        sentence=vectorizer.transform(sentence)
        time.sleep(2)
        print("THIS SENTENCE PROCESSED.")

        nb = naive_bayes.MultinomialNB()
        nb_model = nb.fit(x_train_count,y_train)
       
        a=nb_model.predict(sentence)
        for i in a:
            print("\nTHIS SITUATION IS BEING EVALUATED.")
            time.sleep(2)
            if i== 1:
                print("\n*********RESULT*********\nTHIS SENTENCE IS POSITIVE.")         
            else:
                print("\n*********RESULT*********\nTHIS SENTENCE IS NEGATIVE.")   
        l=[]
        l.append(k)
        l.append(a[0])
        Veri_Tabani_Veri_Ekleme(l)

    
while True:
    
    print("""
    
                                                SENTIMENT ANAlYSIS PROGRAM
    
    YOU CAN CHOOSE THIS SELECTIONS ONE OF THIS CHOCIES
    
    ----------------------------------------------------------------------------------------------
    
    ONE --> YOU WILL ENTER A SENTENCE.CountVectorizer ALGORITHM WILL PROCESS THIS SENTENCE.
    
    AFTER THAT MY PROGRAMME WILL CHOOSE POSITIVE OR NEGATIVE PHRASE.
    
    TWO --> CREATE TABLE FOR DATABASE.
    
    THREE --> ADD DATABASE DATA.
    
    FOUR --> DATABASE CELANING.
    
    FIVE --> IF YOU CAN THIS SELECTION MY PROGRAM WILL CLOSED. 
    
    THANKS FOR USING MY PROGRAM.
    
    ----------------------------------------------------------------------------------------------
    
    
    
    """)
    
    X=int(input("WELCOME TO MY PROGRAM. CAN YOU ENTER A CHOICE TO MY PROGRAM ?\n --> "))
    
    if X == 1:
        Menu()
        continue
    
    if X == 2:
        Veri_Tabanı_Tablo_Olusturma()
        
    elif X==3:
        Veri_Tabani_Veri_Ekleme()
    
    elif X==4:
        Veri_Tabani_Temizleme()
    
    elif X==5:
        print("\nTHIS PROGRAM IS ENDING.")
        time.sleep(2)
        print("THANKS FOR USING MY PROGRAM.")
        break
    else:
        print("\n----------- ERROR ---------\nYOU CAN SELECTED WRONG CHOICE. CAN YOU ENTER A CHOICE TO MY PROGRAM ?\n")
        


