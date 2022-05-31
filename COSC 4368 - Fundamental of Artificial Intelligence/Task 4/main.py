import pandas as pd

#I feel like there must be a better way to code this but i am tired

print('Reading csv file ...')
data=pd.read_csv('heart_failure_clinical_records_dataset.csv')
print('Generating Dataframes ...')

X = data.iloc[:,0:12]
y = data.iloc[:,12]

from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

linear_SVC_results = []
sigmoid_SVC_results = []
logistic_MLP_results = []
tanh_MLP_results = []

kf = KFold(10, shuffle=True)

print("Running SVC and MLP ...")

for train_index, test_index in kf.split(X):
    pipe = make_pipeline(StandardScaler(), SVC(kernel='linear'))
    pipe.fit(X.iloc[train_index,:], y.iloc[train_index])
    linear_SVC_results.append(pipe.score(X.iloc[test_index,:], y.iloc[test_index]))

    pipe = make_pipeline(StandardScaler(), SVC(kernel='sigmoid'))
    pipe.fit(X.iloc[train_index,:], y.iloc[train_index])
    sigmoid_SVC_results.append(pipe.score(X.iloc[test_index,:], y.iloc[test_index]))

    pipe = make_pipeline(StandardScaler(), MLPClassifier(activation='logistic', max_iter=2000))
    pipe.fit(X.iloc[train_index,:], y.iloc[train_index])
    logistic_MLP_results.append(pipe.score(X.iloc[test_index,:], y.iloc[test_index]))

    pipe = make_pipeline(StandardScaler(), MLPClassifier(activation='tanh', max_iter=2000))
    pipe.fit(X.iloc[train_index,:], y.iloc[train_index])
    tanh_MLP_results.append(pipe.score(X.iloc[test_index,:], y.iloc[test_index]))
    
print("Generating Result Statistics ...")

linear_SVC_mean = sum(linear_SVC_results)/len(linear_SVC_results)
sigmoid_SVC_mean = sum(sigmoid_SVC_results)/len(sigmoid_SVC_results)
logistic_MLP_mean = sum(logistic_MLP_results)/len(logistic_MLP_results)
tanh_MLP_mean = sum(tanh_MLP_results)/len(tanh_MLP_results)

linear_SVC_std = (sum([((x - linear_SVC_mean)**2) for x in linear_SVC_results]) / len(linear_SVC_results))**0.5
sigmoid_SVC_std = (sum([((x - sigmoid_SVC_mean)**2) for x in sigmoid_SVC_results]) / len(sigmoid_SVC_results))**0.5
logistic_MLP_std = (sum([((x - logistic_MLP_mean)**2) for x in logistic_MLP_results]) / len(logistic_MLP_results))**0.5
tanh_MLP_std = (sum([((x - tanh_MLP_mean)**2) for x in tanh_MLP_results]) / len(tanh_MLP_results))**0.5

print("linear_SVC_results: ", linear_SVC_results)
print("linear_SVC_mean: ", linear_SVC_mean)
print("linear_SVC_std: ", linear_SVC_std)
print("...")
print("sigmoid_SVC_results: ", sigmoid_SVC_results)
print("sigmoid_SVC_mean: ", sigmoid_SVC_mean)
print("sigmoid_SVC_std: ", sigmoid_SVC_std)
print("...")
print("logistic_MLP_results: ", logistic_MLP_results)
print("logistic_MLP_mean: ", logistic_MLP_mean)
print("logistic_MLP_std: ", logistic_MLP_std)
print("...")
print("tanh_MLP_results: ", tanh_MLP_results)
print("tanh_MLP_mean: ", tanh_MLP_mean)
print("tanh_MLP_std: ", tanh_MLP_std)
