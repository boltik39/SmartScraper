from django.shortcuts import render
from scraper.models import Device
from utils.Googler import Googler
from utils.FileHelper import FileHelper


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def search(request):
    devices = []
    queries = []
    if request.method == "GET":
        query = request.GET['query']
        queries.append(query)
    else:
        queries = FileHelper.get_products_from_excel(request.FILES["excel_file"])

    for item in queries:
        try:
            device_query = Device.objects.get(name=item)
            print(item)
        except Device.DoesNotExist:
            dicty = Googler.search_by_query(item)
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
                                        score=dicty['score'], link=dicty['links'][0])
            device_query.save()
        finally:
            devices.append(device_query)
            print(devices)

    return render(request, 'search_result.html', {"devices" : devices})
