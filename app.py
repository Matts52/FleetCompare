from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

from FlightRadar24.api import FlightRadar24API


app = Flask(__name__)

#callback function for when a new ICAO code is enterred in the text box
@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))



#set up default airlines for when the user opens the page
@app.route('/')
def index():
    return render_template('index.html',  
                           graphJSON1=gm(airline='ACA'),
                           graphJSON2=gm(airline='WJA'))



def gm(airline='UAL'):
    #load instance of the API and get flights
    fr_api = FlightRadar24API()
    flights = fr_api.get_flights(airline=airline)

    #get counts of each of the models in the airline
    model_counts = {}
    for flight in flights:
        try:
            if str(flight)[2:6] in model_counts.keys():
                model_counts[str(flight)[2:6]] += 1
            else:
                model_counts[str(flight)[2:6]] = 1
        except:
            pass

    #load flights into a dataframe for plotly
    lines_df = pd.DataFrame(model_counts.items(), columns=['ICAO', 'Count']).sort_values("ICAO")

    #get the corresponging airline
    airline_info = pd.DataFrame(fr_api.get_airlines())
    try:
        airline_name = airline_info[airline_info["ICAO"] == airline]["Name"].item()
    except:
        airline_name = "Airline Not Found"

    #produce the figure
    fig = px.bar(lines_df, x="ICAO", y="Count", title=airline + " - " + airline_name, 
                 color="Count", color_continuous_scale=['#0d6298', '#abdbe3'],
                                  labels={
                     "ICAO": "Aircraft Model ICAO Code",
                     "Count": "Count in Flight"
                 })

    #create a JSON image for output
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON