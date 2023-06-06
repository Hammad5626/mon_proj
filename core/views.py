from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
import pandas as pd
import requests
import json
import os
from .models import DataModel
from .forms import SignUpForm, SignInForm

# Index View
def index(request):
    return render(request, 'base.html')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            if '@' in username_or_email:
                user = authenticate(request, email=username_or_email, password=password)
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = SignInForm()
    
    return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            # Retrieve the form errors and pass them to the template
            error_messages = form.errors.values()
            for message in error_messages:
                messages.error(request, message)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#Logout View
def logout_view(request):
    logout(request)
    return redirect('index')


# Function to handle missing fields in excel file.
def clean_value(value):
    return value if pd.notnull(value) else None

# View to extract and Upload excel file data.
@user_passes_test(lambda u: u.is_staff)
def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
            file_path = os.path.join(settings.MEDIA_ROOT, excel_file.name)

            if os.path.exists(file_path):
                # File with the same name already exists
                return render(request, 'upload.html', {'file_exists': True})
            else:
                # Save the new file
                with open(file_path, 'wb') as file:
                    for chunk in excel_file.chunks():
                        file.write(chunk)
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                opening_time = (row.get('Opening Time'))
                type = clean_value(row.get('Type'))
                volume = clean_value(row.get('Volume'))
                symbol = clean_value(row.get('Symbol'))
                opening_price = clean_value(row.get('Opening Price'))
                closing_time = clean_value(row.get('Closing Time'))
                price = clean_value(row.get('Price'))
                profit = row.get('Profit')

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

# View to send data to graph.html
@login_required
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

# View to send data to graph2.html
@login_required
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

# View to send data to monthly_stats.html
@login_required
def monthly_stats_view(request):
    template_name = 'monthly_stats.html'

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

    return render(request, template_name, {'context_json': context_json})

# View to calculate drawdown values
@login_required
def drawdown_calculation_view(request):
    template_name = 'drawdown.html'

    data_entries = DataModel.objects.all()
    account_balance = 100
    drawdown_data = []

    for data_entry in data_entries:
        opening_price = data_entry.opening_price
        volume = data_entry.volume
        symbol = data_entry.symbol
        if symbol[:3] == 'USD':
            base_currency = symbol[:3]
            target_currency = symbol[3:]
        elif symbol[3:] == 'USD':
            base_currency = symbol[3:]
            target_currency = symbol[:3]
        else:
            print("Invalid symbol")
        contract_size = 100000
        opening_time = data_entry.opening_time

        accumulated_profit = calculate_accumulated_profit(data_entries, data_entry)

        account_balance += accumulated_profit

        lowest_point = get_lowest_point(base_currency, target_currency, opening_time)

        if lowest_point is not None:
            drawdown = (opening_price - lowest_point) * volume * contract_size

            drawdown_percentage = (drawdown / account_balance) * 100

            drawdown_entry = {
                'opening_price': opening_price,
                'lowest_point': lowest_point,
                'volume': volume,
                'drawdown': drawdown,
                'drawdown_percentage': drawdown_percentage,
            }

            drawdown_data.append(drawdown_entry)

    context = {'drawdown_data': drawdown_data}
    return render(request, template_name, context)

# Function to calculate accumulated profit for drawdown
def calculate_accumulated_profit(data_entries, current_entry):
    accumulated_profit = 0

    for entry in data_entries:
        if entry.pk == current_entry.pk:
            break

        accumulated_profit += entry.profit

    return accumulated_profit

# function to get lowest point from API call for drawdown calculation
def get_lowest_point(base_currency, target_currency, opening_time):
    date = opening_time.date().strftime('%Y-%m-%d')
    api_url = f"https://openexchangerates.org/api/historical/{date}.json?app_id=2d6c79cb6f4e4c349d2cc3590b3ac10f&base={base_currency}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        lowest_point = data["rates"][target_currency]
        return lowest_point
    
    return None