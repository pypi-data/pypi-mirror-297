import numpy as np
import pandas as pd
import joblib
from tabulate import tabulate
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, mean_squared_log_error

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, jaccard_score, f1_score

from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, mutual_info_classif, f_classif, RFE
from mlxtend.feature_selection import ExhaustiveFeatureSelector

class Regression:
    def __init__(self, dataset_path, target_variable, output_path, performance):
        self.dataset_path = dataset_path
        self.target_variable = target_variable
        self.output_path = output_path
        self.performance = performance

    def load_dataset(self):
        try:
            dataset = pd.read_csv(self.dataset_path)
            return dataset
        
        except:
            print("Some error has occured")
            return None
    
    def preprocessing(self):
        dataset = self.load_dataset()
        if dataset is not None:
            X = dataset.drop(self.target_variable, axis=1)
            y = dataset[self.target_variable]

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
        
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        else:
            return
    
    def save_model(self, model):
        joblib.dump(model, self.output_path)

    def performance_evaluation(self, model_name, y_test, y_pred):
        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        msle = mean_squared_log_error(y_test, y_pred)
        rmsle = np.sqrt(msle)
        self.performance[model_name] = {'MAE': mae, 
                                        'MAPE': mape, 
                                        'MSE': mse, 
                                        'RMSE': rmse, 
                                        'MSLE': msle, 
                                        'RMSLE': rmsle}
        return self.performance
    

    def linear_regression(self):
        X_train, X_test, y_train, y_test = self.preprocessing()

        model = LinearRegression()
        model.fit(X_train, y_train)  
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("LinearRegression", y_test, y_pred)
        self.save_model(model)
        return perf
    
    def lasso_regression(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
        
        model = Lasso(selection='random', random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("Lasso", y_test, y_pred)
        self.save_model(model)
        return perf

    def decision_tree_regressor(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = DecisionTreeRegressor(criterion="friedman_mse", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("DecisionTreeRegressor", y_test, y_pred)
        self.save_model(model)
        return perf

    def random_forest_regressor(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = RandomForestRegressor(criterion="friedman_mse", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("RandomForestRegressor", y_test, y_pred)
        self.save_model(model)
        return perf

    def gradient_boosting_regressor(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = GradientBoostingRegressor(loss="huber", criterion="friedman_mse", random_state=42)
        model.fit(X_train, y_train) 
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("GradientBoostingRegressor", y_test, y_pred)
        self.save_model(model)
        return perf

class Classification:
    def __init__(self, dataset_path, target_variable, output_path, performance):
        self.dataset_path = dataset_path
        self.target_variable = target_variable
        self.output_path = output_path
        self.performance = performance
    
    def load_dataset(self):
        try:
            dataset = pd.read_csv(self.dataset_path)
            return dataset
        
        except FileNotFoundError:
            print("File {} not found".format(self.dataset_path))
            return None
        
        except:
            print("Some error has occured")
            return None
    
    def preprocessing(self):
        dataset = self.load_dataset()
        if dataset is not None:
            X = dataset.drop(self.target_variable, axis=1)
            y = dataset[self.target_variable]

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
        
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        else:
            return
    
    def save_model(self, model):
        joblib.dump(model, self.output_path)

    def performance_evaluation(self, model_name,  y_test, y_pred):
        acs = accuracy_score(y_test, y_pred)
        ps = precision_score(y_test, y_pred, average="weighted")
        rs = recall_score(y_test, y_pred, average="weighted")
        js = jaccard_score(y_test, y_pred, average="weighted")
        f1s = f1_score(y_test, y_pred, average="weighted")
        self.performance[model_name] = {'A': acs, 
                                        'P': ps, 
                                        'R': rs, 
                                        'J': js, 
                                        'F1': f1s}
        return self.performance

    def logistic_regression(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = LogisticRegression(multi_class="multinomial", solver="saga", class_weight="balanced", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("LogisticRegression", y_test, y_pred)
        self.save_model(model)
        return perf
        
    def naive_bayes_classification(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = GaussianNB()
        model.fit(X_train, y_train)    
        y_pred = model.predict(X_test)
        
        perf = self.performance_evaluation("GaussianNB", y_test, y_pred)
        self.save_model(model)
        return perf

    def support_vector_classification(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = SVC(degree=3, kernel="sigmoid", class_weight="balanced", decision_function_shape="ovr", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        perf = self.performance_evaluation("SVC", y_test, y_pred)
        self.save_model(model)
        return perf

    def decision_tree_classification(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = DecisionTreeClassifier(criterion="entropy", class_weight="balanced", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("DecisionTreeClassifier", y_test, y_pred)
        self.save_model(model)
        return perf

    def random_forest_classification(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = RandomForestClassifier(criterion="entropy", class_weight="balanced", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("RandomForestClassifier", y_test, y_pred)
        self.save_model(model)
        return perf
    
    def gradient_boosting_classification(self):
        X_train, X_test, y_train, y_test = self.preprocessing()
            
        model = GradientBoostingClassifier(criterion="friedman_mse", random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        perf = self.performance_evaluation("GradientBoostingClassifier", y_test, y_pred)
        self.save_model(model)
        return perf
        
class FeatureSelection:
    def __init__(self,feature_matrix,target_vector):
        self.X = feature_matrix
        self.y = target_vector
        
    def variance_threshold_selector(self):
        selector = VarianceThreshold()
        X_high_variance = selector.fit_transform(self.X)
        return X_high_variance
    
    def chi_square_selector(self):
        selector = SelectKBest(chi2)
        X_selected = selector.fit_transform(self.X, self.y)
        return X_selected
    
    def mutual_information_selector(self):
        selector = SelectKBest(mutual_info_classif)
        X_selected = selector.fit_transform(self.X, self.y)
        return X_selected
    
    def anova_selector(self):
        selector = SelectKBest(f_classif)
        X_selected = selector.fit_transform(self.X, self.y)
        return X_selected
    
    # def lasso_selector(self):
    #     model = Lasso()
    #     model.fit(self.X, self.y)
    #     selected_features = np.where(model.coef_ != 0)[0]
    #     return self.X[:, selected_features], selected_features
    
    '''
    def rfe_selector(self, X, y, n_features=5):
        model = RandomForestRegressor(criterion="friedman_mse", random_state=42)
        rfe = RFE(model, n_features_to_select=n_features)
        rfe.fit_transform(X, y)
        return rfe.ranking_
    
    def rfe_selector(self, X, y, n_features=5):
        model = RandomForestClassifier(criterion="entropy", random_state=42)
        rfe = RFE(model, n_features_to_select=n_features)
        rfe.fit_transform(X, y)
        return rfe.ranking_
    
    def efs_selector(self, X, y):
        model = RandomForestRegressor(criterion="friedman_mse", random_state=42)
        efs = ExhaustiveFeatureSelector(model, min_features=1, max_features=X.shape[1], scoring='neg_mean_squared_error', cv=5)
        efs = efs.fit(X, y)
        return efs.best_idx_
    
    def efs_selector(self, X, y):
        model = RandomForestClassifier(criterion="entropy", random_state=42)
        efs = ExhaustiveFeatureSelector(model, min_features=1, max_features=X.shape[1], scoring='neg_mean_squared_error', cv=5)
        efs = efs.fit(X, y)
        return efs.best_idx_
    '''