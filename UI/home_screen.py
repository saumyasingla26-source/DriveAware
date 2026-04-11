from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class HomeScreen(BoxLayout):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.orientation = 'vertical'
        self.status_label = Label(text="Status: Waiting...", font_size=24)
        self.ear_label = Label(text="EAR: 0.0", font_size=20)
        self.add_widget(self.status_label)
        self.add_widget(self.ear_label)

    def update_status(self, status, ear):
        self.status_label.text = f"Status: {status}"
        self.ear_label.text = f"EAR: {round(ear,3)}"