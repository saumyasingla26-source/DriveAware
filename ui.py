from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
import cv2

from modules.eye_detection_module import EyeDetection
from modules.drowsiness_logic_module import DrowsinessDetector
from modules.alarm_module import AlarmSystem

KV = '''

ScreenManager:
    HomeScreen:
    DashboardScreen:
    GraphScreen:

# ---------------- HOME ---------------- #
<HomeScreen@MDScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: 30
        spacing: 30
        md_bg_color: 0.07, 0.07, 0.1, 1

        MDLabel:
            text: "🚗 Driver Monitoring System"
            halign: "center"
            font_style: "H3"
            theme_text_color: "Custom"
            text_color: 1,1,1,1

        MDLabel:
            text: "AI based Drowsiness Detection"
            halign: "center"
            theme_text_color: "Hint"

        MDRaisedButton:
            text: "Start Monitoring"
            icon: "camera"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0, 0.6, 1, 1
            on_release: app.start_dashboard()


# ---------------- DASHBOARD ---------------- #
<DashboardScreen@MDScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: "horizontal"

        # 🔹 SIDEBAR
        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: 0.22
            padding: 10
            spacing: 15
            md_bg_color: 0.1, 0.1, 0.15, 1

            MDLabel:
                text: "MENU"
                halign: "center"
                theme_text_color: "Hint"

            MDRaisedButton:
                text: "Home"
                icon: "home"
                on_release: app.go_home()

            MDRaisedButton:
                text: "Graph"
                icon: "chart-line"
                on_release: app.go_graph()

        # 🔹 MAIN CONTENT
        MDBoxLayout:
            orientation: "vertical"
            padding: 10
            spacing: 10

            MDTopAppBar:
                title: "Dashboard"
                md_bg_color: 0, 0.5, 1, 1

            # CAMERA BIG
            MDCard:
                size_hint_y: 0.65
                radius: [20]
                elevation: 10

                Image:
                    id: cam

            # STATUS GRID
            MDGridLayout:
                cols: 3
                spacing: 10
                size_hint_y: 0.35

                MDCard:
                    radius: [15]
                    elevation: 6
                    md_bg_color: 0.2,0.2,0.3,1

                    MDBoxLayout:
                        orientation: "vertical"

                        MDIcon:
                            icon: "alert"
                            halign: "center"

                        MDLabel:
                            id: status
                            text: "Status"
                            halign: "center"

                MDCard:
                    radius: [15]
                    elevation: 6
                    md_bg_color: 0.2,0.2,0.3,1

                    MDBoxLayout:
                        orientation: "vertical"

                        MDIcon:
                            icon: "eye"
                            halign: "center"

                        MDLabel:
                            id: ear
                            text: "EAR"
                            halign: "center"

                MDCard:
                    radius: [15]
                    elevation: 6
                    md_bg_color: 0.2,0.2,0.3,1

                    MDBoxLayout:
                        orientation: "vertical"

                        MDIcon:
                            icon: "bell"
                            halign: "center"

                        MDLabel:
                            id: alerts
                            text: "Alerts"
                            halign: "center"


# ---------------- GRAPH ---------------- #
<GraphScreen@MDScreen>:
    name: "graph"

    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20
        md_bg_color: 0.07, 0.07, 0.1, 1

        MDTopAppBar:
            title: "EAR Analytics"
            left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
            md_bg_color: 0, 0.5, 1, 1

        MDRaisedButton:
            text: "Show Graph"
            icon: "chart-line"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0, 0.6, 1, 1
            on_release: app.show_graph()

        MDLabel:
            text: "Visualize EAR trend over time"
            halign: "center"
            theme_text_color: "Hint"
'''

class DMSApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.eye = EyeDetection()
        self.logic = DrowsinessDetector()
        self.alarm = AlarmSystem()

        self.capture = None
        self.alert_count = 0
        self.ear_history = []

        return Builder.load_string(KV)

    # -------- NAVIGATION -------- #
    def start_dashboard(self):
        self.root.current = "dashboard"

        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1/15)

    def go_home(self):
        self.root.current = "home"

    def go_graph(self):
        self.root.current = "graph"

    def go_dashboard(self):
        self.root.current = "dashboard"

    # -------- MAIN LOOP -------- #
    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        # ✅ FIXED CAMERA (natural view)
        frame = cv2.flip(frame, 0)

        try:
            landmarks, left_eye, right_eye = self.eye.process(frame)

            if left_eye and right_eye:
                ear = self.logic.average_ear(left_eye, right_eye)
                self.ear_history.append(ear)

                drowsy = self.logic.check_drowsiness(ear)

                if drowsy:
                    status = "🚨 DROWSY"
                    color = (1, 0, 0, 1)
                    self.alert_count += 1
                    self.alarm.ring_alarm()
                else:
                    status = "😊 AWAKE"
                    color = (0, 1, 0, 1)
            else:
                status = "No Face"
                ear = 0
                color = (1, 0.5, 0, 1)

            screen = self.root.get_screen("dashboard")

            screen.ids.status.text = status
            screen.ids.status.text_color = color
            screen.ids.ear.text = f"EAR: {round(ear,3)}"
            screen.ids.alerts.text = f"Alerts: {self.alert_count}"

        except Exception as e:
            print(e)

        # SHOW CAMERA
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        texture = self._frame_to_texture(rgb)
        self.root.get_screen("dashboard").ids.cam.texture = texture

    # -------- GRAPH -------- #
    def show_graph(self):
        import matplotlib.pyplot as plt

        if len(self.ear_history) == 0:
            print("No data")
            return

        plt.plot(self.ear_history)
        plt.title("EAR Trend Over Time")
        plt.xlabel("Time")
        plt.ylabel("EAR")
        plt.show()

    def _frame_to_texture(self, frame):
        from kivy.graphics.texture import Texture
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        return texture

    def on_stop(self):
        if self.capture:
            self.capture.release()
        self.eye.release()


if __name__ == "__main__":
    DMSApp().run()