# Necessary imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User
from .models import Document
from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse, FileResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings


@csrf_exempt
# Decorator to get only GET request on this end-point
@require_http_methods(["GET"])
# Get users
def users(request):
    response = list(User.objects.values())
    return JsonResponse(response, safe=False)


@csrf_exempt
# Decorator to get only GET request on this end-point
@require_http_methods(["GET"])
# Get documents
def documents(request):
    username = request.user.username
    user = User.objects.get(username=username)
    # document = Document.objects.filter(deleted=False)
    # files = UserDocumentMapping.objects.filter(user=user, document=document)
    # files = Document.objects.all()
    files = user.document_set.filter(deleted=False)
    # return JsonResponse(list(Document.objects.values()), safe=False)
    # return JsonResponse(list(Document.objects.filter(deleted=False).values()), safe=False)
    return render(request, 'upload.html', {
        'files': files
    })


def delete(request, document_id):
    if request.method == 'POST':
        document = Document.objects.filter(document_id=document_id)
        # document.update(deleted=True)
        document.delete()
    return redirect('documents')


@csrf_exempt
# Decorator to get only GET request on this end-point
# @require_http_methods(["POST"])
# Upload File
def upload(request):
    username = request.user.username
    user = User.objects.get(username=username)
    # print(user, type(user))
    context = {}
    if request.method == "POST":
        try:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            document = Document(name=name, file=context['url'], owner_username=username)
            document.save()
            # print("before", user.document_set.filter(deleted=False))
            document.users.add(user)
            document.save()
            # print("after", user.document_set.filter(deleted=False))
            files = user.document_set.filter(deleted=False)
            # print(files)
            context['files'] = files
            return redirect('upload')
        except Exception as e:
            context['noFileChosen'] = "Choose a file to upload"
    files = user.document_set.filter(deleted=False)
    # print(files)
    context['files'] = files
    return render(request, 'upload.html', context)


@csrf_exempt
# Decorator to get only POST request on this end-point
@require_http_methods(["POST"])
# Download File
def download(request, document_id):
    obj = Document.objects.get(document_id=document_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(obj.file).split("/")[2])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@csrf_exempt
# Decorator to get only POST request on this end-point
@require_http_methods(["POST"])
# Share File
def share(request, document_id):
    sharewith = request.POST["sharewith"]
    # print(sharewith, document_id)
    try:
        user = User.objects.get(username=sharewith)
        document = Document.objects.get(document_id=document_id)
        # print("before", user.document_set.filter(deleted=False).count())
        # print(document.users.values())
        document.users.add(user)
        # user.document_set.add(document)
        # user.save()
        document.save()
        # print(document.users.values())
        # print("after", user.document_set.filter(deleted=False).count())
    except Exception as e:
        print("invalid")
    return redirect('upload')


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'commons/signup.html'


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'
