from idlelib import query
from django.shortcuts import render
from pymongo import MongoClient
from pymongo.message import update
client = MongoClient("mongodb+srv://TeamFour:TeamFour1234@cluster0.kwe3f.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-qwx95l-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db = client["Agile"]
def HomePage(request):
    return render(request,'Agile/HomePage.html')
def SIGNUP(request):
    return render(request,'Agile/SignUp.html')
def LOGIN(request):
    return render(request,'Agile/LogIn.html')
def NewProjectPage(response):
    Users = {'programmers': [],'clients':[]}
    tempPro = list(db.users.find({"TYPE": "Programmer"}))
    for pr in tempPro:
        p = pr['ID']
        if (p != None):
            Users['programmers'].append(p)
    tempCli = list(db.users.find({"TYPE": "Client"}))
    for cl in tempCli:
        c = cl['ID']
        if (cl != None):
            Users['clients'].append(c)
    return render(response, "Agile/NewProjectPage.html", Users)
def CreateProjDone(response):
    if response.method == 'POST':
        SV = db.projects
        Programmer_list = response.POST.getlist('programmer')
        client_list = response.POST.getlist('client')
        projects = {
            "ProjectName" : response.POST.get('ProjectName'),
            "Description": response.POST.get('projectDescription'),
            "PManager": response.COOKIES['Email'],
            "Cilents":client_list,
            "Programmer":Programmer_list,
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
def showMyProjects(response):
    if(response.COOKIES['TYPE']=='Admin'):
        return AdminHomePage(response)
    if(response.COOKIES['TYPE']=='Programmer'):
        return ProgrammerHomePage(response)
    if(response.COOKIES['TYPE']=='Client'):
        return ClientHomePage(response)
def LoginStatus(response):
    if response.method=='POST':
        findUser =db.users.find_one({"EMAIL": response.POST.get('EMAIL') , "PASSWORD": response.POST.get("PASSWORD")})
        if(findUser!= None):
            if(findUser['TYPE']=="Admin"):
                result=render(response,"Agile/AdminHomePage.html")
                result.set_cookie('TYPE', findUser['TYPE'], max_age=1800)
                result.set_cookie('Email', response.POST.get('EMAIL'), max_age=1800)
            if (findUser['TYPE'] == "Programmer"):
                result=render(response, "Agile/ProgrammerHomePage.html")
                result.set_cookie('TYPE', findUser['TYPE'],max_age=1800)
                result.set_cookie('Email', response.POST.get('EMAIL'),max_age=1800)
            if (findUser['TYPE'] == "Client"):
                result =render(response, "Agile/ClientHomePage.html")
                result.set_cookie('TYPE', findUser['TYPE'],max_age=1800)
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
def ProjectPage(response):
    PDetails = {'PDetails': []}
    tempPs = db.projects.find_one({"ProjectName": response.POST.get('Project')})
    if(tempPs != None):
        name = tempPs['ProjectName']
        des = tempPs['Description']
        if (name != None):
            PDetails['PDetails'].append(['Project name',name])
        if (des != None):    
            PDetails['PDetails'].append(['Description',des])
        if (response.COOKIES['TYPE'] == 'Admin'):
            result = render(response, "Agile/ProjectPageManager.html", PDetails)
        if (response.COOKIES['TYPE'] == 'Programmer'):
            result = render(response, "Agile/ProjectPageProgrammer.html", PDetails)
        if (response.COOKIES['TYPE'] == 'Client'):
            result = render(response, "Agile/ProjectPageClient.html", PDetails)
        result.set_cookie('Project',response.POST.get('Project'),1800)
    return result
def ProgrammerHomePage(response):
    if response.method == 'POST':
        projects = {'projects': []}
        tempPs = list(db.projects.find({"Programmer": response.COOKIES['Email']}))
        for pr in tempPs:
            p = pr['ProjectName']
            if (p != None):
                projects['projects'].append(p)
    return render(response, "Agile/ProgrammerHomePage.html", projects)
def ClientHomePage(response):
    if response.method == 'POST':
        projects = {'projects': []}
        tempPs = list(db.projects.find({"PManager": response.COOKIES['Email']}))
        for pr in tempPs:
            p = pr['ProjectName']
            if (p != None):
                projects['projects'].append(p)
    return render(response, "Agile/ClientHomePage.html", projects)

def ChangeDetailsPage(response):
    PDetails = {'PDetails': []}
    tempPs = db.projects.find_one({"ProjectName":response.COOKIES['Project']})
    if(tempPs != None):
        name = tempPs['ProjectName']
        des = tempPs['Description']
        if (name != None):
            PDetails['PDetails'].append(['Project name',name])
        if (des != None):    
            PDetails['PDetails'].append(['Description',des])
    result=render(response, "Agile/ChangeDetailsPage.html", PDetails)
    return result
def taskpage(response):
    TDetails = {'PDetails': []}
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'],"USERSTORY": response.COOKIES['Task']})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer=tempPs['Programmer']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['USERSTORY :', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer :', Programmer])
    if(response.COOKIES['TYPE']=='Admin'):
        result=render(response, "Agile/TaskPageManager.html",TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html",TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html",TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME'), 1800)
    return result
def taskpage1(response):
    TDetails = {'PDetails': []}
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.COOKIES['Task']})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer = tempPs['Programmer']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['USERSTORY :', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer :', Programmer])
    if (response.COOKIES['TYPE'] == 'Admin'):
        result = render(response, "Agile/TaskPageManager.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html", TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME1'), 1800)
    return result
def taskpage2(response):
    TDetails = {'PDetails': []}
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.COOKIES['Task']})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer = tempPs['Programmer']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['USERSTORY :', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer :', Programmer])
    if (response.COOKIES['TYPE'] == 'Admin'):
        result = render(response, "Agile/TaskPageManager.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html", TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME2'), 1800)
    return result
def taskpage3(response):
    TDetails = {'PDetails': []}
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.COOKIES['Task']})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer = tempPs['Programmer']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['USERSTORY :', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer :', Programmer])
    if (response.COOKIES['TYPE'] == 'Admin'):
        result = render(response, "Agile/TaskPageManager.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html", TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME3'), 1800)
    return result
def TaskPageEdit(response):
    return render(response, "Agile/TaskPageEdit.html")
def EditTasks(response):
    PDetails = {'PDetails': []}
    myquery={"ProjectName": response.COOKIES['Project'],"USERSTORY": response.COOKIES['Task']};
    newvalues = {"$set": {"ProjectName":  response.COOKIES['Project'],"USERSTORY": response.POST.get('USERSTORY'),"Tasks": response.POST.get('Tasks'),"status": response.POST.get('status')}}
    db.tasks.update_one(myquery,newvalues)
    return render(response, "Agile/TaskPageEdit.html", PDetails)
def updateProjectDetails(response):
    PDetails = {'PDetails': []}
    tempPs = db.projects.find_one({"ProjectName": response.COOKIES['Project']})
    myquery={"ProjectName": response.COOKIES['Project']};
    newvalues = {"$set": {"ProjectName": response.POST.get('ProjectName'),"Description": response.POST.get('projectDescription')}}
    db.projects.update_one(myquery,newvalues)
    if (tempPs != None):
        name = response.POST.get('ProjectName')
        des = response.POST.get('projectDescription')
        if (name != None):
            PDetails['PDetails'].append(['Project name', name])
        if (des != None):
            PDetails['PDetails'].append(['Description', des])
    return render(response, "Agile/ChangeDetailsPage.html", PDetails)
def AddTasks(request):
    return render(request,"Agile/AddTasks.html")
def ADDTASKS(response):
    if response.method == 'POST':
        SV = db.tasks
        task = {
            "ProjectName":response.COOKIES['Project'],
            "USERSTORY":response.POST.get('USERSTORY'),
            "Tasks": response.POST.get('TASKS'),
            "Programmer" : None,
            "status":"TODO"
        }
        SV.insert_one(task)
        client.close()
    return render(response,"Agile/TASKSADDED.html")
def KanbanPage(response):
    if response.method == 'POST':
        tasks = {'tasks':[]}
        tasks1={'tasks':[]}
        tasks2 ={'tasks': []}
        tasks3 = {'tasks': []}
        todo = list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"TODO"}))
        inprogress=list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST"}))
        done = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE"}))
        for pr in todo:
            p = pr['USERSTORY']
            if(p != None):
                tasks['tasks'].append(p)
        for pr in inprogress:
            p = pr['USERSTORY']
            if(p != None):
                tasks1['tasks'].append(p)
        for pr in intest:
            p = pr['USERSTORY']
            if(p != None):
                tasks2['tasks'].append(p)
        for pr in done:
            p = pr['USERSTORY']
            if(p != None):
                tasks3['tasks'].append(p)
    return render(response,"Agile/KanbanPage.html",{"todo":tasks['tasks'],"inprogress":tasks1['tasks'],"intest":tasks2['tasks'],"done":tasks3['tasks']})
def signuptest(user):
    print(user)
def logintest(user):
    print(user)
def createprojecttest(proj):
    print(proj)

def get_item_DL(dictionary, key, number):
    return dictionary.get(key)[number]
def get_item(dictionary, key):
    return dictionary.get(key)