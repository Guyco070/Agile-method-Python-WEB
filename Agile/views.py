from django.shortcuts import render
from pymongo import MongoClient
client = MongoClient("mongodb+srv://TeamFour:TeamFour1234@cluster0.kwe3f.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-qwx95l-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db = client["Agile"]
def HomePage(request):
    return render(request,'Agile/HomePage.html')
def SIGNUP(request):
    return render(request,'Agile/SignUp.html')
def LOGIN(request):
    return render(request,'Agile/LogIn.html')
def NewProjectPage(request):
    return render(request,'Agile/NewProjectPage.html')
def CreateProjDone(response):
    if response.method == 'POST':
        SV = db.projects
        projects = {
            "ProjectName" : response.POST.get('ProjectName'),
            "Description": response.POST.get('projectDescription'),
            "PManager": response.COOKIES['Email'],
        }
        SV.insert_one(projects)
        createprojecttest(projects)
        client.close()
    return render(response,'Agile/CreateProjDone.html')
def SignUpDone(response):
    if response.method == 'POST':
        SV = db.users
        print(response.POST.get('TYPE'))
        user = {
            "ID":response.POST.get('ID'),
            "PASSWORD":response.POST.get('PASSWORD'),
            "EMAIL": response.POST.get('EMAIL'),
            "TYPE" : response.POST.get('TYPE'),
        }
        SV.insert_one(user)
        signuptest(user)
        client.close()
    return render(response, 'Agile/SignupDone.html')
def LoginStatus(response):
    if response.method=='POST':
        findUser =db.users.find_one({"EMAIL": response.POST.get('EMAIL') , "PASSWORD": response.POST.get("PASSWORD")})
        print(findUser)
        if(findUser!= None):
            if(findUser['TYPE']=="Admin"):
                result = AdminHomePage(response)
                result.set_cookie('TYPE', response.POST.get('Admin'),max_age=1800)
                result.set_cookie('Email', response.POST.get('EMAIL'),max_age=1800)
            if (findUser['TYPE'] == "Programmer"):
                result = render(response, 'Agile/ProgrammerHomePage.html')
                result.set_cookie('TYPE', response.POST.get('DEV'),max_age=1800)
                result.set_cookie('Email', response.POST.get('EMAIL'),max_age=1800)
            if (findUser['TYPE'] == "Client"):
                result = render(response, 'Agile/ClientHomePage.html')
                result.set_cookie('TYPE', response.POST.get('CUS'),max_age=1800)
                result.set_cookie('Email',response.POST.get('EMAIL'),max_age=1800)
        else:
            result = render(response, 'Agile/HomePage.html')
            result.set_cookie('Email',response.POST.get('None'),max_age=1800)
    return result
def AdminHomePage(response):
    if response.method == 'POST':
        projects = {'projects':[]}
        tempPs = list(db.projects.find({"PManager": response.COOKIES['Email']}))
        for pr in tempPs:
            p = pr['ProjectName']
            if(p != None):
                projects['projects'].append(p)
    return render(response,"Agile/AdminHomePage.html",projects)
def ProgrammerHomePage(request):
    return render(request,"Agile/ProgrammerHomePage.html")
def ClientHomePage(request):
    return render(request,"Agile/CUSTOMER.html")
def signuptest(user):
    print(user)
def logintest(user):
    print(user)
def createprojecttest(proj):
    print(proj)
