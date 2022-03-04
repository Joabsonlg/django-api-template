from rest_framework.test import APITestCase

from users.models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='a2d4g6rr'
        )

    def test_login(self):
        """
        Ensure we can login a user.
        """
        url = '/api/v1/jwt/create/'
        data = {
            'username': 'testuser',
            'password': 'a2d4g6rr'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_password(self):
        """
        Ensure we can login a user.
        """
        url = '/api/v1/jwt/create/'
        data = {
            'username': 'testuser',
            'password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_login_with_wrong_username(self):
        """
        Ensure we can login a user.
        """
        url = '/api/v1/jwt/create/'
        data = {
            'username': 'wrong_username',
            'password': 'a2d4g6rr'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)


class UserTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testusertest', password='a2d4g6rt')
        self.token = self.login().data['access']

    def login(self):
        data = {
            'username': 'testusertest',
            'password': 'a2d4g6rt',
            'email': 'teste@email.com'
        }
        url = '/api/v1/jwt/create/'
        return self.client.post(url, data, format='json')

    def createUser(self):
        url = '/api/v1/users/'
        data = {
            'username': 'testuser',
            'email': 'teste@email.com',
            'password': 'a2d4g6rr',
            're_password': 'a2d4g6rr'
        }
        return self.client.post(url, data, format='json')

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        response = self.createUser()
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'teste@email.com')
        self.assertTrue(user.is_active, True)
        self.assertFalse(user.is_staff, False)
        self.assertFalse(user.is_superuser, False)

    def test_create_user_with_commom_password(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'testuser',
            'email': 'j@g.com',
            'password': '123456',
            're_password': '123456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_without_password(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'testuser',
            'email': 'teste@email.com',
            're_password': 'a2d4g6rr'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'], ['Este campo é obrigatório.'])

    def test_create_user_without_username(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'email': 'teste@email.com',
            'password': 'a2d4g6rr',
            're_password': 'a2d4g6rr'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'], ['Este campo é obrigatório.'])

    def test_create_user_without_re_password(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'testuser',
            'email': 'teste@email.com',
            'password': 'a2d4g6rr'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['re_password'], ['Este campo é obrigatório.'])

    def test_create_user_with_wrong_re_password(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'testuser',
            'email': 'teste@email.com',
            'password': 'a2d4g6rr',
            're_password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        url = '/api/v1/users/1/'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testusertest')

    def test_retrieve_user_with_wrong_id(self):
        """
        Ensure we can retrieve a user object.
        """
        url = '/api/v1/users/10/'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 404)

    def test_retrieve_user_without_authentication(self):
        """
        Ensure we can retrieve a user object.
        """
        url = '/api/v1/users/{}/'.format(1)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        url = '/api/v1/users/1/'
        data = {
            'username': 'testuser',
            'email': 'teste@test.com',
            'password': 'a2d4g6rr',
            're_password': 'a2d4g6rr'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'teste@test.com')

    def test_update_user_without_authentication(self):
        """
        Ensure we can update a user object.
        """
        url = '/api/v1/users/1/'
        data = {
            'username': 'testuser',
            'email': 'teste@test.com',
            'password': 'a2d4g6rr',
            're_password': 'a2d4g6rr'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_user_with_wrong_id(self):
        """
        Ensure we can update a user object.
        """
        url = '/api/v1/users/10/'
        data = {
            'username': 'testuser',
            'email': 'teste@test.com',
            'password': 'a2d4g6rr',
            're_password': 'a2d4g6rr'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 404)

    def test_update_user_without_password(self):
        """
        Ensure we can update a user object.
        """
        url = '/api/v1/users/1/'
        data = {
            'username': 'testuser',
            'email': 'teste@test.com'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
        url = '/api/v1/users/1/'
        response = self.client.delete(url, {'current_password': 'a2d4g6rt'}, format='json',
                                      HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 204)

    def test_delete_user_without_authentication(self):
        """
        Ensure we can delete a user object.
        """
        url = '/api/v1/users/1/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_user_with_wrong_id(self):
        """
        Ensure we can delete a user object.
        """
        url = '/api/v1/users/10/'
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 404)

    def test_delete_user_without_id(self):
        """
        Ensure we can delete a user object.
        """
        url = '/api/v1/users/'
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 405)

    def test_list_users(self):
        """
        Ensure we can list users objects.
        """
        url = '/api/v1/users/'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, 200)
