from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.images.models import Image
from apps.images.models_organization import Organization, UserProfile

class DeleteImageViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.org = Organization.objects.create(name='OrgTest')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # O UserProfile deve ser criado automaticamente via sinal, basta atualizar a organização:
        self.user.userprofile.organization = self.org
        self.user.userprofile.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        # Cria um arquivo de imagem em memória
        self.img_bytes = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B'
        self.images = [
            Image.objects.create(title=f'img{i}', file=SimpleUploadedFile(f'dummy{i}.gif', self.img_bytes, content_type='image/gif'), organization=self.org, user=self.user)
            for i in range(31)
        ]

    def test_delete_image_redirects_to_same_page(self):
        # Página 2 (imagens 16-30)
        image_to_delete = self.images[16]
        url = reverse('images:delete_image', args=[image_to_delete.id]) + '?page=2&order_by=-upload_date&filetype=image'
        # GET para confirmação
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # POST para exclusão
        post_data = {
            'page': '2',
            'order_by': '-upload_date',
            'filetype': 'image',
            'csrfmiddlewaretoken': resp.cookies['csrftoken'].value if 'csrftoken' in resp.cookies else 'dummy',
        }
        resp2 = self.client.post(url, post_data, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('page=2', resp2.redirect_chain[-1][0])

    def test_delete_last_image_on_page_redirects_to_previous(self):
        # Deleta todas as imagens da página 3 menos uma
        for img in self.images[30:]:
            if img != self.images[30]:
                img.delete()
        url = reverse('images:delete_image', args=[self.images[30].id]) + '?page=3&order_by=-upload_date&filetype=image'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        post_data = {
            'page': '3',
            'order_by': '-upload_date',
            'filetype': 'image',
            'csrfmiddlewaretoken': resp.cookies['csrftoken'].value if 'csrftoken' in resp.cookies else 'dummy',
        }
        resp2 = self.client.post(url, post_data, follow=True)
        self.assertEqual(resp2.status_code, 200)
        # Deve redirecionar para página 2
        self.assertIn('page=2', resp2.redirect_chain[-1][0])
