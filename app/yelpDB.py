import sqlite3
import csv
import os
import pandas as pd
import numpy as np
sqlite3.register_adapter(np.int64, lambda val: int(val))
sqlite3.register_adapter(np.float64, lambda val: float(val))
class EmptyError(Exception):
    pass
class minidatabase:
    def __init__(self, data_base):
        self._DBname = data_base + '.db'
        self.connection = sqlite3.connect(self._DBname,detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False,timeout = 10)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create_table(self,command):
        self.cursor.execute(command)

    def insert_into_table(self,command,p):
        self.cursor.execute(command,p)


    def query_show(self, command):
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        return result


    def query_all(self, command):
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return result


    def show_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        a = self.cursor.fetchall()
        if len(a) > 0:
            print([i[0] for i in a])
        else:
            raise EmptyError('The data base is empty!')

    def set_add(new):
        os.chdir(new)

    def commit(self):
        self.connection.commit()

    def initialize(self,path):
        # DROP table if exits
        self.cursor.execute('''DROP TABLE IF EXISTS review;''')
        self.cursor.execute('''DROP TABLE IF EXISTS business;''')
        # CREATE TABLES

        #-----------------------------------------------------------------------------
        # review table creation
        sql_command = '''
        CREATE TABLE review (
               business_id CHAR,
               date CHAR,
               review_id CHAR,
               stars INT,
               text CHAR,
               type CHAR,
               user_id CHAR,
               votes_cool INT,
               votes_funny INT,
               votes_useful INT);
        '''
        self.create_table(sql_command)
        print('review table set')

        sql_command = '''
        CREATE TABLE business (
            business_id CHAR,
            city CHAR,
            full_address CHAR,
            latitude FLOAT,
            longitude FLOAT,
            name CHAR,
            neighborhoods CHAR,
            review_count INT,
            stars FLOAT,
            state CHAR,
            type CHAR,
            zip_code INT,
            bars INT,
            fast_food INT,
            pizza INT,
            coffee INT,
            burgers INT,
            bakeries INT,
            ice_cream INT,
            desserts INT,
            delis INT,
            barbeque INT,
            steak INT,
            american INT,
            italian INT,
            mexican INT,
            chinese INT,
            japanese INT,
            thai INT,
            indian INT,
            korean INT);
        '''
        self.create_table(sql_command)
        print('Business table set')
        # -----------------------------------------------------------------------------
        #review table insert data
        review = pd.read_csv(path + '/yelp_academic_dataset_review.csv',encoding="utf8")
        command = '''
                    INSERT INTO review (
                    business_id,
                    date,
                    review_id,
                    stars,
                    text,
                    type,
                    user_id,
                    votes_cool,
                    votes_funny,
                    votes_useful) VALUES (?,?,?,?,?,?,?,?,?,?)
                    '''
        for i in zip(review['business_id'],
                     review['date'],
                     review['review_id'],
                     review['stars'],
                     review['text'],
                     review['type'],
                     review['user_id'],
                     review['votes_cool'],
                     review['votes_funny'],
                     review['votes_useful']):
            self.insert_into_table(command, i)
        print('review db set')
        del review

        #business table insert data
        business = pd.read_csv(path + '/yelp_academic_dataset_business.csv', encoding="utf8")
        command = '''
            INSERT INTO business (
            business_id,
            city,
            full_address,
            latitude,
            longitude,
            name,
            neighborhoods,
            review_count,
            stars,
            state,
            type,
            zip_code,
            bars,
            fast_food,
            pizza,
            coffee,
            burgers,
            bakeries,
            ice_cream,
            desserts,
            delis,
            barbeque,
            steak,
            american,
            italian,
            mexican,
            chinese,
            japanese,
            thai,
            indian,
            korean) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        for i in zip(
                business['business_id'],
                business['city'],
                business['full_address'],
                business['latitude'],
                business['longitude'],
                business['name'],
                business['neighborhoods'],
                business['review_count'],
                business['stars'],
                business['state'],
                business['type'],
                business['zip_code'],
                business['bars'],
                business['fast_food'],
                business['pizza'],
                business['coffee'],
                business['burgers'],
                business['bakeries'],
                business['ice_cream'],
                business['desserts'],
                business['delis'],
                business['barbeque'],
                business['steak'],
                business['american'],
                business['italian'],
                business['mexican'],
                business['chinese'],
                business['japanese'],
                business['thai'],
                business['indian'],
                business['korean']):
            self.insert_into_table(command, i)
        print('business db set')
        del business

# --------------------------------------------------------------





        #Test Query

#----------------------------------------------------------------
#queries
    def query_review(self):
        command = '''
                  SELECT *
                  FROM review
                  LIMIT 100
                  '''
        return self.query_show(command)

    def query_business(self):
        command = '''
                  SELECT zip_code, latitude, longitude
                  FROM business
                  LIMIT 100
                  '''
        return self.query_show(command)

    def query_with_cuisine(self, cuisine, zip_code = "null"):
        if zip_code == "null":
            command = '''
                      SELECT business_id, zip_code, latitude, longitude, review_count, stars
                      FROM business
                      WHERE \"{cuisine}\" = 1 AND zip_code BETWEEN 10000 AND 99999
                      '''.format(cuisine= cuisine)
        else:
            zip_upper = zip_code + 10
            zip_lower = zip_code - 10
            command = '''
                      SELECT business_id, zip_code, latitude, longitude, review_count, stars
                      FROM business
                      WHERE \"{cuisine}\" = 1 AND zip_code BETWEEN \"{zip_lower}\" AND \"{zip_upper}\"
                      '''.format(cuisine = cuisine, zip_lower = zip_lower, zip_upper = zip_upper)

        return self.query_all(command)

    # input restaurant_id, output info of it
    def extract_restaurant(self, business_id):
        command = '''
                  SELECT name, full_address, zip_code, latitude, longitude, review_count, stars
                  FROM business
                  WHERE business_id = \"{business_id}\" AND zip_code BETWEEN 10000 AND 99999
                  '''.format(business_id = business_id)
        return self.query_show(command)

    # return top 5 restaurants
    def most_popular(self, query_output):
        if len(query_output) == 0:
            return []
        n = len(query_output[0])
        output = []
        top5 = sorted(query_output, key=lambda x: x[n-1], reverse=True)[0:5]
        top5 = [x[0] for x in top5]
        for id in top5:
            output.append(self.extract_restaurant(id))
        
        return output

    # input query_output, recommend location
    def top_locations(self, query_output):
        zip_codes = list(set([x1 for (x0, x1, x2, x3, x4, x5) in query_output]))
        counts = []
        for zip_code in zip_codes:
            ave = 0
            stars = []
            for row in query_output:
                if row[1] == zip_code:
                    stars.append(row[5])
            ave = sum(stars)/len(stars)
            counts.append((zip_code, ave))

        top5 = sorted(counts, key=lambda x: x[1], reverse=True)[0:5]
        return top5

    # return top5 resturants and location zip_codes
    def metadata_from_cuisine(self, C_output):
        top5 = self.most_popular(C_output)
        recommend = self.top_locations(C_output)
        return [top5, recommend]

    # this is what you should call when you want recommended locations with cuisine type
    def recommend_locations(self, cuisine, zip_code = "null"):
        query_output = self.query_with_cuisine(cuisine, zip_code)

        return self.metadata_from_cuisine(query_output)

    def query_with_location(self, zip_code = "null", lat = "null", long = "null"):
        if zip_code == "null":
            lat_upper = lat + 6
            lat_lower = lat - 6
            long_upper = long + 6
            long_lower = long - 6
            command = '''
                      SELECT business_id, bars, fast_food, pizza, coffee, burgers, bakeries, ice_cream,
                            desserts, delis, barbeque, steak, american, italian, mexican, chinese, japanese,
                            thai, indian, korean, review_count, stars
                      FROM business
                      WHERE latitude BETWEEN \"{lat_lower}\" AND \"{lat_upper}\"
                      AND longitude BETWEEN \"{long_lower}\" AND \"{long_upper}\"
                      '''.format(lat_lower = lat_lower, lat_upper = lat_upper, long_lower = long_lower, long_upper = long_upper)
        else:
            zip_upper = zip_code + 1
            zip_lower = zip_code - 1
            command = '''
                      SELECT business_id, bars, fast_food, pizza, coffee, burgers, bakeries, ice_cream,
                            desserts, delis, barbeque, steak, american, italian, mexican, chinese, japanese,
                            thai, indian, korean, review_count, stars
                      FROM business
                      WHERE zip_code BETWEEN \"{zip_lower}\" AND \"{zip_upper}\"
                      '''.format(zip_lower = zip_lower, zip_upper = zip_upper)

        return self.query_all(command)
    
    # input query_output, recommend cuisines
    def top_cuisines(self, query_output):
        cuisines = ["bars", "fast_food", "pizza", "coffee", "burgers", "bakeries", "ice_cream", "desserts", "delis", "barbeque",
                    "steak", "american", "italian", "mexican", "chinese", "japanese", "thai", "indian", "korean"]
        counts = []
        for cuisine in cuisines:
            ave = 0
            stars = []
            index = cuisines.index(cuisine)
            for row in query_output:
                if row[1+index] == 1:
                    stars.append(row[21])
                    ave = sum(stars)/len(stars)
            counts.append((cuisine, ave))

        top5 = sorted(counts, key=lambda x: x[1], reverse=True)[0:5]
        return top5

    # return top5 resturants and location zip_codes
    def metadata_from_location(self, L_output):
        top5 = self.most_popular(L_output)
        recommend = self.top_cuisines(L_output)
        return [top5, recommend]


    # this is what you should call when you want recommended cuisines with location type
    def recommend_cuisines(self, zip_code = "null", lat = "null", long = "null"):
        query_output = self.query_with_location(zip_code = zip_code, lat = lat, long = long)
        

        return self.metadata_from_location(query_output)


#db = minidatabase('/data/yelpDB')
#db.initialize('../data/yelp_academic_dataset_review')
#db.show_tables()
#a = db.recommend_locations("bars", 85326)
#print(a)
#b = db.recommend_cuisines(85326)
#print(b)
#c = db.recommend_cuisines(lat = 40.3543266, long = -79.9007057)
#print(c)
#db.commit()
#db.close()






