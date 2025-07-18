import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
# from sklearn.inspection import plot_partial_dependence
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_gaussian_quantiles
from sklearn.metrics import mean_squared_error  # 均方误差
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
from sklearn.model_selection import train_test_split
from sklearn import metrics
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from collections import Counter
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.inspection import permutation_importance
import pickle
import shap
from sklearn.metrics import roc_curve, auc
import matplotlib.cm as cm


def calc_metrics(y_test, preds):
    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds)
    recall = recall_score(y_test, preds)
    f1score = f1_score(y_test, preds)
    print(accuracy, precision, recall, f1score)
    return (accuracy, precision, recall, f1score)


def model_predict(model, x_train, y_train, x_test, y_test):
    model = model.fit(x_train, y_train)
    y_predict_train = model.predict(x_train)
    y_predict_test = model.predict(x_test)
    return accuracy_score(y_predict_train, y_train), accuracy_score(y_predict_test, y_test), y_predict_test


def sort_feature(feature_names, feature_vals):
    assert len(feature_names) == len(feature_vals)
    x_and_y = [(x, y) for x, y in zip(feature_names, feature_vals)]
    x_and_y.sort(key=lambda x: -x[1])
    return [item[0] for item in x_and_y], [item[1] for item in x_and_y]


def get_feature_importance(model, x_test, y_test):
    perm_importance = permutation_importance(model, x_test, y_test)
    perm_sorted_idx = perm_importance.importances_mean.argsort()
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(x_test)
    return (model.feature_importances_, perm_sorted_idx, shap_values)


def machine_learning(x, y, split_ratio=0.3, random_seed=28):
    # 训练集、测试集划分
    # 归一化 z-score标准化 (df - df.mean()) / df.std()
    x = (x - x.mean()) / x.std()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=split_ratio, random_state=random_seed,
                                                        shuffle=True)

    print("train size: {}, test size {} ".format(len(x_train), len(x_test)))

    def get_feature_importance(model):
        try:
            return model.feature_importances_
        except AttributeError:
            return None

    map = {}
    # 逻辑回归
    print("开始训练逻辑回归。。。")
    time1 = time.time()
    lr_model = LogisticRegression()
    score_train, score_test, y_predict_test = model_predict(lr_model, x_train, y_train, x_test, y_test)
    y_pred_proba = lr_model.predict_proba(x_test)[:, 1]
    map['Logistic Regression'] = (
    score_train, score_test, get_feature_importance(lr_model), lr_model, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    # 朴素贝叶斯
    print("开始训练朴素贝叶斯。。。")
    time1 = time.time()
    nb_model = GaussianNB()
    score_train, score_test, y_predict_test = model_predict(nb_model, x_train, y_train, x_test, y_test)
    y_pred_proba = nb_model.predict_proba(x_test)[:, 1]
    map['Naive Bayes'] = (score_train, score_test, get_feature_importance(nb_model), nb_model, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    # 决策树
    print("开始训练决策树。。。")
    time1 = time.time()
    dt_model = tree.DecisionTreeClassifier()
    score_train, score_test, y_predict_test = model_predict(dt_model, x_train, y_train, x_test, y_test)
    y_pred_proba = dt_model.predict_proba(x_test)[:, 1]
    map['Decision Tree'] = (score_train, score_test, get_feature_importance(dt_model), dt_model, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    # 随机森林
    print("开始训练随机森林。。。")
    time1 = time.time()
    rf_model = RandomForestClassifier()
    score_train, score_test, y_predict_test = model_predict(rf_model, x_train, y_train, x_test, y_test)
    y_pred_proba = rf_model.predict_proba(x_test)[:, 1]
    map['Random Forest'] = (score_train, score_test, get_feature_importance(rf_model), rf_model, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    # K近邻
    print("开始训练最慢的K近邻，大概需要40min+。。。")
    time1 = time.time()
    kn_model = KNeighborsClassifier()
    score_train, score_test, y_predict_test = model_predict(kn_model, x_train, y_train, x_test, y_test)
    y_pred_proba = kn_model.predict_proba(x_test)[:, 1]
    map['KNN'] = (score_train, score_test, get_feature_importance(kn_model), kn_model, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    # LightGBM
    print("开始训练LightGBM。。。")
    time1 = time.time()
    gbm = lgb.LGBMClassifier(random_state=random_seed)
    score_train, score_test, y_predict_test = model_predict(gbm, x_train, y_train, x_test, y_test)
    y_pred_proba = gbm.predict_proba(x_test)[:, 1]
    # map[random_seed] = (score_train, score_test, get_feature_importance(gbm), gbm)
    # y_pred_train = gbm.predict(x_train)
    # y_pred = gbm.predict(x_test)
    map['LightGBM'] = (score_train, score_test, get_feature_importance(gbm), gbm, y_test, y_pred_proba)
    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    calc_metrics(y_test, y_predict_test)

    #    # SVM
    #    print("开始训练最慢的SVM，大概需要7Hour+。。。")
    #    svm = SVC(probability=True)
    #    score_train, score_test, y_predict_test = model_predict(svm, x_train, y_train, x_test, y_test)
    #    y_pred_proba = svm.predict_proba(x_test)[:,1]
    #    ressult_map['SVM'] = (score_train, score_test, get_feature_importance(svm), svm, y_test, y_pred_proba)
    #    print("用时：{}s  训练集得分:{}  测试集得分:{}".format(time.time() - time1, score_train, score_test))
    #    calc_metrics(y_test, y_predict_test)
    #    f=open('./svm.pkl','wb')
    #    pickle.dump(svm,f)
    #    f.close()

    return map


result_map = {}

# 导入数据
df = pd.read_csv('./bc328.csv')
# 控制变量，例如 gender==0或age>=10等，需要控制变量的话把下一行的#删掉
# df = df.loc[df['gender']==0]
# 自变量
df_src = df[['gender', 'age', 'minzu', 'siblings', 'bo', 'BMI', 'shs', 'sfsc', 'sssc', 'OBSES', 'chat',
             'friends', 'care1', 'care2', 'care3', 'care4', 'care5', 'care6', 'care7', 'care8', 'care0',
             'grade', 'Sregion', 'careBIN', 'Stype', 'drink', 'smoke', 'fedu', 'medu', 'ecBIN',
             'ecf', 'ec0', 'eat1', 'eat2', 'eat3', 'eat4', 'eat5', 'eat6', 'eat7', 'eat8', 'eat9',
             'ST', 'sport', 'screen', 'game', 'video', 'book', 'hos1', 'hos2', 'myopia', 'education']].astype(float)
# 因变量
df_tgt = df[['traditional_any_alt']]
print("Data prepare done")

oversample = SMOTE()
X, Y = oversample.fit_resample(df_src, df_tgt)
print("Oversample done")

# 跑的次数
for i in range(1):
    result_map[i] = machine_learning(X, Y, random_seed=i)
