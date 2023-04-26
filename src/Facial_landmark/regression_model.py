import numpy as np
import os.path as path
from Facial_landmark import read_data as RD
from scipy.stats import pearsonr
from sklearn.datasets import make_friedman2
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor


def create_regressionmodel():
    return Regressionmodel()


class Regressionmodel:
    def __init__(self) -> None:
        self.data_x = None
        self.data_y = None


    def get_data(self):
        """
        @brief: Using VIP dataset as an example
        @return:
            self.data_x: Landmarks(feature).
            self.data_y: BMI value(label)
        """
        rd = RD.create_readdata()
        two_up =  path.abspath(path.join(__file__ ,"../../../paper_data"))
        featpath = (two_up+ "/"+'VIP_G_lm.xlsx' )
        bmipath = (two_up + "/" +'VIP_G_BMI.xlsx')
        self.data_x = rd.read_landmark(lm_path=featpath)
        self.data_y = rd.read_bmi(bmi_path=bmipath)
        return self.data_x,self.data_y

    def SVR_mod(self,imgpath):
        """
        @brief: Use SVR to get BMI value
        @param: 
            imgpath: The path of the image that needs to be measured
        @return:
            img_y: Predicted value of BMI
        """
        rd = RD.create_readdata()
        img_x = rd.get_image_x(imgpath)
        if len(img_x) != 0:
            x,y = self.get_data()
            X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.1)
            regr = svm.SVR(kernel='linear')
            regr.fit(X_train, Y_train)
            img_y = regr.predict(img_x)
            return img_y
        else:
            return 0

    def GPR_mod(self,imgpath):
        rd = RD.create_readdata()
        img_x = rd.get_image_x(imgpath)
        if len(img_x) != 0:
            x,y = self.get_data()
            X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.1)
            kernel = DotProduct() + WhiteKernel()
            gp = GaussianProcessRegressor(kernel=kernel)
            gp.fit(X_train, Y_train.ravel())
            img_y = gp.predict(img_x)
            return img_y
        else:
            return 0

    def LSR_mod(self,imgpath):
        rd = RD.create_readdata()
        img_x = rd.get_image_x(imgpath)
        if len(img_x) != 0:
            x,y = self.get_data()
            X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.1)
            reg = linear_model.LinearRegression()
            reg.fit(X_train,Y_train.ravel())
            img_y = reg.predict(img_x)
            return img_y
        else:
            return 0
        
    def MLP_mod(self,imgpath):
        rd = RD.create_readdata()
        img_x = rd.get_image_x(imgpath)
        if len(img_x) != 0:
            x,y = self.get_data()
            X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.1)
            mlp = MLPRegressor(
                hidden_layer_sizes=(100,50,30), activation='relu',solver='adam',
                alpha=0.01,max_iter=500)
            
            mlp.fit(X_train,Y_train.ravel())
            img_y = mlp.predict(img_x)
            return img_y
        else:
            return 0

