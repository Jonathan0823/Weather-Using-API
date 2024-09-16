import sys
import requests
import cred
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App")
        self.input_line = QLineEdit(self)
        self.button = QPushButton("Get Weather", self)
        self.title = QLabel("Weather App", self)
        self.input_label = QLabel("Input city", self)
        self.temperture_label = QLabel( self)
        self.emoji = QLabel(self)
        self.weather_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(650, 200, 400, 650)
        self.title.setAlignment(Qt.AlignCenter)
        self.input_label.setAlignment(Qt.AlignCenter)
        self.temperture_label.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignCenter)


        self.title.setObjectName("title")
        self.input_label.setObjectName("input_label")
        self.temperture_label.setObjectName("temperture_label")
        self.weather_label.setObjectName("weather_label")
        self.input_line.setObjectName("input_line")
        self.button.setObjectName("button")
        self.emoji.setObjectName("emoji")

        self.setStyleSheet("""
            #title {
                font-size: 40px;
                font-family: Arial;
                color: black;
                font-weight: bold;
            }
            #input_label {
                font-size: 40px;
                font-family: calibri;
                color: black;
                font-style: italic;
            }
            #input_line {
                font-size: 40px;
                font-family: calibri;
                color: black;
                padding: 10px;
            }
            #button {
                font-size: 30px;
                font-family: calibri;
                color: black;
                background-color: #b5d2ff;
                border-radius: 10px;
                border: 3px solid #78acfa;
                padding: 10px, 3px;
                margin: 20px;
            }
            #button:hover {
                background-color: #cce0ff;
            }
            #temperture_label {
                font-size: 30px;
                font-family: Arial;
                color: black;
            }
            #emoji {
                font-size: 100px;
                font-family: Segoe UI Emoji;
                margin: 20px;
            }
            #weather_label {
                font-size: 30px;
                font-family: Arial;
            }
                           
            """)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_line)
        layout.addWidget(self.button)
        layout.addWidget(self.temperture_label)
        layout.addWidget(self.emoji)
        layout.addWidget(self.weather_label)

        self.setLayout(layout)
        self.button.clicked.connect(self.get_weather)
        pass

    def get_weather(self):
        city = self.input_line.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={cred.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            
            if response.status_code == 200:
                self.show_weather(data)
                

        
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.show_error("Bad Request\n Error 400")
                case 401:
                    self.show_error("Unauthorized Error\n Error 401")
                case 403:
                    self.show_error("Forbidden Access\n Error 403")
                case 404:
                    self.show_error("Not Found\n Error 404")
                case 500:
                    self.show_error("Internal Server Error\n Error 500")
                case 502:
                    self.show_error("Bad Gateway\n Error 502")
                case 503:
                    self.show_error("Bad Request\n Error 503")
                case 504:
                    self.show_error("Bad Request\n Error 504")
                case _:
                    self.show_error("Request Error\n Error 400")

        except requests.exceptions.RequestException:
            self.show_error("Request Error\n Error 400")
        
        except requests.exceptions.ConnectionError:
            self.show_error("Connection Error\n please check your internet connection")

    def show_error(self, error):
        self.temperture_label.setStyleSheet("font-size: 30px;"
                                            "font-family: Arial;"
                                            )
        self.temperture_label.setText(error)
        self.emoji.setText("😭")
        self.weather_label.setText("")

    def show_weather(self, data):
        self.temperture_label.setStyleSheet("font-size: 50px;")
        temp = round(data["main"]["temp"] - 273.15, 2)
        weather = data["weather"][0]["description"]
        weather = weather.title()
        self.temperture_label.setText(f"{temp:0.0f}°C")
        weather_id = data["weather"][0]["id"]
        if 200 <= weather_id <= 232:
            self.emoji.setText("⛈️")
        elif 300 <= weather_id <= 321:
            self.emoji.setText("🌧️")
        elif 500 <= weather_id <= 531:
            self.emoji.setText("🌦️")
        elif 600 <= weather_id <= 622:
            self.emoji.setText("❄️")
        elif 701 <= weather_id <= 741:
            self.emoji.setText("🌫️")
        elif weather_id == 762:
            self.emoji.setText("🌋")
        elif weather_id == 771:
            self.emoji.setText("🌫️")
        elif weather_id == 781:
            self.emoji.setText("🌫️")
        elif weather_id == 800:
            self.emoji.setText("☀️")
        elif 801 <= weather_id <= 804:
            self.emoji.setText("⛅")
        else:
            self.emoji.setText("🤷‍♀️")
        self.weather_label.setText(weather)





def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()