from flask import Flask, g, request, jsonify
import pandas as pd
from xml_parser import XML2DataFrame
import os
import random


# Elastic Beanstalk looks for a flask app named 'application'
application = Flask(__name__)

application.config.update(dict(
    XML_PATH='poems/', # the directory containing the XML files
    XML_NAMESPACE='http://www.tei-c.org/ns/1.0', # the namespace used in the XML files
    csv='poems.csv',
    ERROR='errors.txt',
    # analysis tags are used to set bounds on the types of analysis that can be picked from and the
    # range of values for each tag that can be added
    analysis_tags={'form': ['sonnet', 'free','haiku'], 'tone': ['happy', 'sad','indifferent'], \
                   'topic': ['love', 'war','environment','education','history'],\
                   }
))


@application.before_first_request
def create_csv():
    '''
    Create a pandas dataframe from  a bunch of XML files and store it as a CSV
    :return: None
    '''
    parser = XML2DataFrame(application.config['analysis_tags'], namespace=application.config['XML_NAMESPACE'], \
                           error_file=application.config['ERROR'])
    data = parser.xmls_to_dataframe(application.config['XML_PATH'])
    data.to_csv(application.config['csv'], index=False)


@application.route('/')
def base():
    '''
    Provides information regarding what tags can be picked
    :return: all the tags and tag values that can be requestd
    '''
    # Craft an HTML table
    info = '<h1>Poem Box API<h2> <br> <table><tr><td>Parameter</td></tr>'
    for tag in application.config['analysis_tags'].keys():
        info = info + '<tr>'
        for value in application.config['analysis_tags'][tag]:
            info = info + '<td>' + str(value) + '</td>'
        info = info + '</tr>'
    info = info + '</table>'
    return info


@application.route('/poem', methods=['GET'])
def get_poem():
    '''
    Gets a random poem matching as many of the request args as possible
    :return: A poem in JSON form
    '''
    # Check to see if the request matches supported tags and values
    for key in request.args:
        if key not in application.config['analysis_tags'].keys():
            return "the key {} does not exist".format(key)
        if request.args[key] not in application.config['analysis_tags'][key]:
            return "That value {} does not exist for the key {}".format(request.args[key], key)
    df = get_dataframe()
    poem_matches = {} # This will store all the matching poems
    # For each poem, find how many tags match those requested
    for index, row in df.iterrows():
        matches = set(request.args.items()) & set(row.items())
        poem_matches[index] = len(matches)
    # Store all the poems with the maximum matches
    poems = [k for k, v in poem_matches.items() if v == max(poem_matches.values())]
    chosen_poem = random.choice(poems)
    poem_dict = df.iloc[chosen_poem].to_dict()
    poem_dict['matching_attributes'] = poem_matches[chosen_poem]
    return jsonify(poem_dict)

@application.route('/issues', methods=['GET'])
def find_issues():
    '''
    Returns the contents of an error file
    :return: string representation of contents of file
    '''
    error_file = open(application.config['ERROR'])
    # Replace new lines with HTML friendly newlines
    errors = error_file.read().replace('\n', '<br>')
    error_file.close()
    return errors


def get_dataframe():
    '''
    Returns a pandas dataframe or creates a new one if it doesn't yet exist
    :return: pandas dataframe
    '''
    df = getattr(g, '_dataframe', None)
    if df is None:
        df = g._dataframe = pd.read_csv(application.config['csv'])
    return df


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run()
