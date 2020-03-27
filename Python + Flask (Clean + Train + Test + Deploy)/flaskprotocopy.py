# -*- coding: utf-8 -*-
import os
import flask
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
import json
from flask import request
from pymongo import MongoClient

app = flask.Flask(__name__)
conn = MongoClient()
#conn = MongoClient('localhost',27017)

db = conn.showmedawae  # db name
collection = db.realtime  # collection name
#rec = {"0":{"0":0.33184814},"1":{"0":0.006240845},"2":{"0":0.034973145},"3":{"0":0.025390625},"4":{"0":0.054122925},"5":{"0":0.20735168},"6":{"0":0.20256042},"7":{"0":-0.003341675},"8":{"0":-0.079956055},"9":{"0":0.011016846},"10":{"0":0.1307373},"11":{"0":0.17382812},"12":{"0":0.14988708},"13":{"0":0.073272705},"14":{"0":0.030181885},"15":{"0":0.030181885},"16":{"0":0.078063965},"17":{"0":0.106796265},"18":{"0":0.116363525},"19":{"0":0.068481445},"20":{"0":0.001449585},"21":{"0":0.039749146},"22":{"0":0.058914185},"23":{"0":0.044540405},"24":{"0":0.13552856},"25":{"0":0.14988708},"26":{"0":0.1594696},"27":{"0":0.20256042},"28":{"0":0.20735168},"29":{"0":0.2504425},"30":{"0":0.2504425},"31":{"0":0.22650146},"32":{"0":0.23129272},"33":{"0":0.23129272},"34":{"0":0.29353333},"35":{"0":0.2504425},"36":{"0":0.1929779},"37":{"0":0.28396606},"38":{"0":0.3653717},"39":{"0":0.81547546},"40":{"0":0.6813965},"41":{"0":0.41325378},"42":{"0":-0.008132935},"43":{"0":-1.5116882},"44":{"0":-2.9721527},"45":{"0":-3.4509888},"46":{"0":-3.7430878},"47":{"0":-3.7143555},"48":{"0":-3.6425323},"49":{"0":-3.091858},"50":{"0":2.194992},"51":{"0":2.4918823},"52":{"0":2.712143},"53":{"0":2.7169342},"54":{"0":2.6594696},"55":{"0":2.62117},"56":{"0":2.6163788},"57":{"0":2.597229},"58":{"0":2.597229},"59":{"0":2.487091},"60":{"0":2.4822998},"61":{"0":2.578064},"62":{"0":2.62117},"63":{"0":2.6929932},"64":{"0":2.6594696},"65":{"0":2.5349731},"66":{"0":2.4679413},"67":{"0":2.4727325},"68":{"0":2.487091},"69":{"0":2.5206146},"70":{"0":2.4775085},"71":{"0":2.4248352},"72":{"0":2.415268},"73":{"0":2.4583588},"74":{"0":2.5253906},"75":{"0":2.4727325},"76":{"0":2.4727325},"77":{"0":2.4679413},"78":{"0":2.4918823},"79":{"0":2.487091},"80":{"0":2.4966736},"81":{"0":2.4918823},"82":{"0":2.530182},"83":{"0":2.5253906},"84":{"0":2.4966736},"85":{"0":2.4727325},"86":{"0":2.5349731},"87":{"0":2.6642609},"88":{"0":2.6499023},"89":{"0":2.5349731},"90":{"0":2.7217255},"91":{"0":2.8558044},"92":{"0":2.846222},"93":{"0":2.190216},"94":{"0":0.5573578},"95":{"0":0.7728424},"96":{"0":1.1463318},"97":{"0":1.4671631},"98":{"0":1.7448883},"99":{"0":1.6874237},"100":{"0":9.872757},"101":{"0":9.709946},"102":{"0":9.705154},"103":{"0":9.939789},"104":{"0":9.78656},"105":{"0":9.686005},"106":{"0":9.671646},"107":{"0":9.738678},"108":{"0":9.676422},"109":{"0":9.21196},"110":{"0":9.034775},"111":{"0":8.828873},"112":{"0":8.89592},"113":{"0":9.264618},"114":{"0":9.326874},"115":{"0":9.398697},"116":{"0":9.499252},"117":{"0":9.504044},"118":{"0":9.547134},"119":{"0":9.671646},"120":{"0":9.724304},"121":{"0":9.690796},"122":{"0":9.690796},"123":{"0":9.566299},"124":{"0":9.532776},"125":{"0":9.551926},"126":{"0":9.566299},"127":{"0":9.633331},"128":{"0":9.623749},"129":{"0":9.60939},"130":{"0":9.599808},"131":{"0":9.527985},"132":{"0":9.532776},"133":{"0":9.633331},"134":{"0":9.724304},"135":{"0":9.7482605},"136":{"0":9.623749},"137":{"0":9.714737},"138":{"0":9.824875},"139":{"0":10.169632},"140":{"0":10.155273},"141":{"0":9.527985},"142":{"0":8.661285},"143":{"0":6.5496063},"144":{"0":5.8983765},"145":{"0":6.252716},"146":{"0":6.6262207},"147":{"0":7.248703},"148":{"0":8.182449},"149":{"0":9.125763},"150":{"0":-0.13169861},"151":{"0":-0.057662964},"152":{"0":-0.064575195},"153":{"0":-0.08694458},"154":{"0":-0.09919739},"155":{"0":-0.094940186},"156":{"0":-0.076828},"157":{"0":0.006790161},"158":{"0":0.06324768},"159":{"0":0.09680176},"160":{"0":0.10159302},"161":{"0":0.06324768},"162":{"0":0.000396729},"163":{"0":-0.059249878},"164":{"0":-0.101867676},"165":{"0":-0.10932922},"166":{"0":-0.10826111},"167":{"0":-0.094940186},"168":{"0":-0.07470703},"169":{"0":-0.060317993},"170":{"0":-0.043273926},"171":{"0":-0.028900146},"172":{"0":-0.017715454},"173":{"0":-0.016647339},"174":{"0":-0.031555176},"175":{"0":-0.04220581},"176":{"0":-0.045944214},"177":{"0":-0.041671753},"178":{"0":-0.029434204},"179":{"0":-0.016113281},"180":{"0":-0.015045166},"181":{"0":-0.003326416},"182":{"0":0.010513306},"183":{"0":0.033950806},"184":{"0":0.08135986},"185":{"0":0.17297363},"186":{"0":0.29600525},"187":{"0":0.4456787},"188":{"0":0.64701843},"189":{"0":0.893631},"190":{"0":1.1237183},"191":{"0":1.2510223},"192":{"0":1.1056061},"193":{"0":0.80999756},"194":{"0":0.32157898},"195":{"0":-0.15086365},"196":{"0":-0.57803345},"197":{"0":-1.1202545},"198":{"0":-1.3668671},"199":{"0":-1.4669952},"200":{"0":-0.22935486},"201":{"0":-0.07914734},"202":{"0":0.093948364},"203":{"0":0.13868713},"204":{"0":0.10194397},"205":{"0":0.09182739},"206":{"0":0.08862305},"207":{"0":0.019378662},"208":{"0":-0.038146973},"209":{"0":-0.047195435},"210":{"0":-0.026428223},"211":{"0":-0.012039185},"212":{"0":-0.002990723},"213":{"0":-0.025360107},"214":{"0":-0.044006348},"215":{"0":-0.03919983},"216":{"0":-0.022155762},"217":{"0":-0.0131073},"218":{"0":-0.012573242},"219":{"0":-0.019500732},"220":{"0":-0.02482605},"221":{"0":-0.015777588},"222":{"0":-0.018966675},"223":{"0":-0.028015137},"224":{"0":-0.039733887},"225":{"0":-0.05731201},"226":{"0":-0.07170105},"227":{"0":-0.073287964},"228":{"0":-0.05784607},"229":{"0":-0.04347229},"230":{"0":-0.036010742},"231":{"0":-0.004058838},"232":{"0":0.032699585},"233":{"0":0.05293274},"234":{"0":0.058258057},"235":{"0":0.060394287},"236":{"0":0.051345825},"237":{"0":0.025772095},"238":{"0":-0.002990723},"239":{"0":0.006607056},"240":{"0":0.08755493},"241":{"0":0.10620117},"242":{"0":0.24043274},"243":{"0":0.58343506},"244":{"0":1.1379089},"245":{"0":1.5927734},"246":{"0":1.951767},"247":{"0":2.2100983},"248":{"0":2.220749},"249":{"0":2.1605682},"250":{"0":-0.15611267},"251":{"0":-0.24719238},"252":{"0":-0.24293518},"253":{"0":-0.1502533},"254":{"0":-0.07247925},"255":{"0":-0.02720642},"256":{"0":-0.015487671},"257":{"0":0.018600464},"258":{"0":0.043624878},"259":{"0":0.06387329},"260":{"0":0.06492615},"261":{"0":0.058013916},"262":{"0":0.044692993},"263":{"0":0.03829956},"264":{"0":0.027114868},"265":{"0":0.021255493},"266":{"0":0.023925781},"267":{"0":0.030319214},"268":{"0":0.03617859},"269":{"0":0.04043579},"270":{"0":0.044158936},"271":{"0":0.053222656},"272":{"0":0.0526886},"273":{"0":0.056411743},"274":{"0":0.0569458},"275":{"0":0.05747986},"276":{"0":0.0526886},"277":{"0":0.049484253},"278":{"0":0.039901733},"279":{"0":0.02658081},"280":{"0":0.02178955},"281":{"0":0.010070801},"282":{"0":0.011138916},"283":{"0":0.010604858},"284":{"0":0.004211426},"285":{"0":-0.012832642},"286":{"0":-0.027740479},"287":{"0":-0.033065796},"288":{"0":-0.051712036},"289":{"0":-0.09484863},"290":{"0":-0.14118958},"291":{"0":-0.10391235},"292":{"0":0.1000824},"293":{"0":0.3861084},"294":{"0":0.7685394},"295":{"0":1.1664124},"296":{"0":1.5158234},"297":{"0":1.93927},"298":{"0":2.14859},"299":{"0":2.3142395}}
#collection.insert_one(rec)
@app.route("/", methods=["GET","POST"])
def homepage():
    #with open('inputs.json') as f:
    #    data = json.load(f)
    #df = pd.DataFrame.from_dict(data)
    model = load_model("final-model-hopefully.h5")
    if request.is_json:
        req = flask.request.get_json()
        #print(req)
        cursor = collection.find() 
        x = list(cursor)
        #rec = {"0":{"0":0.33184814},"1":{"0":0.006240845},"2":{"0":0.034973145},"3":{"0":0.025390625},"4":{"0":0.054122925},"5":{"0":0.20735168},"6":{"0":0.20256042},"7":{"0":-0.003341675},"8":{"0":-0.079956055},"9":{"0":0.011016846},"10":{"0":0.1307373},"11":{"0":0.17382812},"12":{"0":0.14988708},"13":{"0":0.073272705},"14":{"0":0.030181885},"15":{"0":0.030181885},"16":{"0":0.078063965},"17":{"0":0.106796265},"18":{"0":0.116363525},"19":{"0":0.068481445},"20":{"0":0.001449585},"21":{"0":0.039749146},"22":{"0":0.058914185},"23":{"0":0.044540405},"24":{"0":0.13552856},"25":{"0":0.14988708},"26":{"0":0.1594696},"27":{"0":0.20256042},"28":{"0":0.20735168},"29":{"0":0.2504425},"30":{"0":0.2504425},"31":{"0":0.22650146},"32":{"0":0.23129272},"33":{"0":0.23129272},"34":{"0":0.29353333},"35":{"0":0.2504425},"36":{"0":0.1929779},"37":{"0":0.28396606},"38":{"0":0.3653717},"39":{"0":0.81547546},"40":{"0":0.6813965},"41":{"0":0.41325378},"42":{"0":-0.008132935},"43":{"0":-1.5116882},"44":{"0":-2.9721527},"45":{"0":-3.4509888},"46":{"0":-3.7430878},"47":{"0":-3.7143555},"48":{"0":-3.6425323},"49":{"0":-3.091858},"50":{"0":2.194992},"51":{"0":2.4918823},"52":{"0":2.712143},"53":{"0":2.7169342},"54":{"0":2.6594696},"55":{"0":2.62117},"56":{"0":2.6163788},"57":{"0":2.597229},"58":{"0":2.597229},"59":{"0":2.487091},"60":{"0":2.4822998},"61":{"0":2.578064},"62":{"0":2.62117},"63":{"0":2.6929932},"64":{"0":2.6594696},"65":{"0":2.5349731},"66":{"0":2.4679413},"67":{"0":2.4727325},"68":{"0":2.487091},"69":{"0":2.5206146},"70":{"0":2.4775085},"71":{"0":2.4248352},"72":{"0":2.415268},"73":{"0":2.4583588},"74":{"0":2.5253906},"75":{"0":2.4727325},"76":{"0":2.4727325},"77":{"0":2.4679413},"78":{"0":2.4918823},"79":{"0":2.487091},"80":{"0":2.4966736},"81":{"0":2.4918823},"82":{"0":2.530182},"83":{"0":2.5253906},"84":{"0":2.4966736},"85":{"0":2.4727325},"86":{"0":2.5349731},"87":{"0":2.6642609},"88":{"0":2.6499023},"89":{"0":2.5349731},"90":{"0":2.7217255},"91":{"0":2.8558044},"92":{"0":2.846222},"93":{"0":2.190216},"94":{"0":0.5573578},"95":{"0":0.7728424},"96":{"0":1.1463318},"97":{"0":1.4671631},"98":{"0":1.7448883},"99":{"0":1.6874237},"100":{"0":9.872757},"101":{"0":9.709946},"102":{"0":9.705154},"103":{"0":9.939789},"104":{"0":9.78656},"105":{"0":9.686005},"106":{"0":9.671646},"107":{"0":9.738678},"108":{"0":9.676422},"109":{"0":9.21196},"110":{"0":9.034775},"111":{"0":8.828873},"112":{"0":8.89592},"113":{"0":9.264618},"114":{"0":9.326874},"115":{"0":9.398697},"116":{"0":9.499252},"117":{"0":9.504044},"118":{"0":9.547134},"119":{"0":9.671646},"120":{"0":9.724304},"121":{"0":9.690796},"122":{"0":9.690796},"123":{"0":9.566299},"124":{"0":9.532776},"125":{"0":9.551926},"126":{"0":9.566299},"127":{"0":9.633331},"128":{"0":9.623749},"129":{"0":9.60939},"130":{"0":9.599808},"131":{"0":9.527985},"132":{"0":9.532776},"133":{"0":9.633331},"134":{"0":9.724304},"135":{"0":9.7482605},"136":{"0":9.623749},"137":{"0":9.714737},"138":{"0":9.824875},"139":{"0":10.169632},"140":{"0":10.155273},"141":{"0":9.527985},"142":{"0":8.661285},"143":{"0":6.5496063},"144":{"0":5.8983765},"145":{"0":6.252716},"146":{"0":6.6262207},"147":{"0":7.248703},"148":{"0":8.182449},"149":{"0":9.125763},"150":{"0":-0.13169861},"151":{"0":-0.057662964},"152":{"0":-0.064575195},"153":{"0":-0.08694458},"154":{"0":-0.09919739},"155":{"0":-0.094940186},"156":{"0":-0.076828},"157":{"0":0.006790161},"158":{"0":0.06324768},"159":{"0":0.09680176},"160":{"0":0.10159302},"161":{"0":0.06324768},"162":{"0":0.000396729},"163":{"0":-0.059249878},"164":{"0":-0.101867676},"165":{"0":-0.10932922},"166":{"0":-0.10826111},"167":{"0":-0.094940186},"168":{"0":-0.07470703},"169":{"0":-0.060317993},"170":{"0":-0.043273926},"171":{"0":-0.028900146},"172":{"0":-0.017715454},"173":{"0":-0.016647339},"174":{"0":-0.031555176},"175":{"0":-0.04220581},"176":{"0":-0.045944214},"177":{"0":-0.041671753},"178":{"0":-0.029434204},"179":{"0":-0.016113281},"180":{"0":-0.015045166},"181":{"0":-0.003326416},"182":{"0":0.010513306},"183":{"0":0.033950806},"184":{"0":0.08135986},"185":{"0":0.17297363},"186":{"0":0.29600525},"187":{"0":0.4456787},"188":{"0":0.64701843},"189":{"0":0.893631},"190":{"0":1.1237183},"191":{"0":1.2510223},"192":{"0":1.1056061},"193":{"0":0.80999756},"194":{"0":0.32157898},"195":{"0":-0.15086365},"196":{"0":-0.57803345},"197":{"0":-1.1202545},"198":{"0":-1.3668671},"199":{"0":-1.4669952},"200":{"0":-0.22935486},"201":{"0":-0.07914734},"202":{"0":0.093948364},"203":{"0":0.13868713},"204":{"0":0.10194397},"205":{"0":0.09182739},"206":{"0":0.08862305},"207":{"0":0.019378662},"208":{"0":-0.038146973},"209":{"0":-0.047195435},"210":{"0":-0.026428223},"211":{"0":-0.012039185},"212":{"0":-0.002990723},"213":{"0":-0.025360107},"214":{"0":-0.044006348},"215":{"0":-0.03919983},"216":{"0":-0.022155762},"217":{"0":-0.0131073},"218":{"0":-0.012573242},"219":{"0":-0.019500732},"220":{"0":-0.02482605},"221":{"0":-0.015777588},"222":{"0":-0.018966675},"223":{"0":-0.028015137},"224":{"0":-0.039733887},"225":{"0":-0.05731201},"226":{"0":-0.07170105},"227":{"0":-0.073287964},"228":{"0":-0.05784607},"229":{"0":-0.04347229},"230":{"0":-0.036010742},"231":{"0":-0.004058838},"232":{"0":0.032699585},"233":{"0":0.05293274},"234":{"0":0.058258057},"235":{"0":0.060394287},"236":{"0":0.051345825},"237":{"0":0.025772095},"238":{"0":-0.002990723},"239":{"0":0.006607056},"240":{"0":0.08755493},"241":{"0":0.10620117},"242":{"0":0.24043274},"243":{"0":0.58343506},"244":{"0":1.1379089},"245":{"0":1.5927734},"246":{"0":1.951767},"247":{"0":2.2100983},"248":{"0":2.220749},"249":{"0":2.1605682},"250":{"0":-0.15611267},"251":{"0":-0.24719238},"252":{"0":-0.24293518},"253":{"0":-0.1502533},"254":{"0":-0.07247925},"255":{"0":-0.02720642},"256":{"0":-0.015487671},"257":{"0":0.018600464},"258":{"0":0.043624878},"259":{"0":0.06387329},"260":{"0":0.06492615},"261":{"0":0.058013916},"262":{"0":0.044692993},"263":{"0":0.03829956},"264":{"0":0.027114868},"265":{"0":0.021255493},"266":{"0":0.023925781},"267":{"0":0.030319214},"268":{"0":0.03617859},"269":{"0":0.04043579},"270":{"0":0.044158936},"271":{"0":0.053222656},"272":{"0":0.0526886},"273":{"0":0.056411743},"274":{"0":0.0569458},"275":{"0":0.05747986},"276":{"0":0.0526886},"277":{"0":0.049484253},"278":{"0":0.039901733},"279":{"0":0.02658081},"280":{"0":0.02178955},"281":{"0":0.010070801},"282":{"0":0.011138916},"283":{"0":0.010604858},"284":{"0":0.004211426},"285":{"0":-0.012832642},"286":{"0":-0.027740479},"287":{"0":-0.033065796},"288":{"0":-0.051712036},"289":{"0":-0.09484863},"290":{"0":-0.14118958},"291":{"0":-0.10391235},"292":{"0":0.1000824},"293":{"0":0.3861084},"294":{"0":0.7685394},"295":{"0":1.1664124},"296":{"0":1.5158234},"297":{"0":1.93927},"298":{"0":2.14859},"299":{"0":2.3142395}}
        #z = pd.DataFrame.from_dict(req)
        #print()
        df = pd.DataFrame.from_dict(x[-1])
        print('\n\n\n\n\n\n\n\n\n\n\n')
        print(df)
        print('\n\n\n\n\n\n\n\n')
        #raw_prediction = model.predict(z)
        raw_prediction = model.predict(df.iloc[:,1:])
        p = pd.DataFrame(raw_prediction)
        pred = p.to_json()
        print(pred)
        return pred
    else:
        return "Request was not JSON", 400  


