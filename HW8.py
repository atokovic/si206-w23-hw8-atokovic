# Your name: Azra Tokovic
# Your student id: 16880262
# Your email: atokovic@umich.edu
# List who you have worked with on this homework: Dylan Heiss

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    info = cur.execute('SELECT r.name, c.category, b.building, r.rating FROM restaurants r JOIN categories c ON r.category_id = c.id JOIN  buildings b ON r.building_id = b.id').fetchall()
    final_dct = {}
    for tup in info:
        final_dct[tup[0]] = {"category":tup[1],"building":tup[2],"rating":tup[3]}
    return final_dct

def plot_rest_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    info = cur.execute("SELECT c.category, COUNT(c.category) FROM restaurants r JOIN categories c ON r.category_id = c.id GROUP BY category").fetchall()
    final_dct = {}
    for tup in info:
        final_dct[tup[0]] = tup[1]
    
    sorted_dct = sorted(final_dct.items(), key=lambda x:x[1], reverse=False)
    converted_dct = dict(sorted_dct)

    restants = list(converted_dct.keys())
    count_num = list(converted_dct.values())

    fig = plt.figure(figsize = (10, 4))
    plt.barh(restants, count_num)
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Type of Restaurants")
    plt.title("Type and Number of Restaurants on South University Avenue")
    plt.tight_layout()
    plt.show()
    plt.savefig("South_U_Restaurants_Chart.png")

    return final_dct
    
def find_rest_in_building(building_num, db_filename):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    info = cur.execute(f"SELECT r.name, r.rating FROM restaurants r JOIN buildings b ON r.building_id = b.id WHERE b.building = {building_num}").fetchall()
    sorted_tups = sorted(info, key=lambda x:x[1], reverse=True)
    final_lst = []
    for tup in sorted_tups:
        final_lst.append(tup[0])
    return final_lst

#EXTRA CREDIT
def get_highest_rating(db_filename): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    category_info = cur.execute('SELECT c.category, ROUND(AVG(r.rating),1) FROM restaurants r JOIN categories c ON r.category_id = c.id GROUP BY category ORDER BY AVG(r.rating) ASC').fetchall()
    building_info = cur.execute('SELECT b.building, ROUND(AVG(r.rating),1) FROM restaurants r JOIN buildings b ON r.building_id = b.id GROUP BY building ORDER BY AVG(r.rating) ASC').fetchall()
   
    cat_dct = {}
    for tup in category_info:
        cat_dct[tup[0]] = tup[1]

    bld_dct = {}
    for tup in building_info:
        bld_dct[tup[0]] = tup[1]
    
    
    x = list(cat_dct.keys())
    y = list(cat_dct.values())
    plt.rcParams.update({'font.size': 5})
    plt.figure(figsize = (4, 4))
    plt.subplot(2, 1, 1)
    
    cat = plt.barh(x,y)
    plt.xlabel("Rating")
    plt.ylabel("Categories")
    plt.title("Average Rating of South U Restaurants by Category")
    
    
    plt.subplot(2, 1, 2)
    x = list(bld_dct.keys())
    y = list(bld_dct.values())
    new_x = []
    for num in x:
        new_x.append(str(num))
    bld = plt.barh(new_x,y)
    plt.xlabel("Rating")
    plt.ylabel("Buildings")
    plt.title("Average Rating of South U Restaurants by Building")
    plt.tight_layout()

    plt.show()
    plt.savefig("Average_Ratings.png")

    cat_tups = list(cat_dct.items())
    bld_tups = list(bld_dct.items())

    final = [cat_tups[-1],bld_tups[-1]]
    return final

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
