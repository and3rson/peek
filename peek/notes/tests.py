from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from peek.users.models import User


class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.users = [
            User.objects.create(username='user1'),
            User.objects.create(username='user2')
        ]

        self.notes = []

        for user in self.users:
            self.client.force_authenticate(user)
            group = []
            for i in xrange(3):
                response = self.client.post(reverse('note-list'), dict(
                    body='note{} of {}'.format(
                        i + 1, user.username
                    )
                ))
                group.append(response.data['id'])
            self.notes.append(group)

        self.client.force_authenticate(None)

    def test_unauthorized(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 403)

    def test_get_my_notes(self):
        self.client.force_authenticate(self.users[0])

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(reverse('note-detail', args=(self.notes[0][0],)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(self.notes[0][0]))

    def test_cannot_get_other_user_notes(self):
        self.client.force_authenticate(self.users[0])

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('note-detail', args=(self.notes[1][0],)))
        self.assertEqual(response.status_code, 404)

    def test_create_note(self):
        self.client.force_authenticate(self.users[0])

        response = self.client.post(reverse('note-list'), dict(
            body='note2 of user1',
            color='f05040'
        ))
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('note-detail', args=(response.data['id'],)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], 'note2 of user1')
        self.assertEqual(response.data['color'], 'F05040')

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['order'], 4)
        self.assertEqual(response.data[1]['order'], 3)
        self.assertEqual(response.data[2]['order'], 2)
        self.assertEqual(response.data[3]['order'], 1)

    def test_bad_color(self):
        self.client.force_authenticate(self.users[0])

        response = self.client.patch(reverse('note-detail', args=(str(self.notes[0][0]),)), dict(
            color='dafuq1'
        ))
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(reverse('note-detail', args=(str(self.notes[0][0]),)), dict(
            color='fffffff'
        ))
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(reverse('note-detail', args=(str(self.notes[0][0]),)), dict(
            color='ffffff'
        ))
        self.assertEqual(response.status_code, 200)

    def test_move1(self):
        self.client.force_authenticate(self.users[0])

        # 1 2 3 -> 1 3 2
        response = self.client.post(reverse('note-move', args=(str(self.notes[0][2]),)), dict(
            to=2
        ))
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.data[0]['id'], str(self.notes[0][1]))
        self.assertEqual(response.data[1]['id'], str(self.notes[0][2]))
        self.assertEqual(response.data[2]['id'], str(self.notes[0][0]))

    def test_move2(self):
        self.client.force_authenticate(self.users[0])

        # 1 2 3 -> 3 1 2
        response = self.client.post(reverse('note-move', args=(str(self.notes[0][2]),)), dict(
            to=1
        ))
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.data[0]['id'], str(self.notes[0][1]))
        self.assertEqual(response.data[1]['id'], str(self.notes[0][0]))
        self.assertEqual(response.data[2]['id'], str(self.notes[0][2]))

    def test_move3(self):
        self.client.force_authenticate(self.users[0])

        # 1 2 3 -> 2 3 1
        response = self.client.post(reverse('note-move', args=(str(self.notes[0][0]),)), dict(
            to=999999999
        ))
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.data[0]['id'], str(self.notes[0][0]))
        self.assertEqual(response.data[1]['id'], str(self.notes[0][2]))
        self.assertEqual(response.data[2]['id'], str(self.notes[0][1]))

    def test_move_errors(self):
        self.client.force_authenticate(self.users[0])

        response = self.client.post(reverse('note-move', args=(str(self.notes[0][0]),)), dict(
        ))
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('note-move', args=(str(self.notes[0][0]),)), dict(
            to=-1
        ))
        self.assertEqual(response.status_code, 400)
