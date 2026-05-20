import json
import os
from geopy.geocoders import Nominatim

# Setup locations
locations = [
    "Uvalde, TX",
    "Highland Park, IL",
    "Monterey Park, CA",
    "Nashville, TN"
]

def collect_bounding_boxes(locations, output_file="data/bboxes.json"):
    geolocator = Nominatim(user_agent="gun_violence_research_cga")
    bboxes = {}

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for loc in locations:
        try:
            # Geocode the location
            location = geolocator.geocode(loc)
            if location and hasattr(location, 'raw') and 'boundingbox' in location.raw:
                # Bounding box is a list [lat_min, lat_max, lon_min, lon_max] as strings
                bbox = location.raw['boundingbox']
                bboxes[loc] = {
                    "lat_min": float(bbox[0]),
                    "lat_max": float(bbox[1]),
                    "lon_min": float(bbox[2]),
                    "lon_max": float(bbox[3])
                }
                print(f"✅ Successfully found bounding box for {loc}")
            else:
                print(f"⚠️ Could not find bounding box for {loc}")
        except Exception as e:
            print(f"Error fetching data for {loc}: {e}")

    with open(output_file, "w") as f:
        json.dump(bboxes, f, indent=4)
    print(f"\nSaved bounding boxes to {output_file}")

if __name__ == "__main__":
    collect_bounding_boxes(locations)
