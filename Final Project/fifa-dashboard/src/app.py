# from itertools import count
# from urllib import response
# from flask import Flask, render_template, jsonify, request, send_from_directory
# import numpy as np
# import pandas as pd
# import math #what is this
# import json

# # import r
# from flask_cors import CORS


# app = Flask(__name__)
# app.config["JSON_SORT_KEYS"] = False

# CORS(app)

# class Type:
#     def __init__(self, name, children):
#         self.name = name
#         self.children = children


# class Count:
#     def __init__(self, name, count):
#         self.name = name
#         self.count = count

# class WordFreq:
#     def __init__(self, name, count, pos):
#         self.name = name
#         self.count = count
#         self.pos = pos


# Defense = {"CB", "LB", "LWB", "RB", "RWB"}
# Mid_Fielder = {"CAM", "CDM", "CM", "LM", "RM"}
# Attacker = {"CF", "LW", "RW", "ST"}
# GoalKeeper = {"GK"}
# Others = {"SUB", "nan"}

# dicti = {'2015': 'fifa15.csv', '2016': 'fifa16.csv','2017': 'fifa17.csv','2018': 'fifa18.csv', '2019': 'fifa19.csv', '2020': 'fifa20.csv','2021': 'fifa21.csv','2022': 'fifa22.csv'}

# @app.route("/")
# def hello():
#     return render_template("index.html")

# @app.route('/geo.json')
# def send_geo_json():
#     return send_from_directory('./static/data', 'geo.json')

# @app.route("/fetchdata", methods=["POST"])
# def alldata():
#     val = request.get_json()
#     main_df = pd.read_csv("static/data/" + dicti[str(val['year'])])
#     df = main_df
#     # print(val)

#     if 'value' in val:
#         y = json.loads(val['value'])
#         df = df[df['final_league'].isin(y)]

#     if 'nationality' in val:
#         y = json.loads(val['nationality'])
#         df = df[df['nationality_name'].isin(y)]

#     if 'pos' in val:
#         if (val['pos'] == "Defence"):
#             df = df[df['player_position'].isin(list(Defense))]
#         elif (val['pos'] == "Mid Fielder"):
#             df = df[df['player_position'].isin(list(Mid_Fielder))]
#         elif (val['pos'] == "Attacker"):
#             df = df[df['player_position'].isin(list(Attacker))]
#         elif (val['pos'] == "Goal Keeper"):
#             df = df[df['player_position'].isin(["GK"])]
#         elif (val['pos'] in Defense or val['pos'] in Mid_Fielder or val['pos'] in Attacker):
#             df = df[df['player_position'].isin([val['pos']])]
#         else:
#             print("Invalid input passed")

#     if 'pcpval' in val:
#         y = json.loads(val['pcpval'])
#         df = df[df['sofifa_id'].isin(y)]

#     if 'wfilter' in val:
#         y = json.loads(val['wfilter'])
#         df = df[df["short_name"].isin(y)]

  
#     subdf = df[["nationality_name", "sofifa_id"]]
#     geodata = subdf.groupby("nationality_name").count().to_dict()["sofifa_id"]
    
    
#     pos = dict()
#     for st in df["player_position"]:
#         if st is None or type(st) is not str:
#             continue
#         if st in pos:
#             pos[st] += 1
#         else:
#             pos.update({st: 1})

#     DefList = list()
#     for d in Defense:
#         if d in pos:
#             DefList.append(Count(d, int(pos[d])))

#     MidList = list()
#     for m in Mid_Fielder:
#         if m in pos:
#             MidList.append(Count(m, int(pos[m])))

#     AttList = list()
#     for a in Attacker:
#         if a in pos:
#             AttList.append(Count(a, int(pos[a])))

#     Others = list()
#     for a in Others:
#         if a in pos:
#             Others.append(Count(a, int(pos[a])))

#     # GKList = Count("GK", int(pos["GK"]))

#     PlayerList = list()
#     PlayerList.append(Type("Defence", DefList))
#     PlayerList.append(Type("Mid Fielder", MidList))
#     PlayerList.append(Type("Attacker", AttList))
#     if ("GK" in pos):
#         PlayerList.append(Count("Goal Keeper", pos["GK"]))
#     PlayerList.append(Count("Others", Others))
#     data = Type("Players", PlayerList)


#     WordList = list()
#     wordsdf = df[["short_name", "overall", "pos_type"]]

#     for index, row in wordsdf.iterrows():
#         WordList.append(WordFreq(row["short_name"], row["overall"], row["pos_type"]))

#     wordcloud = json.loads(json.dumps(WordList, default=vars))
#     data = json.loads(json.dumps(data, default=vars))

#     sdf = df[["sofifa_id","age_cluster", "rating_cluster", "wage_cluster", "continent", 'pos_type','pace_cluster','dribbling_cluster']]
#     sdf = sdf.dropna()

