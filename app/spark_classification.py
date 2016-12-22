
from pyspark import SparkContext
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.classification import NaiveBayesModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import SparseVector
import numpy as np
import pandas as pd
#import subprocess
#import os, tempfile, shutil, pickle
from self_defined_functions import *


# names = ['attributes_Delivery', 'attributes_Happy_Hour', 'attributes_Price_Range', "categories",
#         'attributes_Waiter_Service', 'attributes_Wi_Fi', "stars", "zip_code", "city", "state"]
class classification:
	def __init__(self):
		self.sc = SparkContext()

	def loadData(self):
		business = pd.read_csv("/Users/dd/Desktop/app_bda/data/business_clean_2.csv")
		subset_names = ['attributes_Delivery', 'attributes_Happy_Hour', 'attributes_Price_Range', "categories",
		                'attributes_Waiter_Service', 'attributes_Wi_Fi', "stars", "zip_code", "state"]
		subset_cate_names = ['attributes_Delivery', 'attributes_Happy_Hour', 'attributes_Price_Range',
		                	'attributes_Waiter_Service', 'attributes_Wi_Fi', "zip_code", "state"]
		subset = removeNanRows(business[subset_names])
		subset_label = subset["stars"].values
		subset_categorical = vectorized(subset, subset_cate_names)
		subset_cuisines = cuisineVec(subset["categories"])
		subset2 = subset.drop(subset_cate_names + ["stars", "categories"], axis=1)
		subset3 = np.column_stack([subset2, subset_categorical, subset_cuisines])
		return([subset_label, subset3])

	# model and predict
	def runModel(self, train_label, train_features, test_label, test_features):
		#sc = SparkContext()

		data = []
		for x,y in zip(train_label, train_features):
			data.append(LabeledPoint(x, y.tolist()))

		model = NaiveBayes.train(self.sc.parallelize(data))

		pred_stars = []
		for x in test_features:
			print(features)
			pred_stars.append(model.predict(x))

		print(list(zip(pred_stars, test_label)))

		#sc.stop()

		return(MSE(test_label.tolist(), pred_stars))

	# validate model
	def CVPrecision(self, labels, features):
		#sc = SparkContext()

		n = features.shape[0]
		indices = trainTestSplit(n)
		train_index = indices[0]
		test_index = indices[1]

		accuracy = []
		for i in range(5):
			accuracy.append(self.runModel(labels[train_index[i]], features[train_index[i]], labels[test_index[i]], features[test_index[i]]))
		print("Cross Validation MSE:", sum(accuracy)/len(accuracy))
		print(MSE([3.5]*n, labels.tolist()))

		#sc.stop()

	# train and save model
	def trainModel(self, labels, features):
		#sc = SparkContext()

		data = []
		for x,y in zip(labels, features):
			data.append(LabeledPoint(x, y.tolist()))
		model = NaiveBayes.train(self.sc.parallelize(data))
		path = "hdfs:///user/admin/spark"
		model.save(self.sc, path+"/final.model")

		#sc.stop()

	# vectorize new obs, input_ls must be in a fixed order
	# ['attributes_Delivery', 'attributes_Happy_Hour', 'attributes_Waiter_Service', 'attributes_Wi_Fi',
	# 'attributes_Price_Range', "categories", "zip_code", "state"]
	def vecInput(self, input_ls):
		output = [0]*312
		list1 = ["TRUE", "FALSE"]
		list2 = ["no", "paid", "free"]
		list3 = [1.0, 2.0, 3.0, 4.0]
		list4 =  ["Bars", "Fast Food", "Pizza", "Coffee", "Burgers", "Bakeries", "Ice Cream", "Desserts",
				"Delis", "Barbeque", "Steak", "American", "Italian", "Mexican", "Chinese", "Japanese", "Thai",
				"Indian", "Korean"]
		list5 = [1000000000.0, 3000000000.0, 29715.0, 5.0, 10.0, 85003.0, 85004.0, 89101.0, 29710.0, 85006.0,
				85008.0, 89102.0, 89104.0, 85007.0, 85012.0, 89108.0, 85014.0, 89110.0, 85016.0, 89109.0,
				85018.0, 89113.0, 85020.0, 89117.0, 85022.0, 89118.0, 85024.0, 89120.0, 85023.0, 85027.0,
				89119.0, 85029.0, 89121.0, 89123.0, 85032.0, 89128.0, 28202.0, 85034.0, 28204.0, 89130.0, 
				8203.0, 28205.0, 28207.0, 28209.0, 28210.0, 28211.0, 28212.0, 85044.0, 89142.0, 89139.0,
				28216.0, 28217.0, 85050.0, 89146.0, 89148.0, 85053.0, 85054.0, 89145.0, 89147.0, 89149.0,
				28226.0, 28227.0, 89156.0, 89152.0, 89158.0, 89169.0, 85073.0, 28244.0, 28206.0, 85085.0,
				85086.0, 89183.0, 28208.0, 20.0, 28262.0, 28263.0, 28269.0, 28270.0, 28273.0, 28277.0, 28278.0,
				2000000.0, 85120.0, 85122.0, 28214.0, 85128.0, 85132.0, 85138.0, 85139.0, 85142.0, 85143.0,
				15017.0, 85009.0, 200.0, 85013.0, 85201.0, 85202.0, 85203.0, 85204.0, 85205.0, 85206.0, 85207.0,
				85209.0, 85210.0, 85212.0, 85017.0, 85215.0, 85218.0, 85220.0, 85222.0, 85224.0, 85225.0, 85226.0,
				15209.0, 85233.0, 85234.0, 85021.0, 85236.0, 85239.0, 85242.0, 15104.0, 85248.0, 15106.0, 85250.0,
				85251.0, 100000000.0, 85254.0, 85255.0, 85253.0, 85257.0, 85258.0, 85259.0, 85260.0, 85256.0, 85262.0,
				15120.0, 20000.0, 15122.0, 85268.0, 85028.0, 53527.0, 53532.0, 15136.0, 85281.0, 85282.0, 85283.0,
				85284.0, 15221.0, 85286.0, 85031.0, 15235.0, 89103.0, 85295.0, 85296.0, 85033.0, 85298.0, 85297.0,
				85301.0, 53558.0, 85302.0, 85304.0, 85035.0, 53562.0, 85306.0, 85308.0, 85305.0, 85303.0, 85310.0,
				89107.0, 85037.0, 85323.0, 85324.0, 85326.0, 85040.0, 85331.0, 53590.0, 85335.0, 53593.0, 85338.0,
				85339.0, 85340.0, 85042.0, 85342.0, 15201.0, 85345.0, 15203.0, 15205.0, 15206.0, 15207.0, 89115.0,
				61801.0, 61802.0, 85354.0, 15212.0, 15211.0, 15213.0, 15215.0, 15216.0, 15217.0, 15218.0, 15219.0,
				15220.0, 28012.0, 15222.0, 85249.0, 15224.0, 85353.0, 15226.0, 15227.0, 61820.0, 15228.0, 85374.0,
				28027.0, 15232.0, 85048.0, 85378.0, 15234.0, 15236.0, 85381.0, 15238.0, 85382.0, 85383.0, 85051.0, 
				5377.0, 85379.0, 89122.0, 85390.0, 85392.0, 85395.0, 85396.0, 89002.0, 89005.0, 28078.0, 89129.0,
				61874.0, 89011.0, 89012.0, 89014.0, 89015.0, 15289.0, 89131.0, 89030.0, 53703.0, 28104.0, 53704.0,
				89032.0, 28105.0, 53705.0, 89031.0, 89135.0, 53711.0, 28106.0, 53713.0, 53714.0, 53715.0, 53716.0,
				53717.0, 53718.0, 53719.0, 89136.0, 2000.0, 29707.0, 89052.0, 29708.0, 53726.0, 28134.0, 89141.0,
				89074.0, 89081.0, 89084.0]
		list6 = ['SC', 'QC', 'EDH', 'WI', 'ON', 'AZ', 'NV', 'IL', 'PA', 'NC']

		
		# dilivery
		if input_ls[0] in list1:
			output[0+list1.index(input_ls[0])] = 1
		
		# happy hour
		if input_ls[1] in list1:
			output[2+list1.index(input_ls[1])] = 1

		# waiter
		if input_ls[2] in list1:
			output[4+list1.index(input_ls[2])] = 1

		# wifi
		if input_ls[3] in list2:
			output[6+list2.index(input_ls[3])] = 1

		# price
		if input_ls[4] in list3:
			output[9+list3.index(input_ls[4])] = 1

		# categories
		for cat in list4:
			if cat in input_ls[5]:
				output[13+list4.index(cat)] = 1

		# zip
		if input_ls[6] in list5:
			output[22+list5.index(input_ls[6])] = 1

		# state
		if input_ls[7] in list6:
			output[292+list6.index(input_ls[7])] = 1

		return(np.asarray([output]))


	# load model and predict
	def predict(self, features):
		#sc = SparkContext()

		path = "hdfs:///user/admin/spark"
		model = NaiveBayesModel.load(self.sc, path+"/final.model")
		pred_stars = []
		for x in features:
			pred_stars.append(model.predict(x))
		#sprint(pred_stars)
		#sc.stop()

		return(pred_stars)


	def stopSC(self):
		self.sc.stop()


