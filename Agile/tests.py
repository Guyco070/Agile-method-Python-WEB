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
        inprogress = list(db.tasks.find({"ProjectName":response.COOKIES['Project'],"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "INTEST"}))
        done = list(db.tasks.find({"ProjectName": response.COOKIES['Project'], "status": "DONE"}))

        is_task_exist = todo != None & inprogress != None & intest != None & done != None
        self.assertTrue(is_user_inserted)

    def test_getTasksFromDb(self):
        todo = list(db.tasks.find({"status":"TODO"}))
        inprogress=list(db.tasks.find({"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"status": "INTEST"}))
        done = list(db.tasks.find({"status": "DONE"}))
        
        is_task_exist = (todo != None) & (inprogress != None) & (intest != None) & (done != None)
        self.assertTrue(is_task_exist)

    def test_addTASK(self):
        SV = db.tasks

        projectName = " temp_projectName  "
        uStory = " testUSERSTORY "

        uStory = uStory.lstrip()
        uStory = uStory.rstrip()
        projectName = projectName.lstrip()
        projectName = projectName.rstrip()
        
        SV.delete_many({"ProjectName":projectName,"USERSTORY": uStory})
        task = {
                "ProjectName": projectName,
                "USERSTORY": uStory,
                "Tasks": "test_Tasks",
                "SDate": "test_SDate",
                "EDate": "test_EDate",
                "Programmer" : "test_Programmer",
                "status": "test_Status"
            }
        
        SV.insert_one(task)

        is_task_unserted = SV.find_one(task) != None
        self.assertTrue(is_task_unserted)
    
    def test_EditTasks(self):
        projectName = " temp_projectName  "
        uStory = " testUSERSTORY "

        uStory = uStory.lstrip()
        uStory = uStory.rstrip()
        projectName = projectName.lstrip()
        projectName = projectName.rstrip()
        
        DB = db.tasks

        myquery = DB.find_one({"ProjectName":projectName,"USERSTORY": uStory})
        newvalues = {"$set": {"Tasks": "test_Tasks_after_change" }}
        DB.update_one(myquery,newvalues)

        myquery = DB.find_one({"ProjectName":projectName,"USERSTORY": uStory})
        
        self.assertEqual("test_Tasks_after_change", myquery['Tasks'])
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
