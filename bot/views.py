from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from utils.bot import ReturnPrevResult
from utils.ToTelegran import enviar_msg_telegram, enviar_resultado_telegram

from .models import Configuracao, Historico, Sequencia


class HistoricoView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('bot:login')
        giros = Historico.objects.all().order_by('-id')
        return render(request, 'bot/page/index.html', {'giros': giros})

class Sinais(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('bot:login')
        sendTelegram = request.GET.get('SendTelegram')

        prev_result = ReturnPrevResult()
        prev_result = prev_result.get_result()
        if prev_result == None:
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
        if not request.user.is_authenticated:
            return redirect('bot:login')
        config = Configuracao.objects.all().first()
        chave = config.api_telegram
        chat_id = config.id_sala_telegram
        enviar_resultado_telegram(chave, chat_id, res)
        return redirect('bot:sinais')

class Config(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('bot:login')
        config = Configuracao.objects.all().first()

        return render(request, 'bot/page/config.html', {
            'config': config,
        })
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('bot:login')
        api_telegram = request.POST.get('api_telegram')
        id_chat_telegram = request.POST.get('id_chat_telegram')
        config = Configuracao.objects.all().first()

        config.api_telegram = api_telegram
        config.id_sala_telegram = id_chat_telegram
        config.save()

        
        return render(request, 'bot/page/config.html', {
            'config': config,
        })
    
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('bot:sinais')

        return render(request, 'bot/page/login.html')

    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            print(username, password)
            login(request, user = user)
            return redirect('bot:sinais')
        
        return redirect('bot:login')

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('bot:login')
# Create your views here.
