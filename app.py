#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from flask import Flask, render_template, request, flash
import sqlite3
from jj_slice_calc import day_of_week, slice_calc, time_to_slice, fb_post_update
from random import choice
app = Flask(__name__)
app.secret_key = 'my precious'
slicetime = []
supername = ''
introfood = ["So you're slicing {}. Interesting!", "You are going to be slicing {}.", "{}, huh? Interesting choice!", "How about that {}?", "{} sure is tasty! Let's help you out.", "Let's talk {}.", "Everything you need to know about {}."]

connection = sqlite3.connect('jj_slicing.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Profiles (Name TEXT)')


@app.route("/", methods=["POST", "GET"])
def index():
	return render_template('index.html')


@app.route("/new", methods=["POST", "GET"])
def create_profile():
	if request.method == "POST":
		sliceload = []
		nameData = request.form['fname'] + " " + request.form['lname']
		sliceload.append(nameData)
		sliceload.append(request.form['turktime'])
		sliceload.append(request.form['hamtime'])
		sliceload.append(request.form['chztime'])
		sliceload.append(request.form['vittime'])
		sliceload.append(request.form['bftime'])
		with sqlite3.connect('jj_slicing.db') as connection:
			c = connection.cursor()
			c.execute('CREATE TABLE IF NOT EXISTS Profiles (Name TEXT, turk REAL, ham REAL, cheese REAL, vito REAL, beef REAL)')
			c.execute("SELECT * FROM Profiles")
			allData = c.fetchall()
			if nameData in str(allData):
				msh = "🔔 It seems you already have a profile.".decode('utf-8')
			else:
				c.execute('INSERT INTO Profiles VALUES(?, ?, ?, ?, ?, ?)', sliceload)
				msh = "🌟 Profile created!".decode('utf-8')
		flash(msh)
	return render_template('newprofile.html')


@app.route('/old')
def retrieve_profiles():
	with sqlite3.connect('jj_slicing.db') as connection:
		c = connection.cursor()
		c.execute('SELECT * FROM Profiles')
		profdata = c.fetchall()
	return render_template('allprofiles.html', data=profdata)


@app.route('/welcome', methods=["POST", "GET"])
def welcome():
	if request.method == "POST" or request.method == "GET":
		prof = []
		global supername
		supername = request.form['comp_select']
		prof.append(supername)
		with sqlite3.connect('jj_slicing.db') as connection:
			c = connection.cursor()
			c.execute("SELECT turk,ham,cheese,vito,beef FROM Profiles WHERE Name=?", prof)
			slicedump = c.fetchall()
			global slicetime
			del slicetime[:]
			for s in slicedump:
				slicetime.append(s)
		return render_template('welcome.html', name=supername)


@app.route('/resultpage', methods=["POST", "GET"])
def results():
	if request.method == "POST" or request.method == "GET":
		prof = []
		global supername
		prof.append(supername)
		with sqlite3.connect('jj_slicing.db') as connection:
			c = connection.cursor()
			c.execute("SELECT turk,ham,cheese,vito,beef FROM Profiles WHERE Name=?", prof)
			slicedump = c.fetchall()
			global slicetime
			del slicetime[:]
			for s in slicedump:
				slicetime.append(s)
		idx = supername.find(" ")
		fname = supername[:idx]
		food = request.form['foodchoice']
		greet = choice(introfood).format(food).capitalize()
		daystatus = day_of_week(food)
		amt = request.form['numpacks']
		numstatus = slice_calc(food, amt)
		ns = numstatus.split()
		for n in ns:
			if n.isdigit():
				num_packs = n
		timestatus = time_to_slice(num_packs, food, slicetime, fname)
		if 'enough' in numstatus:
			errstatus = numstatus
			return render_template('display.html', heading=greet, stat1=daystatus, stat2=numstatus, errno=errstatus)
		else:
			return render_template('display.html', heading=greet, stat1=daystatus, stat2=numstatus, stat3=timestatus, errno=None)


@app.route('/fbupdate', methods=["POST", "GET"])
def update_fb():
	if request.method == "POST":
		q3 = request.form['slname']
		cms = request.form['msg']
		fdsliced = request.form['fd']
		verify = fb_post_update(fdsliced, cms, q3)
		if verify is True:
			flash("Success! Your post has been shared. Please click home to go back to the homepage.")
		else:
			flash(verify)
	return render_template('updater.html')


@app.route('/search', methods=["POST", "GET"])
def search():
	if request.method == "POST":
		my_result = []
		query = request.form['search']
		with sqlite3.connect('jj_slicing.db') as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM Profiles")
			tables = c.fetchall()
		for t in tables:
			if query in t[0]:
				my_result.append(t)
		renum = len(my_result)
		return render_template('searches.html', results=my_result, renum=renum)


if __name__ == '__main__':
	app.run(debug=True)
