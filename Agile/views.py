from idlelib import query
from django.shortcuts import render
from pymongo import MongoClient
from pymongo.message import update
from datetime import datetime, timedelta

TaskPageProgrammer_flag = True
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
        Programmer_list = get_emails(response.POST.getlist('programmer'))
        client_list = get_emails(response.POST.getlist('client'))

        ProjectName = response.POST.get('ProjectName')
        ProjectName = remove_white_spaces_SE(ProjectName)
        projects = {
            "ProjectName" : ProjectName,
            "Description": response.POST.get('projectDescription'),
            "PManager": response.COOKIES['Email'],
            "Cilents":client_list,
            "Programmer":Programmer_list,
        }
        SV.insert_one(projects)
        client.close()
    return showMyProjects(response)

def SignUpDone(response):
    if response.method == 'POST':
        SV = db.users
        user = {
            "ID":response.POST.get('ID'),
            "PASSWORD":response.POST.get('PASSWORD'),
            "EMAIL": response.POST.get('EMAIL'),
            "TYPE" : response.POST.get('TYPE'),
            "FName" : response.POST.get('FName'),
            "LName" : response.POST.get('LName'),
        }
        SV.insert_one(user)
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
        if 'logout' in response.POST:
            if 'Email' in response.COOKIES:
                result = HomePage(response)
                result.delete_cookie('Email')
                result.delete_cookie('TYPE')
            return result
        if 'bTuser' in response.POST:
            findUser =db.users.find_one({"EMAIL": response.COOKIES['Email']})
        else:
            findUser =db.users.find_one({"EMAIL": response.POST.get('EMAIL') , "PASSWORD": response.POST.get("PASSWORD")})

        if(findUser!= None):
            if 'FName' in findUser:
                user_name = {"FName":findUser['FName'],"LName":findUser['LName']}
            else: user_name = {"FName": "","LName":""}
            if(findUser['TYPE']=="Admin"):
                result=render(response,"Agile/AdminHomePage.html",user_name)
                result.set_cookie('TYPE', findUser['TYPE'], max_age=1800)
                result.set_cookie('Email', findUser['EMAIL'], max_age=1800)
            if (findUser['TYPE'] == "Programmer"):
                result=render(response, "Agile/ProgrammerHomePage.html",user_name)
                result.set_cookie('TYPE', findUser['TYPE'],max_age=1800)
                result.set_cookie('Email', findUser['EMAIL'],max_age=1800)
            if (findUser['TYPE'] == "Client"):
                result =render(response, "Agile/ClientHomePage.html",user_name)
                result.set_cookie('TYPE', findUser['TYPE'],max_age=1800)
                result.set_cookie('Email',findUser['EMAIL'] ,max_age=1800)
                result.set_cookie('ID', findUser['ID'],max_age=1800)
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
    if 'Project' in response.POST:
        tempPs = db.projects.find_one({"ProjectName": response.POST.get('Project')})
    else: tempPs = db.projects.find_one({"ProjectName": response.COOKIES['Project']})
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
        result.set_cookie('Project',response.POST.get('Project'),3000)
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
        tempPs = list(db.projects.find({"Cilents": response.COOKIES['Email']}))
        for pr in tempPs:
            p = pr['ProjectName']
            if (p != None):
                projects['projects'].append(p)
    return render(response, "Agile/ClientHomePage.html", projects)

