from datetime import date
import json
import matplotlib.pyplot as plt
import numpy as np
import requests
def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )


    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    ...
    magnitudes_per_year = {}
    for earthquake in earthquakes:
    
            year = get_year(earthquake)
            magnitude = get_magnitude(earthquake)

            
            if year not in magnitudes_per_year:
                magnitudes_per_year[year] = []

    
            magnitudes_per_year[year].append(magnitude)

    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    ...
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    average_magnitudes = []
    for year in magnitudes_per_year.keys():
        years.append(year)
        average_magnitude = np.mean(magnitudes_per_year[year])
        average_magnitudes.append(average_magnitude)

    plt.figure(figsize=(10, 6))
    plt.plot(years, average_magnitudes, marker = 'o')
    plt.ylabel('average_magnitude')
    plt.xlabel('year')
    plt.title('average_magnitude_per_year')
    plt.grid()
    plt.show()


def plot_number_per_year(earthquakes):
    ...

    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    nums = []
    for year in magnitudes_per_year.keys():
        years.append(year)
        nums.append(len(magnitudes_per_year[year]))
        

    plt.figure(figsize=(10, 6))
    plt.bar(years, nums)
    plt.ylabel('number')
    plt.xlabel('year')
    plt.title('number_per_year')
    plt.grid()
    plt.show()

# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)