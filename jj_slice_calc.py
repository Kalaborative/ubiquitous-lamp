#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from datetime import date, datetime, timedelta
from random import randint
import sqlite3
import facebook

# NOTE: MAKE SURE TO RUN sqlite3_db_profiles.py BEFORE RUNNING THIS CODE
# OTHERWISE THE PROFILE FEATURE WILL NOT WORK ! ! !
q3 = "Drew"

# define our global variables
# In this case, we set these to what we believed would be
# completely full slicing levels, by pack.
fullturkey = 18
fullham = 21
fullvito = 11
fullbeef = 12
fullcheese = 18

# A list of terms the calculator will accept
# This also describes the specific order in which to insert the values.
terms = ['turkey', 'ham', 'cheese', 'vito', 'beef']

profiles = []
sliceload = []
slicetime = []

# Depending on the weekday, different slicing levels are observed.
# This is why this function is necessary.


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


# This be the big function.
def slice_calc(food, amt):
  if food == "ham":
    day_of_week(food)
    leftover = fullham - float(amt)  # Why float? Because we're rounding numbers.
    result = int(round(leftover / 3))  # Rounding an integer would be kinda pointless.
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d hams. 🍘" % result
      dys = dys.decode('utf-8')

  elif food == "turkey":
    day_of_week(food)
    leftover = fullturkey - float(amt)
    result = int(round(leftover / 1))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You would need to slice about %d turkeys. 🦃" % result
      dys = dys.decode('utf-8')

  elif food == "vito":
    day_of_week(food)
    leftover = fullvito - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d salami and capicola. 🌭" % result
      dys = dys.decode('utf-8')

  elif food == "beef":
    day_of_week(food)
    leftover = fullbeef - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d hunks of roast beef. 🍖" % result
      dys = dys.decode('utf-8')

  elif food == "cheese":
    day_of_week(food)
    leftover = fullcheese - float(amt)
    result = int(round(leftover / 3))
    if is_negative(result):
      dys = is_negative(result)
    else:
      dys = "You need to slice %d logs of cheese. 🧀" % result
      dys = dys.decode('utf-8')
  reset_stockvalue()
  return dys

# This function approximates the time it takes to slice a meat.
# Note that this means NO DISTRACTIONS WHATSOEVER!
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


# This basically prevents the program from saying something like..
# "you need to slice -4 turkeys."
# In other words, it's already full dipshit.
def is_negative(n):
  if int(n) <= 0:
    dys = "You have enough! Don't slice anymore."
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

def fb_post_update(fdsliced, cms, q3):
  justfin = "Our rock star, %s, just finished slicing " % q3
  status = justfin + fdsliced + "! " + cms
  try:
    my_token = "EAAN7unK1SmkBAKwXN1A9qfxU76AoVuqTURSDEWmfsnmcH3mX0JlRlOku4loy5IHpHZBtCHezaiDyQ5Pm6T2mAZB0jbuDMNdthZAFujg1gxPvMVq8LtgZAm4V7vAfKladj99gA9sS9Np37iIzWJUkhPFgJAt19HVoISqFZBaYRUwZDZD"
    my_id = "1664030033909655"
    graph = facebook.GraphAPI(access_token=my_token)
    graph.put_object(parent_object=my_id, connection_name='feed', message=status)
    return True
  except Exception as e:
    return e
  
def profile_loader(name):
  sliceload.append(name)
  print "On average, how many minutes does it take to slice 1 turkey?"
  print "If you don't know, guess."
  print "Decimals are accepted."
  tur = raw_input("> ")
  sliceload.append(tur)
  print "Ham?"
  ham = raw_input("> ")
  sliceload.append(ham)
  print "Cheese?"
  chz = raw_input("> ")
  sliceload.append(chz)
  print "And vito?"
  vit = raw_input("> ")
  sliceload.append(vit)
  print "Beef?"
  bf = raw_input("> ")
  sliceload.append(bf)

  with sqlite3.connect("jj_slicing.db") as connection:
    c = connection.cursor()

    c.execute("INSERT INTO Profiles VALUES(?, ?, ?, ?, ?, ?)", sliceload)
  print "Profile complete! Successfully updated database."


def slice_dump(person):
  prof = []
  prof.append(person)
  with sqlite3.connect("jj_slicing.db") as connection:
    c = connection.cursor()
    c.execute("SELECT turk,ham,cheese,vito,beef FROM Profiles WHERE Name=?", prof)
    slicedump = c.fetchall()
    for s in slicedump:
      slicetime.append(s)


# The main function that makes it run infinitely unless told otherwise.


def slicing_helper():
  while True:
    q1 = raw_input("What are you slicing? ")
    q2 = raw_input("How many packs of %s do you have? " % q1)

    if q1 in terms:
      slice_calc(q1, q2)
    else:
      print "Sorry that food item does not exist! Try again."
