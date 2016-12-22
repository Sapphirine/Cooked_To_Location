import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from yelpDB import *

def histogram(query_output_2, query_str_ls):
	df = pd.DataFrame(query_output_2)
	name = "_".join(query_str_ls)
	name = "_".join(name.split("."))
	cwd = os.getcwd()
	file_name = '/static/images/hist/' + name + '.png'
	fig = plt.figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
	y_names = df[0].as_matrix()
	y_pos = np.arange(len(y_names))
	ratings = df[1].as_matrix()
	mmm = plt.barh(y_pos, ratings, align='center', alpha=0.4, color = sns.color_palette("Set2", 5))
	plt.yticks(y_pos, y_names)
	plt.xlabel('Rating')
	plt.xlim([0,6])
	plt.legend(mmm, ratings)
	fig.savefig(cwd + file_name)
	return file_name

##############  test  ##################
#db = minidatabase('../data/yelpDB')
#c = db.recommend_cuisines(lat = 40.3543266, long = -79.9007057)
#print(c[1])
#test = histogram(c[1], ["38.5213", "-79.9007057"])
#print(test)
#db.commit()
#db.close()

