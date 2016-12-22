# Relevant categories
significant_categories = [
	"Bars", "Fast Food", "Pizza", "Coffee", "Burgers",
	"Bakeries", "Ice Cream", "Desserts", "Delis", 
	"Barbeque", "Steak", "American", "Italian", 
	"Mexican", "Chinese", "Japanese", "Thai", 
	"Indian", "Korean"
]

num_categories = len(significant_categories)

f = open('test.txt', 'r+')
for line in f.readlines():
	# Remove '\r\n'
	line = line[:-2]
	# Only Food options
	if 'Restaurants' in line or 'Food' in line:
		my_categories = line.split(';')
		# Vector of size num_categories
		my_vector = [0] * num_categories
		# Loop through my categories
		for my_category in my_categories: 
			for i, category in enumerate(significant_categories):
				# Found match in relevant categories
				if my_category == category:
					my_vector[i] = 1
		print my_vector