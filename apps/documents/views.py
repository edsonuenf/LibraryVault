from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Document
from .forms import DocumentUploadForm

def teste_upload_multiplo(request):
    template = loader.get_template('documents/teste_upload_multiplo_django.html')
    return HttpResponse(template.render({}, request))

@login_required
def document_list(request):
    documents = Document.objects.filter(is_active=True).order_by('-uploaded_at')
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST)
        files = request.FILES.getlist('file')
        if form.is_valid() and files:
            for f in files:
                doc = form.save(commit=False)
                doc.file = f
                doc.uploaded_by = request.user
                doc.save()
            return redirect('documents:list')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/document_upload.html', {'form': form})
