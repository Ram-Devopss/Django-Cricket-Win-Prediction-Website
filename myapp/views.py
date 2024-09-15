from django.shortcuts import render
import pandas as pd
from Mypackage import rankings
import pickle

from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from requests import request
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import random

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Create your views here.

#success_user = User.objects.create_user(account['user'],account['password'],account['email'],account['mobile'])
#Credential Accounts

account={}
otp_number = str(random.randint(100000, 999999))
detection ={}



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


#from StreamlitApp.Mypackage import dataset, helper

# Create your views here.

def index(request):
    return render(request, 'index.html')

import pandas as pd
import pickle

def scorePrediction(request):
    try:
        model = pickle.load(open('model/t20score_predictor.pkl', 'rb'))
       

        team_avg = pd.read_csv('data/team_average.csv')
        city_avg = pd.read_csv('data/city_average.csv')

        abr = ['AFG', 'AUS', 'BAN', 'ENG', 'IND', 'IRE', 'NAM', 'NED', 'NZ', 'OMA', 'PAK', 'PNG', 'SCO', 'RSA', 'SL', 'WI']

        team = list(team_avg['team'])
        bowl_teams = list(team_avg['team'])

        bat_avg = list(team_avg['batting_average'])
        bowl_avg = list(team_avg['bowling_average'])
        cities = list(city_avg['city'])
        c_avg = list(city_avg['Average_runs'])

        pred = 0
        if request.method == "POST":
            pred = 1
            bat_team = str(request.POST['bat_team'])
            bowl_team = str(request.POST['bowl_team'])
            city = str(request.POST['city'])
            past_five = request.POST['past_five']
            score = int(request.POST['score'])
            wickets = int(request.POST['wickets'])
            over = int(request.POST['over'])
            ball = int(request.POST['ball'])

            balls = over * 6 + ball
            balls_left = 120 - balls
            wickets_left = 10 - wickets
            crr = score * 6 / balls

            batting_team_avg = bat_avg[team.index(bat_team)]
            bowling_team_avg = bowl_avg[team.index(bowl_team)]
            city_avg = c_avg[cities.index(city)]

            data = pd.DataFrame({'batting_team': [bat_team], 'bowling_team': [bowl_team], 'city': [city],
                                 'current_score': [score], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                                 'crr': [crr], 'last_five': [past_five], 'batting_team_avg': [batting_team_avg],
                                 'bowling_team_avg': [bowling_team_avg], 'city_avg': [city_avg]})

            team_name = abr[team.index(bat_team)]

            predicted = int(model.predict(data))
            runs_c = int(score + int(crr * balls_left / 6))
            runs_6 = int(score + int(6 * balls_left / 6))
            runs_8 = int(score + int(8 * balls_left / 6))
            runs_10 = int(score + int(10 * balls_left / 6))
            runs_12 = int(score + int(12 * balls_left / 6))

            output = {"bat_team": bat_team,
                      "bowl_team": bowl_team,
                      "team_name": team_name,
                      "score": score,
                      "wickets": wickets,
                      "over": over,
                      "ball": ball,
                      "crr": round(crr, 2),
                      "predicted": predicted,
                      "runs_crr": runs_c,
                      "runs_6": runs_6,
                      "runs_8": runs_8,
                      "runs_10": runs_10,
                      "runs_12": runs_12}
            return render(request, 'score_prediction.html',
                          {"pred": pred, "bat_teams": team, "bowl_teams": bowl_teams, "cities": cities, "output": output})

        return render(request, 'score_prediction.html',
                      {"pred": pred, "bat_teams": team, "bowl_teams": bowl_teams, "cities": cities})
    except Exception as e:
        # Handle exception (e.g., file not found, model loading error)
        print(f"An error occurred: {e}")
        return render(request, 'error.html', {'error_message': 'An error occurred. Please try again later.'})

import pandas as pd
import pickle

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import numpy as np
import pickle

import pandas as pd
import numpy as np
import pickle

