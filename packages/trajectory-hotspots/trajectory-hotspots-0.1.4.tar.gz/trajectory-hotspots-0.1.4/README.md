rajectory-hotspots
trajectory-hotspots is a Python library designed to detect hotspots between two paths. Whether you are analyzing data, mapping points of interest, or simply exploring patterns within datasets, this library provides a robust solution for identifying significant points of convergence or deviation between paths.

Features
Hotspot Detection: Identifies areas where two paths come close to each other or diverge significantly.
Trajectory Resizing: Resizes trajectories with interpolation to ensure more precise analysis.
Distance Calculation: Computes distances between points to determine hotspots with accuracy.
Installation
To install trajectory-hotspots, use pip:

bash
Copy code
pip install trajectory-hotspots
Usage
Here's a quick example of how to use the library:

python
Copy code
from hotspots import detect_hotspots

# Define your paths as lists of latitudes and longitudes (or any other coordinate system)
lat1 = [lat1_point1, lat1_point2, ...]
long1 = [long1_point1, long1_point2, ...]
lat2 = [lat2_point1, lat2_point2, ...]
long2 = [long2_point1, long2_point2, ...]

# Detect hotspots between the two paths
hotspots = detect_hotspots(lat1, long1, lat2, long2)

# Print or process the detected hotspots
print(hotspots)
# Display hotspots on maps
import folium
carte = folium.Map(location=[40,6], zoom_start=4)
trajet1=list(zip(lat1, long1))
trajet2=list(zip(lat2, long2))
folium.PolyLine(locations=trajet1, color='green', tooltip="Trajet 1").add_to(carte)
folium.PolyLine(locations=trajet2, color='blue', tooltip="Trajet 2").add_to(carte)
for Hotspot in hotspots:
  Latp = [sublist[1] for sublist in Hotspot]
  Logp = [sublist[2] for sublist in Hotspot]
  Lat1p = [sublist[3] for sublist in Hotspot]
  Log1p = [sublist[4] for sublist in Hotspot]
  Lat1p.reverse()
  Latp.extend(Lat1p)
  Log1p.reverse()
  Logp.extend(Log1p)
  folium.Polygon(locations=list(zip(Latp, Logp)), color='red', fill=True, fill_color='green', fill_opacity=0.5).add_to(carte)
carte

Why Use trajectory-hotspots?
Versatile: Works with any type of paths, not limited to geographic coordinates.
Easy Integration: Simple to integrate into existing data analysis workflows.
Accurate: Provides precise hotspot detection through interpolation and distance calculations.
Documentation
For more details and advanced usage, please refer to the documentation.

Contributing
If you find any issues or want to contribute to the development of trajectory-hotspots, please check out the GitHub repository for more information on how to get involved.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

