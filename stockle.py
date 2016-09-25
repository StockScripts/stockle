from stockleapi import finance, reddit, twitter, news
import numpy as np
import random

import json
import plotly

from flask import Flask,render_template
app = Flask(__name__)



def get_graph_data(values):

    avg = np.mean(values)

    f = float(avg+1) / (2.0)
    # linearly interpolate that value between the colors red and green
    r, g, b = 1-f, f, 0.
    color = '#%02x%02x%02x' % (int(r*255), int(g*255), b)


    return dict(
            data=[
                {
                    'x': values,
                    #~ 'x': [0.2],
                    'marker': {
                                'color': color,
                                },
                    'boxmean': False,
                    'orientation': 'h',
                    "type": "box",

                },
            ],

            layout={
                    'autosize': False,
                      #~ 'width': 140,
                      'height': 50,
                      'margin': {
                        'l': 0,
                        'r': 0,
                        'b': 0,
                        't': 0,
                        'pad': 1
                      },
                      'paper_bgcolor': 'rgba(0,0,0,0)',
                      'plot_bgcolor': 'rgba(0,0,0,0)',


                    'xaxis': {
                            'range':[-1,1],
                            'zeroline': False,
                            'showticklabels':False,
                            'ticks':'',
                            'showgrid':False,
                            'showline':False,
                        },
                    'yaxis':{
                        'showticklabels':False,
                    },
                }

        )



@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'



@app.route('/summary')
def view_summary():

    titles = ["AAPL", "ADBE","EBAY","GOOGL", "MSFT", "YHOO"]

    title_list = []
    graph_ids = []
    graph_data = []

    for t in titles:
        #~ dic_finance = finance.get_title(t)
        dic_finance = {"symbol":t,"name":t, "price":random.random()*100,"change" : random.random()*4 - 2}


        # values for graphs
        news_items = news.get_items(t)["items"]
        reddit_items = reddit.get_items(t)["items"]
        twitter_items = twitter.get_items(t)["items"]

        graph_ids += [t+"_graph-summary-reddit"]
        graph_data += [get_graph_data([x["sentiment"] for x in reddit_items])]

        graph_ids += [t+"_graph-summary-twitter"]
        graph_data += [get_graph_data([x["sentiment"] for x in twitter_items])]

        graph_ids += [t+"_graph-summary-news"]
        graph_data += [get_graph_data([x["sentiment"] for x in news_items])]

        title_list += [dic_finance]


    graph_JSON = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('template_summary.html', title_list=title_list,graph_ids=graph_ids,
                           graph_JSON=graph_JSON)




@app.route('/detail/<t>')
def show_title_detail(t):

    t = str(unicode(t))

    # details for a given title
    dic_finance = finance.get_title(t)
    #~ dic_finance = {"symbol":t,"name":t, "price":random.random()*100,"change" : random.random()*4 - 2}


    news_items = news.get_items(dic_finance['name'])["items"]
    dic_finance["news"] = news_items

    reddit_items = reddit.get_items(dic_finance['name'])["items"]
    dic_finance["reddit"] = reddit_items

    twitter_items = twitter.get_items(dic_finance['name'])["items"]
    dic_finance["twitter"] = twitter_items


    graph_ids = []
    graph_data = []

    # create and add summary graphs
    graph_ids += [t+"_graph-summary-reddit"]
    graph_data += [get_graph_data([x["sentiment"] for x in reddit_items])]
    graph_ids += [t+"_graph-summary-twitter"]
    graph_data += [get_graph_data([x["sentiment"] for x in twitter_items])]
    graph_ids += [t+"_graph-summary-news"]
    graph_data += [get_graph_data([x["sentiment"] for x in news_items])]


    # create and add individual graphs
    for i,x in enumerate(reddit_items):
        graph_ids += [t+"_reddit_"+str(i+1)]
        graph_data += [get_graph_data([x["sentiment"]])]

    for i,x in enumerate(twitter_items):
        graph_ids += [t+"_twitter_"+str(i+1)]
        graph_data += [get_graph_data([x["sentiment"]])]

    for i,x in enumerate(news_items):
        graph_ids += [t+"_news_"+str(i+1)]
        graph_data += [get_graph_data([x["sentiment"]])]


    graph_JSON = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('template_detail.html', title = dic_finance,graph_ids=graph_ids,
                           graph_JSON=graph_JSON)



#~ @app.route('/post/<int:post_id>')
#~ def show_post(post_id):
    #~ # show the post with the given id, the id is an integer
    #~ return 'Post %d' % post_id


if __name__ == "__main__":
    app.run()
