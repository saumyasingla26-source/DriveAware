from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
import matplotlib.pyplot as plt
import numpy as np

class GraphScreen(BoxLayout):
    def update_graph(self, ear_history):
        # Clear figure and plot
        plt.clf()
        plt.plot(ear_history, color='green')
        plt.ylim(0, 0.5)
        plt.title("EAR over time")
        plt.xlabel("Frame")
        plt.ylabel("EAR")
        plt.tight_layout()

        # Draw figure to numpy array
        fig = plt.gcf()
        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(h, w, 3)

        # Flip vertically for Kivy
        img = np.flipud(img)

        # Convert to Kivy texture
        tex = Texture.create(size=(w, h))
        tex.blit_buffer(img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        self.ids.graph.texture = tex