from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.images.models import Video
from apps.images.models_organization import Organization, UserProfile

class DeleteVideoViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.org = Organization.objects.create(name='OrgTest')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.userprofile.organization = self.org
        self.user.userprofile.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.video_bytes = b'\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42mp41isomavc1'
        self.videos = [
            Video.objects.create(title=f'vid{i}', file=SimpleUploadedFile(f'dummy{i}.mp4', self.video_bytes, content_type='video/mp4'), organization=self.org, user=self.user)
            for i in range(16)
        ]

    def test_delete_video_redirects_to_same_page(self):
        # Página 2 (vídeos 16)
        video_to_delete = self.videos[15]
        url = reverse('images:delete_video', args=[video_to_delete.id]) + '?page=2&order_by=-upload_date&filetype=video'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        post_data = {
            'page': '2',
            'order_by': '-upload_date',
            'filetype': 'video',
            'csrfmiddlewaretoken': resp.cookies['csrftoken'].value if 'csrftoken' in resp.cookies else 'dummy',
        }
        resp2 = self.client.post(url, post_data, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('page=1', resp2.redirect_chain[-1][0])