def ChangeDetailsPage(response):
    PDetails = {'PDetails': [],'programmers': [], 'clients': []}
    tempPro = list(db.users.find({"TYPE": "Programmer"}))
    for pr in tempPro:
        p = pr['ID']
        if (p != None):
            PDetails['programmers'].append(p)
    tempCli = list(db.users.find({"TYPE": "Client"}))
    for cl in tempCli:
        c = cl['ID']
        if (cl != None):
            PDetails['clients'].append(c)

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
    if response.POST.get('TASKNAME') != None:
        taskname = response.POST.get('TASKNAME')
    elif response.POST.get('TASKNAME1') != None:
        taskname = response.POST.get('TASKNAME1')
    elif response.POST.get('TASKNAME2') != None:
        taskname = response.POST.get('TASKNAME2')
    elif response.POST.get('TASKNAME3') != None:
        taskname = response.POST.get('TASKNAME3')
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": taskname})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer=tempPs['Programmer']
        
        if (USERSTORY != None):
            TDetails['PDetails'].append(['User story', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if "SDate" in tempPs:
            sDate=tempPs['SDate']
            eDate=tempPs['EDate']
            TDetails['PDetails'].append(['Estimated start', sDate])
            if (eDate != None):
                TDetails['PDetails'].append(['Estimated end', eDate])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer', Programmer])
    if(response.COOKIES['TYPE']=='Admin'):
        result=render(response, "Agile/TaskPageManager.html",TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html",TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html",TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME'), 1800)
    return result

def TaskPageEdit(response):
    PQuery = db.projects.find_one({"ProjectName": response.COOKIES['Project']})
    return render(response, "Agile/TaskPageEdit.html",PQuery)

def EditTasks(response):
    SV = db.tasks
    projectName = response.COOKIES['Project']

    if 'Delete' in response.POST:
        SV.delete_many({"ProjectName":response.COOKIES['Project'],"USERSTORY": response.COOKIES['Task']})
    else:
        uStory = response.POST.get('USERSTORY')
        tasks = response.POST.get('TASKS')
        s = response.POST.get('startDate')
        e = response.POST.get('endDate')
        p = response.POST.get('programmer')

        uStory = remove_white_spaces_SE(uStory)
        tasks = remove_white_spaces_SE(tasks)

        myquery = db.tasks.find_one ({"ProjectName": projectName,"USERSTORY": response.COOKIES['Task']})
        newvalues = {"$set": {"ProjectName": projectName }}
        if uStory:
            newvalues["$set"]["USERSTORY"] = uStory
        if tasks:
            newvalues["$set"]["Tasks"] = tasks
        if uStory:
            newvalues["$set"]["USERSTORY"] = uStory
        if s :
            sDate = datetime.strptime(s.replace("T"," ")[2:], '%y-%m-%d %H:%M')
            s = sDate.strftime('%d.%m.%y %H:%M') #format change
            if not e:
                eDate = datetime.strptime(myquery["SDate"],'%d.%m.%y %H:%M')
            else: 
                eDate = datetime.strptime(e.replace("T"," ")[2:], '%y-%m-%d %H:%M')
                e = eDate.strftime('%d.%m.%y %H:%M') #format change
            if sDate < eDate:
                newvalues["$set"]["EDate"] = e
        elif e:
            eDate = datetime.strptime(e.replace("T"," ")[2:], '%y-%m-%d %H:%M')
            e = eDate.strftime('%d.%m.%y %H:%M') #format change
            sDate = datetime.strptime(myquery["SDate"],'%d.%m.%y %H:%M')
            if eDate > sDate:
                newvalues["$set"]["EDate"] = e
        if p != 'programmer' :
            newvalues["$set"]["Programmer"] = p
        SV.update_one(myquery,newvalues)
    result = ProjectPage(response)
    result.set_cookie('Project',projectName,3000)
    return result

def updateProjectDetails(response):
    PDetails = {'PDetails': []}
    tempPs = db.projects.find_one({"ProjectName": response.COOKIES['Project']})
    myquery={"ProjectName": response.COOKIES['Project']}
    ProjectName = response.POST.get('ProjectName')

    projectDescription = response.POST.get('projectDescription')
    newvalues = {"$set": {}}
    if ProjectName:
        ProjectName = remove_white_spaces_SE(ProjectName)
        newvalues["$set"]["ProjectName"] = ProjectName
    if projectDescription:
        newvalues["$set"]["Description"] = projectDescription
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
    PQuery = db.projects.find_one({"ProjectName": request.COOKIES['Project']})
    return render(request,"Agile/AddTasks.html",PQuery)

def ADDTASKS(response):
    if response.method == 'POST':
        projectName = response.COOKIES['Project']
        if 'beckToP' in response.POST:
            result = ProjectPage(response)
        else:
            a = response.POST.get('USERSTORY')
            b = response.POST.get('TASKS')
            c = response.POST.get('startDate')
            d = response.POST.get('endDate')
            e = response.POST.get('programmer')
            
            a = remove_white_spaces_SE(a)
            b = remove_white_spaces_SE(b)

            sDate = datetime.strptime(c.replace("T"," ")[2:], '%y-%m-%d %H:%M')
            eDate = datetime.strptime(d.replace("T"," ")[2:], '%y-%m-%d %H:%M')
            c = sDate.strftime('%d.%m.%y %H:%M') #format change
            d = eDate.strftime('%d.%m.%y %H:%M') #format change
            task = {
                "ProjectName":projectName,
                "USERSTORY":a,
                "Tasks": b,
                "SDate": c,
                "EDate": d,
                "Programmer" : e,
                "status":"TODO"
            }
            SV = db.tasks
            SV.insert_one(task)
            client.close()
            result = AddTasks(response)
    result.set_cookie('Project',projectName,3000)
    return result

def KanbanPage(response):
    if response.method == 'POST':
        tasks = {'tasks':[]}
        tasks1={'tasks':[]}
        tasks2 ={'tasks': []}
        tasks3 = {'tasks': []}
        
        if(response.COOKIES['TYPE'] == 'Programmer'):
            todo = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "TODO","Programmer":get_id(response.COOKIES['Email'])})) + list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "TODO","Programmer": response.COOKIES['Email']}))
            inprogress = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INPROGRESS","Programmer":get_id(response.COOKIES['Email'])})) + list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INPROGRESS","Programmer":response.COOKIES['Email']}))
            intest = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST","Programmer":get_id(response.COOKIES['Email'])})) + list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST","Programmer":response.COOKIES['Email']}))
            done = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE","Programmer":get_id(response.COOKIES['Email'])})) + list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE","Programmer":response.COOKIES['Email']}))
        else :
            todo = list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"TODO"}))
            inprogress=list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"INPROGRESS"}))
            intest = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST"}))
            done = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE"}))
        for pr in todo:
            p = pr['USERSTORY']
            if(p != None):
                tasks['tasks'].append([p,color_adapter(pr)])
        for pr in inprogress:
            p = pr['USERSTORY']
            if(p != None):
                tasks1['tasks'].append([p,color_adapter(pr)])
        for pr in intest:
            p = pr['USERSTORY']
            if(p != None):
                tasks2['tasks'].append([p,color_adapter(pr)])
        for pr in done:
            p = pr['USERSTORY']
            if(p != None):
                if('RATE' in pr):
                    r = pr['RATE']
                else: r = 0
                tasks3['tasks'].append([p,r])
    return render(response,"Agile/KanbanPage.html",{"todo":tasks['tasks'],"inprogress":tasks1['tasks'],"intest":tasks2['tasks'],"done":tasks3['tasks']})

