import unittest
import numpy as np
import matplotlib.pyplot as plt 
from mpl_blit.animator import Animator

# @unittest.skip("test passed")
class TestMplBlit(unittest.TestCase):

    def setUp(self):
        # make a new figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        Animator.init_figure()

    def tearDown(self):
        Animator.close()

    # @unittest.skip("test passed")
    def test_circle_patch(self):
        import matplotlib.patches as patches

        patch = self.ax.add_artist(patches.Circle((None, None), 1, animated=True))
        patch.set_color([1,1,0,1])  #yellow
        Animator.add_artist(patch, "patch_art")

        for i in range(1000):
            x = 5 + 3 * np.sin(np.radians(i))
            y = 5 + 3 * np.cos(np.radians(i))
            # patch.center = (x, y)
            # patch.radius = np.sin(i/100)
            patch.set_center((x,y))
            patch.set_radius(np.sin(i/100))
            Animator.update()

    # @unittest.skip("test")
    def test_annotation_arrow(self):

        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

        # usage
        # ax.annotate('local max', xy=(3, 1),  xycoords='data',
        #             xytext=(0.8, 0.95), textcoords='axes fraction',
        #             arrowprops=dict(facecolor='black', shrink=0.05),
        #             horizontalalignment='right', verticalalignment='top',
        #             )
        # https://matplotlib.org/stable/tutorials/text/annotations.html#annotating-with-arrow


        # add annotation for time
        fr_number = self.ax.annotate(
            "0",
            None,
            xycoords="data",
            xytext=(0, 0),
            textcoords="data",
            arrowprops=dict(facecolor='black', alpha=0, arrowstyle="-"),
            ha="left",
            va="top",
            animated=True,
        )

        x = np.linspace(0, 6 * np.pi, 250)

        #add name of annotation artist name, so we can access it again later
        Animator.add_artist(fr_number, "time_ann")            

        for j in range(250):
            fr_number.set_text("frame: {j}".format(j=j))
            fr_number.set_position((np.sin(x[j])+1, np.cos(x[j])+1) )  #set position of the text
            # fr_number.set_x(np.sin(x[j]))
            fr_number.xy = (np.sin(x[j]), np.cos(x[j]))          #set arrow tip position (based on axes)
            # arrow properties are stored as arrow_patch
            fr_number.arrow_patch.set_alpha(1)                   #set arrow alpha
            fr_number.set_alpha(0)                               #set text alpha
            

            Animator.update()

        Animator.close()

    # @unittest.skip("test")
    def test_sine_wave_frame_ann(self):
        x = np.linspace(0, 2 * np.pi, 1000)

        # create a line2D artist
        (ln,) = self.ax.plot([], [], animated=True, label="sine")

        # create annotation artist 
        fr_number = self.ax.annotate(
            "0",
            (0, 1),
            xycoords="data",
            xytext=(0.15, 0.92),
            textcoords="figure fraction",
            ha="left",
            va="top",
            animated=True,
        )

        self.ax.set_xlim(min(x), max(x))
        self.ax.set_ylim(min(np.sin(x)), max(np.sin(x)))
        # add a legend, using either method
        # lg = ax.legend([ln], ["sine"], loc='upper center', bbox_to_anchor=(0.5, 1.10))
        self.ax.legend(loc='upper center',bbox_to_anchor=(0.5, 1.10))

        Animator.add_artist(ln, "line_artist")
        Animator.add_artist(fr_number, "frame_artist")
        
        ln.set_xdata(x)
        for j in range(1000):
            # update the artists
            fr_number.set_text("frame: {j}".format(j=j))
            ln.set_ydata(np.sin(x + (j / 100) * np.pi))
            # tell the blitting manager to do it's thing
            Animator.update()

    def test_scatter_animation(self):
        """Test scatter plot animation
        
        Info gathered at: 
            https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot

        Artist attributes can be changed or retrieved using getter and setter methods.
        More info: https://matplotlib.org/stable/tutorials/intermediate/artists.html

        Interestingly enough, modifications to masked_arrays will be reflected in artists
        without calling the set_xxx method!

        """
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        num_points = 50
        x,y,c = np.random.random((3, num_points))
        scat = self.ax.scatter(x, y, c=c, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")

        # return np.masked_arrays if array length is greater than 1
        xy = scat.get_offsets()
        c = scat.get_array()

        # s is always a 1d array
        s = np.ones(num_points)

        Animator.add_artist(scat, "scatter_artist")
        for j in range(1000):
            # let `array` be a 1d numpy array
            # to change positions (marker center)
            # scat.set_offsets(array)

            # to change sizes (marker size)
            # scat.set_sizes(array)

            # to change color (intensity 0-1)
            # scat.set_array(array)

            # to get offsets, sizes, or colors...use get_xxx, e.g.
            # scat.get_offsets()

            xy += 0.03*(np.random.random((num_points, 2)) - 0.5)
            s = 1024 * (np.random.random(num_points))
            c += 0.02 * (np.random.random(num_points) - 0.5)

            # set attributes. Interesting masked_array behavior...
            # scat.set_offsets(xy)
            scat.set_sizes(s)
            # scat.set_array(c)

            # get attributes to change once again
            # xy = scat.get_offsets()
            s = scat.get_sizes()
            # c = scat.get_array()

            Animator.update()

if __name__ == "__main__":
    unittest.main(verbosity=3) 