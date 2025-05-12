from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.images.models import Image
from apps.images.models_organization import Organization, UserProfile

class ImageFeatureTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.org = Organization.objects.create(name='OrgTest')
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.user.userprofile.organization = self.org
        self.user.userprofile.save()
        self.client = Client()
        self.client.login(username='testuser2', password='testpass2')
        self.img_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;'
        self.image = Image.objects.create(
            title='Test Image',
            file=SimpleUploadedFile('test.gif', self.img_bytes, content_type='image/gif'),
            organization=self.org,
            user=self.user
        )

    def test_upload_image(self):
        url = reverse('images:upload_image')
        response = self.client.post(url, {
            'title': 'Imagem Upload',
            'description': 'Teste de upload',
            'tags': 'teste',
            'images': SimpleUploadedFile('upload.gif', self.img_bytes, content_type='image/gif'),
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Imagem Upload', response.content.decode())

    def test_image_list(self):
        url = reverse('images:image_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Image', response.content.decode())

    def test_image_detail(self):
        url = reverse('images:image_detail', args=[self.image.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Image', response.content.decode())
