import requests
import json
from textblob import TextBlob
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk
nltk.download('punkt')
import random



videoid = "v08qmr8m_-w"
key = ""
url = "https://www.googleapis.com/youtube/v3/commentThreads?key="+key+"&part=snippet&videoId="+videoid+"&textFormat=plainText&maxResults=100&pageToken="
index = len(url)

sum = 0
positive = []
negative = []
neutral = []

currenttime = datetime.now() 
time = currenttime.strftime("%Y%m%d_%H%M%S")
file = open("YT-Analytics_"+str(time)+".txt",'a', encoding="utf-8")

count = 0

posStr = ""
negStr = ""

while True:
   try:
    response = requests.get(url)
    count=count+1
   
    if response.status_code == 200:
        json_data = response.json()
        sum = sum+json_data["pageInfo"]["totalResults"]
      
        for i in json_data["items"]:
            text = i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            blob = TextBlob(text)
            sentiment = blob.sentiment
            if sentiment.polarity > 0:
                 positive.append(text)
                 posStr=posStr+text+"\n"      
            elif sentiment.polarity < 0:
                negative.append(text)  
                negStr=negStr+text+"\n"            
            else:
                neutral.append(text)       
        if "nextPageToken" in json_data:
           items = json_data["nextPageToken"]
   
        else: 
           break
        if count>1:
            url = url[0:index]
        
        url = url+items
    else:
        print(f"Error: {response.text}")
        break
   except requests.RequestException as e:
     print(f"Error: {e}")


file.write("YT-Analytics"+"\n\n")
file.write("Total results - "+str(sum)+"\n")
file.write("Positive results - "+ str(len(positive))+"("+str(int((len(positive)/sum)*100))+"%)"+"\n")
file.write("Negative results - "+ str(len(negative))+"("+str(int((len(negative)/sum)*100))+"%)"+"\n")
file.write("Neutral results - "+ str(len(neutral))+"("+str(int((len(neutral)/sum)*100))+"%)"+"\n\n")
file.write("-> Positive"+"\n")
for i in positive:
    file.write(i+"\n")
file.write("------------------------------------------>\n")

file.write("-> Negative"+"\n")

for i in negative:
        file.write(i+"\n")
file.write("------------------------------------------>\n")

file.write("-> Neutral"+"\n")
for i in neutral:
        file.write(i+"\n")
file.write("------------------------------------------>\n")


file.close()





def generate_summary(text, summarizer, num_sentences):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

# Choose summarization method
summarizer = LsaSummarizer()
# You can try other summarization methods such as LexRankSummarizer or LuhnSummarizer

# Generate random text


# Generate summary
summaryPositive = generate_summary(posStr, summarizer, 2)
summaryNegative = generate_summary(negStr, summarizer, 2)
file = open("YT-Summary"+str(time)+".txt",'a', encoding="utf-8")
file.write("Positive"+"\n")
file.write(summaryPositive+"\n\n")
file.write("Negative"+"\n")
file.write(summaryNegative+"\n\n")
file.write()
file.close()
