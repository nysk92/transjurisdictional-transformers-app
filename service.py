from flask import Flask, jsonify, request, render_template
import numpy as np
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
DEFAULT_CONFIG = 'config.json'

def load_config(filename=None):
	if not filename:
		filename=DEFAULT_CONFIG
	with open(filename) as f:
		config = json.load(f)
	return config

config = load_config()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/copyright')
def copyright():
	return render_template('copyright.html')

@app.route('/trademarks')
def trademarks():
	return render_template('trademarks.html')

@app.route('/dataprotection')
def dataprotection():
	return render_template('dataprotection.html')

@app.route('/<law>/<vec>', methods=["GET"])
def autocomplete(law, vec):
	data = pd.read_csv(config[law]['data'])
	input_secs = [sec for sec in data['sec'] if 'sg' in sec]
	sections = input_secs
	return render_template("autocomplete.html", sections=sections, vec=vec, law=law)
	

@app.route('/result', methods = ['POST'])
def result():
	result = dict(request.form)
	section = result['Section']
	vec_choice = result['Vec']
	law_choice = result['Law']
	vector_path = config[law_choice]['vectors'][vec_choice]
	vectors = np.load(vector_path)
	data_path = config[law_choice]['data']
	data = pd.read_csv(data_path)
	try:
		query = data[data['sec']==section][['sec', 'title', 'url']].to_dict('records')[0]
	except IndexError:
		raise Exception('Fill in a value from the autocomplete list, e.g. "sg_9". Please click back and try again.') 
	if law_choice == 'dataprotection':
		result = retrieve(section, data, vectors, output_juris='eu')
	else:
		result = retrieve(section, data, vectors)
	return render_template("result.html", result=result, query=query, vec_choice=vec_choice)



def retrieve(input_sec, data, vectors, output_juris='uk', k=5):
    vectors = pd.DataFrame(vectors, index=data['sec'])
    juris_split_id = data[data['sec'].str.contains(output_juris)].first_valid_index()
    # get the index for when the next jurisdiction entries start 
    candidate_vecs = vectors[juris_split_id:]
    cos_sims = cosine_similarity(
            [vectors.loc[input_sec]],
            candidate_vecs)
    result_ids = (-cos_sims)[0].argsort()[:k]
    result_secs = candidate_vecs.iloc[result_ids].index
    return {i+1:data[data['sec']==res][['sec', 'title', 'url']].to_dict('records')[0] 
            for i,res in enumerate(result_secs)}