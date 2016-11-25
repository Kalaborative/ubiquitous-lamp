#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from flask import Flask, render_template, request, flash
from datetime import date, datetime, timedelta
import sqlite3
from random import randint
import facebook
from jj_slice_calc import fb_post_update
from random import choice
app = Flask(__name__)
app.secret_key = 'my precious'
slicetime = []
supername = ''
num_packs = 5
introfood = ["So you're slicing {}. Interesting!", "You are going to be slicing {}.", "{}, huh? Interesting choice!", "How about that {}?", "{} sure is tasty! Let's help you out.", "Let's talk {}.", "Everything you need to know about {}."]

connection = sqlite3.connect('jj_slicing.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Profiles (Name TEXT)')


fullturkey = 18
fullham = 21
fullvito = 11
fullbeef = 12
fullcheese = 18


def day_of_week(food):
  day = date.today().strftime("%A")
  if (day == 'Friday' or day == 'Saturday') and food == 'turkey':
    mys = "🗓Today is %s which means you need to slice 2 rows." % day
    mys = mys.decode('utf-8')
    global fullturkey
    fullturkey -= 6
  elif food == 'turkey':
    mys = "🗓Today is %s which means you need to slice 3 rows." % day
    mys = mys.decode('utf-8')
  elif (day == 'Friday' or day == 'Saturday') and food == 'ham':
    mys = "🗓Today is %s which means you need to slice 2 rows." % day
    mys = mys.decode('utf-8')
    global fullham
    fullham -= 7
  elif food == 'ham':
    mys = "🗓Today is %s which means you need to slice 3 rows." % day
    mys = mys.decode('utf-8')
  elif (day == 'Friday' or day == 'Saturday') and food == 'vito':
    mys = "🗓Today is %s which means you need to slice 1.5 rows." % day
    mys = mys.decode('utf-8')
    global fullvito
    fullvito -= 4
  elif food == 'vito':
    mys = "🗓Today is %s which means you need to slice 2 rows." % day
    mys = mys.decode('utf-8')
  elif (day == 'Friday' or day == 'Saturday') and food == 'beef':
    mys = "🗓Today is %s which means you need to slice 1 row." % day
    mys = mys.decode('utf-8')
    global fullbeef
    fullbeef -= 6
  elif food == 'beef':
    mys = "🗓Today is %s which means you need to slice 2 rows." % day
    mys = mys.decode('utf-8')
  elif (day == 'Friday' or day == 'Saturday') and food == 'cheese':
    mys = "🗓Today is %s which means you need to slice 2 rows." % day
    mys = mys.decode('utf-8')
    global fullcheese
    fullcheese -= 6
  elif food == 'cheese':
    mys = "🗓Today is %s which means you need to slice 3 rows." % day
    mys = mys.decode('utf-8')
  return mys


def slice_calc(food, amt):
  if food == "ham":
    leftover = fullham - float(amt)  # Why float? Because we're rounding numbers.
    result = int(round(leftover / 3))  # Rounding an integer would be kinda pointless.
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d hams. 🍘" % result
      dys = dys.decode('utf-8')

  elif food == "turkey":
    leftover = fullturkey - float(amt)
    result = int(round(leftover / 1))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You would need to slice about %d turkeys. 🦃" % result
      dys = dys.decode('utf-8')

  elif food == "vito":
    leftover = fullvito - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d salami and capicola. 🌭" % result
      dys = dys.decode('utf-8')

  elif food == "beef":
    leftover = fullbeef - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d hunks of roast beef. 🍖" % result
      dys = dys.decode('utf-8')

  elif food == "cheese":
    leftover = fullcheese - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d logs of cheese. 🧀" % result
      dys = dys.decode('utf-8')
  reset_stockvalue()
  return dys

def reset_stockvalue():
  global fullturkey
  fullturkey = 18
  global fullham
  fullham = 21
  global fullvito
  fullvito = 11
  global fullbeef
  fullbeef = 12
  global fullcheese
  fullcheese = 18


