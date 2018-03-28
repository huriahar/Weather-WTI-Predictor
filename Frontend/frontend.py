from bottle import *

@route('/static/<filename:path>')
def get_css(filename):
	return static_file(filename, root='./')

@route('/')
def search_form():

	homepage = template('header.tpl') + template('form.tpl')
	return homepage


@route('/', method='POST')
def getresults():
	past = int(request.forms.get('past'))
	if past == 1: past = 5
	elif past == 2: past = 7
	elif past == 3: past = 14
	elif past == 4: past = 30
	else: past = 60

	future = int(request.forms.get('future'))
	if future == 1: future = 1
	elif future == 2: future = 7
	elif future == 3: future = 14
	elif future == 4: future = 30
	elif future == 5: future = 60
	else: future = 90


	year = request.forms.get('year')

	image = '''<img src="/static/img/{},{},{}.png">'''.format(str(past), str(future), str(year))

	###### TO DO ::: Need to add validation on the form! 
	if past == '' or future == '' or year == '':
		return template('header.tpl') + template('form.tpl')
	else:
		return template('header.tpl') + template('form.tpl') + image

@route('/faq')
def faq():

	faq = template('header.tpl') + template('faq.tpl')
	return faq

# @route('/about')
# def about():

# 	about = template('header.tpl') + template('about.tpl')
# 	return about


run(host="localhost", port=8080, debug=True)