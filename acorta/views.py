from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from acorta.models import ShortedUrl
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def redirigir(request, numero):
    try:
        UrlReal = ShortedUrl.objects.get(id=numero).UrlOriginal
        return HttpResponseRedirect(UrlReal)
    except ShortedUrl.DoesNotExist:
        resp = "Ha habido un fallo!"
        return HttpResponse(resp)

@csrf_exempt
def shorted(request):
    if request.method == "GET":
        listaUrls = ShortedUrl.objects.all()
        if ShortedUrl.objects.all().exists():
            resp = "Las Urls acortadas son:<br/>"
            for i in listaUrls:
                resp += "la Url numero: " + str(i.id) + "proviene de: " + i.UrlOriginal + "<br/>"
        else:
            resp = "Todavía no has acrotado ninguna URL! "

        resp += "Que url quieres acortar?" \
                "<form method='POST' action>" \
                "URL a acortar: <input type='text' name='UrlOriginal'><br>" \
                "<input type='submit' value='SEND'></form>"
        return HttpResponse(resp)

    elif request.method == "POST":
        acortada = False
        url = request.POST['UrlOriginal']
        if url.startswith('http://') or url.startswith('https://'):
            UrlReal = url
        else:
            UrlReal = "http://" + url
        listaUrls = ShortedUrl.objects.all()
        for i in listaUrls:
            if i.UrlOriginal == UrlReal:
                UrlAcortada = ShortedUrl.objects.get(UrlOriginal = UrlReal)
                UrlAcortada = UrlAcortada.id
                acortada = True
        if acortada == False:
            url_nueva = ShortedUrl(UrlOriginal = UrlReal)
            url_nueva.save()
            UrlAcortada = url_nueva.id
        resp = "La URL acortada: " + str(UrlAcortada), " proviene de:  " + UrlReal
        return HttpResponse(resp)
    else:
        return HttpResponse('Method not allowed', status=405)