def ClientKanbanPage(response):
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
                tasks['tasks'].append([p,color_adapter(pr)])
        for pr in inprogress:
            p = pr['USERSTORY']
            if(p != None):
                tasks1['tasks'].append([p,color_adapter(pr)])
        for pr in intest:
            p = pr['USERSTORY']
            if(p != None):
                tasks2['tasks'].append([p,color_adapter(pr)])
        for pr in done:
            p = pr['USERSTORY']
            if(p != None):
                if('RATE' in pr):
                    r = pr['RATE']
                else: r = 0
                tasks3['tasks'].append([p,r])
    return render(response,"Agile/Client‏‏KanbanPage.html",{"todo":tasks['tasks'],"inprogress":tasks1['tasks'],"intest":tasks2['tasks'],"done":tasks3['tasks']})

def updateRate(response):
    if 'TASKNAME' or 'TASKNAME1' or 'TASKNAME2' or 'TASKNAME3' in response.POST:
            return taskpage(response)
    elif "rate" in response.POST:
        db.tasks.find_one_and_update({"USERSTORY" : response.POST["rateBut"]},{"$set": {"RATE":response.POST['rate']}},upsert=True)
        return ClientKanbanPage(response)

def TaskPageProgrammer(response):
    global TaskPageProgrammer_flag
    if(TaskPageProgrammer_flag):
        if 'TASKNAME' in response.POST:
            return taskpage(response)
        elif 'TASKNAME1' in response.POST:
            return taskpage1(response)
        elif 'TASKNAME2' in response.POST:
            return taskpage2(response)
        elif 'TASKNAME3' in response.POST:
            return taskpage3(response)
        elif 'passNext' in response.POST:
            tempT = db.tasks.find_one({"USERSTORY": response.POST.get('passNext')})
            status = tempT['status']
            if(status == "TODO"):
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('passNext')},{"$set": {"status": "INPROGRESS"}})
            elif(status == "INPROGRESS"):
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('passNext')},{"$set": {"status": "INTEST"}})
            elif(status == "INTEST"):
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('passNext')},{"$set": {"status": "DONE"}})
        elif 'returnStage' in response.POST:
            tempT = db.tasks.find_one({"USERSTORY": response.POST.get('returnStage')})
            status = tempT['status']
            if status == "INPROGRESS":
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('returnStage')},{"$set": {"status": "TODO"}})
            elif status == "INTEST":
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('returnStage')},{"$set": {"status": "INPROGRESS"}})
            elif status == "DONE":
                db.tasks.find_one_and_update({"USERSTORY": response.POST.get('returnStage')},{"$set": {"status": "INTEST"}})
        client.close()
        TaskPageProgrammer_flag = False
        return KanbanPage(response)
    TaskPageProgrammer_flag = True
    return KanbanPage(response)

