import code
from distutils.debug import DEBUG
from email import message
import email
from operator import le
from time import time
from tkinter import ON
from flask import Flask, render_template, request, url_for, redirect, session,flash



import random
from pymongo import MongoClient

from datetime import date, datetime

# ...


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.secret_key = "testing"





client = MongoClient('localhost', 27017)
db = client.DSmentors

us = db.users
goal=db.goals
rl=db.reality
ab=db.about
skils=db.skills
q=db.test

@app.route('/', methods=('GET', 'POST'))
def welcome():
   return render_template('welcome.html')

@app.route('/analysisI', methods=('GET', 'POST'))
def analysisI():
   return render_template('analysisI.html')



@app.route('/register', methods=('GET', 'POST'))
def register():
   
    

    if request.method=='POST':
        
        name = request.form['nameup']
        email = request.form['emailup']
        password = request.form['passwordup']
        password2 = request.form['passwordup2']

        #if found in database showcase that it's found 
        
        email_found = us.find_one({"email": email})
        


        
        if email_found:
            message = 'This email already exists in database'
            return render_template('welcome.html', message=message)
       



        else:
            if password==password2:
                us.insert_one({'name': name, 'email': email,'password': password, })
                user_data = us.find_one({"email": email})
                new_email = user_data['email']
                return redirect('user_menu')
            else:
                message = 'the 2 passwords do not match '
                return render_template('welcome.html', message=message)

        
    
    




@app.route('/signin', methods=('GET', 'POST'))
def signin():
     
        
        if "email" in session:
            return redirect(url_for("user_menu"))
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

        

            
            email_found = us.find_one({"email": email})
            if email_found :
                email_val = email_found['email']
                passwordcheck = email_found['password']
                #encode the password and check if it matches
            
                
                
                if password==passwordcheck:
                    session["email"] = email_val
                    return redirect(url_for('user_menu'))
                    

                else:
                    
                    message = 'Wrong password'
                    return render_template('welcome.html', message=message)

          
        

            else:
                message = 'User not found'
                return render_template('welcome.html', message=message)

        return render_template('welcome.html')
      
       










@app.route('/user_menu', methods=('GET', 'POST'))
def user_menu():
    if request.method == "GET":
        ar=str(random.randint(1,15))
        # get the id of the note to edit
        quotes_found=q.find_one({'Num':ar})
        if quotes_found:
         return render_template('user_menu.html',quotes_found=quotes_found)
        else:
             message = 'Welcome to mentors office' 
             return render_template('user_menu.html',message=message)


   
    return render_template('user_menu.html')


@app.route('/goals', methods=('GET', 'POST'))
def goals():
   
   if "email" in session:
    acc_mail=session['email'] 
   else:
       return redirect('signin')
    
   emailInGoals=goal.find_one({"email": acc_mail})
   if emailInGoals:
    return redirect('editGoal')
   else:
    data = {}
    if request.method =='POST':
        
            data['email']= acc_mail
            data['exams_of'] = request.form['exams_of']
            data['desc'] = request.form['desc']
            lessons = request.form.getlist('lesson')
            data['lessons']=lessons
            goal.insert_one(data)
            return redirect('user_menu')
    

   return render_template('goals.html')

@app.route('/editGoal', methods=('GET', 'POST'))
def editGoal():
     if "email" in session:
       acc_mail=session['email'] 
     else:
       return redirect('signin')
    
     if request.method == "GET":

        # get the id of the note to edit
        goal_found=goal.find_one({'email':acc_mail})
        if goal_found:
            # direct to edit note page
         return render_template('editGoal.html',goal_found=goal_found)
        else:
            message='you have ot set any goals'
            return render_template('editGoal.html',message=message)


       
        

     elif request.method == "POST":

        #get the data of the note
       
     
       
       
        exams_of = request.form['exams_of']
        desc= request.form['desc']
        lessons = request.form.getlist('lesson')
       

        goal.update_one({'email':acc_mail},{"$set":{'exams_of':exams_of,'desc':desc,'lessons':lessons}})
        return redirect('user_menu')


       


     return render_template('editGoal.html')

@app.route('/reality', methods=('GET', 'POST'))
def reality():
     
   if "email" in session:
    acc_mail=session['email'] 
   else:
       return redirect('signin')
    
   emailInReal=rl.find_one({"email": acc_mail})
   if emailInReal:
    return redirect('editReality')
   else:
    real = {}
    if request.method =='POST':
        
            real['email']= acc_mail
            real['lastTime'] = request.form['lastTime']
            lessons = request.form.getlist('lesson')
            problems = request.form.getlist('problem')
            real['problems']=problems
            real['lessons']= lessons
            rl.insert_one(real)
            return redirect('user_menu')
    

   return render_template('reality.html')

@app.route('/editReality', methods=('GET', 'POST'))
def editReality():
     if "email" in session:
       acc_mail=session['email'] 
     else:
       return redirect('signin')
    
     if request.method == "GET":

        # get the id of the note to edit
        real_found=rl.find_one({'email':acc_mail})
        if real_found:
            # direct to edit note page
         return render_template('editReality.html',real_found=real_found)
        else:
            message='you have ot set any reality'
            return render_template('editReality.html',message=message)


       
        

     elif request.method == "POST":

        #get the data of the note
        
         lastTime = request.form['lastTime']
         lessons = request.form.getlist('lesson')
         problems = request.form.getlist('problem')
         
         rl.update_one({'email':acc_mail},{"$set":{'lastTime':lastTime,'lessons':lessons,'problems':problems}})
         return redirect('user_menu')

     return render_template('editReality.html')



