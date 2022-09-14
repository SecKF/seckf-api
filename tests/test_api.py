"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import json

from tests import settings


def login(testapp):
    """Performs a login action and returns the jwt token"""
    payload = {'username': 'testadmin', 'password': 'testadmin'}
    headers = {'content-type': 'application/json'}
    res = testapp.post('/api/user/login', params=json.dumps(payload), headers=headers)
    assert res.status_code == 200
    response_dict = res.json
    return response_dict.get('Authorization token')


class TestStatus:
    """Status"""

    def test_is_available(self, testapp):
        """App is available"""
        res = testapp.get("/api/")
        assert res.status_code == 200
        assert b'OWASP-SKF API' in res


class TestApi:
    """User login and operations"""

    def test_user_list(self, testapp):
        jwt = login(testapp)
        headers = {'Authorization': jwt}
        res = testapp.get("/api/user/list", headers=headers)
        print(res)
        assert res.status_code == 200

    def test_activate_user(self, testapp):
        """Test if the activate user call is working"""
        payload = {'accessToken': 1234, 'email': 'example@owasp.org', 'password': 'admin', 'repassword': 'admin',
                   'username': 'admin'}
        headers = {'content-type': 'application/json'}
        res = testapp.put("/api/user/activate/1", params=json.dumps(payload), headers=headers)
        assert res.status_code == 200
        response_dict = res.json
        assert response_dict['message'] == "User successfully activated"

    def test_fail_token_activate_user(self, testapp):
        """Test if the fail token activate user call is working"""
        payload = {'accessToken': 123, 'email': 'example@owasp.org', 'password': 'admin', 'repassword': 'admin',
                   'username': 'admin'}
        headers = {'content-type': 'application/json'}
        response = testapp.put('/api/user/activate/1', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "User could not be activated"

    def test_fail_email_activate_user(self, testapp):
        """Test if the fail email activate user call is working"""
        payload = {'accessToken': 1234, 'email': 'woop@owasp.org', 'password': 'admin', 'repassword': 'admin',
                   'username': 'admin'}
        headers = {'content-type': 'application/json'}
        response = testapp.put('/api/user/activate/1', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "User could not be activated"

    def test_fail_password_activate_user(self, testapp):
        """Test if the fail password activate user call is working"""
        payload = {'accessToken': 1234, 'email': 'example@owasp.org', 'password': 'admin', 'repassword': 'admintypo',
                   'username': 'admin'}
        headers = {'content-type': 'application/json'}
        response = testapp.put('/api/user/activate/1', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "User could not be activated"

    def test_login(self, testapp):
        """Test if the login call is working"""
        auth_token = login(testapp)
        assert len(auth_token) > 32

    def test_fail_user_login(self, testapp):
        """Test if the fail user login call is working"""
        payload = {'username': 'adm', 'password': 'admin'}
        headers = {'content-type': 'application/json'}
        response = testapp.post('/api/user/login', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "Login was failed"

    def test_fail_password_login(self, testapp):
        """Test if the fail password login call is working"""
        payload = {'username': 'admin', 'password': 'bla'}
        headers = {'content-type': 'application/json'}
        response = testapp.post('/api/user/login', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "Login was failed"

    def test_login_create(self, testapp):
        """Test if the login create call is working"""
        jwt = login(testapp)
        payload = {'email': 'woop@owasp.org', 'privilege_id': 2}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['email'] == "woop@owasp.org"

    def test_login_list(self, testapp):
        """Test if the login list call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.get('/api/user/list', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['username'] == "admin"

    def test_user_manage(self, testapp):
        """Test if the user manage call is working"""
        jwt = login(testapp)
        payload = {'active': 'False'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/user/manage/2', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "User successfully managed"

    def test_expired_login_create(self, testapp):
        """Test if the expired token login create call is working"""
        payload = {'email': 'test@owasp.org', 'privilege_id': 2}
        headers = {'content-type': 'application/json',
                   'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VySWQiOjEsImlhdCI6MTQ5NjQxMzg1NiwicHJpdmlsZWdlIjoiZWRpdDpyZWFkOm1hbmFnZTpkZWxldGUiLCJleHAiOjE0OTY0MjEwNTZ9.FkwLGwLNqPi87JC8nl2muRB5QLNk01r4XFcaFdFHiDc'}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 403
        response_dict = response.json
        assert response_dict['message'] == "JWT decode error"

    def test_decode_login_create(self, testapp):
        """Test if the decode token login create call is working"""
        payload = {'email': 'test@owasp.org', 'privilege_id': 2}
        headers = {'content-type': 'application/json',
                   'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VySWQiOjEsImlhdCI6MTQ5NjQxMzg1NiwicHJpdmlsZWdlIjoiZWRpdDpyZWFkOm1hbmFnZTpkZWxldGUiLCJleHAiOjE0OTY0MjEwNTZ9.FkwLGwLNqPi87JC8nl2muRB5QLNk01r4XFfoobar'}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 403
        response_dict = response.json
        assert response_dict['message'] == "JWT decode error"

    def test_login_create_priv(self, testapp):
        """Test if the login create privilege_id call is working"""
        jwt = login(testapp)
        payload = {'email': 'test_user2@owasp.org', 'privilege_id': 1}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['email'] == "test_user2@owasp.org"

    def test_get_checklist(self, testapp):
        """Test if the get checklist items call is working"""
        response = testapp.get('/api/checklist/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['checklist_items_checklist_id'] == '1.0'

    def test_update_checklist_item_15(self, testapp):
        """Test if the update specific checklist item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"content": "This is a updated checklist item", "kb_id": 319, "checklist_id": "1.9.1", "maturity": 2,
                   "include_always": "False", "question_id": 8, "add_resources": "http://google.com"}
        response = testapp.put('/api/checklist/update/item/19', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist item successfully updated"

    def test_get_checklist_types(self, testapp):
        """Test if the get all checklist types call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.get('/api/checklist_types/types/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] == 'Architecture, Design and Threat Modeling Requirements'

    def test_new_checklist_cat(self, testapp):
        """Test if the create new checklist category call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"description": "This is a checklist cat description", "name": "Custom security category"}
        response = testapp.put('/api/checklist_category/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist category successfully created"

    def test_update_checklist_cat(self, testapp):
        """Test if the update checklist type call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"name": "Custom security category update",
                   "description": "This is a checklist category description update"}
        response = testapp.put('/api/checklist_category/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist category successfully updated"

    def test_delete_checklist_cat(self, testapp):
        """Test if the delete checklist category call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/checklist_category/delete/2', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist category successfully deleted"

    def test_get_checklist_cat(self, testapp):
        """Test if the get all checklist category call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.get('/api/checklist_category/items', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['name'] == 'Web applications'

    def test_get_checklist_cat_item(self, testapp):
        """Test if the get item checklist category call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.get('/api/checklist_category/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['name'] == 'Web applications'

    def test_new_checklist_type(self, testapp):
        """Test if the create new checklist type call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"description": "This is a checklist type description", "name": "Custom security list",
                   "visibility": 1}
        response = testapp.put('/api/checklist_category/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist category successfully created"

    def test_update_checklist_type(self, testapp):
        """Test if the update checklist type call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"description": "This is a checklist type description update", "name": "Custom security list new",
                   "visibility": 1}
        response = testapp.put('/api/checklist_types/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist item successfully updated"

    def test_delete_checklist_type(self, testapp):
        """Test if the delete checklist type call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/checklist_types/delete/20', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist type successfully deleted"

    def test_new_checklist_item(self, testapp):
        """Test if the create new checklist item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {"content": "This is a new checklist item", "maturity": 1, "kb_id": 12, "include_always": "False",
                   "question_id": 0, "checklist_id": "14.5.41", "add_resources": "http://test.com"}
        response = testapp.put('/api/checklist/new/item/type/13', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist item successfully created"

    def test_delete_checklist_item(self, testapp):
        """Test if the delete a checklist item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/checklist/delete/item/31', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Checklist item successfully deleted"

    def test_get_checklist_question_sprint_3(self, testapp):
        """Test if the get specific checklist item correlated to question sprint call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.get('/api/checklist/item/question_sprint/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['kb_item_id'] == '272'

    def test_get_checklist_item_10(self, testapp):
        """Test if the get specific checklist item call is working"""
        response = testapp.get('/api/checklist/item/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['checklist_id'] == '1.0'

    def test_get_checklist_items_level1(self, testapp):
        """Test if the get specific ASVS checklist item by level call is working"""
        response = testapp.get('/api/checklist/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['checklist_items_content'][0:30] == 'Architecture, Design and Threa'

    def test_get_checklist_items_level2(self, testapp):
        """Test if the get specific ASVS checklist item by level 2 call is working"""
        response = testapp.get('/api/checklist/items/2')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['checklist_items_content'][0:30] == 'Authentication Verification Re'

    def test_get_labs(self, testapp):
        """Test if the get labs items call is working"""
        response = testapp.get('/api/interactive_labs/items')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] == "Path traversal (LFI)"

    def test_get_labs_code_solutions(self, testapp):
        """Test if the get labs code solution items call is working"""
        response = testapp.get('/api/interactive_labs/code/items/solutions/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['vuln'] == "Denial Of Service"

    def test_get_labs_code_items(self, testapp):
        """Test if the get labs code items call is working"""
        response = testapp.get('/api/interactive_labs/code/items/type/php')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['id'] == 1

    def test_get_labs_code_solutions_correct(self, testapp):
        """Test if the get labs code solution item is correct call is working"""
        response = testapp.get('/api/interactive_labs/code/items/code/1/solution/2')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['status'] == "correct"

    def test_get_labs_code_solutions_incorrect(self, testapp):
        """Test if the get labs code solution item is incorrect call is working"""
        response = testapp.get('/api/interactive_labs/code/items/code/1/solution/22')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['status'] == "incorrect"

    def test_get_kb(self, testapp):
        """Test if the get kb items call is working"""
        response = testapp.get('/api/kb/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] == "empty control"

    def test_get_kb_item_10(self, testapp):
        """Test if the get specific kb item call is working"""
        response = testapp.get('/api/kb/9')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['title'] == "J2EE Misconfiguration Weak Access Permissions for EJB Methods"

    def test_update_kb(self, testapp):
        """Test if the update kb items call is working"""
        jwt = login(testapp)
        payload = {'content': 'Unit test content update', 'title': 'Unit test title update'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/kb/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "KB item successfully updated"
        response = testapp.get('/api/kb/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] == "empty control"

    def test_new_kb(self, testapp):
        """Test if the create kb items call is working"""
        jwt = login(testapp)
        payload = {'content': 'Unit test content new', 'title': 'Unit test title new'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/kb/new/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "KB item successfully created"

    def test_create_project(self, testapp):
        """Test if the create new project call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description project', 'name': 'Unit test name project',
                   'version': 'version 1.0'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Project successfully created"

    def test_create_project_fail(self, testapp):
        """Test if the create new project fail call is working"""
        jwt = login(testapp)
        payload = {'description_wrong': 'Unit test description project'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400

    def test_project_items(self, testapp):
        """Test if the project items call is working"""
        jwt = login(testapp)
        headers = {'Authorization': jwt}
        response = testapp.get('/api/project/items', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['name'] == "Design Patterns ASVS LvL 1"

    def test_delete_project_item(self, testapp):
        """Test if the delete project item call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description project', 'name': 'Unit test name project',
                   'checklist_type': 1, 'version': 'version 1.0'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Project successfully created"
        response = testapp.delete('/api/project/delete/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Project successfully deleted"

    def test_create_sprint(self, testapp):
        """Test if the create new sprint call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description sprint', 'name': 'Unit test name sprint', 'project_id': 1}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/sprint/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully created"

    def test_create_sprint_fail(self, testapp):
        """Test if the create new sprint fail call is working"""
        jwt = login(testapp)
        payload = {'description_wrong': 'Unit test description sprint'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/sprint/new', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400

    def test_sprint_item(self, testapp):
        """Test if the sprint item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        payload = {'description': 'Unit test description sprint', 'name': 'Unit test name sprint', 'project_id': 2}
        response = testapp.put('/api/sprint/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully created"
        response = testapp.get(f"/api/sprint/{response_dict['sprint_id']}", headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['name'] == "Unit test name sprint"

    def test_update_sprint_item(self, testapp):
        """Test if the sprint update call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description sprint update', 'name': 'Unit test name sprint update',
                   'project_id': 3}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/sprint/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully updated"
        response = testapp.get('/api/sprint/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['name'] == "Unit test name sprint update"

    def test_delete_sprint_item(self, testapp):
        """Test if the delete project item call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description sprint', 'name': 'Unit test name sprint', 'project_id': 2}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/sprint/new', params=json.dumps(payload), headers=headers)
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully created"
        response = testapp.delete('/api/sprint/delete/2', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully deleted"

    def test_results_sprint(self, testapp):
        """Test if the results sprint call is working"""
        jwt = login(testapp)
        payload = {'description': 'Unit test description project', 'name': 'Unit test name project',
                   'checklist_type': 2, 'version': 'version 1.0'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Project successfully created"
        payload = {'description': 'Unit test description sprint', 'name': 'Unit test name sprint', 'project_id': 3}
        response = testapp.put('/api/sprint/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        payload = {
            'questions': [{'project_id': 3, 'question_id': 1, 'result': 'True', 'sprint_id': 2, 'checklist_type': 1},
                          {'project_id': 3, 'question_id': 2, 'result': 'True', 'sprint_id': 2, 'checklist_type': 1}]}
        response = testapp.put('/api/questions/store/1/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Sprint successfully created"
        response = testapp.get('/api/sprint/stats/2', headers=headers)
        assert response.status_code == 200
        response = testapp.get('/api/sprint/results/2', headers=headers)
        assert response.status_code == 200
        response = testapp.get('/api/sprint/results/export/2', headers=headers)
        assert response.status_code == 200

    def test_delete_project_item_fail(self, testapp):
        """Test if the delete project item fail call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/project/delete/79', headers=headers, expect_errors=True)
        assert response.status_code == 400

    def test_question_items(self, testapp):
        """Test if the get questions item call is working"""
        headers = {'content-type': 'application/json'}
        response = testapp.get('/api/questions/items/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['question'] == "Secure Software Development Lifecycle Requirements"

    def test_question_update(self, testapp):
        """Test if the update questions item call is working"""
        jwt = login(testapp)
        payload = {'question': 'Unit test question', 'checklist_type': 1}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/questions/item/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == 'Question successfully updated'

    def test_question_new(self, testapp):
        """Test if the new question item call is working"""
        jwt = login(testapp)
        payload = {'question': 'New Unit test question', 'checklist_type': 1}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/questions/item/new', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == 'New Question successfully created'

    def test_question_delete(self, testapp):
        """Test if the delete question item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/questions/item/delete/1', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Question successfully deleted"

    def test_auth_protected_call(self, testapp):
        """Test if the delete project item fail call is working"""
        payload = {'description': 'Unit test description project', 'name': 'Unit test name project',
                   'checklist_type': 1, 'version': 'version 1.0'}
        headers = {'content-type': 'application/json', 'Authorization': 'woopwoopwrong'}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 403

    def test_get_code(self, testapp):
        """Test if the get code items call is working"""
        response = testapp.get('/api/code/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] != ""

    def test_get_code_item_10(self, testapp):
        """Test if the get specific code item call is working"""
        response = testapp.get('/api/code/10')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['title'] != ""

    def test_update_code(self, testapp):
        """Test if the update code items call is working"""
        jwt = login(testapp)
        payload = {'code_lang': 'php', 'content': 'Unit test content update', 'title': 'Unit test title update'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/code/update/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Code example item successfully updated"
        response = testapp.get('/api/code/items/1')
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['items'][0]['title'] == "Unit test title update"

    def test_create_code(self, testapp):
        """Test if the create code items call is working"""
        jwt = login(testapp)
        payload = {'code_lang': 'test', 'content': 'Unit test content create', 'title': 'Unit test title create'}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/code/new/1', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Code example item successfully created"
        response = testapp.get('/api/code/items/1')
        assert response.status_code == 200

    def test_delete_code(self, testapp):
        """Test if the delete code item call is working"""
        jwt = login(testapp)
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.delete('/api/code/delete/100', headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['message'] == "Code example item successfully deleted"

    def test_get_description_item(self, testapp):
        """Test if the description call is working"""
        payload = {"question": "what is xss?", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            res = response_dict['options'][0]['answer'][0:29]
            assert res == "Description for XSS injection"

    def test_get_solution_item(self, testapp):
        """Test if the solution call is working"""
        payload = {"question": "how to resolve xss?", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            res = response_dict['options'][0]['answer'][0:26]
            assert res == "Solution for XSS injection"

    def test_code_item_list(self, testapp):
        """Test if the code item is working"""
        payload = {"question": "code for xss filtering?", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert response_dict['options'][0]['answer'] == "Code xss filtering in java"

    def test_no_match(self, testapp):
        """Test if the options are working"""
        payload = {"question": "what is bla?", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert response_dict['options'][0]['answer'] == "Please be more specific"

    def test_get_entity2_item(self, testapp):
        """Test if the options are working"""
        payload = {"question": "what are security headers?", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert response_dict['options'][0]['answer'][0:45] == "Description for API responses security header"

    def test_get_sol_entity2_item(self, testapp):
        """Test if the options are working"""
        payload = {"question": "how to solve rest csrf", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert (response_dict['options'][0]['answer'] == "Solution user restriction for sensitive data") or (
                    response_dict['options'][0]['answer'] == "Solution csrf on rest")

    def test_code_lang_item2(self, testapp):
        """Test if the options are working"""
        payload = {"question": "code example for xss", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert (response_dict['options'][0]['answer']) == "Code encoder" or (
                response_dict['options'][0]['answer']) == "Code xss filtering" or (
                       response_dict['options'][0]['answer']) == "Code x xss protection header" or (
                       response_dict['options'][0]['answer']) == "Code encoder sql esapi"

    def test_code_lang_item(self, testapp):
        """Test if the options are working"""
        payload = {"question": "code example for code encoder", "question_option": 0, "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            assert response_dict['options'][0]['answer'] == "Code encoder in php"

    def test_code_classify_item(self, testapp):
        """Test if the code classify is working"""
        payload = {"question": "code example for xss filtering in java", "question_option": 0,
                   "question_lang": "string"}
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        response = testapp.post('/api/chatbot/question', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        if not settings.GOOGLE:
            res = response_dict['options'][0]['answer'][0:23]
            assert res == "Code for  XSS filtering"

    def test_assert_403_project_new(self, testapp):
        payload = {'description': 'Unit test description project', 'name': 'Unit test name project',
                   'checklist_type': 1, 'version': 'version 1.0'}
        headers = {'content-type': 'application/json'}
        response = testapp.put('/api/project/new', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 403

    def test_assert_403_project_delete(self, testapp):
        payload = {'test': 'test'}
        headers = {'content-type': 'application/json'}
        response = testapp.delete('/api/project/delete/1', params=json.dumps(payload), headers=headers,
                                  expect_errors=True)
        assert response.status_code == 403

    def test_assert_403_user_create(self, testapp):
        payload = {'email': 'test_user123@owasp.org', 'privilege_id': 1}
        headers = {'content-type': 'application/json'}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 403

    def test_assert_400_user_create(self, testapp):
        """Test if the login fail create call is working"""
        jwt = login(testapp)
        payload = {'email': 'test_user@owasp.org', 'privilege_id': 2}
        headers = {'content-type': 'application/json', 'Authorization': jwt}
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers)
        assert response.status_code == 200
        response_dict = response.json
        assert response_dict['email'] == "test_user@owasp.org"
        response = testapp.put('/api/user/create', params=json.dumps(payload), headers=headers, expect_errors=True)
        assert response.status_code == 400
        response_dict = response.json
        assert response_dict['message'] == "User could not be created"
