import json
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from scraper.models import Device
from utils.Googler import Googler
from utils.MathCore import MathCore
from utils.FileHelper import FileHelper
from .forms import LoginForm
from .bases import DEVICE_QUERIES

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
    """Rendering logging page"""
    context = {}
    context['form'] = LoginForm()
    return render(request, 'login.html', context)

def about(request):
    return render(request, 'about.html')

@login_required
def scraper(request):
    """Rendering main page of web-scraper"""
    DEVICE_QUERIES[request.user.get_username()].clear()
    return render(request, 'search_result.html')

@login_required
def search(request):
    """
    Handles request, getting queries from database or scraping from internet by entering to database.
    Returns a response using json that contains device reliability metrics.
    """
    queries = []
    if request.method == "GET":
        query = request.GET['query']
        queries.append(query)
    else:
        queries = FileHelper.get_products_from_excel(request.FILES["excel_file"])

    for item in queries:
        try:
            device_query = Device.objects.get(name=item)
            if device_query not in DEVICE_QUERIES[request.user.get_username()]:
               DEVICE_QUERIES[request.user.get_username()].append(device_query)
        except Device.DoesNotExist:
            dicty = Googler.search_by_query(item)
            links = ""
            for link in dicty["links"]:
                links += link + "; "
            device_query = Device(name=dicty['name'], mttr=dicty['mttr'], 
                                        mtbf=dicty['mtbf'], failure_rate='%.2E' % Decimal(dicty['failure_rate']),
                                        failure_rate_in_storage_mode='%.2E' % Decimal(dicty['failure_rate_in_storage_mode']),
                                        storage_time=dicty['storage_time'],
                                        minimal_resource=dicty['minimal_resource'],
                                        gamma_percentage_resource=dicty['gamma_percentage_resource'],
                                        average_resource=dicty['average_resource'],
                                        average_lifetime=dicty['average_lifetime'],
                                        recovery_intensity=dicty['recovery_intensity'],
                                        system_reliability=dicty['system_reliability'],
                                        score=dicty['score'], link=links)
            device_query.save(using='default')
            DEVICE_QUERIES[request.user.get_username()].append(device_query)
        finally:
            data = {}
            context = {
                'devices' : DEVICE_QUERIES[request.user.get_username()],
            }
            data = {'rendered_data' : render_to_string('table_devices.html', context=context)}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")

def export_devices_to_xlsx(request):
    """
    Exporting device's info to xlsx
    """
    devices = DEVICE_QUERIES[request.user.get_username()]
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename={time}-devices.xlsx'.format(time=datetime.now().strftime('%d-%m-%Y'),
    )
    wb = FileHelper.export_products_to_xlsx(devices)
    wb.save(response)
    return response

def delete(request):
    """
    Deleting devices from user's query list
    """
    if request.method == "POST":
        devices_ids = request.POST.getlist('id[]')
        for id in devices_ids:
            device = Device.objects.get(pk=id)
            DEVICE_QUERIES[request.user.get_username()].remove(device)
        return HttpResponse()

def add_device(request):
    """
    Accepts posted data with device's info, calculates remaining parameters, enters to database.
    Returns a message about the status of the process.
    """
    if request.method == "POST":
        device_dict = {}
        name = request.POST["FormName"]
        django_messages = []
        try:
            device_query = Device.objects.get(name=name)
            messages.add_message(request, messages.ERROR, 'This device already exists.')
        except Device.DoesNotExist:
            device_dict["MTTR"] = float(request.POST["FormMTTR"])
            device_dict["MTBF"] = float(request.POST["FormMTBF"])
            device_dict["Links"] = [request.POST["FormLink"]]
            new_dict = MathCore.calculate_param(device_dict)
            new_dict["name"] = name
            device_query = Device(name=new_dict['name'], mttr=new_dict['MTTR'], 
                                        mtbf=new_dict['MTBF'], failure_rate='%.2E' % Decimal(new_dict['Failure rate']),
                                        failure_rate_in_storage_mode='%.2E' % Decimal(new_dict['failure rate in storage mode']),
                                        storage_time=new_dict['Storage time'],
                                        minimal_resource=new_dict['Minimal resource'],
                                        gamma_percentage_resource=new_dict['Gamma percentage resource'],
                                        average_resource=new_dict['Average resource'],
                                        average_lifetime=new_dict['Average lifetime'],
                                        recovery_intensity=new_dict['recovery intensity'],
                                        system_reliability=new_dict['System Reliability'], score=0,
                                        link=new_dict['Links'])
            device_query.save(using="default")
            messages.add_message(request, messages.SUCCESS, name+' is saved.')
        finally:
            data = {}
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
                })
            data['messages'] = django_messages
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
