import News,json,requests,time,tweepy,io,sys

try:
    with open("Config.json") as f:
        Config = json.loads(f.read())
        Language = Config["Language"]
        CustomMessage = Config["CustomMessage"]
        consumer_key = Config["consumer_key"]
        consumer_secret = Config["consumer_secret"]
        access_token = Config["access_token"]
        access_token_secret = Config["access_token_secret"]
        delay = Config["CheckNewsEveryXSeconds"]
except:
    sys.exit()
    print("Sorry something went wrong while reading the config file.")

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    redirect_url = auth.get_authorization_url()
    api = tweepy.API(auth)
except tweepy.TweepError:
    sys.exit()
    print("Sorry the Auth you are using is invaild.")

while True:
    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : Language.lower()}).json()["battleroyalenews"]["news"]["messages"]
    
    with open("StoredNews.json") as f:
        StoredNews = json.loads(f.read()) #Load the stored news

    if FortniteGame != StoredNews: #If the news on the api aren't the same as stored on the file
        News.GetNews().save("News.png") #Idk how to post the image directly on twitter... so we need to save it as a file first
        api.update_with_media("News.png")#Upload the image

        with open("StoredNews.json","w+") as f:
            f.write(json.dumps(FortniteGame)) #Overwrites the old news
        print("Uploaded News on Twitter")
    else:
        time.sleep(delay) #The script will wait for 5 Seconds