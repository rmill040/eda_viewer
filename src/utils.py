# -*- coding: utf-8 -*-

# Import libraries from api
from utils_api import *


######################
"""HELPER FUNCTIONS"""
######################

class UiLoader(QUiLoader):
    """ADD DESCRIPTION"""
    def __init__(self, base_instance):
        QUiLoader.__init__(self, base_instance)
        self.base_instance = base_instance


    def createWidget(self, class_name, parent=None, name=''):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        if parent is None and self.base_instance:
            return self.base_instance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.base_instance: setattr(self.base_instance, name, widget)
            return widget


def load_ui(ui_file, base_instance=None):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    loader = UiLoader(base_instance)
    widget = loader.load(ui_file)
    QMetaObject.connectSlotsByName(widget)
    return widget


def get_model(model_name, model_type):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    models = {
        'Classification': {
            'Random Forests':         RandomForestClassifier,
            'K-Nearest Neighbors':    KNeighborsClassifier,
            'Support Vector Machine': SVC,
            'Neural Network':         MLPClassifier,
            'Gaussian Process':       GaussianProcessClassifier,
            'Linear Model':           LogisticRegression,
            'Extra Trees':            ExtraTreesClassifier,
            'Gradient Boosting':      GradientBoostingClassifier,
            'Decision Tree':          DecisionTreeClassifier
        },
        'Regression': {
            'Random Forests':         RandomForestRegressor,
            'K-Nearest Neighbors':    KNeighborsRegressor,
            'Support Vector Machine': SVR,
            'Neural Network':         MLPRegressor,
            'Gaussian Process':       GaussianProcessRegressor,
            'Linear Model':           LinearRegression,
            'Extra Trees':            ExtraTreesRegressor,
            'Gradient Boosting':      GradientBoostingRegressor,
            'Decision Tree':          DecisionTreeRegressor
            },
        'Clustering': {
            'K-Means':       KMeans,
            'DBSCAN':        DBSCAN,
            'Agglomerative': AgglomerativeClustering
        }
    }

    return models[model_type][model_name]()


def pretty_print_dict(model_params):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    if 'pooling_func' in model_params.keys(): 
        model_params = {k:v for k,v in model_params.items() if k != 'pooling_func'}

    return json.dumps(model_params, indent=4)


def text_to_dict(model_params):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    return json.loads(model_params)


def message_box(message, informativeText, type, question=False):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # TODO: ADD DETAILED TEXT WITH TRACEBACKS AND EXCEPTION CATCHING
    msg = QMessageBox()
    msg.setText(message)
    msg.setInformativeText(informativeText)

    if type == "warning":
        msg.setIcon(QMessageBox.Warning)
    elif type == "error":
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)

    if question:
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        return msg.exec_() # Return messagebox 
    else:
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def univariate_statistics(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    results = OrderedDict()
    if 'int' in str(data.dtypes) or 'float' in str(data.dtypes):
        results['Mean']     = np.mean(data)
        results['Median']   = np.median(data)
        results['Variance'] = np.var(data)
        results['SD']       = np.std(data)
        results['Skewness'] = ss.skew(data)
        results['Kurtosis'] = ss.kurtosis(data)
        results['CV']       = results['SD']/results['Mean']
        results['Minimum']  = np.min(data)
        results['Maximum']  = np.max(data)
        results['P 0.5%']   = np.percentile(data, 0.5)
        results['P 2.5%']   = np.percentile(data, 2.5)
        results['P 25%']    = np.percentile(data, 25)
        results['P 75%']    = np.percentile(data, 75)
        results['P 97.5%']  = np.percentile(data, 97.5)
        results['P 99.5%']  = np.percentile(data, 99.5)
        results['IQR']      = results['P 75%'] - results['P 25%']

    else:
        results['Unique']  = len(np.unique(data))
        results['Mode']    = ss.mode(data)[0]
        results['Minimum'] = np.min(data)
        results['Maximum'] = np.max(data)

    return results


def is_numeric(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    if 'int' in str(data.dtypes) or 'float' in str(data.dtypes):
        return 1
    else:
        return 0


def value_counts_grouped(data, value_counts):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # Calculate counts and bins
    counts, bins  = np.histogram(data, bins='doane')
    n_bins        = len(bins)

    # Create grouped frequency table
    index, values = [], []
    for i in xrange(n_bins-1):

        # Last interval is closed
        if i == (n_bins-2):
            index.append('[{:.3f}, {:.3f}]'.format(bins[i], bins[i+1]))
        
        # Other intervals are half-open (open to left, closed to right)
        else:
            index.append('[{:.3f}, {:.3f})'.format(bins[i], bins[i+1]))
        
        values.append(counts[i])

    return pd.DataFrame(values, columns=['Count'], index=index)


def unsupervised_ml(X, model):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # Fit model, make class predictions, calculate clustering metrics
    y_pred  = model.fit_predict(X)
    scores  = [silhouette_score(X, y_pred), calinski_harabaz_score(X, y_pred)]

    return y_pred, scores


def supervised_ml(X, y, model, model_type):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # Define cross-validation generator
    y_pred, scores = np.zeros(y.shape), np.zeros(N_SPLITS)
    if model_type == 'Regression':
        cv_generator = KFold(n_splits=N_SPLITS, shuffle=True).split(X)
    else:
        cv_generator = StratifiedKFold(n_splits=N_SPLITS, shuffle=True).split(X, y)

    # Iterate over train, test splits
    fold = 0
    for train_idx, test_idx in cv_generator:
        
        # Separate into train/test and features/labels
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Standardize data
        scaler          = StandardScaler().fit(X_train)
        X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

        # Train and make predictions
        model.fit(X_train, y_train)
        y_pred[test_idx] = model.predict(X_test)

        # Calculate score
        if model_type == 'Regression':
            scores[fold] = mean_squared_error(y_test, y_pred[test_idx])
        else:
            scores[fold] = accuracy_score(y_test, y_pred[test_idx])

        fold += 1

    # Return predictions
    return y_pred, scores


def model_metrics(y_true, y_pred, model_type):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    pass


def get_spaced_colors(n, offset):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    max_value = 16581375 # 255**3
    interval  = int(max_value / float(n + offset*10))
    colors    = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
    for i in colors: yield [(int(i[:2], 16)/float(255), 
                             int(i[2:4], 16)/float(255), 
                             int(i[4:], 16)/float(255))]


def check_for_categorical_label(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    return np.sum(pd.value_counts(data) >= N_SPLITS)


def tablewidgets_to_dataframes(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # Hold all dataframes
    dfs = {}

    # Iterate over each table
    for col_name, table in data.iteritems():
        n, df = table.rowCount(), {}
        for row in xrange(n): df[str(table.item(row, 0).text())] = [float(table.item(row, 1).text())]
        
        # Make a column vector with variable named based on specified key
        df = pd.DataFrame(df).T
        df.columns = [col_name]
        dfs[col_name] = df

    # Return dataframes
    return dfs
