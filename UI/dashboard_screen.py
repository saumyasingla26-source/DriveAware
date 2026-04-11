from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class DashboardScreen(BoxLayout):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.orientation = 'vertical'
        self.cam_feed = Image()
        self.add_widget(self.cam_feed)

    def update_status(self,status,ear,alerts):
        self.status_text=f"{status}"
        self.ear_text = f"EAR: {ear:.3f}"
        self.alerts_text = f"Alerts: {alerts}"

        
    def update_frame(self, frame):
        import cv2
        from kivy.graphics.texture import Texture

        if frame is None:
            return
        frame = cv2.flip(frame, 0)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(rgb.shape[1], rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        self.cam_feed.texture = texture