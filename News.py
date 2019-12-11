import requests,json,textwrap

from datetime import datetime
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

#Colors
TitleColor = (36,41,63)
NewsBGColor = (28,164,211)
DescriptionColor = (64,159,233)


def GetNews():
    try:
        with open("Config.json") as f:
            Config = json.loads(f.read())
            Language = Config["Language"]
            CustomMessage = Config["CustomMessage"]
    except:
        print("Sorry something went wrong while reading the config file...")
        return
    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : Language.lower()}).json()["battleroyalenews"]["news"]["messages"]
    
    AvoidScam = "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg"

    if (len(FortniteGame) == 1 and FortniteGame[0]["image"] != AvoidScam) or (len(FortniteGame) == 2 and FortniteGame[1]["image"] == AvoidScam):
        return News1(FortniteGame[0],Language,CustomMessage)
    elif (len(FortniteGame) == 2 and FortniteGame[0]["image"] != AvoidScam and FortniteGame[1]["image"] != AvoidScam):
        return News2(FortniteGame,Language,CustomMessage)
    else:
        return News3(FortniteGame,Language,CustomMessage)

def News1(Message,Language,CustomMessage):
    NewsAdpsace = Image.open("assets/3/T_newPVP_Texture.png","r")
    Background = Image.open("assets/Background.png","r")
    Draw = ImageDraw.Draw(Background)

    Title = Message["title"].upper()
    Description = Message["body"]

    def Adspace(X,Y,SpaceText):
        X -= 14
        Y -= 14

        AdspaceLeft = NewsAdpsace.crop((0, 0, 23, 50))
        AdspaceMiddle = NewsAdpsace.crop((23, 0, 66, 50)).resize((AdspaceFont.getsize(SpaceText)[0] - 15,50), Image.ANTIALIAS)
        AdspaceRight = NewsAdpsace.crop((66, 0, 100, 50))
    
        Background.paste(AdspaceLeft,(X,Y),AdspaceLeft)
        Background.paste(AdspaceMiddle,(X + AdspaceLeft.width,Y),AdspaceMiddle)
        Background.paste(AdspaceRight,(X + AdspaceLeft.width + AdspaceMiddle.width,Y),AdspaceRight)
        AdspaceLeft = NewsAdpsace.crop((0, 0, 21, 50))

        if Language.upper() == "JA":
            Draw.text((X + AdspaceLeft.width - 3, Y + 7), SpaceText, font=AdspaceFont)
        else:
            Draw.text((X + AdspaceLeft.width - 3, Y + 4), SpaceText, font=AdspaceFont)

    #Fonts
    if Language.upper() == "JA":
        AdspaceFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.ttf', 32)  
    else:
        AdspaceFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/BurbankSmall-Bold.ttf', 32)
    
    GenAt = ImageFont.truetype('assets/Fonts/BurbankSmall-Bold.ttf', 25)
    Credits = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 45)

    NewsImage = Image.open(BytesIO(requests.get(Message["image"]).content)) #Download the Imag
    NewsImage = NewsImage.resize((1024, 510), Image.ANTIALIAS) #Resize the downloaded Image

    NewsCardHeight = 0
    TitleFontSize = 60

    if Language.upper() == "JA":
        while ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize).getsize(Title)[0] > 1035:
            TitleFontSize -= 1
        
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize)
        
        NewDesc = ""
        for Desc in Description.split("\n"):
            for Des in textwrap.wrap(Desc, width=45):
                NewDesc += f'\n{Des}'

        Description = NewDesc #Split the Description
    else:
        while ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize).getsize(Title)[0] > 1035:
            TitleFontSize -= 1
        
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize)
        
        NewDesc = ""
        for Desc in Description.split("\n"):
            for Des in textwrap.wrap(Desc, width=65):
                NewDesc += f'\n{Des}'

        Description = NewDesc #Split the Description

    NewsCardHeight += Draw.multiline_textsize(Description,font=DescriptionFont,spacing=17)[1] + 26 #Add the Description
    NewsCardHeight += TitleFont.getsize(Title)[1] #Add the Title Size
    NewsCardHeight += NewsImage.height #Add the Image Size

    #Positions
    Left = ((Background.width - (NewsImage.width + 10))) / 2
    Top = (Background.height - NewsCardHeight - 154) - ((Background.height - NewsCardHeight - 154) / 2)
    Right = Background.width - Left
    Buttom = Background.height - ((Background.height - NewsCardHeight + 154) / 2)

    Draw.rectangle((Left,Top,Right,Buttom),fill="white")#Draw White Box
    Draw.text((Left + 28,Top + 5 + NewsImage.height + 9),Title,TitleColor, font=TitleFont) #Draw Title
    Draw.multiline_text((Left + 29, Top + NewsImage.height + TitleFont.getsize(Title)[1] - 2),Description,DescriptionColor,font=DescriptionFont,spacing=17) #Draw Description
    Draw.text((10,10),datetime.now().strftime('Generated at %Y-%m-%d %H:%M:%S UTC | Assets Property of Epic Games and Responsive Owners'),font=GenAt) #Draw Gen. At
    if Credits.getsize("Made by @LupusLeaks")[1] < (Top - 30):
        Draw.text(((Background.width - Credits.getsize("Made by @LupusLeaks")[0]) / 2,Top - 65),"Made by @LupusLeaks",font=Credits)
    Background.paste(NewsImage,(int(Left) + 5,int(Top) + 5)) #Paste News Image

    #Draw Custom Message
    Middle = (Background.width - Credits.getsize(CustomMessage)[0]) / 2
    Y = Buttom + ((Background.height - Buttom) - Credits.getsize(CustomMessage)[1]) / 2
    Draw.text((Middle,Y),CustomMessage,font=Credits)

    if "adspace" in Message:
        Adspace(int(Left),int(Top),Message["adspace"])

    return Background


