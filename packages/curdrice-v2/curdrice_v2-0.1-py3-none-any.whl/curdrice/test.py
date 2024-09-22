from curdrice.models import *
import zipfile

import warnings
warnings.filterwarnings("ignore")

def regression_testing(dataset_path, target_variable, files, zip_name):
    def linear_regression_testing(dataset_path, target_variable, output_path, performance):
        r = Regression(dataset_path, target_variable, output_path, performance)
        x = r.linear_regression()
        metrics["LinearRegression"] = x["LinearRegression"]

    def lasso_regression_testing(dataset_path, target_variable, output_path, performance):
        r = Regression(dataset_path, target_variable, output_path, performance)
        x = r.lasso_regression()
        metrics["Lasso"] = x["Lasso"]

    def decision_tree_regressor_testing(dataset_path, target_variable, output_path, performance):
        r = Regression(dataset_path, target_variable, output_path, performance)
        x = r.decision_tree_regressor()
        metrics["DecisionTreeRegressor"] = x["DecisionTreeRegressor"]

    def random_forest_regressor_testing(dataset_path, target_variable, output_path, performance):
        r = Regression(dataset_path, target_variable, output_path, performance)
        x = r.random_forest_regressor()
        metrics["RandomForestRegressor"] = x["RandomForestRegressor"]

    def gradient_boosting_regressor_testing(dataset_path, target_variable, output_path, performance):
        r = Regression(dataset_path, target_variable, output_path, performance)
        x = r.gradient_boosting_regressor()
        metrics["GradientBoostingRegressor"] = x["GradientBoostingRegressor"]

    def zip_compile():
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in files:
                zipf.write(file)
        
    metrics = dict()
    def dataframe(metrics):
        data = []
        col = ['Model Name', 
           'Mean Absolute Error', 
           'Mean Absolute Percentage Error', 
           'Mean Squared Error', 
           'Root Mean Squared Error',             
           'Mean Squared Log Error', 
           'Root Mean Squared Log Error']
        
        for key in metrics.keys():
            model = key
            mae = metrics[key]['MAE']
            mape = metrics[key]['MAPE']
            mse = metrics[key]['MSE']
            rmse = metrics[key]['RMSE']
            msle = metrics[key]['MSLE']
            rmsle = metrics[key]['RMSLE']
            row = [model, mae, mape, mse, rmse, msle, rmsle]
            data.append(row)
                
        df = pd.DataFrame(data=data, columns=col)
        #df.to_csv("regression_metrics.csv", index=False)
        #table = tabulate(df, headers=col, tablefmt="grid")
        return df

    def result_regression():
        linear_regression_testing(dataset_path, target_variable, "LinReg.joblib", dict())
        lasso_regression_testing(dataset_path, target_variable, "Lasso.joblib", dict())
        decision_tree_regressor_testing(dataset_path, target_variable, "DTR.joblib", dict())
        random_forest_regressor_testing(dataset_path, target_variable, "RFR.joblib", dict())
        gradient_boosting_regressor_testing(dataset_path, target_variable, "GBR.joblib", dict())
        # table = dataframe(metrics)
        # print(table)
        df = dataframe(metrics)
        df.to_csv("Metrics.csv", index=False)

    result_regression()
    zip_compile()

def classification_testing(dataset_path, target_variable, files, zip_name):
    def logistic_regression_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.logistic_regression()
        metrics["LogisticRegression"] = x["LogisticRegression"]

    def naive_bayes_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.naive_bayes_classification()
        metrics["GaussianNB"] = x["GaussianNB"]
    
    def support_vector_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.support_vector_classification()
        metrics["SVC"] = x["SVC"]

    def decision_tree_classification_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.decision_tree_classification()
        metrics["DecisionTreeClassifier"] = x["DecisionTreeClassifier"]

    def random_forest_classification_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.random_forest_classification()
        metrics["RandomForestClassifier"] = x["RandomForestClassifier"]

    def gradient_boosting_classification_testing(dataset_path, target_variable, output_path, performance):
        r = Classification(dataset_path, target_variable, output_path, performance)
        x = r.gradient_boosting_classification()
        metrics["GradientBoostingClassifier"] = x["GradientBoostingClassifier"]

    def zip_compile():
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in files:
                zipf.write(file)

    metrics = dict()
    
    def dataframe(metrics):
        data = []
        col = ['Model Name', 
           'Accuracy Score', 
           'Precision Score', 
           'Recall Score', 
           'Jaccard Score',             
           'F1 Score']
        
        for key in metrics.keys():
            model = key
            a = metrics[key]['A']
            p = metrics[key]['P']
            r = metrics[key]['R']
            j = metrics[key]['J']
            f1 = metrics[key]['F1']
            row = [model, a, p, r, j, f1]
            data.append(row)
                
        df = pd.DataFrame(data=data, columns=col)
        #table = tabulate(df, headers=col, tablefmt="grid")
        return df

    def result_classification():
        logistic_regression_testing(dataset_path, target_variable, "LogReg.joblib", dict())
        naive_bayes_testing(dataset_path, target_variable, "NB.joblib", dict())
        support_vector_testing(dataset_path, target_variable, "SVC.joblib", dict())
        decision_tree_classification_testing(dataset_path, target_variable, "DTC.joblib", dict())
        random_forest_classification_testing(dataset_path, target_variable, "RFC.joblib", dict())
        gradient_boosting_classification_testing(dataset_path, target_variable, "GBC.joblib", dict())
        df = dataframe(metrics)
        df.to_csv("Metrics.csv", index=False)
        #print(table)

    result_classification()
    zip_compile()

def feature_selection_testing(dataset_path, feature_matrix, target_vector, features):
    def variance_threshold_selector_testing(dataset_path, feature_matrix, target_vector, features):
        fs = FeatureSelection(dataset_path, feature_matrix, target_vector)
        x = fs.variance_threshold_selector()
        features['variance threshold'] = x
        
    def chi_square_selector_testing(dataset_path, feature_matrix, target_vector, features):
        fs = FeatureSelection(dataset_path, feature_matrix, target_vector)
        x = fs.chi_square_selector()
        features['chi square'] = x
        
    def mutual_information_selector_testing(dataset_path, feature_matrix, target_vector, features):
        fs = FeatureSelection(dataset_path, feature_matrix, target_vector)
        x = fs.mutual_information_selector()
        features['mutual information'] = x

    def anova_selector_testing(dataset_path, feature_matrix, target_vector, features):
        fs = FeatureSelection(dataset_path, feature_matrix, target_vector)
        x = fs.anova_selector()
        features['anova'] = x

    features = dict()
    def result_feature_selction():
        variance_threshold_selector_testing(dataset_path, feature_matrix, target_vector, dict())
        chi_square_selector_testing(dataset_path, feature_matrix, target_vector, dict())
        mutual_information_selector_testing(dataset_path, feature_matrix, target_vector, dict())
        anova_selector_testing(dataset_path, feature_matrix, target_vector, dict())

        print(features)

    result_feature_selction()