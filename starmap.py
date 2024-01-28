
from data import DataStarMap

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

from datetime import datetime
from os import listdir, mkdir
import numpy as np
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR')

font_path = 'utils/montserrat.ttf'
font_e = fm.FontEntry(font_path, 'montserrat')
fm.fontManager.ttflist.insert(0, font_e)

plt.rcParams['font.family'] = font_e.name

class StarMap(DataStarMap):

    def __init__(self, when, lat: float = -2.5116631, long: float = -44.3072184, limit_magnitude: int = 10):
        super().__init__()
        self.when = when
        self.lat = lat
        self.long = long
        self.stars, self.edges_star1, self.edges_star2 = self.collect_celestial_data(when = when, lat = lat, long = long)
        self.limiting_magnitude = limit_magnitude

    def star_map(self, location: str, chart_size: int, max_star_size: int, show: bool = False, daylight: bool = False, circle: bool = True):

        if daylight:
            fc = 'white'
            star_color = 'black'
            col_lines = 'black'
            font_color = 'black'
        else:
            fc = 'black' # '#041A40'
            star_color = 'white'
            col_lines = 'white'
            font_color = 'white'

        # Define the number of stars and brightness of stars to include
        
        bright_stars = (self.stars.magnitude <= self.limiting_magnitude)
        magnitude = self.stars['magnitude'][bright_stars]
        marker_size = max_star_size * 10 ** (magnitude / -2.5)

        # Calculate the constellation lines
        xy1 = self.stars[['x', 'y']].loc[self.edges_star1].values
        xy2 = self.stars[['x', 'y']].loc[self.edges_star2].values
        lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)

        # Time to build the figure!
        fig, ax = plt.subplots(figsize = (chart_size, chart_size), facecolor = fc)

        # Draw the constellation lines.
        ax.add_collection(
            LineCollection(lines_xy, colors = col_lines, linewidths = 0.15)
        )

        # Draw the stars.
        ax.scatter(
            self.stars['x'][bright_stars], self.stars['y'][bright_stars],
            s = marker_size, color = star_color, marker = '.', linewidths = 0,
            zorder = 2
        )

        if circle:
            border = plt.Circle((0, 0), 1, color = fc, fill = True)
            ax.add_patch(border)

            horizon = Circle((0, 0), radius = 1, transform = ax.transData)
            for col in ax.collections:
                col.set_clip_path(horizon)
        else:
            ax.set_aspect('equal')

        # Finally, add other settings
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        plt.axis('off')
        when_datetime = datetime.strptime(self.when, '%Y-%m-%d %H:%M')
        text = f'''
        Local de Observação: {location}, {str(round(self.lat, 2))}, {str(round(self.long, 2))}
        Data e Hora: {when_datetime.strftime('%d de %B de %Y às %H:%M')}
        Magnitude Limite: {str(self.limiting_magnitude)}
        '''

        plt.figtext(0.5, 0, text, horizontalalignment = 'center', color = font_color, fontsize = 10)
        filename = f"images/{location}_{when_datetime.strftime('%Y%m%d_%H%M')}.png"
        
        if 'images' not in listdir():
            mkdir('images')
            plt.savefig(filename, format='png', dpi=1200)
        else:
            plt.savefig(filename, format='png', dpi=1200)

        if show:
            plt.show()

        plt.close()

if __name__ == '__main__':

    generator = StarMap(when = '2024-01-23 10:29', lat = 35.680715, long = 139.767349, limit_magnitude = 10) # lat = -3.219105, long = -45.000949,

    generator.star_map(
        location = 'Tóquio, Japão', chart_size = 10, max_star_size = 100, daylight = True
    )