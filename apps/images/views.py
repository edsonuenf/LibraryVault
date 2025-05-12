from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageUploadForm, DocumentUploadForm, VideoUploadForm, AudioUploadForm
from .models import Image, Document, Video, Audio
from .models_like import Like
from .models_organization import UserProfile
from django.http import JsonResponse, HttpResponse, FileResponse
import os
from django.conf import settings
import json
import logging
logger = logging.getLogger(__name__)

@login_required
def relatorio_imagens_usuario(request):
    images = Image.objects.filter(user=request.user).order_by('-upload_date')
    if request.GET.get('export') == 'csv':
        import csv
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_imagens_usuario.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Título', 'Arquivo', 'Data de Upload', 'Organização', 'Usuário'
        ])
        for image in images:
            writer.writerow([
                image.id,
                smart_str(image.title),
                smart_str(image.original_filename),
                image.upload_date.strftime('%d/%m/%Y %H:%M') if image.upload_date else '',
                smart_str(image.organization),
                smart_str(image.user.username)
            ])
        return response
    return render(request, 'images/relatorio_imagens_usuario.html', {'images': images})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        files = request.FILES.getlist('images')  # campo múltiplo do template
        logger.warning(f"Arquivos de imagem recebidos: {[f.name for f in files]}")
        if form.is_valid() and files:
            # Validar todos os arquivos antes de salvar
            invalid_files = []
            for f in files:
                try:
                    form.clean_uploaded_file(f)
                except Exception:
                    invalid_files.append(f.name)
            if invalid_files:
                msg = 'Arquivo(s) não permitido(s): ' + ", ".join(invalid_files)
                messages.error(request, msg)
            else:
                import hashlib
                from django.core.files.base import ContentFile
                user_profile = UserProfile.objects.get(user=request.user)
                for f in files:
                    ext = os.path.splitext(f.name)[1].lower()
                    # Gera hash do nome original + username
                    hash_str = hashlib.sha256((f.name + request.user.username).encode('utf-8')).hexdigest()
                    unique_name = f"{hash_str}_{request.user.username}{ext}"
                    # Caminho absoluto para salvar o original
                    original_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images')
                    os.makedirs(original_dir, exist_ok=True)
                    original_path = os.path.join(original_dir, unique_name)
                    # Salva arquivo original
                    with open(original_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    # Redimensiona e salva webp 460px
                    from PIL import Image as PILImage
                    pil_img = PILImage.open(original_path)
                    w, h = pil_img.size
                    new_width = 460
                    if w > new_width:
                        new_height = int(h * (new_width / w))
                        pil_img_460 = pil_img.resize((new_width, new_height), PILImage.LANCZOS)
                    else:
                        pil_img_460 = pil_img.copy()
                    pil_img_460 = pil_img_460.convert('RGB')
                    webp_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images', '460')
                    os.makedirs(webp_dir, exist_ok=True)
                    webp_name = f"{hash_str}_{request.user.username}.webp"
                    webp_path = os.path.join(webp_dir, webp_name)
                    pil_img_460.save(webp_path, 'WEBP', quality=90)
                    # Salva no banco
                    img = Image(
                        title=form.cleaned_data['title'],
                        user=request.user,
                        organization=user_profile.organization,
                        original_filename=f.name,
                    )
                    # Salva campo file apontando para o arquivo original
                    img.file.name = f"uploads/images/{unique_name}"
                    # Salva campo file_460 apontando para o webp
                    img.file_460.name = f"uploads/images/460/{webp_name}"
                    img.save()
                    logger.warning(f"Salvo: {img.title} - {unique_name} e {webp_name}")
                logger.warning("Upload de imagens finalizado com sucesso!")
                messages.success(request, 'Imagem(ns) enviada(s) com sucesso!')
                return redirect('images:upload_image')
        else:
            logger.warning(f"Formulário inválido ou nenhum arquivo enviado: {form.errors}")
            messages.error(request, 'Erro ao enviar o formulário. Verifique os campos obrigatórios e o arquivo.')
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload_image.html', {'form': form})

@login_required
def image_list(request):
    from apps.config.pagination import CustomPaginator
    from django.core.paginator import EmptyPage, PageNotAnInteger
    from apps.config.utils import get_global_settings
    settings = get_global_settings()
    user_profile = UserProfile.objects.get(user=request.user)
    order_by = request.GET.get('order_by', '-upload_date')
    # Mapeamento seguro de opções
    order_options = {
        'upload_date': 'upload_date',
        'upload_date_asc': 'upload_date',
        'original_filename': 'original_filename',
    }
    # Determina o campo e direção de ordenação
    if order_by == 'upload_date' or order_by == '-upload_date':
        order_field = '-upload_date' if order_by.startswith('-') or order_by == 'upload_date' else 'upload_date'
    elif order_by == 'upload_date_asc':
        order_field = 'upload_date'
    elif order_by == 'original_filename':
        order_field = 'original_filename'
    else:
        order_field = '-upload_date'
    images_qs = Image.objects.filter(organization=user_profile.organization).order_by(order_field)
    paginator = CustomPaginator(images_qs, settings.items_per_page)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user, image__in=images_qs).values_list('image_id', flat=True))
    # Monta a URL absoluta da miniatura 460 para cada imagem na página
    import os
    from django.conf import settings
    for image in images:
        import os
        # Tenta encontrar o nome base do arquivo original
        if image.file and image.file.name:
            base_name = os.path.splitext(os.path.basename(image.file.name))[0]
        elif hasattr(image, 'original_filename') and image.original_filename:
            base_name = os.path.splitext(os.path.basename(image.original_filename))[0]
        else:
            base_name = None
        display_url = ''
        if base_name:
            webp_name = base_name + '.webp'
            webp_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images', '460', webp_name)
            webp_url = os.path.join(settings.MEDIA_URL, 'uploads', 'images', '460', webp_name)
            if os.path.isfile(webp_path):
                display_url = webp_url
        # Se não achou webp, tenta o file_460
        if not display_url and image.file_460 and image.file_460.url:
            display_url = image.file_460.url
        image.display_460_url = display_url
    # Cálculo robusto de intervalo de páginas para navegação
    total_pages = images.paginator.num_pages
    current_page = images.number
    visible = getattr(settings, 'pagination_visible_pages', 5)
    half = visible // 2
    if total_pages <= visible:
        page_range_to_show = list(images.paginator.page_range)
    else:
        start = max(current_page - half, 1)
        end = start + visible - 1
        if end > total_pages:
            end = total_pages
            start = max(end - visible + 1, 1)
        page_range_to_show = list(range(start, end + 1))
    return render(request, 'images/image_list.html', {
        'images': images,
        'liked_ids': liked_ids,
        'order_by': order_by,
        'page_obj': images,
        'page': page,
        'settings': settings,
        'page_range_to_show': page_range_to_show,
    })