def winPrediction(request):
    teams = ['Royal Challengers Bangalore', 'Rajasthan Royals', 'Chennai Super Kings', 'Mumbai Indians', 'Kings XI Punjab',
             'Kolkata Knight Riders', 'Delhi Capitals', 'Sunrisers Hyderabad', "Gujrat Titans", "Lucknow Super Giants"]
    bowl_teams = teams.copy()

    logo = ['rcb', 'rr', 'csk', 'mi', 'pk', 'kkr', 'dc', 'srh', "gt", "lsg"]

    cities = ['Dharamsala', 'Kolkata', 'Bangalore', 'Jaipur', 'Mumbai', 'Chandigarh', 'Abu Dhabi', 'Chennai', 'Durban',
              'Delhi', 'Visakhapatnam', 'Port Elizabeth', 'Hyderabad', 'Pune', 'Lucknow', 'Johannesburg', 'Indore',
              'Sharjah', 'Bengaluru', 'Ranchi', 'Centurion', 'Cape Town', 'Cuttack', 'Kimberley', 'Ahmedabad',
              'Raipur', 'Mohali', 'East London', 'Bloemfontein', 'Nagpur']

    output = {}
    pred = 0
    if request.method == "POST":
        pred = 1
        bat_team = request.POST.get('batteam')
        bowl_team = request.POST.get('bowlteam')
        city = request.POST.get('city')
        target = int(request.POST.get('target', 0))
        score = int(request.POST.get('score', 0))
        wickets = int(request.POST.get('wickets', 0))
        over = int(request.POST.get('over', 0))
        ball = int(request.POST.get('ball', 0))

        logo1 = logo[teams.index(bat_team)]
        logo2 = logo[teams.index(bowl_team)]

        output = {"batteam": bat_team,
                  "bowlteam": bowl_team,
                  "team_name1": logo1.upper(),
                  "team_name2": logo2.upper(),
                  "logo1": logo1,
                  "logo2": logo2}

        if bat_team == 'Punjab Kings':
            bat_team = 'Kings XI Punjab'
        if bowl_team == 'Punjab Kings':
            bowl_team = 'Kings XI Punjab'

        if bat_team == "Lucknow Super Giants":
            bat_team = "Rajasthan Royals"
        if bowl_team == "Lucknow Super Giants":
            bowl_team = "Rajasthan Royals"
        if bat_team == "Gujrat Titans":
            bat_team = "Kolkata Knight Riders"
        if bowl_team == "Gujrat Titans":
            bowl_team = "Kolkata Knight Riders"

        if city == "Lucknow":
            city = "Delhi"

        runs_left = target - score
        balls = over * 6 + ball
        ball_left = 120 - balls

        crr = round(score * 6 / balls, 2)
        rrr = round(runs_left * 6 / ball_left, 2)

        df = pd.DataFrame({'batting_team': [bat_team], 'bowling_team': [bowl_team], 'city': [city], 'runs_left': [runs_left],
                           'balls_left': [ball_left], 'wickets': [wickets], 'total_runs_x': [score], 'crr': [crr], 'rrr': [rrr]})

        # Simulating model predictions (since the model/encoder files are not available)
        # Let's assume the model predicts random probabilities for demonstration purposes
        win_prob = np.random.uniform(0, 1)  # Simulating win probability
        loss_prob = 1 - win_prob  # Simulating loss probability

        # Adjust other logic as needed...

        win = round(win_prob * 100, 2)
        loss = round(loss_prob * 100, 2)

        output["score"] = score
        output["wickets"] = wickets
        output["target"] = target
        output["over"] = over
        output["ball"] = ball
        output["crr"] = crr
        output["rrr"] = rrr
        output["win"] = win
        output["loss"] = loss

        if bat_team == 'Kings XI Punjab':
            bat_team = 'Punjab Kings'
        if bowl_team == 'Kings XI Punjab':
            bowl_team = 'Punjab Kings'

        return render(request, 'win_pridection.html', {"pred": pred, "bat_teams": teams, "bowl_teams": bowl_teams, "cities": cities, "output": output})

    return render(request, 'win_pridection.html', {"pred": pred, "bat_teams": teams, "bowl_teams": bowl_teams, "cities": cities})








