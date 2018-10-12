import requests
import json

from flask import Flask, jsonify, render_template, request
from errors import bad_request

app = Flask(__name__)

# query = "To secure the plutonium, White Widow tasks Ethan with extracting Lane from an \
# armoured convoy moving through Paris. She provides one of the plutonium cores as a payment \
# in kind for the mission."

#s = "Alice Kingsleigh has spent the past three years following in her father's footsteps and sailing the high seas. Upon her return to London from China, she learns her ex-fianc\u00e9, Hamish Ascot, has taken over his father's company and plans to have Alice sell him over her father's ship in exchange for her family home.[clarification needed] Alice follows a butterfly she recognizes as Absolem and returns to Wonderland through a mirror.\nAlice is greeted by the White Queen, the White Rabbit, the Tweedles, the Dormouse, the March Hare, Bayard and the Cheshire Cat. They inform her that the Mad Hatter, Tarrant Hightopp, is acting madder than usual because his family is missing. Alice tries to console him, but the Mad Hatter remains sure of his family's survival of the Attack of the Jabberwocky day.\nBelieving that finding the Hatter's family is the only way to stop his deteriorating health, the White Queen sends Alice to consult Time himself and convince him to save the Hatter's family in the past. The Queen cautions Alice that history will be destroyed if anyone sees their past or future self. Upon visiting Time's palace, Alice finds the Chronosphere, an object that powers all time in Underland.\nAfter being told by Time that altering the past is impossible, Alice steals the Chronosphere and travels back in time, shortly after finding the exiled Red Queen, Iracebeth of Crims, is in the care of Time. The Red Queen urges Time to go after Alice. Alice accidentally flies to the day of Iracebeth's coronation, where a younger Tarrant begins a mockery of the Red Queen when the royal crown does not fit her abnormal head. This causes Iracebeth to melt down. Her father deems her inappropriate to rule and passes the title of queen to her younger sister Mirana, the White Queen.\nAlice learns of an event in Iracebeth and Mirana's past that caused friction between the two, and she travels back in time again, hoping it will change Iracebeth's ways and cease the Jabberwocky from killing the Hatter's family. The young Mirana steals a tart from her mother and eats it. When confronted by their mother, Mirana lies about eating the tart, and Iracebeth is accused, causing her to run out of the castle in sadness. Alice sees her about to run into a clock, the event that deforms her head and personality. She is able to get the clock out of the way, but fails to change the past as Iracebeth trips and slams her head anyway.\nAlice is then confronted by a weakened Time, who scolds her for putting all of time in danger. She runs into a nearby mirror back into the real world, where she wakes up in a mental hospital, diagnosed with female hysteria. By the help of her mother, she returns to Underland, where she travels to the Attack of the Jabberwocky and discovers that the Hatter's family never died, but were captured by Iracebeth. Returning to the present, Alice discovers the Hatter at the brink of death.\nAfter Alice tearfully says that she believes him, Tarrant awakens and reforms back to his normal self. The Underlanders go to the Red Queen's castle, where Tarrant finds his family shrunk and trapped in an ant farm. Iracebeth apprehends them and steals the Chronosphere from Alice, taking Mirana back to the day she lied about the tart. By the time Tarrant and Alice get there, Iracebeth and her past self see each other. Time becomes irrelevant, and Underland begins to freeze. Using the Chronosphere, Alice and the Hatter race back to the present, where Alice is able to place the Chronosphere back in its original place.\nWith the Chronosphere stabilized, Underland reverts to normal. The Hatter reunites with his family. Mirana apologizes to Iracebeth for lying, and both of them make amends. Alice bids her friends farewell and returns to the real world where her mother refuses to return Alice's ship over to Hamish, and the two set to travel the world together with their own company.\n"

parameters = {"key":"AIzaSyAiLqwMAwE0sq_-XivG1P6Ll2ptUSN_LSQ"}
#https://cloud.google.com/natural-language/docs/categories

@app.route('/')
def home():
    return str("Home Page")


@app.route('/categories',methods=['GET','POST'])
def get_categories():
    text = request.json.get('article')
    if text is None:
        return bad_request('Input string is empty or null')
    
    doc = {
        "type": "PLAIN_TEXT",
        "language": "en",
        "content": text
        }

    body = {
            "document": doc
            }
    try:
        response = requests.post("https://language.googleapis.com/v1/documents:classifyText",json=body,params = parameters)
        categories = response.json()
        return jsonify({"categories":[i['name'].replace('/','') for i in categories['categories']],"status":"OK","gcp_res_code":response.status_code})
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        return jsonify({"error":"OOps: Something Else"+err,"gcp_res_code":response.status_code})
    except requests.exceptions.HTTPError as errh:
        return jsonify({"error":"Http Error: "+err,"gcp_res_code":response.status_code})
    except requests.exceptions.ConnectionError as errc:
        return jsonify({"error":"Error Connecting: "+errc,"gcp_res_code":response.status_code})
    except requests.exceptions.Timeout as errt:
        return jsonify({"error":"Timeout Error: "+errc,"gcp_res_code":response.status_code})
    

if __name__ =="__main__":
    app.run(debug=True)