@login_required
def toggle_like(request, image_id):
    from django.http import JsonResponse
    if request.method == 'POST':
        image = get_object_or_404(Image, id=image_id)
        like, created = Like.objects.get_or_create(user=request.user, image=image)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': image.likes.count()})
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required
def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    liked = False
    if request.user.is_authenticated:
        from .models_like import Like
        liked = Like.objects.filter(user=request.user, image=image).exists()
    return render(request, 'images/image_detail.html', {'image': image, 'liked': liked})

@login_required
def image_export_metadata(request, pk, fmt):
    image = get_object_or_404(Image, pk=pk)
    meta = {
        'id': image.id,
        'title': image.title,
        'description': image.description,
        'original_date': str(image.original_date) if image.original_date else '',
        'upload_date': str(image.upload_date),
        'author': image.author,
        'copyright': image.copyright,
        'keywords': image.keywords,
        'collection': image.collection,
        'catalog_number': image.catalog_number,
        'physical_location': image.physical_location,
        'provenance': image.provenance,
        'cross_reference': image.cross_reference,
        'width': image.width,
        'height': image.height,
        'dpi': image.dpi,
        'file_format': image.file_format,
        'file_size': image.file_size,
        'bit_depth': image.bit_depth,
        'color_mode': image.color_mode,
        'color_profile': image.color_profile,
        'geolocation': image.geolocation,
        'exif_data': image.exif_data,
    }
    if fmt == 'json':
        return JsonResponse(meta, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    elif fmt == 'xml':
        from django.utils.xmlutils import SimplerXMLGenerator
        import io
        stream = io.StringIO()
        xml = SimplerXMLGenerator(stream, 'utf-8')
        xml.startDocument()
        xml.startElement('image', {})
        for k, v in meta.items():
            xml.startElement(str(k), {})
            xml.characters(str(v))
            xml.endElement(str(k))
        xml.endElement('image')
        xml.endDocument()
        return HttpResponse(stream.getvalue(), content_type='application/xml')
    else:
        return HttpResponse('Formato não suportado', status=400)

import logging
logger = logging.getLogger(__name__)

@login_required
def relatorio_imagens_usuario(request):
    images = Image.objects.filter(user=request.user).order_by('-upload_date')
    if request.GET.get('export') == 'csv':
        import csv
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_imagens_usuario.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Título', 'Arquivo', 'Data de Upload', 'Organização', 'Usuário'
        ])
        for image in images:
            writer.writerow([
                image.id,
                smart_str(image.title),
                smart_str(image.original_filename),
                image.upload_date.strftime('%d/%m/%Y %H:%M') if image.upload_date else '',
                smart_str(image.organization),
                smart_str(image.user.username)
            ])
        return response
    return render(request, 'images/relatorio_imagens_usuario.html', {'images': images})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST)
        files = request.FILES.getlist('file')
        logger.warning(f"Arquivos recebidos: {[f.name for f in files]}")
        if form.is_valid() and files:
            # Validar todos os arquivos antes de salvar
            invalid_files = []
            for f in files:
                try:
                    form.clean_uploaded_file(f)
                except Exception:
                    invalid_files.append(f.name)
            if invalid_files:
                msg = 'Arquivo(s) não permitido(s): ' + ", ".join(invalid_files)
                messages.error(request, msg)
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                import uuid
                from django.core.files.base import ContentFile
                for f in files:
                    ext = f.name.split('.')[-1]
                    unique_name = f"{uuid.uuid4().hex}.{ext}"
                    content = f.read()
                    doc = Document(
                        title=form.cleaned_data['title'],
                        authors=form.cleaned_data.get('authors', ''),
                        subject=form.cleaned_data.get('subject', ''),
                        description=form.cleaned_data.get('description', ''),
                        creation_date=form.cleaned_data.get('creation_date'),
                        publication_date=form.cleaned_data.get('publication_date'),
                        publisher=form.cleaned_data.get('publisher', ''),
                        version=form.cleaned_data.get('version', ''),
                        languages=form.cleaned_data.get('languages', ''),
                        keywords=form.cleaned_data.get('keywords', ''),
                        doc_type=form.cleaned_data.get('doc_type', ''),
                        user=request.user,
                        organization=user_profile.organization,
                        original_filename=f.name,
                    )
                    doc.file.save(unique_name, ContentFile(content), save=True)
                    logger.warning(f"Salvo: {doc.title} - {unique_name}")
                logger.warning("Upload de documentos finalizado com sucesso!")
                messages.success(request, 'Documento(s) enviado(s) com sucesso!')
                return redirect('images:upload_document')
        else:
            logger.warning(f"Form inválido: {form.errors}")
            messages.error(request, 'Erro ao enviar o formulário. Verifique os campos obrigatórios e o arquivo.')
    else:
        form = DocumentUploadForm()
    return render(request, 'images/upload_document.html', {'form': form})

