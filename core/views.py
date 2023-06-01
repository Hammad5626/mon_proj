from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.template.defaultfilters import json_script
import pandas as pd
import json
from .models import DataModel
from .forms import AdminLoginForm

def clean_value(value):
    return value if pd.notnull(value) else None

def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                opening_time = clean_value(row.get('Opening Time'))
                type = clean_value(row.get('Type'))
                volume = clean_value(row.get('Volume'))
                symbol = clean_value(row.get('Symbol'))
                opening_price = clean_value(row.get('Opening Price'))
                closing_time = clean_value(row.get('Closing Time'))
                price = clean_value(row.get('Price'))
                profit = clean_value(row.get('Profit'))

                data = DataModel(
                    opening_time=opening_time,
                    type=type,
                    volume=volume,
                    symbol=symbol,
                    opening_price=opening_price,
                    closing_time=closing_time,
                    price=price,
                    profit=profit
                )
                data.save()

            return render(request, 'success.html')
        else:
            return render(request, 'error.html')
    return render(request, 'upload.html')





def graph_view(request):
    data = DataModel.objects.values('profit', 'opening_price', 'opening_time')
    profit_list = [entry['profit'] for entry in data]
    opening_price_list = [entry['opening_price'] for entry in data]
    opening_time_list = [entry['opening_time'].strftime('%Y-%m-%d') for entry in data]

    context = {
        'profit_list': profit_list,
        'opening_price_list': opening_price_list,
        'opening_time_list': opening_time_list,
    }
    
    context_json = json.dumps(context)

    return render(request, 'graph.html', {'context_json': context_json})

def graph2_view(request):
    data = DataModel.objects.values('profit', 'opening_price', 'opening_time')
    profit_list = [entry['profit'] for entry in data]
    opening_price_list = [entry['opening_price'] for entry in data]
    opening_time_list = [entry['opening_time'].strftime('%Y-%m-%d') for entry in data]

    context = {
        'profit_list': profit_list,
        'opening_price_list': opening_price_list,
        'opening_time_list': opening_time_list,
    }
    
    context_json = json.dumps(context)

    return render(request, 'graph2.html', {'context_json': context_json})



def index(request):
    return render(request, 'base.html')

class AdminLoginView(LoginView):
    template_name = 'admin_login.html'

    def get_form_class(self):
        return AdminLoginForm

def admin_logout(request):
    logout(request)
    return redirect('index')
