from textblob import TextBlob
import pandas as pd
from difflib import SequenceMatcher
import streamlit as st
from PIL import Image
import urllib.request

similarity_URL = "https://raw.githubusercontent.com/BISMCA/Recommender-Engine/main/Topic.csv"
Reference_URL = "https://raw.githubusercontent.com/BISMCA/Recommender-Engine/main/Pos_Recommendation_Table.csv"


similarity_table = pd.read_csv(similarity_URL)
Reference_Table = pd.read_csv(Reference_URL)

#Set webpage width
#st.set_page_config(layout="wide")
#Webpage header

#Adding Cache
#Streamlit Page
st.cache(suppress_st_warning=True)

urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/e-comm.jpg?raw=true',
   "Myecommerce.png")
img = Image.open("Myecommerce.png")
st.image(img, caption = 'Myecommerce')


#Building webpage

st.subheader("Hi, Help us improve suggestions for you by giving us a feedback")

option1 = st.selectbox(
    'Product',
    ('T-shirt','Formal Shirt','Shirt'))

#Recommendation Section

Text = st.text_input('Please tell us more about the reason for your return:')

#Spellcheck
Text = str(TextBlob(Text).correct())

#Calculating Sentiment and Creating Dataframe

blob = TextBlob(Text)
sentiment = blob.sentiment.polarity
sent_score = [[abs(sentiment)]]
sentiment = pd.DataFrame(sent_score, columns = ['sent_score'])

#Calculating similarity_score and adding a column to topics
similarity_table['Similarity_Score'] = similarity_table['topic_keyword'].apply(lambda x: SequenceMatcher(None, Text, x).ratio())

#Finding Row based on highest similarity score and extracting the topic no.
topic_table = similarity_table[similarity_table['Similarity_Score'] == similarity_table.Similarity_Score.max()] 

#Finding out relevant topic number and assigning a number
tt = topic_table.loc[topic_table['Similarity_Score'] == topic_table.Similarity_Score.max(),'topic_num'].iloc[0]
tts = format(tt, '.1f')

#Filtering recommendation based on very low similarity_score

value = [[0.15]]
threshold = pd.DataFrame(value, columns = ['Value'])
y=threshold.Value[0]

#If similarity score is lower than 0.15 then recommend products with excellent product review

dtf2 = (Reference_Table[Reference_Table['Dominant_Topic'] == 3.0]) if topic_table.Similarity_Score.max() < threshold['Value'].max() else (Reference_Table[Reference_Table['Neg_Topic'].str.contains(tts)])
dtf2 = dtf2.sort_values(by = 'Sentiment', ascending = False)

#Filtering Recommendation based on Sentiment

threshold_sent_score = [[0.56]]
threshold_sentiment = pd.DataFrame(threshold_sent_score, columns = ['threshold_sent_score'])
x=threshold_sentiment.threshold_sent_score[0]
dtf2 = (dtf2.loc[dtf2['Sentiment']>= sentiment.sent_score[0]]) if sentiment.sent_score[0] <x else (dtf2.loc[dtf2['Sentiment']>=x])
dtf3 = dtf2.loc[dtf2['Item'] == option1]
Few_More_Products = dtf3[['Star Rating','Sentiment','Price', 'Item','Brand','Review','Product_Keywords']]
Few_More_Products['Word_Similarity'] = Few_More_Products['Product_Keywords'].apply(lambda x: SequenceMatcher(None, Text, x).ratio())
Few_More_Products = Few_More_Products.sort_values(by = 'Word_Similarity', ascending = False)
Few_More_Products = Few_More_Products[['Star Rating','Price','Item','Brand','Review','Product_Keywords']].head(6)


#Hiding Indices
blankIndex=['']*len(Few_More_Products)
Few_More_Products.index=blankIndex

##Webpages
if st.button('Submit'):
    st.write('Thank you for your valuable feedback') #displayed when the button is clicked
else:
    st.write('') #when the button is not clicked
    
uploaded_files = st.file_uploader("Choose an image to upload", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:",uploaded_file.name)
    st.write(bytes_data)
    
#Camera Input

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    #To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        #Check the type of bytes_data:
        #Should output: <class 'bytes'>
        st.write(type(bytes_data))
        
        
Price = st.slider('What is your budget?',0,2000)
st.write("My budget is", Price)


##Loading dataframe in streamlit webpage
st.subheader("Here are a few products that might meet your expectations:")

#Display a product table
#st.dataframe(Few_More_Products)

#Loading images
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt1.jpg?raw=true',
   "img1.png")
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt2.jpg?raw=true',
   "img2.png")
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt3.jpg?raw=true',
   "img3.png")
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt4.jpg?raw=true',
   "img4.png")
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt5.jpg?raw=true',
   "img5.png")
urllib.request.urlretrieve(
  'https://github.com/BISMCA/Recommender-Engine/blob/main/Tshirt6.jpg?raw=true',
   "img6.png")


image1 = Image.open("img1.png")
image2 = Image.open("img2.png")
image3 = Image.open("img3.png")
image4 = Image.open("img4.png")
image5 = Image.open("img5.png")
image6 = Image.open("img6.png")


#Creating columns
col1,col2,col3,col4 = st.columns(4)

#Loading Product 1
with col1:
    m=0
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image1, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 13):
        st.write('You have bought this product')
    else:
        st.write('')
    

#Loading Product 2

with col4:
    m=1
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image2, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 23):
        st.write('You have bought this product')
    else:
        st.write('')

#Loading Product 3

with col1:
    m=2
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image3, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 33):
        st.write('You have bought this product')
    else:
        st.write('')

#Loading Product 4

with col4:
    m=3
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image4, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 43):
        st.write('You have bought this product')
    else:
        st.write('')

#Loading Product 5

with col1:
    m=4
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image5, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 53):
        st.write('You have bought this product')
    else:
        st.write('')

#Loading Product 6

with col4:
    m=5
    star_rating = Few_More_Products.iloc[m,0]
    brand = Few_More_Products.iloc[m,3]
    item = Few_More_Products.iloc[m,2]
    price = Few_More_Products.iloc[m,1]
    keyword = Few_More_Products.iloc[m,5]
    st.image(image6, caption= Few_More_Products.iloc[m,2], width = 100, use_column_width=100)
    
    #Loading Product Description
    st.write('Brand:',brand)
    st.write('Price:', price)
    st.write('Rating:', star_rating)
    st.write('Product Description:', keyword)
    
    if st.button('Buy Now', key = 63):
        st.write('You have bought this product')
    else:
        st.write('')
