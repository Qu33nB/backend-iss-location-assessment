#!/usr/bin/env python
import sys
import requests
import turtle
import time


__author__ = 'Qu33nB via demo'


base_url = 'http://api.open-notify.org'
iss_icon = 'iss.gif'
world_map = 'map.gif'


def get_astronauts():
    """Return a dict of current astronauts and their spacecrafts"""
    r = requests.get(base_url + '/astros.json')
    r.raise_for_status()
    return r.json()['people']


def get_iss_location():
    """Returns the current location (lat, lon) of ISS as a float tuple"""
    r = requests.get(base_url + '/iss-now.json')
    r.raise_for_status()
    coordinates = r.json()['iss_position']
    lat = float(coordinates['latitude'])
    lon = float(coordinates['longitude'])
    return lat, lon


def map_iss(lat, lon):
    """Draws a world map and place ISS icon at lat, lon"""
    iss_map = turtle.Screen()
    iss_map.setup(720, 360)
    iss_map.bgpic(world_map)
    iss_map.setworldcoordinates(-180, -90, 180, 90)

    iss_map.register_shape(iss_icon)
    iss = turtle.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    return iss_map

def compute_rise_time(lat, lon):
    '''Returns the next horizon rise-time of ISS for specific lat/lon'''
    params = {'lat': lat, 'lon': lon}
    r = requests.get(base_url + '/iss-pass.json', params=params)
    r.raise_for_status()

    passover_time = r.json()['response'][1]['risetime']
    return time.ctime(passover_time)


def main():
    # Part A: People in space and their spacecrafts
    astro_dict = get_astronauts()
    print('\nCurrent people in space: {}'.format(len(astro_dict)))
    for astronaut in astro_dict:
        print(' - {} in {}'.format(astronaut['name'], astronaut['craft']))
    
    # Part B: Current position of ISS
    lat, lon = get_iss_location()
    print('\nCurrent ISS coordinates: lat={:.02f} lon={:.02f}'.format(lat, lon))

    # Part C: Render current ISS on world map
    screen = None
    try:
        # Attempts to load turtle and tk
        screen = map_iss(lat, lon)

        # Part D: Compute next pass-over time for our location
        indy_lat = 39.768403
        indy_lon = -86.158068
        location = turtle.Turtle()
        location.penup()
        location.color('aquamarine')
        location.goto(indy_lon, indy_lat)
        location.dot(5)
        location.hideturtle()
        next_pass = compute_rise_time(indy_lat, indy_lon)
        location.write(next_pass, align='center', font=('Arial', 12, 'normal'))
    except RuntimeError as e:
        print("ERROR: problem loading graphics: " + str(e))

    # leave the screen open until the user clicks on it
    if screen is not None:
        print('Click on the screen to exit...')
        screen.exitonclick()


if __name__ == '__main__':
    main()
