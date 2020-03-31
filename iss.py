#!/usr/bin/env python
import json
import requests
import turtle
import time


__author__ = 'Qu33nB'


def astronauts():
    """Get list of astronauts in space anad print their full names, the spacecraft they are currently on board, and the total number of astronauts in space."""
    url = 'http://api.open-notify.org/astros.json'
    response = requests.get(url).json()
    num_of_astronauts = response['number']
    print(num_of_astronauts)
    astronauts = response['people']
    for astro in astronauts:
        print ('{} is on Spacecraft {}'.format(astro['name'], astro['craft']))
    print ('On ISS = {}'.format(response['number']))

# Part B.


def spacestation():
    """Pulls the current LAT / LON of the ISS from the URL"""
    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url).json()
    coordinates = response['iss_position']
    lat = coordinates['latitude']
    long = coordinates['longitude']
    timestamp = response['timestamp']
    print ('Latitude: ' + lat)
    print ('Longitude: ' + long)
    print ('Time data was pulled: {}'.format(time.ctime(timestamp)))
    return lat, long, timestamp

# Part C


def map(lat, long):
    """Creates the world map and plots the location of the ISS"""
    world_map = turtle.Screen()
    world_map.setup(720, 360)
    world_map.bgpic('map.gif')
    world_map.setworldcoordinates(-180, -90, 180, 90)
    world_map.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(float(long), float(lat))

# Part D
    """Sends LAT/LON of Indy to URL, URL returns JSON timestamp of when ISS will
    passover the given LAT/LON. Plots Indy's location with a passover time."""
    indy_lat = 39.76691
    indy_long = -86.14996
    url = 'http://api.open-notify.org/iss-pass.json?lat={}&lon={}'.format(
        indy_lat, indy_long)
    response = requests.get(url).json()
    passover_time = response['response'][0]['risetime']
    indy = turtle.Turtle()
    indy.penup()
    indy.goto(indy_long, indy_lat)
    indy.dot(7, 'yellow')
    indy.hideturtle()
    indy.color('yellow')
    indy.write(time.ctime(passover_time))


def main():
    astronauts()
    coord = spacestation()
    map(coord[0], coord[1])
    turtle.exitonclick()


if __name__ == '__main__':
    main()
