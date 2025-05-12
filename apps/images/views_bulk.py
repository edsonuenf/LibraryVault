from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Image, Video, Document, Audio
from .forms_bulk import BulkDeleteImagesForm

@login_required
def bulk_delete_documents(request):
    from django.core.paginator import Paginator
    from django.urls import reverse
    from .models import Document
    if request.method == 'POST':
        ids = request.POST.getlist('document_ids')
        page = request.POST.get('page', '1')
        filetype = request.POST.get('filetype', '')
        ordering = request.POST.get('ordering', 'recent')
        msg = 'Documentos excluídos com sucesso!'
        if ids:
            Document.objects.filter(id__in=ids).delete()
            # Recalcular paginação
            user_profile = None
            try:
                from .models_organization import UserProfile
                user_profile = UserProfile.objects.get(user=request.user)
            except Exception:
                pass
            documents_qs = Document.objects.all()
            if user_profile:
                documents_qs = documents_qs.filter(organization=user_profile.organization)
            if filetype:
                documents_qs = documents_qs.filter(file__iendswith=filetype)
            order_field = '-uploaded_at' if ordering == 'recent' else 'uploaded_at'
            documents_qs = documents_qs.order_by(order_field)
            paginator = Paginator(documents_qs, 15)
            try:
                page_num = int(page)
            except Exception:
                page_num = 1
            if paginator.num_pages < page_num:
                page_num = paginator.num_pages
            if paginator.count == 0:
                page_num = 1
            if page_num < 1:
                page_num = 1
            # Se a página ficou vazia, volta para anterior
            if paginator.count == 0:
                page_num = 1
                msg += ' Não há mais itens nesta lista, voltando para a página 1.'
            elif paginator.num_pages < page_num or (page_num > 1 and len(paginator.page(page_num).object_list) == 0):
                page_num -= 1
                msg += f' Você excluiu o último item da página, voltando para a página {page_num}.'
            if page_num == 1:
                url = reverse('images:document_list') + '?page=1'
            else:
                url = reverse('images:document_list') + f'?page={page_num}'
            if filetype:
                url += f'&filetype={filetype}'
            if ordering:
                url += f'&ordering={ordering}'
            from django.contrib import messages
            messages.success(request, msg)
            return redirect(url)
        from django.contrib import messages
        messages.info(request, 'Nenhum item selecionado para exclusão.')
        return redirect('images:document_list')
    return redirect('images:document_list')

@login_required
def bulk_delete_images(request):
    from django.core.paginator import Paginator
    from django.urls import reverse
    if request.method == 'POST':
        ids = request.POST.getlist('image_ids')
        page = request.POST.get('page', '1')
        ordering = request.POST.get('ordering', 'recent')
        filetype = request.POST.get('filetype', '')
        if ids:
            images = Image.objects.filter(id__in=ids)
            for image in images:
                if image.file and image.file.path:
                    import os
                    if os.path.isfile(image.file.path):
                        os.remove(image.file.path)
                # Remove arquivo 460 com o mesmo nome do arquivo original, na pasta 460
                import os
                from django.conf import settings
                original_filename = os.path.basename(image.file.name)
                file_460_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images', '460', original_filename)
                if os.path.isfile(file_460_path):
                    os.remove(file_460_path)
                image.delete()
        # Após exclusão, verifica se ainda há imagens na página
        user_profile = request.user.userprofile
        order_field = '-upload_date' if ordering == 'recent' else 'upload_date'
        images_qs = Image.objects.filter(organization=user_profile.organization)
        if filetype:
            images_qs = images_qs.filter(file__iendswith=filetype)
        images_qs = images_qs.order_by(order_field)
        paginator = Paginator(images_qs, 15)
        try:
            page_num = int(page)
        except Exception:
            page_num = 1
        if paginator.num_pages < page_num:
            page_num = paginator.num_pages
        msg = 'Itens excluídos com sucesso!'
        if page_num < 1:
            page_num = 1
        # Se a página ficou vazia, volta para anterior
        if paginator.count == 0:
            page_num = 1
            msg += ' Não há mais itens nesta lista, voltando para a página 1.'
        elif paginator.num_pages < page_num or (page_num > 1 and len(paginator.page(page_num).object_list) == 0):
            page_num -= 1
            msg += f' Você excluiu o último item da página, voltando para a página {page_num}.'
        if page_num == 1:
            url = reverse('images:image_list') + '?page=1'
        else:
            url = reverse('images:image_list') + f'?page={page_num}'
        if filetype:
            url += f'&filetype={filetype}'
        if ordering:
            url += f'&ordering={ordering}'
        from django.contrib import messages
        messages.success(request, msg)
        return redirect(url)
    from django.contrib import messages
    messages.info(request, 'Nenhum item selecionado para exclusão.')
    return redirect('images:image_list')

