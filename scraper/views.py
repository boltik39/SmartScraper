from django.shortcuts import render
from scraper.models import Device
from utils.Googler import Googler
from utils.FileHelper import FileHelper


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def search(request):
    if request.method == "GET":
        query = request.GET['query']

        device_query = Device.objects.filter(name=query)

        if device_query:
            dicty = device_query.values()
            return render(request, 'search_result.html',
                        {'name': dicty[0]['name'],
                        'mttr': dicty[0]['mttr'],
                        'mtbf': dicty[0]['mtbf'],
                        'fail': dicty[0]['failure_rate'],
                        'stor_mode': dicty[0]['failure_rate_in_storage_mode'],
                        'stor_time': dicty[0]['storage_time'],
                        'min_res': dicty[0]['minimal_resource'],
                        'gam': dicty[0]['gamma_percentage_resource'],
                        'a_res': dicty[0]['average_resource'],
                        'a_life': dicty[0]['average_lifetime'],
                        'rec_inten': dicty[0]['recovery_intensity'],
                        'sys_rel': dicty[0]['system_reliability'],
                        'score': dicty[0]['score']})

        else:
            dicty = Googler.search_by_query(query)
            return render(request, 'search_result.html',
                        {'name': dicty['name'],
                        'mttr': dicty['mttr'],
                        'mtbf': dicty['mtbf'],
                        'fail': dicty['failure_rate'],
                        'stor_mode': dicty['failure_rate_in_storage_mode'],
                        'stor_time': dicty['storage_time'],
                        'min_res': dicty['minimal_resource'],
                        'gam': dicty['gamma_percentage_resource'],
                        'a_res': dicty['average_resource'],
                        'a_life': dicty['average_lifetime'],
                        'rec_inten': dicty['recovery_intensity'],
                        'sys_rel': dicty['system_reliability'],
                        'score': dicty['score']})
    else:
        products = FileHelper.get_products_from_excel(request.FILES["excel_file"])
        return render(request, 'search_result.html')
