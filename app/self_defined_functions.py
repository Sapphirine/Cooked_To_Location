import numpy as np
from random import shuffle
def MSE(list1, list2):
    mse = 0
    n = len(list1)
    for x,y in zip(list1, list2):
        mse += (x-y)**2
    mse = mse/n
    return(mse)

# get indices of the rows containing NaN values
def isNan(value):
    if isinstance(value, str):
        if value == "NaN" or value == "nan":
            return(True)
    elif isinstance(value, float):
        if np.isnan(value):
            return(True)
    return(False)
    
def removeNanRows(df):
    output = df.copy()
    for name in list(df.columns.values):
        rownames = list(output[name].index[output[name].apply(isNan)])
        rowindex = [list(output.index).index(x) for x in rownames]
        output = output.drop(output.index[rowindex])
    return(output)

# deal with categorical values, only one value in each cell
def vectorized(df, cols_names_ls):
    output = []
    for name in cols_names_ls:
        print(name)
        column = df[name].tolist()
        if str(column[0]) in ["TRUE", "FALSE"]:
            total = ["TRUE", "FALSE"]
        elif str(column[0]) in ["no", "paid", "free"]:
            total = ["no", "paid", "free"]
        elif str(column[0]) in ["1.0", "2.0", "3.0", "4.0"]:
            total = ["1.0", "2.0", "3.0", "4.0"]
        else:
            total = list(set(column))
        # for i in range(len(total)):
        #     print(total[i])
        features = []
        for value in column:
            feature = [0]*len(total)
            if value in total:
                feature[total.index(value)] = 1
            features.append(feature)
        output.append(features)
    return(np.column_stack(output))

# vectorize cuisine type
def cuisineVec(input_list):
    cuisines = ["Bars", "Fast Food", "Pizza", "Coffee", "Burgers", "Bakeries", "Ice Cream", "Desserts", "Delis", "Barbeque",
                "Steak", "American", "Italian", "Mexican", "Chinese", "Japanese", "Thai", "Indian", "Korean"]
    n = len(cuisines)
    output = []
    for obs in input_list:
        feature = [0]*n
        for cuisine in cuisines:
            if cuisine.lower() in str(obs).lower():
                feature[cuisines.index(cuisine)] = 1
        output.append(feature)
    return(output)

def trainTestSplit(n):
    indices = list(range(n))
    sector = int(0.2*n)
    train_index = []
    test_index = []
    shuffle(indices)
    for i in range(5):
        if i == 0:
            test_index.append(indices[i:i+sector])
            train_index.append(indices[i+sector:])
        else:
            test_index.append(indices[i*sector:i*sector+sector])
            train_index.append(indices[:i*sector-sector+2] + indices[i*sector+sector:])
    return([train_index, test_index])