#     return jsonify({
#         "sunburst": data,
#         "geoData": geodata,
#         "data": df.to_json(orient='records'),
#         "mainData": main_df.to_json(orient='records'),
#         "wordcloud": wordcloud,
#         "pcpdata": sdf.to_dict("records"),
#     })



# if __name__ == "__main__":
#     app.run(host="localhost", port=5005, debug=True)



from flask import Flask, render_template, jsonify, request, send_from_directory
import pandas as pd
import json
from flask_cors import CORS

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
CORS(app)

class Type:
    def __init__(self, name, children):
        self.name = name
        self.children = children

class Count:
    def __init__(self, name, count):
        self.name = name
        self.count = count

class WordFreq:
    def __init__(self, name, count, pos):
        self.name = name
        self.count = count
        self.pos = pos

Defense = {"CB", "LB", "LWB", "RB", "RWB"}
Mid_Fielder = {"CAM", "CDM", "CM", "LM", "RM"}
Attacker = {"CF", "LW", "RW", "ST"}
GoalKeeper = {"GK"}
Other_Positions = {"SUB", "nan"}

dicti = {
    '2015': 'fifa15.csv', '2016': 'fifa16.csv', '2017': 'fifa17.csv',
    '2018': 'fifa18.csv', '2019': 'fifa19.csv', '2020': 'fifa20.csv',
    '2021': 'fifa21.csv', '2022': 'fifa22.csv'
}

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/geo.json')
def send_geo_json():
    return send_from_directory('static/data', 'geo.json')

@app.route("/fetchdata", methods=["POST"])
def alldata():
    val = request.get_json()
    year = str(val.get('year'))
    if year not in dicti:
        return jsonify({"error": "Invalid year selected"}), 400
    
    file_path = "C:/Users/Mritunjay Maddhesiya/Downloads/Final Project/Final Project/fifa-dashboard/src/static/data/fifa18.csv"
    df = pd.read_csv(file_path)
    
    if 'value' in val:
        df = df[df['final_league'].isin(json.loads(val['value']))]
    
    if 'nationality' in val:
        df = df[df['nationality_name'].isin(json.loads(val['nationality']))]
    
    if 'pos' in val:
        pos_val = val['pos']
        if pos_val == "Defence":
            df = df[df['player_position'].isin(Defense)]
        elif pos_val == "Mid Fielder":
            df = df[df['player_position'].isin(Mid_Fielder)]
        elif pos_val == "Attacker":
            df = df[df['player_position'].isin(Attacker)]
        elif pos_val == "Goal Keeper":
            df = df[df['player_position'] == "GK"]
        elif pos_val in Defense or pos_val in Mid_Fielder or pos_val in Attacker:
            df = df[df['player_position'] == pos_val]
    
    if 'pcpval' in val:
        df = df[df['sofifa_id'].isin(json.loads(val['pcpval']))]
    
    if 'wfilter' in val:
        df = df[df["short_name"].isin(json.loads(val['wfilter']))]
    
    geodata = df.groupby("nationality_name")["sofifa_id"].count().to_dict()
    
    pos_counts = df["player_position"].value_counts().to_dict()
    
    DefList = [Count(d, pos_counts.get(d, 0)) for d in Defense if d in pos_counts]
    MidList = [Count(m, pos_counts.get(m, 0)) for m in Mid_Fielder if m in pos_counts]
    AttList = [Count(a, pos_counts.get(a, 0)) for a in Attacker if a in pos_counts]
    OthersList = [Count(o, pos_counts.get(o, 0)) for o in Other_Positions if o in pos_counts]
    
    PlayerList = [
        Type("Defence", DefList),
        Type("Mid Fielder", MidList),
        Type("Attacker", AttList)
    ]
    
    if "GK" in pos_counts:
        PlayerList.append(Count("Goal Keeper", pos_counts["GK"]))
    
    PlayerList.append(Count("Others", OthersList))
    data = Type("Players", PlayerList)
    
    word_columns = ["short_name", "overall"]
    if "pos_type" in df.columns:
        word_columns.append("pos_type")
    wordsdf = df[word_columns].dropna()
    
    WordList = [WordFreq(row["short_name"], row["overall"], row.get("pos_type", "Unknown")) for _, row in wordsdf.iterrows()]
    
    sdf = df[["sofifa_id", "age_cluster", "rating_cluster", "wage_cluster", "continent", 'pos_type', 'pace_cluster', 'dribbling_cluster']].dropna()
    
    return jsonify({
        "sunburst": json.loads(json.dumps(data, default=vars)),
        "geoData": geodata,
        "data": df.to_json(orient='records'),
        "wordcloud": json.loads(json.dumps(WordList, default=vars)),
        "pcpdata": sdf.to_dict("records"),
    })

if __name__ == "__main__":
    app.run(host="localhost", port=5005, debug=True)