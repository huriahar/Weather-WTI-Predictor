from bottle import *

@route('/static/<filename:path>')
def get_css(filename):
	return static_file(filename, root='./')

@route('/')
def search_form():

	homepage = template('header.tpl') + template('form.tpl')
	return homepage


@route('/results', method='POST')
def getresults():
	past = request.forms.get('past')
	future = request.forms.get('future')
	year = request.forms.get('year')

	image = '''<img src="/static/img/{},{},{}.png">'''.format(str(past), str(future), str(year))

	###### TO DO ::: Need to add validation on the form! 
	if past == '' or future == '' or year == '':
		return template('header.tpl') + template('form.tpl')
	else:
		return template('header.tpl') + image

@route('/faq')
def faq():

	faq = template('header.tpl') + template('faq.tpl')
	return faq

# @route('/about')
# def about():

# 	about = template('header.tpl') + template('about.tpl')
# 	return about


run(host="localhost", port=8080, debug=True)