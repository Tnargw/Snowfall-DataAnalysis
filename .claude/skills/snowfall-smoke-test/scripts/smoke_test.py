#!/usr/bin/env python3
"""Regenerate map.html for saved address/date-range test cases without interactive input()."""
import argparse
import json
import os
import sys
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from api.map import MapGenerator
from api.weather import WeatherDataFetcher
from api.nearby import NearbyCities

DEFAULT_CASES = [
    {"address": "Rexburg, Idaho", "start_date": "2024-01-01", "end_date": "2024-01-03"},
]


def run_case(case):
    address = case["address"]
    start_date = case["start_date"]
    end_date = case["end_date"]

    map_generator = MapGenerator()
    location = map_generator.geolocator.geocode(address)
    if location is None:
        return False, "Could not geocode address"

    nearby = NearbyCities()
    nearby_data = nearby.get_nearby_cities_geonames(location.latitude, location.longitude)
    if not nearby_data:
        return False, "No nearby cities returned"

    data = []
    weather_fetcher = WeatherDataFetcher()
    for name, coords in nearby_data.items():
        responses = weather_fetcher.fetch_weather_data(coords[0], coords[1], start_date, end_date)
        for response in responses:
            row = weather_fetcher.process_weather_data(response)
            if row not in data:
                data.append(row)

    if not data:
        return False, "No weather data collected"

    m = map_generator.get_map(address)
    if m is None:
        return False, "Map generation failed"

    map_generator.add_heat_map(m, data)

    map_path = os.path.join(PROJECT_ROOT, "map.html")
    if not os.path.exists(map_path):
        return False, "map.html was not written"
    if time.time() - os.path.getmtime(map_path) > 30:
        return False, "map.html was not updated recently"
    size = os.path.getsize(map_path)
    if size < 1000:
        return False, f"map.html suspiciously small ({size} bytes)"

    return True, f"OK - {len(data)} data points, map.html {size} bytes"


def main():
    parser = argparse.ArgumentParser(description="Smoke-test the snowfall map pipeline")
    parser.add_argument("--cases", help="Path to a JSON file with a list of {address, start_date, end_date}")
    args = parser.parse_args()

    if args.cases:
        with open(args.cases) as f:
            cases = json.load(f)
    else:
        cases = DEFAULT_CASES

    failures = 0
    for i, case in enumerate(cases, 1):
        label = f"{case['address']} ({case['start_date']} to {case['end_date']})"
        try:
            ok, message = run_case(case)
        except Exception as e:
            ok, message = False, f"Exception: {e}"
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Case {i}: {label} - {message}")
        if not ok:
            failures += 1

    print()
    if failures:
        print(f"{failures}/{len(cases)} case(s) failed.")
        sys.exit(1)
    else:
        print(f"All {len(cases)} case(s) passed.")


if __name__ == "__main__":
    main()
