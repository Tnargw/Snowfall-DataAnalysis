# Overview

This program utilizes data from Open-Meteo's Historical Weather Api to return information on snowfall amount across a given date range.


My purpose in making this program was simply that I was curious to see how snowfall varies between areas over a long period of time.
I decided to have the information shown on a map both to make it easier to see and understand.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the data set, the questions and answers, the code running and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

My main question that I wanted to be answered with this program is how much more it snows in Rexburg Idaho than the surrounding areas.
From using the program I found that the area just north of Rexburg has had the most snowfall over the last five years.

# Development Environment

To make this program I used the following APIs.

Open-Meteo: This Api will return Historical Weather information given a latitude, longitude, and date range.

Geonames: This api will return cities near a given latitude and longitude.

Folium: This api takes the given set of coordinates and data and generates the .html map to be shown with the heatmap showing snowfall amount.

{Describe the programming language that you used and any libraries.}

# Useful Websites

* [Open-Meteo Documentation](https://open-meteo.com/en/docs)
* [Geonames Documentation](https://www.geonames.org/manual.html)
* [Folium Documentation](https://python-visualization.github.io/folium/lates)

# Future Work

* Add option for heatmaps over time utilizing Foliums heatmap with time plugin
* Improve the functions that find nearby cities to get more accurate locations.
* Add option to allow users to save maps.