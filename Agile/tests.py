from django.test import SimpleTestCase
from Agile.views import remove_white_spaces_SE, get_emails, get_id
from Agile.views import split_tasks, array_tasksToString, switch_tasks, add_tasks, remove_tasks, set_numbers, tasks_bubbleSort, tasks_edit_acts, get_edit_tasks_string
from Agile.views import BadHeaderError, sendmail, send_mail, EMAIL_HOST_USER
from Agile.views import datetime, timedelta
from Agile.views import client, db


class Test(SimpleTestCase):
    def test_remove_white_spaces_SE_func(self):
        self.assertEquals(remove_white_spaces_SE("   str_to_update    "), "str_to_update")

    def test_get_emails(self):
        self.assertEquals(get_emails(["Gaico10"]), ["gaico10@walla.com"])

    def test_get_id(self):
        self.assertEquals(get_id("gaico10@walla.com"), "Gaico10")

    def test_split_tasks_EliminateFalse(self):
        self.assertEquals(split_tasks("1) task one. 2) task two. 3) task three.", eliminate_empty=False), ['1) task one.', '2) task two.', '3) task three.'])

    def test_split_tasks_eliminateTrue(self):
        self.assertEquals(split_tasks("1) task one. 2) task two. 3) task three. 4) 5) five.", eliminate_empty=True), ['1) task one.', '2) task two.', '3) task three.', '4) five.'])

    def test_get_array_tasksToString(self):
        self.assertEquals(array_tasksToString(['1) task one.', '2) task two.', '3) task three.']), "1) task one.\n2) task two.\n3) task three.")

    def test_switch_tasks(self):
        self.assertEquals(switch_tasks(['1) task one.', '2) task two.', '3) task three.'], ['2) new task two.', '3) task three.', '4) new task four']), ['1) task one.', '2) new task two.', '3) task three.'])

    def test_add_tasks(self):
        self.assertEquals(add_tasks(['1) task one.', '2) task two.', '3) task three.'], ['2) new task two.', '3) task three.', '4) new task four']), ['1) task one.', '2) task two.', '3) task three.', '4) new task four'])

    def test_remove_tasks(self):
        self.assertEquals(remove_tasks(['1) task one.', '2) ', '3) task three.']), ['1) task one.', '3) task three.'])

    def test_set_numbers(self):
        self.assertEquals(set_numbers(['1) task one.', '3) task three.']), ['1) task one.', '2) task three.'])

    def test_set_numbers_one_task_add(self):  # if len(tasks_arr) == 1 and "29)" in tasks_arr[0]:  return tasks_arr
        self.assertEquals(set_numbers(['29) added task.']), ['29) added task.'])

    def test_tasks_bubbleSort(self):
        self.assertEquals(tasks_bubbleSort(['2) task two.', '3) task three.', '1) task one.']), ['1) task one.', '2) task two.', '3) task three.'])

    # integration test - tasks_edit_acts is using as a pipeline with: switch_tasks, add_tasks, remove_tasks, tasks_bubbleSort, set_numbers
    def test_tasks_tasks_edit_acts(self):
        self.assertEquals(tasks_edit_acts(['1) task one.', '2) task two.', '3) task three.'], '2) new task two. 4) new task four. 3) '), ['1) task one.', '2) new task two.', '3) new task four.'])

    # integration test - get_edit_tasks_string is using as a pipeline with: split_tasks, tasks_edit_acts
    def test_get_edit_tasks_string(self):
        self.assertEquals(get_edit_tasks_string('1) task one. 2) task two. 3) task three.', '2) new task two. 4) new task four. 3) '), '1) task one.\n2) new task two.\n3) new task four.')

    def test_SignUp_DBInsert(self):
        SV = db.users
        SV.delete_many({"ID": "Gaico10", "EMAIL": "gaico10@walla.com"})
        SV.delete_many({"ID": "", "EMAIL": ""})
        user = {
            "ID": "Gaico10",
            "PASSWORD": "123456",
            "EMAIL": "gaico10@walla.com",
            "TYPE": "Programmer",
            "FName": "Guy",
            "LName": "Cohen"
        }
        SV.insert_one(user)
        client.close()
        is_user_inserted = SV.find_one(user) is not None
        self.assertTrue(is_user_inserted)

    def test_sendmail(self):
        self.assertTrue(sendmail("test mail - subject", "test mail - body", [EMAIL_HOST_USER]))

    # integration - sign in and send an registration mail
    def test_SignUp_DBInsert_with_conformation(self):
        SV = db.users
        SV.delete_many({"ID": "Gaico10", "EMAIL": "gaico10@walla.com"})
        SV.delete_many({"ID": "", "EMAIL": ""})
        user = {
            "ID": "Gaico10",
            "PASSWORD": "123456",
            "EMAIL": "gaico10@walla.com",
            "TYPE": "Programmer",
            "FName": "Guy",
            "LName": "Cohen"
        }
        SV.insert_one(user)
        client.close()
        user_from_db = SV.find_one(user)
        is_user_inserted = user_from_db is not None

        if is_user_inserted:
            is_user_inserted = sendmail("test confirmation mail - subject", "test mail confurmation - body", [user_from_db["EMAIL"]])
        self.assertTrue(is_user_inserted)

    def test_LOGIN_DBFind_true(self):
        is_user_Exist = db.users.find_one({
            "ID": "Gaico10",
            "PASSWORD": "123456",
            "EMAIL": "gaico10@walla.com",
            "TYPE": "Programmer",
            "FName": "Guy",
            "LName": "Cohen"
        }) is not None
        self.assertTrue(is_user_Exist)

    def test_LOGIN_DBFind_false(self):
        is_user_Exist = db.users.find_one({
            "ID": "abcdefg123456789",
            "PASSWORD": "112344342",
            "EMAIL": "ppp@gmail.com",
            "TYPE": "friend",
            "FName": "Guy",
            "LName": "Cohen"
        }) is not None
        self.assertFalse(is_user_Exist)

    # 5,21,37
    def test_Project_DBFind_true(self):
        Programmer_list = get_emails(["Gaico10"])
        Clients_list = get_emails(["Gaico10"])

        is_project_Exist = db.projects.find_one({
            "ProjectName": "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "gaico10@walla.com",
            "Cilents": Clients_list,
            "Programmer": Programmer_list
        }) is not None
        self.assertTrue(is_project_Exist)

    def test_CreateProjDone_DBInsert(self):
        SV = db.projects
        Programmer_list = get_emails(["Gaico10"])
        Clients_list = get_emails(["Gaico10"])
        SV.delete_many({"ProjectName": "Test_project"})
        project = {
            "ProjectName": "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "gaico10@walla.com",
            "Cilents": Clients_list,
            "Programmer": Programmer_list
        }
        SV.insert_one(project)
        client.close()
        is_project_inserted = SV.find_one(project) is not None
        self.assertTrue(is_project_inserted)

    def test_Project_DBFind_false(self):
        is_project_Exist = db.projects.find_one({
            "ProjectName": "abcdefg123456789 ",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "Gaico10",
            "Cilents": None,
            "Programmer": None
        }) is not None
        self.assertFalse(is_project_Exist)

    # 6
    def test_update_project_programer_DBInsert_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName": "Test_project"},
            {"$addToSet": {"Programmer": "Test_programmer"}}
        )

        is_programmer_inserted = "Test_programmer" in SV.find_one({"ProjectName": "Test_project"})["Programmer"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    # 7
    def test_update_project_programer_DBRemoved_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName": "Test_project"},
            {"$pull": {"Programmer": "Test_programmer"}}
        )

        is_programmer_inserted = "Test_programmer" not in SV.find_one({"ProjectName": "Test_project"})["Programmer"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    # 8
    def test_update_project_Client_DBInsert_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName": "Test_project"},
            {"$addToSet": {"Clients": "Test_Client"}}
        )

        is_programmer_inserted = "Test_Client" in SV.find_one({"ProjectName": "Test_project"})["Clients"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    # 9
    def test_update_project_Client_DBRemoved_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName": "Test_project"},
            {"$pull": {"Clients": "Test_Client"}}
        )

        is_programmer_inserted = "Test_Client" not in SV.find_one({"ProjectName": "Test_project"})["Clients"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    # 11
    def test_RemoveTASK(self):
        SV = db.tasks
        SV.delete_many({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})
        is_task_removed = SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"}) is None
        self.assertTrue(is_task_removed)

    # 10
    def test_addTASK(self):
        SV = db.tasks
        SV.delete_many({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})
        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        uStory = remove_white_spaces_SE(uStory)
        projectName = remove_white_spaces_SE(projectName)
        task = {
            "ProjectName": projectName,
            "USERSTORY": uStory,
            "Tasks": "test_Tasks",
            "SDate": "test_SDate",
            "EDate": "test_EDate",
            "Programmer": "Gaico10",
            "status": "test_Status"
        }

        SV.insert_one(task)

        is_task_inserted = SV.find_one(task) is not None
        self.assertTrue(is_task_inserted)

    # integration - add a full task with smart add and getting the string of the tasks for display
    def test_ADDTASKS_smart(self):
        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        tasks = array_tasksToString(split_tasks("1) task one. 2) task two. 3) task three.", eliminate_empty=True))
        now = datetime.now()
        SDate = datetime.strptime("10.05.21 10:12", '%d.%m.%y %H:%M')
        EDate = now + timedelta(days=10)  # EDate = now + 10 days
        Programmer = "Gaico10"

        uStory = remove_white_spaces_SE(uStory)
        tasks = remove_white_spaces_SE(tasks)

        task = {
            "ProjectName": projectName,
            "USERSTORY": uStory,
            "Tasks": tasks,
            "SDate": SDate,
            "EDate": EDate,
            "Programmer": Programmer,
            "status": "TODO"
        }
        SV = db.tasks
        SV.insert_one(task)
        is_task_inserted = SV.find_one(task) is not None
        client.close()

        US_from_db = SV.find_one(task)  # tasks in US_from_db is a legit string of tasks
        is_task_inserted = US_from_db is not None

        if not is_task_inserted:
            self.assertTrue(is_task_inserted)
        else:
            self.assertEqual(US_from_db["Tasks"], "1) task one.\n2) task two.\n3) task three.")  # chack that the string is ready fot display after insert to DB

    # 12 - integration - update start/end time for task + time meeting
    def test_meet_times(self):
        now = datetime.now()
        SDate = datetime.strptime("10.05.21 11:12", '%d.%m.%y %H:%M')
        EDate = now + timedelta(days=10)  # EDate = now + 10 days

        db.tasks.find_one_and_update({"USERSTORY": "testUSERSTORY"}, {"$set": {"SDate": SDate, "EDate": EDate}}, upsert=True)  # update start/end time for task

        task = db.tasks.find_one({"USERSTORY": "testUSERSTORY", "SDate": SDate, "EDate": EDate})

        EDate = task["EDate"]
        if (EDate - timedelta(days=7)) >= now:  # EDate - timedelta(7) = EDate - 7 days
            color_view = "green"

        self.assertEqual(color_view, "green")

    # integration - update end time for task + time not meeting
    def test_not_meet_times(self):
        now = datetime.now()
        EDate = datetime.strptime("20.05.21 11:12", '%d.%m.%y %H:%M')

        db.tasks.find_one_and_update({"USERSTORY": "testUSERSTORY"}, {"$set": {"EDate": EDate}}, upsert=True)  # update end time for task

        task = db.tasks.find_one({"USERSTORY": "testUSERSTORY", "EDate": EDate})

        EDate = task["EDate"]
        if (EDate - timedelta(days=7)) < now:  # EDate - timedelta(7) = EDate - 7 days
            color_view = "red"

        self.assertEqual(color_view, "red")

    # 13,24,40
    def test_getTasksFromDb_to_KanbanPage_TODO(self):
        todo = list(db.tasks.find({"status": "TODO"}))
        is_tasks_status_match = True
        for t in todo:
            is_tasks_status_match += t["status"] == "TODO"
        self.assertTrue(is_tasks_status_match)

    # 14,25,41
    def test_getTasksFromDb_to_KanbanPage_inprogress(self):
        inprogress = list(db.tasks.find({"status": "INPROGRESS"}))
        is_tasks_status_match = True
        for t in inprogress:
            is_tasks_status_match += t["status"] == "INPROGRESS"
        self.assertTrue(is_tasks_status_match)

    # 15,27,42
    def test_getTasksFromDb_to_KanbanPage_done(self):
        done = list(db.tasks.find({"status": "DONE"}))
        is_tasks_status_match = True
        for t in done:
            is_tasks_status_match += t["status"] == "DONE"
        self.assertTrue(is_tasks_status_match)

    # 16,26,43
    def test_getTasksFromDb_to_KanbanPage_intest(self):
        intest = list(db.tasks.find({"status": "INTEST"}))
        is_tasks_status_match = True
        for t in intest:
            is_tasks_status_match += t["status"] == "INTEST"
        self.assertTrue(is_tasks_status_match)

    # 17,18,28,38
    def test_mail_sent(self):
        projectName = " Test_project  "
        sender = "unit test"
        mailDescription = "From - " + sender + " (type of user): " + "description of the emaill."
        message = "About Project: " + projectName + ".\nSender Mail: " + EMAIL_HOST_USER + "\n\n" + "Body of the email."
        has_sent = 0
        try:
            has_sent = send_mail(mailDescription, message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=True)
        except BadHeaderError:  # pragma: no cover
            print("Codnt send mail (Apparently the recipients email is incorrect). pleas try again later...")

        self.assertEqual(has_sent, 1)

    def test_mail_sent_t_few(self):
        projectName = " Test_project  "
        sender = "unit test"
        mailDescription = "From - " + sender + " (type of user): " + "description of the emaill."
        message = "About Project: " + projectName + ".\nSender Mail: " + EMAIL_HOST_USER + "\n\n" + "Body of the email."
        has_sent = 0
        try:
            has_sent = send_mail(mailDescription, message, EMAIL_HOST_USER, [EMAIL_HOST_USER, EMAIL_HOST_USER], fail_silently=True)
        except BadHeaderError:  # pragma: no cover
            print("Codnt send mail (Apparently the recipients email is incorrect). pleas try again later...")

        self.assertEqual(has_sent, 1)

    def test_mail_sent_not_legit(self):
        projectName = " Test_project  "
        sender = "unit test"
        mailDescription = "From - " + sender + " (type of user): " + "description of the emaill."
        message = "About Project: " + projectName + ".\nSender Mail: " + EMAIL_HOST_USER + "\n\n" + "Body of the email."
        has_sent = 0
        try:
            send_mail(mailDescription, message, EMAIL_HOST_USER, ["not_legit"], fail_silently=False)
        except BadHeaderError:  # pragma: no cover
            has_sent = 0

        self.assertEqual(has_sent, 0)

    def test_mail_sent_empty(self):
        projectName = " Test_project  "
        sender = "unit test"
        mailDescription = "From - " + sender + " (type of user): " + "description of the emaill."
        message = "About Project: " + projectName + ".\nSender Mail: " + EMAIL_HOST_USER + "\n\n" + "Body of the email."
        has_sent = 0
        try:
            has_sent = send_mail(mailDescription, message, EMAIL_HOST_USER, [], fail_silently=True)
        except BadHeaderError:  # pragma: no cover
            print("Codnt send mail (Apparently the recipients email is incorrect). pleas try again later...")

        self.assertEqual(has_sent, 0)

    # 29,36
    def test_Update_TaskStatus(self):
        SV = db.tasks
        SV.delete_many({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})
        SV.insert_one({
            "ProjectName": "Test_project",
            "USERSTORY": "testUSERSTORY",
            "Tasks": "test_Tasks",
            "SDate": "test_SDate",
            "EDate": "test_EDate",
            "Programmer": "Gaico10",
            "status": "test_Status",
        })
        SV.find_one_and_update(
            {"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"},
            {"$set": {"status": "TODO"}}
        )
        is_status_inserted = "TODO" == SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})["status"]

        client.close()
        self.assertTrue(is_status_inserted)

    # 30
    def test_Update_TaskStatus_INPROGRESS(self):
        SV = db.tasks
        SV.find_one_and_update(
            {"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"},
            {"$set": {"status": "INPROGRESS"}}
        )
        is_status_inserted = "INPROGRESS" == SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})["status"]
        client.close()
        self.assertTrue(is_status_inserted)

    # 31
    def test_Update_TaskStatus_INTEST(self):
        SV = db.tasks
        SV.find_one_and_update(
            {"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"},
            {"$set": {"status": "INTEST"}}
        )
        is_status_inserted = "INTEST" == SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})["status"]
        client.close()
        self.assertTrue(is_status_inserted)

    # 32
    def test_Update_TaskStatus_TODO(self):
        SV = db.tasks
        SV.find_one_and_update(
            {"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"},
            {"$set": {"status": "TODO"}}
        )
        is_status_inserted = "TODO" == SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})["status"]
        client.close()
        self.assertTrue(is_status_inserted)

    # 33
    def test_Update_TaskStatus_DONE(self):
        SV = db.tasks

        SV.find_one_and_update(
            {"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"},
            {"$set": {"status": "DONE"}}
        )
        is_status_inserted = "DONE" == SV.find_one({"ProjectName": "Test_project", "USERSTORY": "testUSERSTORY"})["status"]
        client.close()
        self.assertTrue(is_status_inserted)

    def test_EditTasks(self):
        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        uStory = remove_white_spaces_SE(uStory)
        projectName = remove_white_spaces_SE(projectName)

        DB = db.tasks

        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})
        newvalues = {"$set": {"Tasks": "1) task one.\n2) task two.\n3) task three."}}
        DB.update_one(myquery, newvalues)

        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})
        self.assertEqual("1) task one.\n2) task two.\n3) task three.", myquery['Tasks'])

    # integration - edit task with smart edit and getting the string of the tasks for display
    def test_EditTasks_smart(self):
        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        uStory = remove_white_spaces_SE(uStory)
        projectName = remove_white_spaces_SE(projectName)

        tasks = '   2) new task two. 4) new task four. 3) '

        tasks = remove_white_spaces_SE(tasks) + " "

        DB = db.tasks

        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})
        newvalues = {"$set": {"ProjectName": projectName}}
        if myquery:
            tasks = get_edit_tasks_string(myquery["Tasks"], tasks)
            newvalues["$set"]["Tasks"] = tasks

        DB.update_one(myquery, newvalues)
        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})
        self.assertEqual(myquery['Tasks'], '1) task one.\n2) new task two.\n3) new task four.')

    # 44
    def test_rate_add(self):
        db.tasks.find_one_and_update({"USERSTORY": "testUSERSTORY"}, {"$set": {"RATE": "3"}}, upsert=True)
        is_rated = db.tasks.find_one({"USERSTORY": "testUSERSTORY", "RATE": "3"}) is None
        self.assertFalse(is_rated)

    def test_rate_update(self):
        db.tasks.find_one_and_update({"USERSTORY": "testUSERSTORY"}, {"$set": {"RATE": "5"}}, upsert=True)
        is_rate_updated = db.tasks.find_one({"USERSTORY": "testUSERSTORY", "RATE": "5"}) is None
        self.assertFalse(is_rate_updated)

    def test_homepage_url(self):
        response = self.client.get('./Templates/Agile/')
        self.assertEquals(response.status_code, 404)

    def test_SIGNUP_url(self):
        user = {"ID": "test_user", "PASSWORD": "test_password", "EMAIL": "test@gmail.com", "TYPE": "Admin"}
        response = self.client.post('./Templates/Agile/SIGNUP', data=user, follow=True)
        self.assertEquals(response.status_code, 404)

    def test_LOGIN_url(self):
        response = self.client.get('./Templates/Agile/LOGIN')
        self.assertEquals(response.status_code, 404)

    def test_SignUpDone_url(self):
        response = self.client.get('./Templates/Agile/SignUpDone')
        self.assertEquals(response.status_code, 404)

    # integration - signup and then login
    def test_signup_and_login(self):
        # signup
        SV = db.users
        SV.delete_many({"ID": "Gaico10", "EMAIL": "gaico10@walla.com"})
        SV.delete_many({"ID": "", "EMAIL": ""})
        user = {
            "ID": "Gaico10",
            "PASSWORD": "123456",
            "EMAIL": "gaico10@walla.com",
            "TYPE": "Programmer",
            "FName": "Guy",
            "LName": "Cohen"
        }
        # login
        SV.insert_one(user)
        is_user_Exist = db.users.find_one({
            "ID": "Gaico10",
            "PASSWORD": "123456",
            "EMAIL": "gaico10@walla.com",
            "TYPE": "Programmer",
            "FName": "Guy",
            "LName": "Cohen"
        }) is not None
        self.assertTrue(is_user_Exist)

    # integration - create a project and edit
    def test_createproj_and_edit(self):
        # create Project
        SV = db.projects
        Programmer_list = get_emails(["Gaico10"])
        Clients_list = get_emails(["Gaico10"])
        SV.delete_many({"ProjectName": "Test_project"})
        project = {
            "ProjectName": "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "gaico10@walla.com",
            "Cilents": Clients_list,
            "Programmer": Programmer_list
        }
        SV.insert_one(project)
        # update project
        Programmer_list = get_emails(["Gaico10"])
        Clients_list = get_emails(["Gaico10"])

        is_project_Exist = db.projects.find_one({
            "ProjectName": "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "gaico10@walla.com",
            "Cilents": Clients_list,
            "Programmer": Programmer_list
        }) is not None
        self.assertTrue(is_project_Exist)

    # integration - create a user story and edit
    def test_createtask_and_edit(self):
        SV = db.tasks

        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        uStory = remove_white_spaces_SE(uStory)
        projectName = remove_white_spaces_SE(projectName)
        task = {
            "ProjectName": projectName,
            "USERSTORY": uStory,
            "Tasks": "test_Tasks",
            "SDate": "test_SDate",
            "EDate": "test_EDate",
            "Programmer": "Gaico10",
            "status": "test_Status"
        }

        SV.insert_one(task)
        projectName = " Test_project  "
        uStory = " testUSERSTORY "

        uStory = remove_white_spaces_SE(uStory)
        projectName = remove_white_spaces_SE(projectName)

        DB = db.tasks

        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})
        newvalues = {"$set": {"Tasks": "test_Tasks_after_change"}}
        DB.update_one(myquery, newvalues)

        myquery = DB.find_one({"ProjectName": projectName, "USERSTORY": uStory})

        self.assertEqual("test_Tasks_after_change", myquery['Tasks'])
