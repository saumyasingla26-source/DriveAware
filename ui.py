from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

import cv2
import numpy as np
import matplotlib.pyplot as plt

from modules.eye_detection_module import EyeDetection
from modules.drowsiness_logic_module import DrowsinessDetector
from modules.alarm_module import AlarmSystem


KV = '''
ScreenManager:

    HomeScreen:
    DashboardScreen:
    GraphScreen:


<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: 40
        spacing: 25
        md_bg_color: 0.95, 0.97, 1, 1

        MDIcon:
            icon: "car-brake-alert"
            halign: "center"
            font_size: "100sp"
            theme_text_color: "Custom"
            text_color: 0.2, 0.5, 1, 1

        MDLabel:
            text: "Driver Monitoring System"
            halign: "center"
            font_style: "H5"

        MDLabel:
            text: "AI-based Drowsiness Detection"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "START MONITORING"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 1, 1
            on_release: app.root.current = "dashboard"


<DashboardScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        md_bg_color: 0.97, 0.98, 1, 1

        # CAMERA CARD
        MDCard:
            radius: [20]
            elevation: 10

            MDIcon:
                icon: "video"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                opacity: 0.2

            Image:
                id: cam
                allow_stretch: True
                keep_ratio: True

        # STATUS ROW
        MDBoxLayout:
            size_hint_y: 0.18
            spacing: 8

            MDCard:
                md_bg_color: 0.2, 0.6, 1, 1
                radius: [15]

                MDBoxLayout:
                    orientation: "vertical"

                    MDIcon:
                        icon: "heart-pulse"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

                    MDLabel:
                        id: status
                        text: "READY"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

            MDCard:
                md_bg_color: 0.1, 0.8, 0.4, 1
                radius: [15]

                MDBoxLayout:
                    orientation: "vertical"

                    MDIcon:
                        icon: "eye"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

                    MDLabel:
                        id: ear
                        text: "EAR 0.0"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

            MDCard:
                md_bg_color: 1, 0.6, 0.2, 1
                radius: [15]

                MDBoxLayout:
                    orientation: "vertical"

                    MDIcon:
                        icon: "alert"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

                    MDLabel:
                        id: alerts
                        text: "0"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1

        # CONTROLS
        MDBoxLayout:
            size_hint_y: 0.15
            spacing: 10

            MDRaisedButton:
                text: "START"
                md_bg_color: 0.1, 0.8, 0.4, 1
                icon: "play"
                on_release: app.start_detection()

            MDRaisedButton:
                text: "PAUSE"
                md_bg_color: 1, 0.6, 0, 1
                icon: "pause"
                on_release: app.pause_detection()

            MDRaisedButton:
                text: "ANALYTICS"
                md_bg_color: 0.2, 0.6, 1, 1
                icon: "chart-line"
                on_release: app.root.current = "graph"


<GraphScreen>:
    name: "graph"

    MDBoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 15
        md_bg_color: 0.95, 0.97, 1, 1

        MDLabel:
            text: "📊 Driver Analytics Dashboard"
            halign: "center"
            font_style: "H5"

        # MAIN GRAPH
        MDCard:
            radius: [20]
            elevation: 10

            Image:
                id: graph_img

        # STATS PANEL
        MDBoxLayout:
            size_hint_y: 0.2
            spacing: 10

            MDCard:
                md_bg_color: 0.2, 0.6, 1, 1
                radius: [15]

                MDLabel:
                    id: avg_ear
                    text: "Avg EAR: 0.0"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1

            MDCard:
                md_bg_color: 0.1, 0.8, 0.4, 1
                radius: [15]

                MDLabel:
                    id: max_ear
                    text: "Max EAR: 0.0"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1

            MDCard:
                md_bg_color: 1, 0.6, 0.2, 1
                radius: [15]

                MDLabel:
                    id: alert_score
                    text: "Alert Score: 0"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1

        MDRaisedButton:
            text: "GENERATE ANALYTICS"
            md_bg_color: 0.2, 0.6, 1, 1
            icon: "chart-box"
            on_release: app.show_graph()

        MDRaisedButton:
            text: "BACK"
            md_bg_color: 0.5, 0.5, 0.5, 1
            icon: "arrow-left"
            on_release: app.root.current = "dashboard"
'''


class HomeScreen(MDScreen):
    pass


class DashboardScreen(MDScreen):
    pass


class GraphScreen(MDScreen):
    pass


class DMSApp(MDApp):

    def build(self):
        self.eye = EyeDetection()
        self.logic = DrowsinessDetector()
        self.alarm = AlarmSystem()

        self.capture = cv2.VideoCapture(0)

        self.running = False
        self.alert_count = 0
        self.ear_history = []

        root = Builder.load_string(KV)
        self.dashboard = root.get_screen("dashboard")

        Clock.schedule_interval(self.update, 1/15)
        return root

    # ---------------- CONTROL ----------------
    def start_detection(self):
        self.running = True

    def pause_detection(self):
        self.running = False

    # ---------------- MAIN LOOP ----------------
    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        frame = cv2.flip(frame, 0)
        screen = self.dashboard

        if self.running:
            try:
                _, left_eye, right_eye = self.eye.process(frame)

                if left_eye and right_eye:
                    ear = self.logic.average_ear(left_eye, right_eye)
                    self.ear_history.append(ear)

                    drowsy = self.logic.check_drowsiness(ear)

                    screen.ids.ear.text = f"EAR {round(ear, 3)}"

                    if drowsy:
                        screen.ids.status.text = "DROWSY 🚨"
                        self.alert_count += 1
                        self.alarm.ring_alarm()
                    else:
                        screen.ids.status.text = "AWAKE 😊"

                    screen.ids.alerts.text = str(self.alert_count)

                else:
                    screen.ids.status.text = "NO FACE"

            except Exception as e:
                print("Error:", e)

        else:
            screen.ids.status.text = "PAUSED"

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        screen.ids.cam.texture = texture

    # ---------------- ADVANCED GRAPH ----------------
    def show_graph(self):
        if len(self.ear_history) == 0:
            return

        data = np.array(self.ear_history)

        avg_ear = float(np.mean(data))
        max_ear = float(np.max(data))
        alert_score = self.alert_count

        # UPDATE STATS UI
        graph_screen = self.root.get_screen("graph")
        graph_screen.ids.avg_ear.text = f"Avg EAR: {avg_ear:.3f}"
        graph_screen.ids.max_ear.text = f"Max EAR: {max_ear:.3f}"
        graph_screen.ids.alert_score.text = f"Alert Score: {alert_score}"

        # PLOT
        plt.figure(figsize=(6, 3))
        plt.plot(data, linewidth=2)
        plt.title("EAR Trend Analysis")
        plt.xlabel("Time")
        plt.ylabel("EAR")
        plt.grid()

        plt.savefig("graph.png")
        plt.close()

        graph_screen.ids.graph_img.source = "graph.png"

    # ---------------- CLEAN EXIT ----------------
    def on_stop(self):
        self.capture.release()
        self.eye.release()


if __name__ == "__main__":
    DMSApp().run()