from flask import Flask, render_template, request
from flask_restful import Api
import gymnasium as gym
import requests
import json
# from flask_cors import CORS
import warnings

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

LOCAL = False
if LOCAL:
    prefix = "http://localhost:5222"
else:
    prefix = "https://bvme.azurewebsites.net"

def fromReset(seed):
    sendit = {"seed": str(seed)}
    warnings.warn('in reset1 ' + str(sendit))
    try:
        response = None
        response = requests.request("POST",prefix + "/api/reset", 
                                    json = json.dumps(sendit),
                                    headers={"content-type": "application/json"})
        warnings.warn("post call in reset")
        warnings.warn("response status code: ", response.status_code)
        if response.status_code == 200:
            return response.json()
    except:
        warnings.warn("in except for reset")
        return  {"player_sum": "1", 
                "dealer_sum": "1", 
                "usable_ace": str(False),
                "history": "not right reset",
                "terminated": str(False),
                "reward": "0.0",
                "seed": str(seed)}

def fromStep(action, seed):
    sendit = {"action": str(action),
              "seed": str(seed)}
    print("sendit", sendit)
    response = requests.request("POST",prefix + "/api/step", 
                                json = sendit,
                                headers={"content-type": "application/json"})
    print("response", response.json())
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        return response.json()
    return  {"player_sum": "1", 
                "dealer_sum": "1", 
                "usable_ace": str(False),
                "history": "not right step", #+ str(response.status_code),
                "terminated": str(False),
                "reward": "0.0",
                "seed": str(seed)}

def fromBonsai(seed):
    pass

@app.route('/')
def index():
    return render_template("index.html", content="Welcome to the Blackjack Game2!")

@app.route("/play", methods=["POST", "GET"])
def play():
    data1 = {}
    warnings.warn('Warning Message: in play')
    print("in play")
    if request.method == "POST":
        if request.form["HitStick"] == "Hit":
            warnings.warn('Warning Message: Hit')
            data1 = fromStep(1,request.form["seed"])
            return render_template("play.html",last_action="Hit", dealer_card=data1["dealer_sum"], player_card=data1["player_sum"], usable_ace=data1["usable_ace"], terminated=data1["terminated"], reward=data1["reward"], history=data1["history"], seed=data1["seed"])
        elif request.form["HitStick"] == "Stick":
            data1 = fromStep(0,request.form["seed"])
            return render_template("play.html",last_action="Stick", dealer_card=data1["dealer_sum"], player_card=data1["player_sum"], usable_ace=data1["usable_ace"], terminated=data1["terminated"], reward=data1["reward"], history=data1["history"], seed=data1["seed"])
        elif request.form["HitStick"] == "Reset":
            data1 = fromReset(request.form["seed"])
            return render_template("play.html",last_action="Reset", dealer_card=data1["dealer_sum"], player_card=data1["player_sum"], usable_ace=data1["usable_ace"], terminated=data1["terminated"], reward=data1["reward"], history=data1["history"],seed=data1["seed"])
        elif request.form["HitStick"] == "Bonsai":
            data1 = fromBonsai(request.form["seed"])
            return render_template("play.html",last_action="Bonsai", dealer_card=data1["dealer_sum"], player_card=data1["player_sum"], usable_ace=data1["usable_ace"], terminated=data1["terminated"], reward=data1["reward"], history=data1["history"],seed=data1["seed"])
    else:
        print("in main page reset")
        data1 = fromReset(seed=42)
        return render_template("play.html",last_action="Reset Start", dealer_card=data1["dealer_sum"], player_card=data1["player_sum"], usable_ace=data1["usable_ace"], terminated=data1["terminated"], reward=data1["reward"], history=data1["history"], seed=data1["seed"])

