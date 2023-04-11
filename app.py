from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

from FlightRadar24.api import FlightRadar24API


app = Flask(__name__)

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
    
    fr_api = FlightRadar24API()
    #flights = fr_api.get_flights(aircraft_type=ICAO_Code, airline="UAL")

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


    lines_df = pd.DataFrame(model_counts.items(), columns=['ICAO', 'Count'])


    fig = px.bar(lines_df, x="ICAO", y="Count", title=airline, color="Count", color_continuous_scale=['#0d6298', '#abdbe3'])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(fig.data[0])
    
    return graphJSON