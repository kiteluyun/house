#导入线性回归模型
from sklearn.linear_model import LinearRegression
import numpy as np
#编写基于线性回归模型预测的函数
#x自变量，y因变量，predict_value预测的新样本
def linear_model_main(x,y,predict_value):
    '''#1.创建模型'''
    regr = LinearRegression()
    #2.使用已有的数据训练当前的模型，fit().\方法
    regr.fit(x,y)
    #3.预测的新样本，需要进行格式化
    predict_value = np.array([predict_value]).reshape(-1,1)
    #[[6]],predict()方法里的x参数是数组或者矩阵
    predict_outcome = regr.predict(predict_value)
    #4.返回预测的结果
    return predict_outcome
#测试是否预测合理
if __name__ == '__main__':
    '''1.创建训练样本'''
    x_data = [[4],[8],[9],[8],[7],[12],[6],[10],[6],[9],[10],[6]]
    y_data = [9,20,22,15,17,23,18,25,10,20,20,17]
    #2.创建预测样本,代表投入的广告费
    predict_value = 8
    #3.通过样本的训练，预测投入的广告费，能返回多少销售额
    predict_outcome = linear_model_main(x_data,y_data,predict_value)
    print(predict_outcome[0])