@login_required
def bulk_delete_audios(request):
    from django.core.paginator import Paginator
    from django.urls import reverse
    if request.method == 'POST':
        ids = request.POST.getlist('audio_ids')
        page = request.POST.get('page', '1')
        filetype = request.POST.get('filetype', '')
        ordering = request.POST.get('ordering', 'recent')
        if ids:
            audios = Audio.objects.filter(id__in=ids)
            for audio in audios:
                if audio.file and audio.file.path:
                    import os
                    if os.path.isfile(audio.file.path):
                        os.remove(audio.file.path)
                audio.delete()
        # Após exclusão, verifica se ainda há áudios na página
        user_profile = request.user.userprofile
        order_field = '-uploaded_at' if ordering == 'recent' else 'uploaded_at'
        audios_qs = Audio.objects.filter(organization=user_profile.organization)
        if filetype:
            audios_qs = audios_qs.filter(file__iendswith=filetype)
        audios_qs = audios_qs.order_by(order_field)
        paginator = Paginator(audios_qs, 15)
        try:
            page_num = int(page)
        except Exception:
            page_num = 1
        if paginator.num_pages < page_num:
            page_num = paginator.num_pages
        msg = 'Itens excluídos com sucesso!'
        if page_num < 1:
            page_num = 1
        # Se a página ficou vazia, volta para anterior
        if paginator.count == 0:
            page_num = 1
            msg += ' Não há mais itens nesta lista, voltando para a página 1.'
        elif paginator.num_pages < page_num or (page_num > 1 and len(paginator.page(page_num).object_list) == 0):
            page_num -= 1
            msg += f' Você excluiu o último item da página, voltando para a página {page_num}.'
        if page_num == 1:
            url = reverse('images:audio_list') + '?page=1'
        else:
            url = reverse('images:audio_list') + f'?page={page_num}'
        if filetype:
            url += f'&filetype={filetype}'
        if ordering:
            url += f'&ordering={ordering}'
        from django.contrib import messages
        messages.success(request, msg)
        return redirect(url)
    from django.contrib import messages
    messages.info(request, 'Nenhum item selecionado para exclusão.')
    return redirect('images:audio_list')

@login_required
def bulk_delete_videos(request):
    if request.method == 'POST':
        ids = request.POST.getlist('video_ids')
        page = request.POST.get('page', '1')
        order_by = request.POST.get('order_by', '')
        if ids:
            from django.conf import settings
            import os
            videos = Video.objects.filter(id__in=ids)
            for video in videos:
                if video.file and video.file.path:
                    if os.path.isfile(video.file.path):
                        os.remove(video.file.path)
                video.delete()
        # Após exclusão, verifica se ainda há vídeos na página
        user_profile = request.user.userprofile
        filters = {'organization': user_profile.organization}
        ordering = '-uploaded_at'
        if order_by == 'upload_date_asc':
            ordering = 'uploaded_at'
        elif order_by == 'original_filename':
            ordering = 'original_filename'
        videos_qs = Video.objects.filter(**filters).order_by(ordering)
        from django.core.paginator import Paginator
        paginator = Paginator(videos_qs, 15)
        try:
            page_num = int(page)
        except Exception:
            page_num = 1
        if paginator.num_pages < page_num:
            page_num = paginator.num_pages
        if page_num < 1:
            page_num = 1
        redirect_url = f"/images/list-videos/?page={page_num}"
        if order_by:
            redirect_url += f"&order_by={order_by}"
        return redirect(redirect_url)
    return redirect('images:video_list')

    if request.method == 'POST':
        ids = request.POST.getlist('image_ids')
        if ids:
            images = Image.objects.filter(id__in=ids)
            for image in images:
                if image.file and image.file.path:
                    import os
                    if os.path.isfile(image.file.path):
                        os.remove(image.file.path)
                # Remove arquivo 460 com o mesmo nome do arquivo original, na pasta 460
                import os
                from django.conf import settings
                original_filename = os.path.basename(image.file.name)
                file_460_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images', '460', original_filename)
                if os.path.isfile(file_460_path):
                    os.remove(file_460_path)
                image.delete()
        from django.contrib import messages
        messages.success(request, 'Itens excluídos com sucesso!')
        # Padroniza para sempre incluir ?page=1 na URL ao redirecionar para a primeira página
        url = reverse('images:video_list') + '?page=1'
        return redirect(url)
    from django.contrib import messages
    messages.info(request, 'Nenhum item selecionado para exclusão.')
    return redirect('images:image_list')
