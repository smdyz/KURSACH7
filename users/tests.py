from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class UserCreateAPIViewTest(APITestCase):

    def test_create_user(self):
        url = reverse('users:user_create')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """Проверяем, что пользователь создан в базе данных"""

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_create_user_invalid_data(self):
        url = reverse('users:user_create')
        data = {
            'username': 'testuser2',
            # Отсутствует пароль
            'email': 'test2@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Проверяем, что пользователь не создан в базе данных"""

        self.assertFalse(User.objects.filter(username='testuser2').exists())


class UserUpdateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com',
                                                        password='adminpassword')

    def test_update_user(self):
        self.client.force_login(self.admin_user)  # Логинимся под администратором
        url = reverse('users:user_update', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updated_email@example.com',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что пользователь действительно был обновлен в базе данных"""

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, 'Updated First Name')
        self.assertEqual(updated_user.last_name, 'Updated Last Name')
        self.assertEqual(updated_user.email, 'updated_email@example.com')

    def test_update_user_unauthorized(self):
        url = reverse('users:user_update', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updated_email@example.com',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        """Проверяем, что пользователь не был изменен в базе данных"""

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Updated First Name')

    def test_update_user_partial_fields(self):
        self.client.force_login(self.admin_user)
        url = reverse('users:user_update', kwargs={'pk': self.user.pk})
        data = {
            'last_name': 'Updated Last Name',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что только указанное поле было обновлено, остальные остались прежними"""

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.last_name, 'Updated Last Name')
        self.assertEqual(updated_user.first_name, '')

    def test_update_user_invalid_data(self):
        self.client.force_login(self.admin_user)
        url = reverse('users:user_update', kwargs={'pk': self.user.pk})
        data = {
            'email': 'invalid_email',  # Неверный формат email
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Проверяем, что пользователь не был изменен в базе данных"""

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'invalid_email')


class UserDestroyAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com',
                                                        password='adminpassword')

    def test_delete_user_as_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('users:user_destroy', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        """Проверяем, что пользователь был удален из базы данных"""

        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_delete_user_as_owner(self):
        self.client.force_login(self.user)
        url = reverse('users:user_destroy', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        """Проверяем, что пользователь был удален из базы данных"""

        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_delete_user_unauthorized(self):
        url = reverse('users:user_destroy', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        """Проверяем, что пользователь не был удален из базы данных"""

        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserListAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com',
                                                        password='adminpassword')

    def test_get_user_list_as_authenticated_user(self):
        self.client.force_login(self.user)
        url = reverse('users:user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что список пользователей содержит созданного пользователя"""

        self.assertIn('testuser', str(response.data))

    def test_get_user_list_as_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('users:user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что список пользователей содержит созданного пользователя"""

        self.assertIn('testuser', str(response.data))


class UserRetrieveAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com',
                                                        password='adminpassword')

    def test_get_user_as_authenticated_user(self):
        self.client.force_login(self.user)
        url = reverse('users:user_retrieve', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что полученные данные соответствуют ожидаемым данным пользователя"""

        self.assertEqual(response.data['username'], 'testuser')

    def test_get_user_as_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('users:user_retrieve', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что полученные данные соответствуют ожидаемым данным пользователя"""

        self.assertEqual(response.data['username'], 'testuser')


class UserProfileUpdateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com',
                                                   password='otherpassword')

    def test_update_user_profile(self):
        self.client.force_login(self.user)
        url = reverse('users:user_update')
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updated_email@example.com',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что профиль пользователя был успешно обновлен"""

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, 'Updated First Name')
        self.assertEqual(updated_user.last_name, 'Updated Last Name')
        self.assertEqual(updated_user.email, 'updated_email@example.com')

    def test_update_user_profile_unauthorized(self):
        url = reverse('users:user_update')
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updated_email@example.com',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        """Проверяем, что профиль пользователя не был изменен"""

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Updated First Name')