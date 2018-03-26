from bottle import *

@route('/static/<filename:path>')
def get_css(filename):
	return static_file(filename, root='./static/img/')

@route('/')
def search_form():

	homepage = template('header.tpl') + template('form.tpl')
	return homepage


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

	faq = template('header.tpl') + template('faq.tpl')
	return faq

@route('/about')
def about():

	about = template('header.tpl') + template('about.tpl')
	return about


@route('/sample')
def sampleresults():
	test = template('header.tpl') + template('sampleresults.tpl')
	return test

run(host="localhost", port=8080, debug=True)