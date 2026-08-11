# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Python CLI program that visualizes historical snowfall data on a map. Given an address and a date range, it geocodes the address, finds nearby cities, fetches historical daily snowfall totals for each, and renders the results as a Folium heatmap saved to `map.html`.

There is no requirements/dependency manifest in the repo — the venv (`.venv`, Python 3.12) has the packages installed directly. Required libraries (per [README.md](README.md)): `geopy`, `folium`, `openmeteo-requests`, `requests-cache`, `retry-requests`, `numpy`.

## Commands

Run the program (prompts interactively for address, start date, and end date in `YYYY-MM-DD` format):

```bash
python main.py
```

There is no test suite, linter, or build step configured in this repository.

## Architecture

The program is a straight-line pipeline driven by [main.py](main.py), with each stage delegated to a class in `api/`:

1. **`api/map.py` — `MapGenerator`**: Wraps `geopy.Nominatim` for geocoding an address to lat/lon, and wraps `folium` for building the map, overlaying the heatmap layer, saving it to `map.html`, and opening it in a browser.
2. **`api/nearby.py` — `NearbyCities`**: Calls the Geonames `findNearbyPlaceNameJSON` API to get cities within a radius (default 100km, max 10 results) of a given lat/lon. Returns a `{city_name: (lat, lon)}` dict. Note: the Geonames username is hardcoded in this file.
3. **`api/weather.py` — `WeatherDataFetcher`**: Calls Open-Meteo's Historical Weather archive API (`archive-api.open-meteo.com`) for `snowfall_sum` over the given date range, using a persistent `requests_cache` session (`.cache.sqlite`, never expires) with retry logic. `process_weather_data` reduces a response to `[latitude, longitude, total_snowfall]`.

`main.py` ties these together: geocode the input address → get nearby cities → for each nearby city, fetch and process its weather data (skipping duplicate lat/lon/snowfall triples, since nearby-city lookups sometimes collide) → accumulate `[lat, lon, snowfall]` rows → render as a heatmap on the map centered on the input address → save and open `map.html`.

Two external services require network access and are unauthenticated/keyed by hardcoded usernames: Geonames (`api/nearby.py`) and Open-Meteo (`api/weather.py`, no key required). Geocoding uses OpenStreetMap's Nominatim via `geopy`.

`.cache.sqlite` (repo root and `api/`) is the `requests_cache` HTTP cache for weather API responses — it is generated data, not source.
