import time
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, AdaBoostClassifier, \
    GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from xgboost import XGBClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


data = pd.read_csv('dataset_halfSecondWindow.csv', index_col=0)
data.drop(columns=['id','activityrecognition#0', 'activityrecognition#1', 'time'] ,inplace=True, axis=1)


features = ['target', 'user', 'android.sensor.accelerometer#mean', 'android.sensor.accelerometer#min', 'android.sensor.accelerometer#max', 'android.sensor.accelerometer#std',
            'android.sensor.gyroscope#mean', 'android.sensor.gyroscope#min', 'android.sensor.gyroscope#max', 'android.sensor.gyroscope#std',
            'sound#mean', 'sound#max', 'sound#min', 'sound#std']


#prueba: quitar lo que no son means
for feature in data.columns.to_list():
    if feature in features:
        pass
    else:
        data.drop(columns=[feature], inplace=True, axis=1)


seeds=[42]#, 42, 100]
for seed in seeds:
    X, y = data.drop('target', axis=1),data['target']
    # split teniendo en cuenta los users
    gs = GroupShuffleSplit(n_splits=2, train_size=.8, random_state=seed)
    train_ix, test_ix = next(gs.split(X, y, groups=X.user))
    train = data.loc[train_ix]
    test = data.loc[test_ix]

    X_train, y_train = train.drop('target', axis=1), train['target']
    X_train = X_train.drop('user', axis=1)

    for var in X_train.columns.to_list():
        X_train[var] = X_train[var].fillna(X_train[var].mean())
        #X_train[var] = data.groupby("target").transform(lambda x: x.fillna(x.mean()))[[var]]



    test = test[train.columns.to_list()]
    for var in X_train.columns.to_list():
        '''
        if test[var].isnull().sum()/test.shape[0] > 0.8:
            test[col] = test[col].fillna(X_train[col].median())
        else:
            test[col] = test[col].fillna(test[col].median())
        '''
        test[var] = test[var].fillna(X_train[var].mean())
    X_test, y_test = test.drop('target', axis=1), test['target']
    X_test = X_test.drop('user', axis=1)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    '''
    lda = LinearDiscriminantAnalysis()
    X_train_lda = lda.fit(X_train_scaled, y_train).transform(X_train_scaled)
    X_test_lda = lda.transform(X_test_scaled)
    '''

    tree_classifiers = {
        "Decision Tree": DecisionTreeClassifier(random_state=seed),
        "Extra Trees": ExtraTreesClassifier(random_state=seed,n_estimators=100),
        "Random Forest": RandomForestClassifier(random_state=seed,n_estimators=100),
        #"AdaBoost": AdaBoostClassifier(random_state=seed,n_estimators=100),
        #"Skl GBM": GradientBoostingClassifier(random_state=42,n_estimators=100),
        #"Skl HistGBM": HistGradientBoostingClassifier(random_state=seed,max_iter=100),
        #"XGBoost": XGBClassifier(random_state=seed,n_estimators=100),
        #"LightGBM": LGBMClassifier(random_state=seed,n_estimators=100),
        #"CatBoost": CatBoostClassifier(random_state=seed,n_estimators=100, verbose=False),
    }

    locals()["results_" + str(seed)] = pd.DataFrame({'Model': [], 'Accuracy': [], 'Bal Acc.': [], 'Time': []})
    for model_name, model in tree_classifiers.items():
        start_time = time.time()
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        total_time = time.time() - start_time
        locals()["results_" + str(seed)]  = locals()["results_" + str(seed)] .append({"Model": model_name,
                                  "Accuracy": metrics.accuracy_score(y_test, y_pred) * 100,
                                  "Bal Acc.": metrics.balanced_accuracy_score(y_test, y_pred) * 100,
                                  "Time": total_time},
                                 ignore_index=True)
        print(f'{seed}:{model} done in {total_time}')

print('jaja')