clf = classification()


#data = clf.loadData()


#labels = data[0]
#features = data[1]
#print(features.shape)
#clf.CVPrecision(labels, features)

#clf.trainModel(labels, features)
#print("goodgoodgood")
#clf.predict(features)
input = ["TRUE", "FALSE", "TRUE", "free", 4.0, "coffee", 89084.0, "NY"]
features = clf.vecInput(input)
#print(features)
print("xxxxxxxxxxxx")
rating = clf.predict(features)
print(rating)
# input = ["TRUE", "FALSE", "TRUE", "free", 4.0, "coffee", 89084.0, "NC"]
# features = clf.vecInput(input)
# clf.predict(features)
# print("ooooooooooooooooooooo")
clf.stopSC()
print("done")



# print("Training accuracy:", MSE(pred_stars, subset_label))

# print(model.predict(np.array([1.0, 0.0])))
# print(model.predict(sc.parallelize([[1.0, 0.0]])).collect())

# sparse_data = [
# LabeledPoint(0.0, SparseVector(2, {1: 0.0})),
# LabeledPoint(0.0, SparseVector(2, {1: 1.0})),
# LabeledPoint(1.0, SparseVector(2, {0: 1.0}))
# ]

# model = NaiveBayes.train(sc.parallelize(sparse_data))
# print("classification result")
# print(model.predict(SparseVector(2, {1: 1.0})))
# print(model.predict(SparseVector(2, {0: 1.0})))

#path = "/Users/admin/Chenlu_files/Courses/Columbia/big_data/project/output"

# path = "hdfs:///user/admin/spark"
# subprocess.call(["hadoop", "fs", "-rm", "-f", path])
# model.save(sc, path+"/test.model")

# sameModel = NaiveBayesModel.load(sc, path+"/test.model")
# sameModel.predict(SparseVector(2, {0: 1.0})) == model.predict(SparseVector(2, {0: 1.0}))


