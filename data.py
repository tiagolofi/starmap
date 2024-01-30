
from datetime import datetime
from tzwhere import tzwhere
from pytz import timezone, utc

from skyfield.api import Star, load, load_file, wgs84
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN

from utils.mod_hipparcos import mod_load_dataframe
from os import listdir

class DataStarMap(object):

    def __init__(self):
        
        self.url_constellation = 'https://raw.githubusercontent.com/skyfielders/python-skyfield/master/ci/constellationship.fab'
    
        if ['de421bsp', 'hip_main.dat', 'constellationship.fab'] not in listdir():
            self.__download_data()
            self.eph, self.stars, self.constellations = self.__load_data()
        else:
            self.eph, self.stars, self.constellations = self.__load_data()

    def __load_data(self):

        return load_file('./de421.bsp'), mod_load_dataframe('./hip_main.dat'), stellarium.parse_constellations(open('./constellationship.fab', 'rb')) 

    def __download_data(self):

        load('de421.bsp')

        # hipparcos dataset
        with load.open(hipparcos.URL) as f:
            hipparcos.load_dataframe(f)

        # constellation dataset

        with load.open(self.url_constellation) as f:
            stellarium.parse_constellations(f)

    def collect_celestial_data(self, when: str, lat: float, long: float):

        # Convert date string into datetime object
        dt = datetime.strptime(when, '%Y-%m-%d %H:%M')

        # Define datetime and convert to UTC based on location coordinates
        timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
        print(timezone_str)
        local = timezone(timezone_str)
        utc_dt = local.localize(dt, is_dst=None).astimezone(utc)

        # Define observer using location coordinates and current UTC time
        t = load.timescale().from_datetime(utc_dt)
        observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)

        # An ephemeris on Earth position.
        earth = self.eph['earth']

        # And the constellation outlines list.
        edges = [edge for name, edges in self.constellations for edge in edges]
        edges_star1 = [star1 for star1, star2 in edges]
        edges_star2 = [star2 for star1, star2 in edges]


        # Define the angle and center the observation location by the angle - position
        # observer.from_altaz(alt_degrees=90, az_degrees=0)
        ra, dec, distance = observer.radec()
        center_object = Star(ra = ra, dec = dec)

        # Build the stereographic projection - field_of_view_degrees = 180.0
        center = earth.at(t).observe(center_object)
        projection = build_stereographic_projection(center)

        # Compute the x and y coordinates based on the projection
        star_positions = earth.at(t).observe(Star.from_dataframe(self.stars))
        self.stars['x'], self.stars['y'] = projection(star_positions)

        return self.stars, edges_star1, edges_star2

