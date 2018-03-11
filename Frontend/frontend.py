from bottle import *

# @route('/static/<filename:path>')
# def get_css(filename):
# 	return static_file(filename, root='./')

@route('/')
def search_form():

	main_homepage = template('index.tpl') 
	return main_homepage


@route('/results', method='POST')
def getresults():
	past = request.forms.get('past')
	future = request.forms.get('future')

	# TO DO ::: Need to add validation on the form! 


	if past == '' or future == '':
		redirect('/')
	else:
		return '''<p> STILL WORKING ON RESULTS PAGE</p>'''


@route('/faq')
def faq():
	return '''<p>STILL WORKING ON IT</p>'''

@route('/about')
def faq():
	return '''<p>STILL WORKING ON IT</p>'''

run(host="localhost", port=8080, debug=True)