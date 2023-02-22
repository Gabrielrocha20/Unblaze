from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from utils.bot import ReturnPrevResult

from .models import Historico, Sequencia


class HistoricoView(View):
    def get(self, request):
        giros = Historico.objects.all().order_by('-id')
        return render(request, 'bot/page/index.html', {'giros': giros})

class Sinais(View):
    def get(self, request):
        prev_result = ReturnPrevResult()
        prev_result = prev_result.get_result()
        if not prev_result:
            return HttpResponse('Nada')
        return render(request, 'bot/page/sinais.html', {
            'color': prev_result[0],
            'match': prev_result[1],
            'porcentagem': prev_result[2],
            })

# Create your views here.