@app.route("/predict", methods=["GET","POST"])
def predict():
    
    if request.is_json:
        req = flask.request.get_json()
        #print(req)
        df = pd.DataFrame.from_dict(req)
        model = load_model("final-model-hopefully.h5")
        raw_prediction = model.predict(df)
        p = pd.DataFrame(raw_prediction)
        pred = p.to_json()
        print(pred)
        return pred
    else:
        return "Request was not JSON", 400

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    #app.debug=True
    app.run(host='192.168.43.206',port=8080)
    
#m = pd.read_csv('combined.csv')
#m = m.iloc[:1,:-1]
#m.to_json('input1.json')
'''
import os
import json
import pymongo
from flask import Flask
from flask import request
app = Flask(__name__)
usr = os.environ['58ddb111-8b75-487d-b4b4-a684338d2f96']
pwd = os.environ['jogodisk']
client = pymongo.MongoClient("mongodb+srv://" + usr + ":" + pwd + "@firstcluster-obuqd.mongodb.net/test?retryWrites=true&w=majority")
db = client['SampleDatabase']
collection = db['SampleCollection']
@app.route("/", methods=['POST'])
def insert_document():
    req_data = request.get_json()
    collection.insert_one(req_data).inserted_id
    return ('', 204)
@app.route('/')
def get():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
if __name__ == '__main__':
    app.run()
    
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://127.0.0.1:27017/start?compressors=disabled&gssapiServiceName=mongodb')
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)'''