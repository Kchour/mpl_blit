"""This module provides a helper class for using matplotlib animations
    based on the advanced blitting tutorial

https://matplotlib.org/stable/tutorials/advanced/blitting.html

"""
import matplotlib.pyplot as plt
import logging

my_logger = logging.getLogger(__name__)
    
class Animator:
    """Helper class for matplotlib animations
        Class instances are used to keep track of different figures and their
        respective artists so that we can efficiently redraw them for
        animations.

        `instances` looks like the following: 
        {
            "figure_names": Animator objects
        }

        Each Animator object is created per figure and keeps track of all
        artists within the figure axes.
    
    Todo:
        * Add support for subplots
        * Test usage multiple figures

    """
    # keep track of Animator instances (keyed by fig num (int))
    instances = {}

    def __init__(self, figure_number:int, figure_name:str):
        self.figure_number = figure_number
        self.figure_name = figure_name
        self.background = None
        self.artists = {}

        # grab the background on every draw            
        fig = plt.figure(figure_number)

        # support redraw events
        self.ax = fig.axes[0]
        self.canvas = fig.canvas    
        self.cid = self.canvas.mpl_connect("draw_event", self._on_draw)

    def _add_artists(self, artist, artist_name: str): 
        """Add artist to dictionary"""
        self.artists[artist_name] = {'artist': [artist]}    

    def _on_draw(self, event):
        """Callback to register with 'draw_event'"""
        cv = self.canvas
        fig = cv.figure
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self.background = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()
        cv.blit(fig.bbox)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        
        # sort artists by zorder
        sorted_artist = sorted(self.artists.values(), key=lambda x: x['artist'][0].get_zorder())

        for a in sorted_artist:
            # Draw artists
            try:
                fig.draw_artist(a['artist'][0])
            except Exception as e:
                # THis will usually happen if we set shapes to None initially. 
                # Sometimes we expect exceptions...need better error handling
                my_logger.warn("Something iffy with the artist", exc_info=True)

    @classmethod
    def get_artist(cls, artist_name: str, fig_num: int):
        if artist_name in cls.instances[fig_num].artists:
            return cls.instances[fig_num].artists[artist_name]['artist'][0]

    @classmethod
    def del_artist(cls, artist_name: str, fig_num: int):
        """Removes a particular artist from both the Animator instance and the axes"""
        if artist_name in cls.instances[fig_num].artists:
            cls.instances[fig_num].artists[artist_name]['artist'][0].remove()
            del cls.instances[fig_num].artists[artist_name]

    @classmethod
    def init_figure(cls, figure_number: int=None, figure_name: str=""):
        """Store reference to figure axes and and fig object via Animator object

        Args:
            figure_number (int): (optional) if not specified, we will grab number from latest figure
                number starts from 1.
            figure_name (str): (optional) name of figure

        """
        # plt.show(block=False)
        plt.ion()    
        # the following is required required for blitting to work properly.
        plt.pause(0.1)

        # Crete an Animator instance for each fig number. Fig name is optional
        # if fig num is not specified, then get number for current fig
        _fig_num = cls.get_fig_num(figure_number)
        o = Animator(_fig_num, figure_name)
        cls.instances[_fig_num] = o

    @staticmethod
    def get_fig_num(figure_number):
        """Pass through function. When figure number is None, return
        the current figure number. Lowest index starts at 1.

        """
        if figure_number is None:
            return plt.gcf().number
        else:
            return figure_number

    @classmethod
    def add_artist(cls, artist, artist_name: str, figure_number: int=None):
        """Add an artist primitive object to Animator class

        first create artist externally using matplotlib, then 
        pass it here through this function call. Must give 
        a unique string name!

        """
        _fig_num = cls.get_fig_num(figure_number)
        if artist_name not in cls.instances[_fig_num].artists:
            artist.set_animated(True)
            cls.instances[_fig_num]._add_artists(artist, artist_name)

    @classmethod
    def update(cls, figure_number: int=None, pause_time:float=0):
        """Render all artist changes to screen
        
        Call this function after making changes to a frame.

        """
        _fig_num = cls.get_fig_num(figure_number)
        fig = plt.figure(_fig_num)
        ax = fig.axes[0]

        if cls.instances[_fig_num].background is None:
            cls.instances[_fig_num]._on_draw(None)
        else:
            # restore background 
            fig.canvas.restore_region(cls.instances[_fig_num].background)
            
            cls.instances[_fig_num]._draw_animated()
            # blit the axes
            fig.canvas.blit(fig.bbox)

        # flush events
        fig.canvas.flush_events()

        # pause if necessary
        if pause_time>0:
            plt.pause(0.001)

    @classmethod
    def reset(cls):
        """remove all Animator instances"""
        cls.instances = {}

    @classmethod
    def close(cls):
        cls.reset()
        plt.close()




