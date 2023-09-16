from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from utils.bot import ReturnPrevResult
from utils.ToTelegran import enviar_msg_telegram, enviar_resultado_telegram

from .models import Configuracao, Historico, Sequencia


class HistoricoView(View):
    def get(self, request):
        giros = Historico.objects.all().order_by('-id')
        return render(request, 'bot/page/index.html', {'giros': giros})

class Sinais(View):
    def get(self, request):
        sendTelegram = request.GET.get('SendTelegram')

        prev_result = ReturnPrevResult()
        prev_result = prev_result.get_result()
        if not prev_result:
            return HttpResponse('Nada')
        if sendTelegram:
            config = Configuracao.objects.all().first()
            chave = config.api_telegram
            chat_id = config.id_sala_telegram
            enviar_msg_telegram(chave, chat_id, prev_result[0], prev_result[2])
        return render(request, 'bot/page/sinais.html', {
            'color': f'image/cbox{prev_result[0].capitalize()}.png',
            'matchs': prev_result[1],
            'porcentagem': prev_result[2],
            'sendTelegram': sendTelegram,
            'gale': 'gale',
            'win': 'win',
            'loss': 'loss',
            'white': 'white'
            })
class CheckResultado(View):
    def get(self, request, res):
        config = Configuracao.objects.all().first()
        chave = config.api_telegram
        chat_id = config.id_sala_telegram
        enviar_resultado_telegram(chave, chat_id, res)
        return redirect('bot:sinais')

class Config(View):
    def get(self, request):
        config = Configuracao.objects.all().first()

        return render(request, 'bot/page/config.html', {
            'config': config,
        })
    def post(self, request):
        api_telegram = request.POST.get('api_telegram')
        id_chat_telegram = request.POST.get('id_chat_telegram')
        config = Configuracao.objects.all().first()

        config.api_telegram = api_telegram
        config.id_sala_telegram = id_chat_telegram
        config.save()

        
        return render(request, 'bot/page/config.html', {
            'config': config,
        })

# Create your views here.