@login_required
def document_list(request):
    from apps.config.pagination import CustomPaginator
    from django.core.paginator import EmptyPage, PageNotAnInteger
    from apps.config.utils import get_global_settings
    settings = get_global_settings()
    user_profile = UserProfile.objects.get(user=request.user)
    filetype = request.GET.get('filetype', '')
    ordering = request.GET.get('ordering', 'recent')
    order_field = '-uploaded_at' if ordering == 'recent' else 'uploaded_at'
    documents_qs = Document.objects.filter(organization=user_profile.organization)
    if filetype:
        documents_qs = documents_qs.filter(file__iendswith=filetype)
    documents_qs = documents_qs.order_by(order_field)
    paginator = CustomPaginator(documents_qs, settings.items_per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'images/document_list.html', {
        'documents': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'filetype': filetype,
        'ordering': ordering,
        'page': page
    })

@login_required
def download_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    response = FileResponse(doc.file.open('rb'), as_attachment=True, filename=doc.original_filename or os.path.basename(doc.file.name))
    return response

@login_required
def download_audio(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    response = FileResponse(audio.file.open('rb'), as_attachment=True, filename=audio.original_filename or os.path.basename(audio.file.name))
    return response

@login_required
def download_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    response = FileResponse(video.file.open('rb'), as_attachment=True, filename=video.original_filename or os.path.basename(video.file.name))
    return response

@login_required
def download_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    # Sempre retorna o arquivo original com o nome original
    response = FileResponse(image.file.open('rb'), as_attachment=True, filename=image.original_filename or os.path.basename(image.file.name))
    return response

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        files = request.FILES.getlist('file')
        if form.is_valid() and files:
            invalid_files = []
            for f in files:
                try:
                    form.clean_uploaded_file(f)
                except Exception:
                    invalid_files.append(f.name)
            if invalid_files:
                msg = 'Arquivo(s) não permitido(s): ' + ", ".join(invalid_files)
                messages.error(request, msg)
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                for f in files:
                    vid = Video(
                        title=form.cleaned_data['title'],
                        user=request.user,
                        organization=user_profile.organization,
                        original_filename=f.name,
                        file=f
                    )
                    vid.save()
                messages.success(request, 'Vídeo(s) enviado(s) com sucesso!')
                return redirect('images:upload_video')
        else:
            messages.error(request, 'Erro ao enviar o formulário. Verifique os campos obrigatórios e o arquivo.')
    else:
        form = VideoUploadForm()
    return render(request, 'images/upload_video.html', {'form': form})

@login_required
def video_list(request):
    from apps.config.pagination import CustomPaginator
    from django.core.paginator import EmptyPage, PageNotAnInteger
    from apps.config.utils import get_global_settings
    settings = get_global_settings()
    user_profile = UserProfile.objects.get(user=request.user)
    order_by = request.GET.get('order_by', 'upload_date')
    if order_by == 'upload_date':
        ordering = '-uploaded_at'
    elif order_by == 'upload_date_asc':
        ordering = 'uploaded_at'
    elif order_by == 'original_filename':
        ordering = 'original_filename'
    else:
        ordering = '-uploaded_at'
    videos_qs = Video.objects.filter(organization=user_profile.organization).order_by(ordering)
    from apps.config.pagination import CustomPaginator
    from django.core.paginator import EmptyPage, PageNotAnInteger
    paginator = CustomPaginator(videos_qs, settings.items_per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'images/video_list.html', {
        'videos': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'order_by': order_by
    })

@login_required
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        logger.warning(f"Arquivos de áudio recebidos: {[f.name for f in files]}")
        if form.is_valid() and files:
            # Validar todos os arquivos antes de salvar
            invalid_files = []
            for f in files:
                try:
                    form.clean_uploaded_file(f)
                except Exception:
                    invalid_files.append(f.name)
            if invalid_files:
                msg = 'Arquivo(s) não permitido(s): ' + ", ".join(invalid_files)
                messages.error(request, msg)
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                for f in files:
                    audio = Audio(
                        title=form.cleaned_data['title'],
                        user=request.user,
                        organization=user_profile.organization,
                        file=f
                    )
                    audio.save()
                    logger.warning(f"Salvo: {audio.title} - {f.name}")
                logger.warning("Upload de áudios finalizado com sucesso!")
                messages.success(request, 'Áudio(s) enviado(s) com sucesso!')
                return redirect('images:upload_audio')
        else:
            logger.warning(f"Formulário inválido ou nenhum arquivo enviado: {form.errors}")
            messages.error(request, 'Erro ao enviar o formulário. Verifique os campos obrigatórios e o arquivo.')
    else:
        form = AudioUploadForm()
    return render(request, 'images/upload_audio.html', {'form': form})

@login_required
def audio_list(request):
    from apps.config.pagination import CustomPaginator
    from django.core.paginator import EmptyPage, PageNotAnInteger
    from apps.config.utils import get_global_settings
    settings = get_global_settings()
    user_profile = UserProfile.objects.get(user=request.user)
    filetype = request.GET.get('filetype', '')
    ordering = request.GET.get('ordering', 'recent')
    order_field = '-uploaded_at' if ordering == 'recent' else 'uploaded_at'
    audios_qs = Audio.objects.filter(organization=user_profile.organization)
    if filetype:
        audios_qs = audios_qs.filter(file__iendswith=filetype)
    audios_qs = audios_qs.order_by(order_field)
    paginator = CustomPaginator(audios_qs, settings.items_per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'images/audio_list.html', {
        'audios': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'filetype': filetype,
        'ordering': ordering,
        'page': page
    })

@login_required
def delete_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        # Remove o arquivo físico
        if doc.file and os.path.isfile(doc.file.path):
            os.remove(doc.file.path)
        doc.delete()
        return redirect('images:document_list')
    return render(request, 'images/confirm_delete.html', {'document': doc})

from django.http import HttpResponse

@login_required
def delete_image(request, pk):
    from django.core.paginator import Paginator
    from django.urls import reverse
    page = request.POST.get('page') or request.GET.get('page') or '1'
    order_by = request.POST.get('order_by') or request.GET.get('order_by') or '-upload_date'
    filetype = request.POST.get('filetype') or request.GET.get('filetype') or ''
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        from django.contrib import messages
        messages.error(request, 'Nenhuma imagem foi encontrada com esse identificador.')
        return redirect('images:image_list')
    if request.method == 'POST':
        import os
        from django.conf import settings
        from django.contrib import messages
        if image.file and os.path.isfile(image.file.path):
            os.remove(image.file.path)
        if image.file_460 and os.path.isfile(image.file_460.path):
            os.remove(image.file_460.path)
        image.delete()
        # Após exclusão, verifica se ainda há imagens na página
        user_profile = request.user.userprofile
        order_field = order_by
        images_qs = Image.objects.filter(organization=user_profile.organization)
        if filetype:
            images_qs = images_qs.filter(file__iendswith=filetype)
        images_qs = images_qs.order_by(order_field)
        paginator = CustomPaginator(images_qs, settings.items_per_page)
        print(f'[DEBUG][delete_image] queryset count após exclusão: {images_qs.count()}')
        try:
            page_num = int(page)
        except Exception:
            page_num = 1
        print(f'[DEBUG][delete_image] page_num inicial: {page_num}, paginator.num_pages: {paginator.num_pages}')
        if paginator.num_pages < page_num:
            page_num = paginator.num_pages
        if page_num < 1:
            page_num = 1
        # Se não há mais imagens, volta para página 1
        msg = 'Imagem excluída com sucesso!'
        if paginator.count == 0:
            page_num = 1
            msg += ' Não há mais imagens nesta lista, voltando para a página 1.'
        # Se a página de origem ficou vazia, volta para anterior (mas nunca menor que 1)
        elif page_num > 1 and len(paginator.page(page_num).object_list) == 0:
            page_num = max(1, page_num - 1)
            msg += f' Você excluiu o último item da página, voltando para a página {page_num}.'
        # Caso contrário, permanece na página de origem
        print(f'[DEBUG][delete_image] page_num final para redirecionamento: {page_num}')
        url = reverse('images:image_list') + f'?page={page_num}'
        if filetype:
            url += f'&filetype={filetype}'
        if order_by:
            url += f'&order_by={order_by}'
        messages.success(request, msg)
        return redirect(url)
    return render(request, 'images/confirm_delete.html', {'image': image, 'page': page, 'ordering': order_by, 'filetype': filetype})

from django.contrib import messages

@login_required
def delete_audio(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    if request.method == 'POST':
        if audio.file and os.path.isfile(audio.file.path):
            os.remove(audio.file.path)
        audio.delete()
        return redirect('images:audio_list')
    return render(request, 'images/confirm_delete.html', {'audio': audio})

@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        try:
            if video.file and os.path.isfile(video.file.path):
                os.remove(video.file.path)
        except PermissionError:
            messages.error(request, "Não foi possível excluir o arquivo porque ele está em uso. Feche qualquer programa que esteja usando o vídeo e tente novamente.")
            return redirect('images:video_list')
        video.delete()
        return redirect('images:video_list')
    return render(request, 'images/confirm_delete.html', {'video': video})

@login_required
def dashboard_video_stats(request):
    from django.utils import timezone
    from django.db.models.functions import TruncMonth
    from django.db.models import Count
    current_year = timezone.now().year
    if request.user.is_superuser:
        videos_qs = Video.objects.filter(uploaded_at__year=current_year)
    else:
        videos_qs = Video.objects.filter(user=request.user, uploaded_at__year=current_year)
    videos_month = videos_qs.annotate(month=TruncMonth('uploaded_at')).values('month').annotate(count=Count('id')).order_by('month')
    videos_per_month = {m:0 for m in range(1,13)}
    for entry in videos_month:
        if entry['month']:
            videos_per_month[entry['month'].month] += entry['count']
    return [videos_per_month[m] for m in range(1,13)]
