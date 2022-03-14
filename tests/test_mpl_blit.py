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


        Animator.init_figure()

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

        x = np.linspace(0, 6 * np.pi, 1000)

        #add name of annotation artist name, so we can access it again later
        Animator.add_artist(fr_number, "time_ann")            

        for j in range(1000):
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
    def test_basic_mpl_feature(self):
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

        # make sure our window is on the screen and drawn
        plt.show(block=False)
        plt.pause(.1)

        Animator.init_figure()
        Animator.add_artist(ln, "line_artist")
        Animator.add_artist(fr_number, "frame_artist")
        
        ln.set_xdata(x)
        for j in range(1000):
            # update the artists
            fr_number.set_text("frame: {j}".format(j=j))
            # ln.set_ydata(np.sin(x + (j / 100) * np.pi))
            # tell the blitting manager to do it's thing
            Animator.update()

if __name__ == "__main__":
    unittest.main(verbosity=3) 