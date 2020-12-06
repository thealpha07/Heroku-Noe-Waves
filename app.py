from flask import Flask, flash , redirect, render_template , request, session, abort , Markup
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from time import sleep
import pyeeg
import pickle
# import warnings
from werkzeug.utils import secure_filename
import os


from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB



app = Flask(__name__)

app.secret_key = os.urandom(12)

final_ans_g = list()
length_g=0
name_g=""


def seizures():

	names = ["RFC"]


	clf_score = []
	#X_test=pickle.load(open("X_TEST.csv","rb"))
	print("hello")
	X_test=pd.read_csv("X_TEST.csv")

	# print("1111111111111111111111111111111")
	# print(X_test,"============================")
	# print("2222222222222222222222222222222222")
	# ans = pickle.load(open("Random Forest.h5",'rb'))
	# NN=pickle.load(open("Nearest Neighbors.h5",'rb'))
	final_ans=[]
	for i in names:
		ss='RFC.pkl'
		print(ss)
		model=pickle.load(open(ss,'rb'))
		ans=model.predict(X_test)
	

		print(ans)
		final_ans.append(ans)
		print(f"***********************{i}***********************")
		print(ans)
		print(f"Total Healthy : {sum([1 if i==0 else 0 for i in ans])}")
		print(f"Total Epileptic : {sum([1 if i==1 else 0 for i in ans])}")
		length=len(ans)
	return length,final_ans	








@app.route("/",methods=['GET','POST'])
def home():
	# seizures()
	# if request.methods=="POST"
	# print(request.form)
	# print(request.form['name'])
	return render_template("index_final.html")

@app.route("/sec",methods=['GET','POST'])
def sec():
	print("========================")
	print(request.form)
	print("dfdg")
	# print(request.files['file1'])
	session['name'] = request.form['name']
	global name_g 
	name_g=request.form['name']
	print(request.files)
	print("sd")
	# print(request.form['file'])	
	f = request.files['file']
	f.save("X_TEST.csv")
	# print("f",f)
	print("hi")

	# print(request.files["file1"])
	# print(request.files['file'])
	length,final_ans=seizures()
	print("end")
	# return "sdfsd"
	global final_ans_g
	final_ans_g=final_ans
	global length_g
	length_g=length
	# session['final_ans']=final_ans
	session['length']=length
	return render_template("dashboard_final.html",length=length,NN=final_ans[0],
	NN_h=sum([1 if i==0 else 0 for i in final_ans[0]]),
	NN_e=sum([1 if i==1 else 0 for i in final_ans[0]]),

	name=name_g)









if __name__ == "__main__":

    app.run()