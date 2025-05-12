from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.images.models import Document
from apps.images.models_organization import Organization, UserProfile

class DeleteDocumentViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.org = Organization.objects.create(name='OrgTest')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.userprofile.organization = self.org
        self.user.userprofile.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.doc_bytes = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        self.docs = [
            Document.objects.create(title=f'doc{i}', file=SimpleUploadedFile(f'dummy{i}.pdf', self.doc_bytes, content_type='application/pdf'), organization=self.org, user=self.user)
            for i in range(16)
        ]

    def test_delete_document_redirects_to_same_page(self):
        # Página 2 (documento 16)
        doc_to_delete = self.docs[15]
        url = reverse('images:delete_document', args=[doc_to_delete.id]) + '?page=2&order_by=-upload_date&filetype=document'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        post_data = {
            'page': '2',
            'order_by': '-upload_date',
            'filetype': 'document',
            'csrfmiddlewaretoken': resp.cookies['csrftoken'].value if 'csrftoken' in resp.cookies else 'dummy',
        }
        resp2 = self.client.post(url, post_data, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('page=1', resp2.redirect_chain[-1][0])
