import sys
import os
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests


def get_pincode_from_coordinates(latitude, longitude):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'format': 'json',
        'lat': latitude,
        'lon': longitude,
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'YourAppName/1.0 (your.email@example.com)'
    }
    print(f"Fetching pincode for coordinates: {latitude}, {longitude}")
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if 'address' in data and 'postcode' in data['address']:
            return int(data['address']['postcode'])
        else:
            print("Postcode not found in the response.")
            return 0

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 0
    except ValueError as e:
        print(f"Error processing response: {e}")
        return 0
        


class Bridge(QObject):
    coordinates_received = pyqtSignal(int)

    

    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        x = get_pincode_from_coordinates(lat,lng)
        print(x)
        self.coordinates_received.emit(x)

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer")
        self.setGeometry(100, 100, 500, 800)

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("pybridge", self.bridge)
        self.webview.page().setWebChannel(self.channel)

        # Load the local HTML file
        self.load_map()

    def load_map(self):
        # Load local HTML file with Leaflet map
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map.html")
        self.webview.setUrl(QUrl.fromLocalFile(map_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.bridge.coordinates_received.connect(lambda lat, lng: print(f'{lat},{lng}'))
    window.show()
    sys.exit(app.exec_())