@app.route('/aboutyou', methods=('GET', 'POST'))
def aboutyou():
      if "email" in session:
         acc_mail=session['email'] 
      else:
       return redirect('signin')
    
      emailInabout=ab.find_one({"email": acc_mail})
      if emailInabout:
            return redirect('editabout')
      else:
            about = {}
            if request.method =='POST':
                
                    about['email']= acc_mail
                    about['gender'] = request.form['gender']
                    about['work'] = request.form['work']
                    about['first_major_choice'] = request.form['first_major_choice']
                    about['second_major_choice'] = request.form['second_major_choice']
                    about['security_choice'] = request.form['security_choice']
                    about['pedagogical_adequacy'] = request.form['pedagogical_adequacy']
                    ab.insert_one(about)
                    return redirect('user_menu')
            

       
    
      return render_template('aboutyou.html')

@app.route('/editabout', methods=('GET', 'POST'))
def editabout():
    
    return render_template('editabout.html')


@app.route('/skills', methods=('GET', 'POST'))
def skills():
     if "email" in session:
         acc_mail=session['email'] 
     else:
       return redirect('signin')
    
     emailInskill=skils.find_one({"email": acc_mail})
     if emailInskill:
        return redirect('editskils')
     else:
            about = {}
            if request.method =='POST':
                
                    about['email']= acc_mail
                    about['StressB'] = request.form['StressB']
                    about['StressA'] = request.form['StressA']
                    about['KnowledgeB'] = request.form['KnowledgeB']
                    about['KnowledgeA'] = request.form['KnowledgeA']
                    about['TimeB'] = request.form['TimeB']
                    about['TimeA'] = request.form['TimeA']
                    about['email']= acc_mail
                    about['DistanceB'] = request.form['DistanceB']
                    about['DistanceA'] = request.form['DistanceA']
                    about['LackB'] = request.form['LackB']
                    about['LackA'] = request.form['LackA']
                    about['AnotherB'] = request.form['AnotherB']
                    about['AnotherA'] = request.form['AnotherA']

                    about['skil1'] = request.form['skil1']
                    about['skilr1'] = request.form['skilr1']
                    about['skil2'] = request.form['skil2']
                    about['skilr2'] = request.form['skilr2']
                    about['skil3'] = request.form['skil3']
                    about['skilr3'] = request.form['skilr3']
                    about['skil4'] = request.form['skil4']
                    about['skilr4'] = request.form['skilr4']
                    about['skil5'] = request.form['skil5']
                    about['skilr5'] = request.form['skilr5']
                    about['skil6'] = request.form['skil6']
                    about['skilr6'] = request.form['skilr6']

                    


                    skils.insert_one(about)
                    return redirect('user_menu')
    
     return render_template('skills.html')

    
@app.route('/editskils', methods=('GET', 'POST'))
def editskils():
    if "email" in session:
       acc_mail=session['email'] 
    else:
       return redirect('signin')
    
    if request.method == "GET":

        # get the id of the note to edit
        skil_found=skils.find_one({'email':acc_mail})
        if skil_found:
            # direct to edit note page
         return render_template('editskils.html',skil_found=skil_found)
        else:
            message='you have ot set any '
            return render_template('editskils.html',message=message)


       
        

    elif request.method == "POST":

        #get the data of the note
       
     
       
                    StressB = request.form['StressB']
                    StressA = request.form['StressA']
                    KnowledgeB = request.form['KnowledgeB']
                    KnowledgeA = request.form['KnowledgeA']
                    TimeB = request.form['TimeB']
                    TimeA = request.form['TimeA']
                    
                    DistanceB = request.form['DistanceB']
                    DistanceA = request.form['DistanceA']
                    LackB = request.form['LackB']
                    LackA = request.form['LackA']
                    AnotherB = request.form['AnotherB']
                    AnotherA = request.form['AnotherA']

                    skil1 = request.form['skil1']
                    skilr1 = request.form['skilr1']
                    skil2 = request.form['skil2']
                    skilr2 = request.form['skilr2']
                    skil3 = request.form['skil3']
                    skilr3 = request.form['skilr3']
                    skil4 = request.form['skil4']
                    skilr4 = request.form['skilr4']
                    skil5 = request.form['skil5']
                    skilr5 = request.form['skilr5']
                    skil6 = request.form['skil6']
                    skilr6 = request.form['skilr6']
       

                    skils.update_one({'email':acc_mail},{"$set":{'StressB':StressB,'StressA':StressA,'KnowledgeB':KnowledgeB,'KnowledgeA':KnowledgeA,
                    'TimeB':TimeB,'TimeA':TimeA,'DistanceB':DistanceB,'DistanceA':DistanceA,
                    'LackB':LackB,'LackA':LackA,'AnotherB':AnotherB,'AnotherA':AnotherA,
                    'skil1':skil1,'skilr1':skilr1,'skil2':skil2,'skilr2':skilr2,
                    'skil3':skil3,'skilr3':skilr3,'skil4':skil4,'skilr4':skilr4,
                    'skil5':skil5,'skilr5':skilr5,'skil6':skil6,'skilr6':skilr6

                    }})
                    return redirect('user_menu')
    
    return render_template('editskils.html')


@app.route('/will', methods=('GET', 'POST'))
def will():
     if "email" in session:
       acc_mail=session['email'] 
     else:
       return redirect('signin')
    
    
     if request.method == "GET":
        course=["AnalysisI",
    "JAVA",
    "EducationalPsychology",
    "DataStructures",
    "Statistics",
    "AlgorithmsComplexity",
    "ArtificialIntelligence",
    "DigitalCommunications",
    "IT_CentricProfessionalDevelopment",
    "FinalYearProject"]

        # get the id of the note to edit
        course_found=random.sample(course, 4)
        return render_template('will.html',course_found=course_found)
        
       
    
     return render_template('will.html')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)