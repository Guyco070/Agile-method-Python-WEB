from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from Agile.views import *

class Test(SimpleTestCase):
    
    def test_SignUp_DBInsert(self):
        SV = db.users
        SV.delete_many({"ID" : "Guyco070", "EMAIL": "gaico070@gmail.com"})
        SV.delete_many({"ID" : "", "EMAIL": ""})
        user = {
            "ID": "Guyco070",
            "PASSWORD": 123456,
            "EMAIL": "gaico070@gmail.com",
            "TYPE" : "Admin",
        }
        SV.insert_one(user)
        client.close()
        is_user_inserted = SV.find_one(user) != None
        self.assertTrue(is_user_inserted)
    
    def test_LOGIN_DBFind_true(self):
        is_user_Exist = db.users.find_one({
            "ID": "Guyco070",
            "PASSWORD": 123456,
            "EMAIL": "gaico070@gmail.com",
            "TYPE" : "Admin",
        }) != None
        self.assertTrue(is_user_Exist)

    def test_LOGIN_DBFind_false(self):
        is_user_Exist = db.users.find_one({
            "ID": "abcdefg123456789",
            "PASSWORD": 112344342,
            "EMAIL": "ppp@gmail.com",
            "TYPE" : "friend",
        }) != None
        self.assertFalse(is_user_Exist)

    def test_CreateProjDone_DBInsert(self):
        SV = db.projects
        Programmer_list = ["Guyco070"]
        Clients_list = ["Guyco070"]
        SV.delete_one({"ProjectName" : "Test_project"})
        project = {
            "ProjectName" : "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "Guyco070",
            "Cilents":Clients_list ,
            "Programmer": Programmer_list
        }
        SV.insert_one(project)
        client.close()
        is_project_inserted = SV.find_one(project) != None
        self.assertTrue(is_project_inserted)
    def test_getTasksFromDb(self):
        todo = list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"TODO"}))
        inprogress=list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST"}))
        done = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE"}))
        print(todo)
        print(inprogress)
        print(done)
     def test_getTasksFromDb(self):
        todo = list(db.tasks.find({"status":"TODO"}))
        inprogress=list(db.tasks.find({"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"status": "INTEST"}))
        done = list(db.tasks.find({"status": "DONE"}))
        print(todo)
        print(inprogress)
        print(done)
     def test_EditTasks(self):
        uStory = self['USERSTORY']
        tasks = self['TASKS']
        s = self['startDate']
        e = self['endDate']
        p =  self['programmer']
        uStory = uStory.lstrip()
        uStory = uStory.rstrip()
        tasks = tasks.lstrip()
        tasks = tasks.rstrip()
        projectName = self['Project']
        myquery = db.tasks.find_one ({"ProjectName":projectName,"USERSTORY": uStory})
        newvalues = {"$set": {"ProjectName": projectName }}
        db.tasks.update_one(myquery,newvalues)
        print("ok);
     def test_addTASK(self):
        task = {
                "ProjectName":self['projectName'],
                "USERSTORY":self['USERSTORY'],
                "Tasks": self['Tasks'],
                "SDate": self['SDate'],
                "EDate": self['EDate'],
                "Programmer" : self['Programmer'],
                "status":self['Status']
            }
         SV = db.tasks
         SV.insert_one(task)
         print(tasks)
         print("new task added!")
    '''
    def test_homepage_url(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_SIGNUP_url(self):
        response = self.client.get('/SIGNUP')
        self.assertEquals(response.status_code, 200)

    def test_LOGIN_url(self):
        response = self.client.get('/LOGIN')
        self.assertEquals(response.status_code, 200)

    def test_SignUpDone_url(self):
        response = self.client.get('/SignUpDone')
        self.assertEquals(response.status_code, 200)
    '''
