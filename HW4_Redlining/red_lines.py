# step 1: load the redlines_data.json file which was 
# originally from https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson
# and understand the structure of it. the json object will be used to construct DetroitDistrict Instance

# import libraries
import random                               # for random seed
import json                                 # for loading json file
import os                                   # for file path
import random                               # randomly pick latitude and longitude
import numpy as np
import matplotlib.pyplot as plt     
from matplotlib.patches import Polygon      # drawing polygon using matplotlib
from matplotlib.path import Path            # for drawing a customized path
import requests                             # API calls
from collections import Counter             # count the word frequency in findCommonWords method 
import re                                   # remove all punctuation in long strings

random.seed(17)

class DetroitDistrict:
    """
    A class representing a district in Detroit with attributes related to historical redlining.
    coordinates,holcGrade,holcColor,id,description should be load from the redLine data file
    if cache is not available

    Parameters 
    ------------------------------
    coordinates : list of lists, 2D List, not list of list of list
        Coordinates defining the district boundaries from the json file
        Note that some districts are non-contiguous, which may
        effect the structure of this attribute

    holcGrade : str
        The HOLC grade of the district.

    id : str
        The identifier for the district, the HOLC ID.

    description : str, optional
        Qualitative description of the district.

    holcColor : str, optional
        A string represent the color of the holcGrade of the district

    randomLat : float, optional
        A random latitude within the district (default is None).

    randomLong : float, optional
        A random longitude within the district (default is None).

    medIncome : int, optional
        Median household income for the district, to be filled later (default is None).
        
    censusTract : str, optional
        Census tract code for the district (default is None).

    Attributes
    ------------------------------
    self.coordinates 
    self.holcGrade 
    holcColor : str
        The color representation of the HOLC grade.
        • Districts with holc grade A should be assigned the color 'darkgreen'
        • Districts with holc grade B should be assigned the color 'cornflowerblue'
        • Districts with holc grade C should be assigned the color 'gold'
        • Districts with holc grade D should be assigned the color 'maroon'
        If there is no input for holcColor, it should be generated based on the holcGrade and the rule above.
    self.id 
    self.description 
    self.randomLat 
    self.randomLong 
    self.medIncome 
    self.censusTract 
    """
    def __init__(self, coordinates, holcGrade, 
                 id, description, holcColor = None, 
                 randomLat = None, randomLong = None, 
                 medIncome = None, censusTract = None):
        self.coordinates = coordinates
        self.holcGrade = holcGrade
        self.id = id
        self.description = description
        self.holcColor = holcColor
        self.randomLat = randomLat
        self.randomLong = randomLong
        self.medIncome = medIncome
        self.censusTract = censusTract