def News3(data,Language,CustomMessage):
    NewsAdpsace = Image.open("assets/3/T_newPVP_Texture.png","r")

    #Fonts
    if Language.upper() == "JA":
        AdspaceFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.ttf', 25)  
        NewsFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', 190)
    else:
        AdspaceFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/burbanksmall-bold.ttf', 25)
        NewsFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 235)
        

    DateFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 35)
    GenAt = ImageFont.truetype('assets/Fonts/BurbankSmall-Bold.ttf', 25)
    Credits = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 45)

    Background = Image.open("assets/Background.png","r")
    Draw = ImageDraw.Draw(Background)

    def Adspace(X,Y,SpaceText):
        X -= 14
        Y -= 14

        AdspaceLeft = NewsAdpsace.crop((0, 0, 23, 50))
        AdspaceMiddle = NewsAdpsace.crop((23, 0, 66, 50)).resize((AdspaceFont.getsize(SpaceText)[0] - 15,50), Image.ANTIALIAS)
        AdspaceRight = NewsAdpsace.crop((66, 0, 100, 50))
    
        Background.paste(AdspaceLeft,(X,Y),AdspaceLeft)
        Background.paste(AdspaceMiddle,(X + AdspaceLeft.width,Y),AdspaceMiddle)
        Background.paste(AdspaceRight,(X + AdspaceLeft.width + AdspaceMiddle.width,Y),AdspaceRight)
        AdspaceLeft = NewsAdpsace.crop((0, 0, 21, 50))

        if Language.upper() == "JA":
            Draw.text((X + AdspaceLeft.width - 3, Y + 7), SpaceText, font=AdspaceFont)
        else:
            Draw.text((X + AdspaceLeft.width - 3, Y + 4), SpaceText, font=AdspaceFont)

    msg = ""
    TitleFontS = 100
    Title = ""
    for index,Message in enumerate(data):
        if index > 2:
            break

        if len(Message["body"]) > len(msg) and "body" in Message:
            msg = Message["body"]
            
        TitleFontSize = 60
        while ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize).getsize(Message["title"].upper())[0] > 507:
            TitleFontSize -= 1
        if TitleFontSize < TitleFontS:
            TitleFontS = TitleFontSize
            Title = Message["title"]

    if Language.upper() == "JA":
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontS)
    else:
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontS)

    if Language.upper() == "JA":
        NewDesc = ""
        for Desc in msg.split("\n"):
            for Des in textwrap.wrap(Desc, width=19):
                NewDesc += f'\n{Des}'

        msg = NewDesc #Split the Description
    else:
        NewDesc = ""
        for Desc in msg.split("\n"):
            for Des in textwrap.wrap(Desc, width=39):
                NewDesc += f'\n{Des}'

        msg = NewDesc #Split the Description
    
    NewsCardHeight = 0
    NewsCardHeight += 257 + 5 #Add the Image Size
    NewsCardHeight += TitleFont.getsize(Title)[1] + 17 #Add the Title Size
    NewsCardHeight += Draw.multiline_textsize(msg,font=DescriptionFont,spacing=13)[1] + 7#Add the Description

    if Language.upper() == "JA":
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontS)
    else:
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontS)

    #Positions
    Buttom = Background.height - ((Background.height - NewsCardHeight - 122) - ((Background.height - NewsCardHeight - 122) / 2))
    Top = ((Background.height - NewsCardHeight + 122) / 2)
    
    if Language.upper() == "JA":
        NewsT = "ニュース"
    else:
        NewsT = "NEWS"
    #Draw News
    Middle = (Background.width - NewsFont.getsize(NewsT)[0]) / 2
    Y = 65 + NewsFont.getsize(NewsT)[1]

    Draw.text((Middle - 2,Top - Y),NewsT,NewsBGColor,font=NewsFont)
    Draw.text((Middle + 2,Top - Y),NewsT,NewsBGColor,font=NewsFont)

    Draw.text((Middle,Top - Y + 2),NewsT,NewsBGColor,font=NewsFont)
    Draw.text((Middle,Top - Y - 2),NewsT,NewsBGColor,font=NewsFont)

    Draw.text((Middle,Top - Y),NewsT,font=NewsFont)

    #Draw Made by Me
    Middle = (Background.width - Credits.getsize("Made by @LupusLeaks on Twitter")[0]) / 2
    Y = 25 + Credits.getsize(NewsT)[1]
    Draw.text((Middle,Top - Y),"Made by @LupusLeaks on Twitter",font=Credits)

    #Draw Date
    Draw.text((10,10),datetime.now().strftime('Generated at %Y-%m-%d %H:%M:%S UTC | Assets Property of Epic Games and Responsive Owners'),font=GenAt) #Draw Gen. At

    #Draw Custom Message
    Middle = (Background.width - Credits.getsize(CustomMessage)[0]) / 2
    Y = Buttom + ((Background.height - Buttom) - Credits.getsize(CustomMessage)[1]) / 2
    Draw.text((Middle,Y),CustomMessage,font=Credits)

    X = 109
    for index,Message in enumerate(data):
        if index > 2:
            break
        Title = Message["title"].upper()
        Description = Message["body"]
        
        NewsImage = Image.open(BytesIO(requests.get(Message["image"]).content)) #Download the Imag
        NewsImage = NewsImage.resize((533, 257), Image.ANTIALIAS) #Resize the downloaded Image
        
        TitleFontSize = 43
        
        if Language.upper() == "JA":
            while ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize).getsize(Title)[0] > 507:
                TitleFontSize -= 1
        
            TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize)
            NewDesc = ""
            for Desc in Description.split("\n"):
                for Des in textwrap.wrap(Desc, width=19):
                    NewDesc += f'\n{Des}'

            Description = NewDesc #Split the Description
        else:
            while ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize).getsize(Title)[0] > 507:
                TitleFontSize -= 1
        
            TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize)
            NewDesc = ""
            for Desc in Description.split("\n"):
                for Des in textwrap.wrap(Desc, width=39):
                    NewDesc += f'\n{Des}'

            Description = NewDesc #Split the Description
        
        Draw.rectangle((X,Top,X + 10 + 533,Buttom),fill="white")#Draw White Box
        Background.paste(NewsImage,(int(X + 5),int(Top + 5))) #paste Background
        Draw.text((X + 28,Top + 5 + NewsImage.height + 7),Title,TitleColor, font=TitleFont) #Draw Title

        Draw.multiline_text((X + 29, Top + NewsImage.height + TitleFont.getsize(Title)[1] - 2),Description,DescriptionColor,font=DescriptionFont,spacing=13) #Draw Description
        
        if "adspace" in Message:
            Adspace(int(X),int(Top),Message["adspace"])
        
        X += 579

    return Background