def time_to_slice(num_packs, food, slicetime, q3):
  num_packs = int(num_packs)
  if food == 'turkey':
    num_packs *= slicetime[0][0]
    a = "It would take about %d minutes to slice %s." % (num_packs, food)
    adj_packs = adjusted_time(num_packs)  # Shit happens. That's why we need an ADJUSTED time.
    int_packs = int(adj_packs)
    b = overhour_filter(int_packs)  # I'll explain this later.
    c = is_a_lot(int_packs, q3)  # This too.
  elif food == 'ham':
    num_packs *= slicetime[0][1]
    a = "It would take about %r minutes to slice %s." % (num_packs, food)
    adj_packs = adjusted_time(num_packs)
    int_packs = int(adj_packs)
    b = overhour_filter(int_packs)
    c = is_a_lot(int_packs, q3)
  elif food == 'cheese':
    num_packs *= slicetime[0][2]
    a = "It would take about %d minutes to slice %s." % (num_packs, food)
    adj_packs = adjusted_time(num_packs)
    int_packs = int(adj_packs)
    b = overhour_filter(int_packs)
    c = is_a_lot(int_packs, q3)
  elif food == 'vito':
    num_packs *= slicetime[0][3]
    a = "It would take about %d minutes to slice %s." % (num_packs, food)
    adj_packs = adjusted_time(num_packs)
    int_packs = int(adj_packs)
    b = overhour_filter(int_packs)
    c = is_a_lot(int_packs, q3)
  elif food == 'beef':
    num_packs *= slicetime[0][4]
    a = "It would take about %d minutes to slice %s." % (num_packs, food)
    adj_packs = adjusted_time(num_packs)
    int_packs = int(adj_packs)
    b = overhour_filter(int_packs)
    c = is_a_lot(int_packs, q3)
  return a, b, c

# So the concept of this is given any duration of time, in minutes,
# how likely would it be for an order to just pop in once or twice.
# This would be EXTREMELY difficult to do, so I simply guestimated
# by applying a small but random amount of minutes to our time.
def adjusted_time(ntime):
  if ntime < 10:
    ntime = ntime + randint(1, 4)
    return ntime
  elif ntime >= 10 and ntime < 30:
    ntime = ntime + randint(6, 14)
    return ntime
  elif ntime >= 30 and ntime < 60:
    ntime = ntime + randint(12, 19)
    return ntime
  elif ntime >= 60 and ntime < 91:
    ntime = ntime + randint(20, 38)
    return ntime
  elif ntime >= 91 and ntime < 120:
    ntime = ntime + randint(26, 44)
    return ntime
  else:
    ntime = ntime + randint(30, 50)
    return ntime


# How much is "a lot"? Well wouldn't you like to know!


def is_a_lot(n, q3):
  if n < 35:
    sit = "Lucky for you, %s, there's not a lot you have to do. Whoopee!" % q3
  elif n >= 35 and n < 50:
    sit = "Looks like you have quite a bit of slicing to do, %s. " % q3
  elif n >= 50 and n < 80:
    sit = "This might take a while but it shouldn't be overwhelming, %s." % q3
  elif n >= 80 and n < 110:
    sit = "You've got some serious work to do, %s. Chop chop!" % q3
  elif n >= 110:
    sit = "You have a LOT of slicing to do, %s! I'd get movin'!" % q3
  return sit


# So unfortunately the way the timedelta object works, it maxes out at 59 minutes.
# So for every adjusted time over that, I have to dissect it into hours and minutes.
# Fortunately, that wasn't very hard to figure out.
def overhour_filter(n):
  now = datetime.now()
  if n < 59:
    new_now = now + timedelta(minutes=n)
    end_time = new_now.strftime("%I:%M %p")
    done = "You should be done by about %s." % end_time
  elif n >= 59:
    min_v = n % 60
    hour_v = n / 60
    if min_v == 0:
      min_v = min_v + 1
    new_now = now + timedelta(minutes=min_v, hours=hour_v)
    end_time = new_now.strftime("%I:%M %p")
    done = "You should be done by about %s." % end_time
  return done

def is_negative(n):
  if int(n) <= 0:
    dys = "You have enough! Don't slice anymore."
    return dys


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
		global num_packs
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