class RedLines:
    """
    A class to manage and analyze redlining district data.

    Attributes
    ----------
    districts : list of DetroitDistrict
        A list to store instances of DetroitDistrict.

    """
    def __init__(self, cacheFile = None):
        """
        Initializes the RedLines class without any districts.
        assign districts attribute to an empty list
        """
        # start with a empty list
        self.districts = []

        # only load cache if file path is provided
        # use loadCache method in the class
        if cacheFile is not None:
            self.loadCache(cacheFile)

    def createDistricts(self, fileName):
        """
        Creates DetroitDistrict instances from redlining data in a specified file.
        Based on the understanding in step 1, load the file, parse the json object, 
        and create 238 districts instance.
        Finally, store districts instance in a list, 
        and assign the list to be districts attribute of RedLines.

        Parameters
        ----------
        fileName : str
            The name of the file containing redlining data in JSON format.

        Hint
        ----------
        The data for description attribute could be from  
        one of the dict key with only number.

        """
        # get the directory where this script file is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # join that directory with file name
        json_file = os.path.join(script_dir, fileName)

        f = open(json_file)
        data = json.load(f)
        f.close()

        features = data['features']

        for f in features:

            # coordinates under geometry, coordinates
            coordiantes = f.get('geometry', {}).get('coordinates', {})[0][0]

            # holcGrade under properties and holc_grade
            holcGrade = f.get('properties', {}).get('holc_grade', {})

            # id under properties and holc_id
            id = f.get('properties', {}).get('holc_id', {})

            # real description hid in the properties, area_description_data and 8
            description = f.get('properties', {}).get('area_description_data', {}).get('8', {})

            # cannot find any color part. thus, use the docstring rule
            if holcGrade == 'A':
                holcColor = 'darkgreen'
            elif holcGrade == 'B':
                holcColor = 'cornflowerblue'
            elif holcGrade == 'C':
                holcColor = 'gold'
            else:
                holcColor = 'maroon'
            
            # random part use the coordinates and library random
            random_point = random.choice(coordiantes)
            randomLong, randomLat = random_point

            # median income hid in the properties, area_description_data, and 1b
            # text sample = 'Jr. Executives, business men, mechanics $3000-5000'
            text = f.get('properties', {}).get('area_description_data', {}).get('1b', {})
            if '$' in text:
                money_part = text.split('$')[-1]
                if '-' in money_part:
                    low, high = money_part.split('-', 1)                # maxsplit = 1; split at mosst 2 parts
                    try:
                        income_min = int(low.strip())
                        income_max = int(high.strip())
                        medIncome = (income_min + income_max) / 2
                    except ValueError:
                        medIncome = None
                else:
                    medIncome = None
            else:
                medIncome = None

            district = DetroitDistrict(coordiantes, holcGrade, id, description,
                                       holcColor, randomLat, randomLong, medIncome)
        
            self.districts.append(district)
        
        return self.districts
            
    def plotDistricts(self):
        """
        Plots the districts using matplotlib, displaying each district's location and color.
        Name it redlines_graph.png and save it to the current directory. 
        """
        fig, ax = plt.subplots()

        for district in self.districts:
            points = district.coordinates
            poly = Polygon(
                points,
                closed = True,
                facecolor = district.holcColor,
                edgecolor = 'black',
                linewidth = 0.5,
                alpha = 0.6
            )
            ax.add_patch(poly)
            ax.autoscale()

        plt.rcParams["figure.figsize"] = (15,15)

        # get the directory where this script file is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # join that directory with figure name
        png_file = os.path.join(script_dir, 'redlines_graph.png')
        plt.savefig(png_file, dpi = 300)

        plt.show()

    def generateRandPoint(self):
        """
        Generates a random point within the boundaries of each district.

        This method creates a mesh grid of points covering the geographical area of interest
        and then selects a random point within the boundary of each district.

        Attributes
        ----------
        self.districts : list of DetroitDistrict
            The list of district instances in the RedLines class.

        Note
        ----
        The random point is assigned as the randomLat and randomLong for each district.
        This method assumes the 'self.districts' attribute has been populated with DetroitDistrict instances.
        """
        # xgrid = [-83.5, -83.496, -83.492, ...]
        # ygrid = [42.1, 42.104, 42.108, ...]
        xgrid = np.arange(-83.5, -82.8, 0.004)                  # make multiple points from left most to right most
        ygrid = np.arange(42.1, 42.6, 0.004)

        # xmesh =
        #        [[-83.5,   -83.496, -83.492, ...],
        #         [-83.5,   -83.496, -83.492, ...],
        #         [-83.5,   -83.496, -83.492, ...]]
        # ymesh = 
        #        [[42.1,    42.1,    42.1],
        #         [42.104,  42.104,  42.104],
        #         [42.108,  42.108,  42.108]]

        # ^ latitude (y)
        # | 
        # |  ● ● ● ● ●  (125 rows total)
        # |  ● ● ● ● ●
        # |  ● ● ● ● ●
        # +------------------> longitude (x)
        #   175 columns

        xmesh, ymesh = np.meshgrid(xgrid, ygrid)
        points = np.vstack((xmesh.flatten(), ymesh.flatten())).T
        
        for district in self.districts:

            # create a path polygon from coordinates of current district
            p = Path(district.coordinates)

            # find which grid points fall inside the polygon of current district
            # contains_points return a boolean array
            grid = p.contains_points(points)

            # np.where(grid)[0] gives the indexes of all True values -> all inside points
            # random.choice() picks one random index
            # points[...] fetches that coordinate
            # point = [random_longtitude, random_latitude]
            point = points[random.choice(list(np.where(grid)[0]))]

            print(district, ' : ', point)
            district.randomLong = point[0]
            district.randomLat = point[1]

    def fetchCensus(self):
        """
        Fetches the census tract for each district in the list of districts using the FCC API.

        This method iterates over the all districts in `self.districts`, retrieves the census tract 
        for each district based on its random latitude and longitude, and updates the district's 
        `censusTract` attribute.

        Note
        ----
        The method fetches data from "https://geo.fcc.gov/api/census/area" and assumes that 
        `randomLat` and `randomLong` attributes of each district are already set.

        The function `fetch` is an internal helper function that performs the actual API request.

        In the api call, check if the response.status_code is 200.
        If not, it might indicate the api call made is not correct, check your api call parameters.

        If you get status_code 200 and other code alternativly, it could indicate the fcc webiste is not 
        stable. Using a while loop to make anther api request in fetch function, until you get the correct result. 

        Important
        -----------
        The order of the API call parameter has to follow the following. 
        'lat': xxx,'lon': xxx,'censusYear': xxx,'format': 'json' Or
        'lat': xxx,'lon': xxx,'censusYear': xxx
        """

        url = 'https://geo.fcc.gov/api/census/area'

        # fetch: internal helper function that actually make the API call
        def fetch(lat, lon, censusYear):
            params = {
                'lat': lat,
                'lon': lon,
                'censusYear': censusYear
            }
            while True:
                try:
                    response = requests.get(url, params = params)
                    
                    if response.status_code == 200:
                        return response.json()
                    else:
                        print('Retrying...')

                except Exception as e:
                    print('Error fetching data: ', e)

        for district in self.districts:

            lat = district.randomLat
            lon = district.randomLong
            data = fetch(lat, lon, 2010)

            if 'results' in data and len(data['results']) > 0:
                # get the census tract number (middle 6 digits)
                block_fips = data['results'][0]['block_fips']
                tract = block_fips[2:11]
                # print(f'{district.id} Census Tract: ', block_fips)

                # assign such tract code to the attribute of the class object
                district.censusTract = tract
    
    def fetchIncome(self):
        """
        Retrieves the median household income for each district based on the census tract.

        This method requests income data from the ACS 5-Year Data via the U.S. Census Bureau's API 
        for the year 2018. It then maps these incomes to the corresponding census tracts and updates 
        the median income attribute of each district in `self.districts`.

        Note
        ----
        The method assumes that the `censusTract` attribute for each district is already set. It updates 
        the `medIncome` attribute of each district based on the fetched income data. If the income data 
        is not available or is negative, the median income is set to 0.
        """
        # API endpoint for getting median income
        url = 'https://api.census.gov/data/2018/acs/acs5'

        # from https://api.census.gov/data/2018/acs/acs5/variables.html
        # we know that the name of parameter is B19013_001E
        for district in self.districts:

            # get the state no., county no. and tract no
            state_no = 26
            county_no = district.censusTract[0:3]
            tract_no = district.censusTract[3:9]

            # params for api call
            params = {
                'get': 'B19013_001E',
                'for': f'tract:{tract_no}',
                'in': f'state:{state_no}+county:{county_no}',
                'key': '8fd15654d4868bb3efbed7d3d66ec710bbcbb8ce'
            }

            response = requests.get(url, params = params)
            data = response.json()

            # the data output would be [['B19013_001E', 'state', 'county', 'tract'], ['116583', '26', '125', '187000']]
            district.medIncome = int(data[1][0])

    def cacheData(self, fileName):
        """
        Saves the current state of district data to a file in JSON format.
        Using the __dict__ magic method on each district instance, and save the 
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.
        You should name the cache file as redlines_cache.json

        Parameters
        ----------
        filename : str
            The name of the file where the district data will be saved.
        """

        # get the directory where this script file is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # join that directory with file name
        json_file = os.path.join(script_dir, fileName)

        # converts objects to dictionary that can be serialized for json
        data_to_cache = [district.__dict__ for district in self.districts]

        # save to json
        with open(json_file, 'w', encoding = 'utf-8') as f:
            json.dump(data_to_cache, f, indent = 4)

    def loadCache(self, fileName):
        """
        Loads district data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the district data.
            You should name the cache file as redlines_cache.json

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        load_success = False

        # get the directory where this script file is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # join that directory with file name
        json_file = os.path.join(script_dir, fileName)

        # check whether the fileName exists in the folder
        # also check the fileName size is greater than 0
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            load_success = True
            with open(json_file, 'r', encoding = 'utf-8') as f:
                data_list = json.load(f)
            self.districts = [DetroitDistrict(**data) for data in data_list]

        return load_success

    def calcIncomeStats(self):
        """
        Use np.median and np.mean to
        Calculates the mean and median of median household incomes for each district grade (A, B, C, D).

        This method computes the mean and median incomes for districts grouped by their HOLC grades.
        The results are stored in a list following the pattern: [AMean, AMedian, BMean, BMedian, ...].
        After your calculations, you need to round the result to the closest whole int.
        Relate reading https://www.w3schools.com/python/ref_func_round.asp


        Returns
        -------
        list
            A list containing mean and median income values for each district grade in the order A, B, C, D.
        """
        grade_income = {'A': [], 'B': [], 'C': [], 'D': []}

        for district in self.districts:
            if district.medIncome and district.medIncome > 0:
                grade_income[district.holcGrade].append(district.medIncome)
        
        result = []

        for grade in ['A', 'B', 'C', 'D']:
            # [AMean, AMedian, BMean, BMedian, ...] list
            result.append(int(round(np.mean(grade_income[grade]))))
            result.append(int(round(np.median(grade_income[grade]))))
        
        return result

    def findCommonWords(self):
        """
        Analyzes the qualitative descriptions of each district category (A, B, C, D) and identifies the
        10 most common words unique to each category.

        This method aggregates the qualitative descriptions for each district category, splits them into
        words, and computes the frequency of each word. It then identifies and returns the 10 most 
        common words that are unique to each category, excluding common English filler words.

        Returns
        -------
        list of lists
            A list containing four lists, each list containing the 10 most common words for each 
            district category (A, B, C, D). The first list should represent grade A, and second for grade B,etc.
            The words should be in the order of their frequency.

        Notes
        -----
        - Common English filler words such as 'the', 'of', 'and', etc., are excluded from the analysis.
        - The method ensures that the common words are unique across the categories, i.e., no word 
        appears in more than one category's top 10 list.
        - Regular expressions could be used for word splitting to accurately capture words from the text.
        - Counter from collections could also be used.

        """
        filler_words = {
                        'the', 'of', 'and', 'a', 'in', 'is', 'are', 'to', 'for', 'on',
                        'this', 'but', 'there', 'that', 'it', 'at', 'as', 'be', 'by',
                        'from', 'an', 'or', 'so', 'with', 'was', 'were', 'have', 'has',
                        'had', 'not', 'do', 'does', 'did', 'if', 'then', 'than', 'which',
                        'who', 'whom', 'what', 'when', 'where', 'why', 'how', 'see', 'area'
                        }

        grade_word_frequency = {'A': Counter(), 'B': Counter(), 'C': Counter(), 'D': Counter()}

        # for this method, first use split to split the long string into several words
        # then use counter() from collections to count the freqeuncy of each word
        for district in self.districts:

            description = district.description.lower()
            cleaned = re.sub(r'[^\w\s]', '', description)
            cleaned_split_desc = cleaned.split()

            filtered_words = [w for w in cleaned_split_desc if w not in filler_words]

            grade_word_frequency[district.holcGrade].update(filtered_words)
            
        result = []

        for grade in ['A', 'B', 'C', 'D']:
            top_ten_word_count = grade_word_frequency[grade].most_common(10)
            top_ten_word = [word for word, count in top_ten_word_count]
            result.append(top_ten_word)

        return result

# ue main function to test your class implementations
# feel free to modify the example main function
def main():

    myRedLines = RedLines()
    print(myRedLines.createDistricts('redlines_data.json'))
    myRedLines.plotDistricts()
    myRedLines.generateRandPoint()
    myRedLines.fetchCensus()
    myRedLines.fetchIncome()
    '''
    myRedLines.calcRank()  # Assuming you have this method
    myRedLines.calcPopu()  # Assuming you have this method
    '''
    myRedLines.cacheData('redlines_cache.json')
    myRedLines.loadCache('redlines_cache.json')
    print(myRedLines.calcIncomeStats())
    print(myRedLines.findCommonWords())

if __name__ == '__main__':
    main()