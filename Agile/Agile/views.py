from django.shortcuts import render
from pymongo import MongoClient
client = MongoClient("mongodb+srv://TeamFour:TeamFour1234@cluster0.kwe3f.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-qwx95l-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db = client["Agile"]
def HomePage(request):
    return render(request,'Agile/HomePage.html')
def SIGNUP(request):
    return render(request,'Agile/SignUp.html')
def LOGIN(request):
    return render(request,'Agile/LogIn.html');
def NewProjectPage(request):
    return render(request,'Agile/NewProjectPage.html')
def CreateProjDone(response):
    if response.method == 'POST':
        SV = db.projects
        projects = {
            "ProjectName" : response.POST.get('ProjectName'),
            "Description": response.POST.get('projectDescription'),
        }
        SV.insert_one(projects)
        createprojecttest(projects)
        client.close()
    return render(response,'Agile/CreateProjDone.html')
def SignUpDone(response):
    if response.method == 'POST':
        SV = db.users
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
        if(findUser!= None):
            if(findUser['TYPE']=="Admin"):
                result = render(response, 'Agile/AdminHomePage.html')
                result.set_cookie('TYPE', response.POST.get('Admin'))
                result.set_cookie('Email', response.POST.get('EMAIL'))
            if (findUser['TYPE'] == "Dev"):
                result = render(response, 'Agile/ProgrammerHomePage.html')
                result.set_cookie('TYPE', response.POST.get('DEV'))
                result.set_cookie('Email', response.POST.get('EMAIL'))
            if (findUser['TYPE'] == "CUSTOMER"):
                result = render(response, 'Agile/ClientHomePage.html')
                result.set_cookie('TYPE', response.POST.get('CUS'))
                result.set_cookie('Email',response.POST.get('EMAIL'))
        else:
            result = render(response, 'Agile/HomePage.html')
            result.set_cookie('Email',response.POST.get('None'))
    logintest(findUser)
    return result
def AdminHomePage(request):
    return render(request,"Agile/AdminHomePage.html")
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
