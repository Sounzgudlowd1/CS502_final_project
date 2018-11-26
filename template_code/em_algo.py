from sklearn.naive_bayes import MultinomialNB
from get_data import get_data_tfidf
from sklearn.model_selection import train_test_split
import numpy as np

#get features
def get_params(mnb):
    model_params = mnb.class_log_prior_
    for elt in mnb.feature_log_prob_:
        model_params = np.concatenate((model_params, elt))
    return model_params

#get same data from the project, if you want to test just replace this line of code
X, y = get_data_tfidf('data-1_train.csv')

#set 80% of it to unlabelled
X_labelled, X_unlabelled, y_labelled, y_unlabelled = train_test_split(X, y, test_size = 0.8) #never use y_unlabelled, that's cheating

#train on labelled data only
mnb = MultinomialNB()
mnb.fit(X_labelled, y_labelled)
y_pred = mnb.predict(X_labelled)
print(np.sum(y_pred == y_labelled)/len(y_pred))


#now predict on unlabelled data, overwrites the original true labels
y_unlabelled = mnb.predict(X_unlabelled)

#make sure that order is unchanged so set X to the concatenation of labelled an unlabelled, same with y
X = np.concatenate((X_labelled, X_unlabelled))
y = np.concatenate((y_labelled, y_unlabelled))

#now do initial fitting on labelled and unlabelled data
mnb.fit(X, y)
params = get_params(mnb)

i = 1
while True:
    print(i)

    i += 1

    #reset label for the unlabelled data
    y_unlabelled = mnb.predict(X_unlabelled)

    #re concatenate for y, no need to do this again for X
    y = np.concatenate((y_labelled, y_unlabelled))

    #re fit
    mnb = MultinomialNB()
    mnb.fit(X, y)

    #get new param set
    new_params = get_params(mnb)

    #get the sum of absolute differences of the model parameters
    diff = np.sum(abs(new_params - params))
    print(diff) #print it for fun
    params = new_params  #set the current model params to the new model params
    if diff < 0.001:  #and break if gap is small enough
        break

y_pred = mnb.predict(X_labelled)
print(np.sum(y_pred == y_labelled)/len(y_pred))
