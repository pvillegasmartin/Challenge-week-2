import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics


def analysis_nulls(data):
    '''Find % of null values per feature with target clustering'''
    perc_nulls = pd.DataFrame((data.isnull().sum() / data.shape[0]).sort_index(ascending=False))
    for el in data['target'].unique():
        locals()["data_" + str(el)] = data[data['target'] == el]
        locals()["perc_nulls_" + str(el)] = (
                    locals()["data_" + str(el)].isnull().sum() / locals()["data_" + str(el)].shape[0]).sort_index(
            ascending=False)
        perc_nulls[str(el)] = locals()["perc_nulls_" + str(el)]
    return perc_nulls[perc_nulls[0]>0]

def sorting_nulls(data):
    '''Manage the null values in diferent ways:
        - Droping column if all targets has >79% of null values
        -
    '''
    perc_nulls = analysis_nulls(data)
    #deleting all features with more than 80% of null values over all clusters (targets)
    threshold = 0.75
    columns_to_delete = perc_nulls[(perc_nulls[0]>threshold) & (perc_nulls['Bus']>threshold) & (perc_nulls['Walking']>threshold) & (perc_nulls['Train']>threshold) & (perc_nulls['Car']>threshold) & (perc_nulls['Still']>threshold)]
    data.drop(columns=list(columns_to_delete.index), inplace=True, axis=1)
    perc_nulls = perc_nulls.loc[~perc_nulls.index.isin(columns_to_delete.index)]

    #deleting other columns
    columns_to_delete = ['android.sensor.step_counter#min', 'android.sensor.step_counter#max', 'speed#max', 'speed#min', 'android.sensor.rotation_vector#min', 'android.sensor.rotation_vector#max']
    data.drop(columns=columns_to_delete, inplace=True, axis=1)


    perc_nulls = analysis_nulls(data)
    for var in perc_nulls.index:
        data[var] = data[var] / data["time"]
        data[[var]] = data.groupby("target").transform(lambda x: x.fillna(x.mean()))[[var]]

    '''
    #adjusting features that depend on time
    data['android.sensor.step_counter#mean'] = data['android.sensor.step_counter#mean'] / data["time"]
    data['speed#mean'] = data['speed#mean'] / data["time"]
    data['android.sensor.rotation_vector#mean'] = data['android.sensor.rotation_vector#mean'] / data["time"]
    data['android.sensor.proximity#mean'] = data['android.sensor.proximity#mean'] / data["time"]
    data['android.sensor.pressure#mean'] = data['android.sensor.pressure#mean'] / data["time"]

    #adjusting features with mean
    for el in data['target'].unique():
        data[['android.sensor.step_counter#mean','speed#mean','sound#mean', 'android.sensor.rotation_vector#std', 'android.sensor.rotation_vector#mean', 'android.sensor.proximity#mean', 'android.sensor.pressure#mean']] = data.groupby("target").transform(lambda x: x.fillna(x.mean()))[['android.sensor.step_counter#mean', 'speed#mean','sound#mean', 'android.sensor.rotation_vector#std', 'android.sensor.rotation_vector#mean', 'android.sensor.proximity#mean', 'android.sensor.pressure#mean']]

    
    #fill with the mean of the main feature
    for el in data['target'].unique():
        data[['sound#min','sound#max','android.sensor.proximity#max', 'android.sensor.proximity#min']] = data.groupby("target").fillna(data[data['target']==el]['sound#mean'].mean())[['sound#min','sound#max','android.sensor.proximity#max', 'android.sensor.proximity#min']]
    '''

    #filling features that 0 means nothing for them
    #data[['speed#mean','speed#max']] = data[['speed#mean','speed#max']].fillna(0)


    #TODO ELIMINAR - sirve para ir modificando las columnas
    perc_nulls = analysis_nulls(data)

    columns_to_delete = ['time']
    data.drop(columns=columns_to_delete, inplace=True, axis=1)

    return data

def get_x_y (data):
    data.drop(columns=['id','activityrecognition#0', 'activityrecognition#1'] ,inplace=True, axis=1)
    data = sorting_nulls(data)
    #todo modificar los usuarios test
    x,y = data.drop('target', axis=1),data['target']
    return x,y

if __name__ == "__main__":
    data = pd.read_csv('dataset_halfSecondWindow.csv', index_col=0)
    X,y = get_x_y(data)
    #split teniendo en cuenta los users
    gs = GroupShuffleSplit(n_splits=2, train_size=.85, random_state=42)
    train_ix, test_ix = next(gs.split(X, y, groups=X.user))
    X_train = X.loc[train_ix]
    y_train = y.loc[train_ix]
    X_test = X.loc[test_ix]
    y_test = y.loc[test_ix]

    X_train, X_test = X_train.drop('user', axis=1), X_test.drop('user', axis=1)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    decision_tree = DecisionTreeClassifier(random_state=42)
    decision_tree.fit(X_train, y_train)
    y_pred = decision_tree.predict(X_test)
    print(metrics.accuracy_score(y_test, y_pred)*100)

    print('jaja')