from django.shortcuts import render
from django.http import HttpResponse, response
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.conf import settings

import json
from .models import Home
from django.core.files.storage import FileSystemStorage
import uuid
import os
from django.template.defaulttags import csrf_token
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
import string
import random
from django.core.serializers import serialize
from json import loads as jloads

from django.utils.translation import activate
from django.utils import translation


def lang_switch(langs="tr"):
    if langs == "tr":
        activate('tr')
    else:
        activate('en')


    return redirect("/")


def index(request, langs="tr"):
    lang_switch(langs)

    return render(request, 'index.html', { 'lang' : langs})


def application_query(request, langs="tr"):
    lang_switch(langs)

    return render(request, 'application_query.html', {'lang': langs})



@csrf_protect
def application_submit(request, langs="tr"):
    lang_switch(langs)

    if request.method == 'POST':
        response_data = {}

      
        code = request.POST.get('code')
    
        newHome = Home.objects.filter(code=str(code))
        data = list(newHome.values())
        if newHome:
            response_data['data'] = data[0],
            response_data['result'] = 'success'
            response_data['title'] = _('Tebrikler')
            response_data['message'] = _('Başvuru bilgileriniz yükleniyor')
  

        else:
            response_data['result'] = 'error'
            response_data['title'] = _('Hmmm')
            response_data['message'] = _('Lütfen başvuru kodunuzu kontrol edip tekrardan deneyinizz')

     

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return redirect("/" + langs)


@csrf_protect
def submit(request, langs="tr"):
    lang_switch(langs)
    
    if request.method == 'POST':
        response_data = {}

      
        S = 32  # number of characters in the string.  
        ranCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
      


        try:
            myfile = request.FILES['image']
            fs = FileSystemStorage()

            ext = myfile.name.split('.')[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            filename = os.path.join('uploads/form', filename)
            filename = fs.save(filename, myfile)
            image = fs.url(filename)

            title = request.POST.get('title')
            description = request.POST.get('description')
            link = request.POST.get('link')

            email = request.POST.get('email')

            newHome = Home(
                title=title,
                description=description,
                link=link,
                email=email,
                image=filename,
                statu=False,
                code=str(ranCode)
            )

            newHome.save()
            response_data['result'] = 'success'
            response_data['title'] = _('Tebrikler')
            response_data['message'] = _('Tebrikler başarılı bir şekilde başvurunuz yapıldı. Başvuru Kodunuz : {} ').format(str(ranCode))

        except:
            response_data['result'] = 'error'
            response_data['title'] = _('Hmmm')
            response_data['message'] = _('Lütfen gerekli alanları doldurup, Tekrardan deneyiniz')

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return redirect("/" + langs)
