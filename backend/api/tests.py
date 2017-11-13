from django.test import TestCase, Client
from .models import User, create_user, Room
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.urls import reverse
from django.core.files import File
from backend.settings import BASE_DIR
from io import BytesIO
import json
import hashlib
import os


class ApiRoomListTest(TestCase):
    def setUp(self):
        create_user(
            username='skystar',
            password='doge',
            nickname='usezmap',
            email='asdf@asdf.com'
        )

        cache.clear()

    def test_room_initially_no_rooms(self):
        client = Client()
        client.login(username='skystar', password='doge')

        response = client.get(
            reverse('room')
        )

        data = response.json()

        self.assertEqual(len(data), 0)

    def test_room_create_without_password(self):
        client = Client()
        client.login(username='skystar', password='doge')

        post_data = {
            'title': 'doge room',
        }

        response = client.post(
            reverse('room'),
            json.dumps(post_data),
            content_type='application/json',
        )

        data = response.json()
        room_data = cache.get('room:' + data['room_id'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['room_id'], room_data['room_id'])
        self.assertIs(data['is_private'], False)

        response = client.get(
            reverse('room')
        )

        data = response.json()

        self.assertEqual(data[0]['title'], 'doge room')
        self.assertEqual(data[0]['is_private'], False)

    def test_room_create_with_password(self):
        client = Client()
        client.login(username='skystar', password='doge')

        post_data = {
            'title': 'doge room',
            'password': 'dogecoin',
        }

        response = client.post(
            reverse('room'),
            json.dumps(post_data),
            content_type='application/json',
        )

        data = response.json()
        room_data = cache.get('room:' + data['room_id'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['room_id'], room_data['room_id'])
        self.assertIs(data['is_private'], True)

        self.assertEqual(response.status_code, 201)

        response = client.get(
            reverse('room')
        )

        data = response.json()
        room = Room.objects.get(id=1)

        hashed_password = hashlib.sha256(b'dogecoin').hexdigest()

        self.assertEqual(data[0]['title'], 'doge room')
        self.assertEqual(data[0]['is_private'], True)
        self.assertEqual(room.password, hashed_password)


class ApiProfileTest(TestCase):
    def setUp(self):
        user = create_user(
            username='skystar',
            password='doge',
            nickname='usezmap',
            email='asdf@asdf.com'
        )
        image_path = os.path.join(BASE_DIR, 'api/test_data/test_image.png')

        with open(image_path, 'rb') as f:
            avatar_file = File(f)
            avatar_file.name = 'test_image.png'
            user.profile.avatar = avatar_file
            user.profile.save()

    def test_profile_not_authenticated(self):
        client = Client()

        post_data = {
            'nickname': 'new_nick',
        }

        response = client.put(
            reverse('profile', kwargs={'username': 'skystar'}),
            json.dumps(post_data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)

    def test_get_profile(self):
        client = Client()
        client.login(username='skystar', password='doge')

        response = client.get(
            reverse('profile', kwargs={'username': 'skystar'})
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['nickname'], 'usezmap')

    def test_edit_profile(self):
        client = Client()
        client.login(username='skystar', password='doge')

        post_data = {
            'nickname': 'new_nick',
        }

        response = client.put(
            reverse('profile', kwargs={'username': 'skystar'}),
            json.dumps(post_data),
            content_type='application/json',
        )

        user = User.objects.get(id=1)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(user.profile.nickname, 'new_nick')

    def test_avatar_not_authenticated(self):
        client = Client()

        response = client.get(
            reverse('avatar')
        )

        self.assertEqual(response.status_code, 401)

    def test_avatar_valid_image(self):
        client = Client()
        client.login(username='skystar', password='doge')

        user = User.objects.get(id=1)

        image_path = os.path.join(BASE_DIR, 'api/test_data/test_image.png')

        with open(image_path, 'rb') as f:
            response = client.post(
                reverse('avatar'),
                {'avatar': f}
            )

        os.remove(user.profile.avatar.path)
        self.assertEqual(response.status_code, 204)

    def test_avatar_invalid_image(self):
        client = Client()
        client.login(username='skystar', password='doge')

        f = BytesIO(os.urandom(100))
        response = client.post(
            reverse('avatar'),
            {'avatar': f}
        )

        self.assertEqual(response.status_code, 400)

    def test_avatar_large_image(self):
        client = Client()
        client.login(username='skystar', password='doge')

        f = BytesIO(os.urandom(1024 * 1024 * 2))
        response = client.post(
            reverse('avatar'),
            {'avatar': f}
        )

        self.assertEqual(response.status_code, 413)


class ApiSignUpTest(TestCase):
    def setUp(self):
        pass

    def test_sign_up_success(self):
        client = Client()
        post_data = {
            'username': 'skystar',
            'password': 'doge',
            'nickname': 'nicknick',
            'email': 'asdf@asdf.com',
        }
        client.post(
            reverse('sign_up'),
            json.dumps(post_data),
            content_type='application/json',
        )

        user = authenticate(username='skystar', password='doge')
        self.assertTrue(user)

    def test_sign_up_fail(self):
        client = Client()
        post_data = {
            'username': 'skystar',
            'password': 'doge',
            'email': 'asdf@asdf.com',
        }
        response = client.post(
            reverse('sign_up'),
            json.dumps(post_data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)

        response = client.get(
            reverse('sign_up'),
        )

        self.assertEqual(response.status_code, 405)


class ApiSignInTest(TestCase):
    def setUp(self):
        create_user(
            username='skystar',
            password='doge',
            nickname='usezmap',
            email='asdf@asdf.com'
        )

    def test_sign_in_success(self):
        client = Client()
        post_data = {
            'username': 'skystar',
            'password': 'doge',
        }
        response = client.post(
            reverse('sign_in'),
            json.dumps(post_data),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(data['username'], 'skystar')

    def test_sign_in_fail(self):
        client = Client()
        post_data = {
            'username': 'skystar',
            'password': 'not doge',
        }
        response = client.post(
            reverse('sign_in'),
            json.dumps(post_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

        response = client.get(
            reverse('sign_in'),
        )
        self.assertEqual(response.status_code, 405)


class ApiSignOutTest(TestCase):
    def test_sign_out_success(self):
        client = Client()

        response = client.get(
            reverse('sign_out'),
        )
        self.assertEqual(response.status_code, 200)

    def test_sign_out_fail(self):
        client = Client()
        post_data = {}
        response = client.post(
            reverse('sign_out'),
            json.dumps(post_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 405)


class ApiSessionTest(TestCase):
    def setUp(self):
        create_user(
            username='skystar',
            password='doge',
            nickname='usezmap',
            email='asdf@asdf.com'
        )

    def test_verify_session_success(self):
        client = Client()
        client.login(username='skystar', password='doge')

        response = client.get(
            reverse('verify_session'),
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['username'], 'skystar')

    def test_verify_session_unauthorized(self):
        client = Client()

        response = client.get(
            reverse('verify_session'),
        )

        self.assertEqual(response.status_code, 401)

    def test_verify_session_not_allowed(self):
        client = Client()

        response = client.post(
            reverse('verify_session'),
            json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 405)


class ModelTest(TestCase):
    def setUp(self):
        create_user(
            username='skystar',
            password='doge',
            nickname='usezmap',
            email='asdf@asdf.com'
        )

    def test_User_model(self):
        me = authenticate(username='skystar', password='doge')
        self.assertTrue(me)

        me = authenticate(username='skystar', password='not doge')
        self.assertFalse(me)
