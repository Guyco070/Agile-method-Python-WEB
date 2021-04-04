from django.shortcuts import render
from pymongo import MongoClient
client = MongoClient("mongodb+srv://TeamFour:TeamFour1234@cluster0.kwe3f.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-qwx95l-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db = client["Agile"]
def HomePage(request):
    return render(request,'Agile/HomePage.html')
def SIGNUP(request):
    return render(request,'Agile/SignUp.html')
def SignUpDone(response):
    if response.method == 'POST':
        SV = db.users
        user = {
            "ID":response.POST.get('ID'),
            "PASSWORD":response.POST.get('PASSWORD'),
            "EMAIL": response.POST.get('EMAIL'),
        }
        SV.insert_one(user)
        client.close()
    return render(response, 'Agile/SignupDone.html')
def LoginStatus(response):
    if response.method=='POST':
        findUser=db.users.find_one({"EMAIL": response.POST.get('EMAIL') , "PASSWORD": response.POST.get("PASSWORD")})
        print(findUser)
    result=render(response,'Agile/AdminHomePage.html')
    result.set_cookie('Email',response.POST.get('EMAIL'))
    return result