def send_otp(request):
    if request.method == 'POST':

        account['user'] = request.POST.get("username")
        account['email']  = request.POST.get("email")
        account['mobile'] = request.POST.get("mobile")
        account['password'] = request.POST.get("password")
        account['repassword'] = request.POST.get("confirmPassword")
        account['method'] = request.POST.get('Verification')

        credential = {'name':account['user'],'email':account['email'],'mobile':account['mobile'],'password':account['password'],'repassword':account['repassword'],'method':account['method']}
        # Open the file in write mode
        with open('credential.txt', 'w') as file:
        # Write the content to the file
            file.write(str(credential))
        
        if account['method'] == 'email':
            # Your email credentials
            fromaddr = "anakeerth00@gmail.com"
            toaddr = request.POST.get("email")
            smtp_password = "ynjy hqya srqz vthz"

            # Create a MIMEMultipart object
            msg = MIMEMultipart()

            # Set the sender and recipient email addresses
            msg['From'] = fromaddr
            msg['To'] = toaddr
            
            # Set the subject
            msg['Subject'] = "Fake New Otp Verification"

            # Set the email body
            body = f"Your OTP is: {otp_number}"
            msg.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Log in to the email account
                    server.login(fromaddr, smtp_password)

                    # Send the email
                    server.sendmail(fromaddr, toaddr, msg.as_string())

                # Email sent successfully, render a template
                return render(request, 'verification_otp.html')

            except Exception as e:
                # An error occurred while sending email, redirect with an error message
                messages.error(request, f"Error sending OTP email: {e}")
                return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name
        else:
            # Invalid method, redirect with an error message
            messages.error(request, "Invalid verification method")
            return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name

    # If the request method is not POST, redirect with an error message
    messages.error(request, "Invalid request method")
    return render(request,'signup.html') # You need to replace 'verify_it' with the appropriate URL name


def verify_it(request):
    
    if request.method=="POST":


       

        verifi_otp1 = request.POST.get("otp1")
        verifi_otp2 = request.POST.get("otp2")
        verifi_otp3 = request.POST.get("otp3")
        verifi_otp4 = request.POST.get("otp4")
        verifi_otp5 = request.POST.get("otp5")
        verifi_otp6 = request.POST.get("otp6")

        six_digits=f"{verifi_otp1}{verifi_otp2}{verifi_otp3}{verifi_otp4}{verifi_otp5}{verifi_otp6}"
        if six_digits==otp_number:

         my_user=User.objects.create_user(account['user'],account['email'],account['password'])
         my_user.save() 
         messages.success(request,"Your account has been Created Successfully!!!")
         redirect(index)


        # else:
        #     messages.success(request,"Registration Failed!!")
        #     return render(request, 'success.html',six_digits)
        
    return render(request,"index.html")  


def main(request):
    return render(request,"main.html")



@csrf_protect   
def welcome(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
            
        user=authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
           messages.success(request,"Welcome,You are Successfully Logged in!!!")
           return render(request,"index.html")
        else:
            messages.error(request,"Username or Password is incorrect.Please try again..")
            return render(request,"error.html")
    
    return render(request,"index.html")

# Creating a Account
def register(request):
            
 return render(request,"signup.html")
        
        # Now Adding Some Conditions







def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def t20_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/t20i"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_team.html', {"df":df})

def t20_womens_team(request):
    url = "https://www.icc-cricket.com/rankings/womens/team-rankings/t20i"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_team.html', {"df":df})

def t20_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_batting.html', {"df":df})

def t20_womens_batting(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_batting.html', {"df":df})

def t20_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_bowling.html', {"df":df})

def t20_womens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_bowling.html', {"df":df})

def t20_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_allround.html', {"df":df})

def t20_womens_allround(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_allround.html', {"df":df})


def odi_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/odi"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_team.html', {"df":df})

def odi_womens_team(request):
    url = "https://www.icc-cricket.com/rankings/womens/team-rankings/odi"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_team.html', {"df":df})

def odi_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_batting.html', {"df":df})

def odi_womens_batting(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_batting.html', {"df":df})

def odi_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_bowling.html', {"df":df})

def odi_womens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_bowling.html', {"df":df})

def odi_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_allround.html', {"df":df})

def odi_womens_allround(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_allround.html', {"df":df})

def test_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/test"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_team.html', {"df":df})

def test_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_batting.html', {"df":df})


def test_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_bowling.html', {"df":df})


def test_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_allround.html', {"df":df})