def get_emails(users):
    Programmer_list = list([])
    for temp_pr in users:
        temp_e = db.users.find_one({ "ID": temp_pr})
        Programmer_list.append(temp_e["EMAIL"])
    return Programmer_list

def get_id(usere):
    return db.users.find_one({ "EMAIL": usere})['ID']

def get_item_DL(dictionary, key, number):
    return dictionary.get(key)[number]

def get_item(dictionary, key):
    return dictionary.get(key)

def remove_white_spaces_SE(str_to_update): #remove white spaces from start+end of string
    str_to_update = str_to_update.lstrip()
    str_to_update = str_to_update.rstrip()
    return str_to_update

def color_adapter(pr):
    if "EDate" in pr:
        EDate = datetime.strptime(pr["EDate"],'%d.%m.%y %H:%M')
        now = datetime.now()
        
        if pr["status"] == "TODO":
            if (EDate - timedelta(days=7)) < now:  # EDate - timedelta(7) = EDate - 5 days
                return "red"
            else: "green"

        if pr["status"] == "INPROGRESS":
            if (EDate - timedelta(days=5)) < now:  # EDate - timedelta(5) = EDate - 5 days
                return "red"
            else: "green"

        if pr["status"] == "INTEST":
            if (EDate - timedelta(days=3)) < now:  # EDate - timedelta(3) = EDate - 3 days
                return "red"
            else: "green"

    '''
    sDate = datetime.strptime(s.replace("T"," ")[2:], '%y-%m-%d %H:%M')
    s = sDate.strftime('%d.%m.%y %H:%M') #format change
    if not e:
        eDate = datetime.strptime(myquery["SDate"],'%d.%m.%y %H:%M')
    '''
'''
def taskpage1(response):
    TDetails = {'PDetails': []}
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.POST.get('TASKNAME')})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer=tempPs['Programmer']
        sDate=tempPs['SDate']
        eDate=tempPs['EDate']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['User story', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (sDate != None):
            TDetails['PDetails'].append(['Estimated start', sDate])
        if (eDate != None):
            TDetails['PDetails'].append(['Estimated end', eDate])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer', Programmer])
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
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.POST.get('TASKNAME2')})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer=tempPs['Programmer']
        sDate=tempPs['sDate']
        eDate=tempPs['eDate']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['User story', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (sDate != None):
            TDetails['PDetails'].append(['Estimated start', sDate])
        if (eDate != None):
            TDetails['PDetails'].append(['Estimated end', eDate])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer', Programmer])
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
    tempPs = db.tasks.find_one({"ProjectName": response.COOKIES['Project'], "USERSTORY": response.POST.get('TASKNAME3')})
    if (tempPs != None):
        USERSTORY = tempPs['USERSTORY']
        Tasks = tempPs['Tasks']
        Programmer=tempPs['Programmer']
        sDate=tempPs['SDate']
        eDate=tempPs['EDate']
        if (USERSTORY != None):
            TDetails['PDetails'].append(['User story', USERSTORY])
        if (Tasks != None):
            TDetails['PDetails'].append(['Tasks', Tasks])
        if (sDate != None):
            TDetails['PDetails'].append(['Estimated start', sDate])
        if (eDate != None):
            TDetails['PDetails'].append(['Estimated end', eDate])
        if (Programmer != None):
            TDetails['PDetails'].append(['Programmer', Programmer])
    if (response.COOKIES['TYPE'] == 'Admin'):
        result = render(response, "Agile/TaskPageManager.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Programmer'):
        result = render(response, "Agile/TaskPageProgrammer.html", TDetails)
    if (response.COOKIES['TYPE'] == 'Client'):
        result = render(response, "Agile/TaskPageClient.html", TDetails)
    result.set_cookie('Task',response.POST.get('TASKNAME3'), 1800)
    return result
'''