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
    result=render(response,'Agile/loginstatus.html')
    result.set_cookie('UserID',response.POST.get('ID'))
    return result
def NewProjectPage(request):
    return render(request,'Agile/NewProjectPage.html')
def CreateProjDone(response):
    if response.method == 'POST':
        SV = db.projects
        projects = {
            "ProjectName" : response.POST.get('ProjectName'),
        }
        SV.insert_one(projects)
        client.close()
    return render(response,'Agile/CreateProjDone.html')
