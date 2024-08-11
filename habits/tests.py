from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Habits
from users.models import User


class HabitCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('habits:habit_create')

    """
    Проверяем создание привычки для аутентифицированного пользователя
    """

    def test_create_habit(self):
        data = {
            'owner': self.user.id,
            'place': 'Park',
            'time': '07:00:00',
            'action': 'Jogging',
            'is_pleasant_habit': True,
            'related_habit': None,
            'periodicity': 3,
            'reward': 'Ice Cream',
            'time_to_complete': 30,
            'is_public': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), 1)
        habit = Habits.objects.get()
        self.assertEqual(habit.place, 'Park')
        self.assertEqual(habit.action, 'Jogging')

    """
    Проверяем, что создание привычки без аутентификации не разрешено
    """

    def test_create_habit_without_authentication(self):
        self.client.logout()
        data = {
            'owner': self.user.id,
            'place': 'Park',
            'time': '07:00:00',
            'action': 'Jogging',
            'is_pleasant_habit': True,
            'related_habit': None,
            'periodicity': 3,
            'reward': 'Ice Cream',
            'time_to_complete': 30,
            'is_public': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HabitListAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('habits:habits_list')

        self.habit1 = Habits.objects.create(
            owner=self.user,
            place='Park',
            time='07:00:00',
            action='Jogging',
            is_pleasant_habit=True,
            periodicity=3,
            reward='Ice Cream',
            time_to_complete=30,
            is_public=True
        )

        self.habit2 = Habits.objects.create(
            owner=self.admin_user,
            place='Gym',
            time='08:00:00',
            action='Workout',
            is_pleasant_habit=True,
            periodicity=5,
            reward='Protein Shake',
            time_to_complete=45,
            is_public=False
        )

    """
    Проверяем получение списка привычек для обычного пользователя
    """

    def test_list_habits(self):
        """
        Проверяем, что обычный пользователь видит только свои привычки.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['owner'], self.user.id)

    """
    Проверяем получение списка привычек для администратора
    """

    def test_list_habits_as_admin(self):
        """
        Проверяем, что администратор видит все привычки.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn(self.habit1.id, [habit['id'] for habit in response.data['results']])
        self.assertIn(self.habit2.id, [habit['id'] for habit in response.data['results']])


class PublicHabitListAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('habits:pablichabit_list')

        self.habit1 = Habits.objects.create(
            owner=self.user,
            place='Park',
            time='07:00:00',
            action='Jogging',
            is_pleasant_habit=True,
            periodicity=3,
            reward='Ice Cream',
            time_to_complete=30,
            is_public=True
        )

        self.habit2 = Habits.objects.create(
            owner=self.user,
            place='Gym',
            time='08:00:00',
            action='Workout',
            is_pleasant_habit=True,
            periodicity=5,
            reward='Protein Shake',
            time_to_complete=45,
            is_public=False
        )

    def test_list_public_habits(self):
        """
        Проверяем, что список публичных привычек содержит только публичные привычки.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue(response.data['results'][0]['is_public'])


class HabitRetrieveAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client.login(username='testuser', password='testpassword')

        # Создаем несколько привычек
        self.habit1 = Habits.objects.create(
            owner=self.user,
            place='Park',
            time='07:00:00',
            action='Jogging',
            is_pleasant_habit=True,
            periodicity=3,
            reward='Ice Cream',
            time_to_complete=30,
            is_public=True
        )

        self.habit2 = Habits.objects.create(
            owner=self.admin_user,
            place='Gym',
            time='08:00:00',
            action='Workout',
            is_pleasant_habit=True,
            periodicity=5,
            reward='Protein Shake',
            time_to_complete=45,
            is_public=False
        )

    def test_retrieve_own_habit(self):
        """
        Проверяем, что пользователь может получить свои привычки.
        """
        url = reverse('habits:habit_detail', kwargs={'pk': self.habit1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.habit1.id)

    def test_retrieve_other_user_habit(self):
        """
        Проверяем, что пользователь не может получить привычки других пользователей.
        """
        url = reverse('habits:habit_detail', kwargs={'pk': self.habit2.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_habit_as_admin(self):
        """
        Проверяем, что администратор может получить любые привычки.
        """
        self.client.login(username='admin', password='adminpassword')
        url = reverse('habits:habit_detail', kwargs={'pk': self.habit1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.habit1.id)


class HabitUpdateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client.login(username='testuser', password='testpassword')
        self.habit1 = Habits.objects.create(
            owner=self.user,
            place='Park',
            time='07:00:00',
            action='Jogging',
            is_pleasant_habit=True,
            periodicity=3,
            reward='Ice Cream',
            time_to_complete=30,
            is_public=True
        )

        self.habit2 = Habits.objects.create(
            owner=self.admin_user,
            place='Gym',
            time='08:00:00',
            action='Workout',
            is_pleasant_habit=True,
            periodicity=5,
            reward='Protein Shake',
            time_to_complete=45,
            is_public=False
        )

    def test_update_own_habit(self):
        """
        Проверяем, что пользователь может обновить свои привычки.
        """
        url = reverse('habits:habit_update', kwargs={'pk': self.habit1.id})
        data = {'action': 'Running'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, 'Running')

    def test_update_other_user_habit(self):
        """
        Проверяем, что пользователь не может обновить привычки других пользователей.
        """
        url = reverse('habits:habit_update', kwargs={'pk': self.habit2.id})
        data = {'action': 'Swimming'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_habit_as_admin(self):
        """
        Проверяем, что администратор может обновить любые привычки.
        """
        self.client.login(username='admin', password='adminpassword')
        url = reverse('habits:habit_update', kwargs={'pk': self.habit1.id})
        data = {'action': 'Cycling'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, 'Cycling')


class HabitDestroyAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client.login(username='testuser', password='testpassword')
        self.habit1 = Habits.objects.create(
            owner=self.user,
            place='Park',
            time='07:00:00',
            action='Jogging',
            is_pleasant_habit=True,
            periodicity=3,
            reward='Ice Cream',
            time_to_complete=30,
            is_public=True
        )

        self.habit2 = Habits.objects.create(
            owner=self.admin_user,
            place='Gym',
            time='08:00:00',
            action='Workout',
            is_pleasant_habit=True,
            periodicity=5,
            reward='Protein Shake',
            time_to_complete=45,
            is_public=False
        )

    def test_destroy_own_habit(self):
        """
        Проверяем, что пользователь может удалить свои привычки.
        """
        url = reverse('habits:habit_delete', kwargs={'pk': self.habit1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.filter(pk=self.habit1.id).exists())

    def test_destroy_other_user_habit(self):
        """
        Проверяем, что пользователь не может удалить привычки других пользователей.
        """
        url = reverse('habits:habit_delete', kwargs={'pk': self.habit2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Habits.objects.filter(pk=self.habit2.id).exists())

    def test_destroy_habit_as_admin(self):
        """
        Проверяем, что администратор может удалить любые привычки.
        """
        self.client.login(username='admin', password='adminpassword')
        url = reverse('habits:habit_delete', kwargs={'pk': self.habit1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.filter(pk=self.habit1.id).exists())
