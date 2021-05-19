import requests
import json
import time
import telebot
from datetime import date
from datetime import timedelta  
from flask import Flask

TOKEN = "1808547179:AAEvffvEj5ZZ5nDA0NZeXe1VQAmboD-vA8Y"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
while(1):
    welcome="https://api.telegram.org/bot1808547179:AAEvffvEj5ZZ5nDA0NZeXe1VQAmboD-vA8Y/sendMessage?chat_id=-499789072&text=Hello i'm alive. When there is any slot free in your district, I will notify you every 60 Second. Thanks !! For your Patience."
    requests.get(welcome)
    msg=[]
    for i in range(1,8):
     today = date.today()+timedelta(days=i)
     day=today.strftime("%d-%m-%Y")
     for i in range[710,763]:
        i=str(i)
        x="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+i+"&date="+day
        data=requests.get(x,headers=headers)
        results=json.loads(data.text)
        count=results["sessions"]
        if(len(count)>0):
            msg=[]
            for session in count:
                msg.append({
            "Ditrict Name":session["district_name"],
		    "Block Name":session["block_name"],
            "Block PIN":session["pincode"],
			"Center Name":session["name"],
			"Center Address":session["address"],
			"Date":session["date"],
			"Free Space":session["available_capacity"],
			"Chages":session["fee"],
			"Name Of Vaccine":session["vaccine"],
			"Age For Vaccination":session["min_age_limit"],
            "Cowin Login":["https://selfregistration.cowin.gov.in/"]
            })
            parse_data=json.dumps(msg)
            parse_data=parse_data.replace("{","")
            parse_data=parse_data.replace("}","\n\n")
            parse_data=parse_data.replace("[","")
            parse_data=parse_data.replace("]","")
            parse_data=parse_data.replace(",","\n\n")
            parse_data=parse_data.replace('"',' ')
            print(parse_data)
            welcome1="https://api.telegram.org/bot1808547179:AAEvffvEj5ZZ5nDA0NZeXe1VQAmboD-vA8Y/sendMessage?chat_id=-499789072&text=Notification for: "+session["district_name"]
            requests.get(welcome1)
            nd_url="https://api.telegram.org/bot1808547179:AAEvffvEj5ZZ5nDA0NZeXe1VQAmboD-vA8Y/sendMessage?chat_id=-499789072&text="+parse_data
            y=requests.get(nd_url)
            
            print(y)
            time.sleep(10)
    time.sleep(60)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

