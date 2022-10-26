from datetime import datetime
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from scraper.models import Device
from utils.Googler import Googler
from utils.FileHelper import FileHelper
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

__DEVICE_QUERIES = []

class LoginUser(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context
    def get_success_url(self):
        return reverse_lazy('scraper')

def home(request):
    context = {}
    context['form'] = LoginForm()
    return render(request, 'login.html', context)


def about(request):
    return render(request, 'about.html')

def scraper(request):
    return render(request, 'search_result.html')

def search(request):
    queries = []
    if request.method == "GET":
        query = request.GET['query']
        queries.append(query)
    else:
        queries = FileHelper.get_products_from_excel(request.FILES["excel_file"])

    for item in queries:
        try:
            device_query = Device.objects.using('default').get(name=item)
            __DEVICE_QUERIES.append(device_query)
        except Device.DoesNotExist:
            dicty = Googler.search_by_query(item)
            links = ""
            for link in dicty["links"]:
                links += link + "; "
            device_query = Device(name=dicty['name'], mttr=dicty['mttr'], 
                                        mtbf=dicty['mtbf'], failure_rate=dicty['failure_rate'],
                                        failure_rate_in_storage_mode=dicty['failure_rate_in_storage_mode'],
                                        storage_time=dicty['storage_time'],
                                        minimal_resource=dicty['minimal_resource'],
                                        gamma_percentage_resource=dicty['gamma_percentage_resource'],
                                        average_resource=dicty['average_resource'],
                                        average_lifetime=dicty['average_lifetime'],
                                        recovery_intensity=dicty['recovery_intensity'],
                                        system_reliability=dicty['system_reliability'],
                                        score=dicty['score'], link=links)
            device_query.save(using='default')
            __DEVICE_QUERIES.append(device_query)
            device_query.save(using='local')
    return render(request, 'search_result.html', {"devices": __DEVICE_QUERIES})


def export_devices_to_xlsx(request):
    devices = Device.objects.using('local').all()
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename={time}-devices.xlsx'.format(time=datetime.now().strftime('%H-%M-%S'),
    )
    wb = FileHelper.export_products_to_xlsx(devices)
    wb.save(response)
    return response