from django import forms
from .models import Image, Document, Video, Audio

class ImageUploadForm(forms.ModelForm):
    ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.cdr', '.tif', '.tiff', '.webp']

    class Meta:
        model = Image
        fields = [
            'title', 'description', 'original_date', 'author', 'copyright', 'keywords',
            'collection', 'catalog_number', 'physical_location', 'provenance', 'cross_reference',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Praia do Forte'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Breve descrição da imagem'}),
            'original_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'copyright': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: CC-BY-SA'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: praia, sol, verão'}),
            'collection': forms.Select(attrs={'class': 'form-select'}),
            'catalog_number': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_location': forms.TextInput(attrs={'class': 'form-control'}),
            'provenance': forms.TextInput(attrs={'class': 'form-control'}),
            'cross_reference': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_uploaded_file(self, file):
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            from django.core.exceptions import ValidationError
            tipos = ', '.join([e.upper().replace('.', '') for e in self.ALLOWED_EXTENSIONS])
            raise ValidationError(
                f"Tipo de arquivo não permitido: {ext}. Permitidos: {tipos}."
            )
        return file


class DocumentUploadForm(forms.ModelForm):
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.odt', '.txt']

    class Meta:
        model = Document
        fields = [
            'title', 'authors', 'subject', 'description', 'creation_date', 'publication_date',
            'publisher', 'version', 'languages', 'keywords', 'doc_type'
        ]
        widgets = {
            'creation_date': forms.DateInput(attrs={'type': 'date'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'keywords': forms.TextInput(attrs={'placeholder': 'palavra1, palavra2, ...'}),
        }

    def clean_uploaded_file(self, file):
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Tipo de arquivo não permitido: {ext}. Permitidos: PDF, DOCX, ODT, TXT.")
        return file


class VideoUploadForm(forms.ModelForm):
    ALLOWED_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']

    def clean_uploaded_file(self, file):
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            from django.core.exceptions import ValidationError
            raise ValidationError("Tipo de arquivo não permitido: {}. Permitidos: MP4, AVI, MOV, WMV, FLV, MKV, WEBM.".format(ext))
        return file

    class Meta:
        model = Video
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AudioUploadForm(forms.ModelForm):
    ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.aac', '.m4a', '.flac']

    def clean_uploaded_file(self, file):
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            from django.core.exceptions import ValidationError
            tipos = ', '.join([e.upper().replace('.', '') for e in self.ALLOWED_EXTENSIONS])
            raise ValidationError(
                f"Tipo de arquivo não permitido: {ext}. Permitidos: {tipos}."
            )
        return file

    class Meta:
        model = Audio
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
