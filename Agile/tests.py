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