def News2(data,Language,CustomMessage):
    NewsAdpsace = Image.open("assets/3/T_newPVP_Texture.png","r")

    #Fonts
    if Language.upper() == "JA":
        AdspaceFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.ttf', 25) 
        NewsFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', 190)
    else:
        AdspaceFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 32)
        DescriptionFont = ImageFont.truetype('assets/Fonts/burbanksmall-bold.ttf', 25)
        NewsFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 235)
        

    DateFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 35)
    GenAt = ImageFont.truetype('assets/Fonts/BurbankSmall-Bold.ttf', 25)
    Credits = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 45)
    NewsFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', 235)

    Background = Image.open("assets/Background.png","r")
    Draw = ImageDraw.Draw(Background)

    def Adspace(X,Y,SpaceText):
        X -= 14
        Y -= 14

        AdspaceLeft = NewsAdpsace.crop((0, 0, 23, 50))
        AdspaceMiddle = NewsAdpsace.crop((23, 0, 66, 50)).resize((AdspaceFont.getsize(SpaceText)[0] - 15,50), Image.ANTIALIAS)
        AdspaceRight = NewsAdpsace.crop((66, 0, 100, 50))
    
        Background.paste(AdspaceLeft,(X,Y),AdspaceLeft)
        Background.paste(AdspaceMiddle,(X + AdspaceLeft.width,Y),AdspaceMiddle)
        Background.paste(AdspaceRight,(X + AdspaceLeft.width + AdspaceMiddle.width,Y),AdspaceRight)
        AdspaceLeft = NewsAdpsace.crop((0, 0, 21, 50))

        if Language.upper() == "JA":
            Draw.text((X + AdspaceLeft.width - 3, Y + 7), SpaceText, font=AdspaceFont)
        else:
            Draw.text((X + AdspaceLeft.width - 3, Y + 4), SpaceText, font=AdspaceFont)

    msg = ""
    TitleFontS = 100
    Title = ""
    for index,Message in enumerate(data):
        if index > 1:
            break

        if len(Message["body"]) > len(msg) and "body" in Message:
            msg = Message["body"]
            
        TitleFontSize = 60
        while ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize).getsize(Message["title"].upper())[0] > 507:
            TitleFontSize -= 1
        if TitleFontSize < TitleFontS:
            TitleFontS = TitleFontSize
            Title = Message["title"]

    if Language.upper() == "JA":
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontS)
    else:
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontS)

    if Language.upper() == "JA":
        NewDesc = ""
        for Desc in msg.split("\n"):
            for Des in textwrap.wrap(Desc, width=19):
                NewDesc += f'\n{Des}'

        msg = NewDesc #Split the Description
    else:
        NewDesc = ""
        for Desc in msg.split("\n"):
            for Des in textwrap.wrap(Desc, width=39):
                NewDesc += f'\n{Des}'

        msg = NewDesc #Split the Description
    
    NewsCardHeight = 0
    NewsCardHeight += 257 + 5 #Add the Image Size
    NewsCardHeight += TitleFont.getsize(Title)[1] + 17 #Add the Title Size
    NewsCardHeight += Draw.multiline_textsize(msg,font=DescriptionFont,spacing=13)[1] + 7#Add the Description

    if Language.upper() == "JA":
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontS)
    else:
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontS)

    #Positions
    Buttom = Background.height - ((Background.height - NewsCardHeight - 122) - ((Background.height - NewsCardHeight - 122) / 2))
    Top = ((Background.height - NewsCardHeight + 122) / 2)
    
    if Language.upper() == "JA":
        NewsT = "ニュース"
    else:
        NewsT = "NEWS"
    #Draw News
    Middle = (Background.width - NewsFont.getsize(NewsT)[0]) / 2
    Y = 65 + NewsFont.getsize(NewsT)[1]

    Draw.text((Middle - 2,Top - Y),NewsT,NewsBGColor,font=NewsFont)
    Draw.text((Middle + 2,Top - Y),NewsT,NewsBGColor,font=NewsFont)

    Draw.text((Middle,Top - Y + 2),NewsT,NewsBGColor,font=NewsFont)
    Draw.text((Middle,Top - Y - 2),NewsT,NewsBGColor,font=NewsFont)

    Draw.text((Middle,Top - Y),NewsT,font=NewsFont)

    #Draw Made by Me
    Middle = (Background.width - Credits.getsize("Made by @LupusLeaks on Twitter")[0]) / 2
    Y = 25 + Credits.getsize(NewsT)[1]
    Draw.text((Middle,Top - Y),"Made by @LupusLeaks on Twitter",font=Credits)

    #Draw Date
    Draw.text((10,10),datetime.now().strftime('Generated at %Y-%m-%d %H:%M:%S UTC | Assets Property of Epic Games and Responsive Owners'),font=GenAt) #Draw Gen. At

    #Draw Custom Message
    Middle = (Background.width - Credits.getsize(CustomMessage)[0]) / 2
    Y = Buttom + ((Background.height - Buttom) - Credits.getsize(CustomMessage)[1]) / 2
    Draw.text((Middle,Y),CustomMessage,font=Credits)

    X = 398
    for index,Message in enumerate(data):
        if index > 1:
            break
        Title = Message["title"].upper()
        Description = Message["body"]
        
        NewsImage = Image.open(BytesIO(requests.get(Message["image"]).content)) #Download the Imag
        NewsImage = NewsImage.resize((533, 257), Image.ANTIALIAS) #Resize the downloaded Image
        
        TitleFontSize = 43
        
        if Language.upper() == "JA":
            while ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize).getsize(Title)[0] > 507:
                TitleFontSize -= 1
        
            TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.ttf', TitleFontSize)
            NewDesc = ""
            for Desc in Description.split("\n"):
                for Des in textwrap.wrap(Desc, width=19):
                    NewDesc += f'\n{Des}'

            Description = NewDesc #Split the Description
        else:
            while ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize).getsize(Title)[0] > 507:
                TitleFontSize -= 1
        
            TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigCondensed-Black.ttf', TitleFontSize)
            NewDesc = ""
            for Desc in Description.split("\n"):
                for Des in textwrap.wrap(Desc, width=39):
                    NewDesc += f'\n{Des}'

            Description = NewDesc #Split the Description
        
        Draw.rectangle((X,Top,X + 10 + 533,Buttom),fill="white")#Draw White Box
        Background.paste(NewsImage,(int(X + 5),int(Top + 5))) #paste Background
        Draw.text((X + 28,Top + 5 + NewsImage.height + 7),Title,TitleColor, font=TitleFont) #Draw Title

        Draw.multiline_text((X + 29, Top + NewsImage.height + TitleFont.getsize(Title)[1] - 2),Description,DescriptionColor,font=DescriptionFont,spacing=13) #Draw Description
        
        if "adspace" in Message:
            Adspace(int(X),int(Top),Message["adspace"])
        
        X += 579

    return Background