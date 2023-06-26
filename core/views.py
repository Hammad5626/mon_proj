from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from datetime import timedelta
import pandas as pd
import requests
import datetime
import json
import os
from .models import DataModel, UserModel
from .forms import SignUpForm, SignInForm

# Function to handle missing fields in excel file.
def clean_value(value):
    return value if pd.notnull(value) else None

def parse_datetime(value):
    if value != None:
        date_formats = ["%d.%m.%y %H:%M", "%d.%m.%Y %H:%M", "%m/%d/%Y %H:%M"]
        for format in date_formats:
            try:
                return datetime.datetime.strptime(value, format)
            except ValueError:
                pass
        raise ValueError("Invalid datetime format")

def get_data(user):
    data = DataModel.objects.filter(user=user).values('profit', 'time', 'type', 'net_profit')
    profit_list = [entry['profit'] for entry in data]
    net_profit_list = [entry['net_profit'] for entry in data]
    type_list = [entry['type'] for entry in data]
    time_list = [entry['time'].strftime('%Y-%m-%d') for entry in data]

    context = {
        'profit_list': profit_list,
        'type_list': type_list,
        'time_list': time_list,
        'net_profit_list': net_profit_list,
    }
    return context

@login_required
def user_data(request, user_id):
    try:
        user = UserModel.objects.get(id=user_id)
        context = get_data(user)
        context_json = json.dumps(context)
        return render(request, 'user_data.html', {'user': user, 'context_json': context_json})
    except UserModel.DoesNotExist:
        return render(request, 'user_not_found.html')
    
# Index View
def index(request):
    return render(request, 'base.html')

def user_list(request):
    users = UserModel.objects.all()
    return render(request, 'user_list.html', {'users': users})

def favorite_users(request):
    favorite_users = UserModel.objects.filter(is_favorite=True)
    return render(request, 'favourite_users.html', {'favorite_users': favorite_users})

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

    # Add a check for the existence of the form object before rendering the template
    if form:
        return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html')

#Logout View
def logout_view(request):
    logout(request)
    return redirect('index')

# View to extract and Upload excel file data.
@user_passes_test(lambda usr: usr.is_staff)
def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        user_name = request.POST['user_name']
        if excel_file.name.endswith('.xlsx'):
            
            # To save file in media folder
            file_path = os.path.join(settings.MEDIA_ROOT, excel_file.name)
            if os.path.exists(file_path):
                return render(request, 'upload.html', {'file_exists': True})
            else:
                with open(file_path, 'wb') as file:
                    for chunk in excel_file.chunks():
                        file.write(chunk)

            # Reading and writing data on database
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                time = row.get('Time')
                try:
                    time = clean_value(parse_datetime(time))
                except ValueError as e:
                    return render(request, 'error.html', {'error_message': str(e)})
                type = clean_value(row.get('Type'))
                volume = clean_value(row.get('Volume'))
                symbol = clean_value(row.get('Symbol'))
                opening_price = clean_value(row.get('Price'))
                volume_spent = clean_value(row.get('Volume'))
                closing_time = row.get('Time')
                try:
                    closing_time = clean_value(parse_datetime(closing_time))
                except ValueError as e:
                    return render(request, 'error.html', {'error_message': str(e)})
                price = clean_value(row.get('Price'))
                commision = clean_value(row.get('Commission'))
                swap = clean_value(row.get('Swap'))
                profit = row.get('Profit')
                net_profit = row.get('Net Profit:\n\nProfit - Commision - Swap')
                user, _ = UserModel.objects.get_or_create(name=user_name)
                data = DataModel(
                    user=user,
                    time=time,
                    type=type,
                    volume=volume,
                    symbol=symbol,
                    opening_price=opening_price,
                    volume_spent = volume_spent,
                    closing_time=closing_time,
                    price=price,
                    commision=commision,
                    swap=swap,
                    profit=profit,
                    net_profit=net_profit,
                )
                data.save()

            # If upload is successful
            return render(request, 'success.html')
        # If not excel file
        else:
            return render(request, 'error.html')
    return render(request, 'upload.html')

@require_POST
def toggle_favorite(request):
    user_id = request.POST.get('user_id')
    is_favorite = request.POST.get('is_favorite')

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        user.is_favorite = is_favorite.lower() == 'true'  # Convert string to boolean
        user.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})

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
        time = data_entry.time

        accumulated_profit = calculate_accumulated_profit(data_entries, data_entry)

        account_balance += accumulated_profit

        lowest_point = get_lowest_point(base_currency, target_currency, time)

        if lowest_point is not None:
            drawdown = (opening_price - lowest_point) * volume * contract_size

            drawdown_percentage = (drawdown / account_balance) * 100

            drawdown_entry = {
                'date': time.date(),
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
def get_lowest_point(base_currency, target_currency, time):
    date = time.date().strftime('%Y-%m-%d')
    api_url = f"https://openexchangerates.org/api/historical/{date}.json?app_id=2d6c79cb6f4e4c349d2cc3590b3ac10f&base={base_currency}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        lowest_point = data["rates"][target_currency]
        return lowest_point
    
    return None

#----------------------------Just Experimenting-----------------------------------------------    
    # base_currency = "USD"
    # data_entries = DataModel.objects.all()
    # start_date = min([entry.time.date() for entry in data_entries]) - timedelta(days=30)
    # end_date = max([entry.time.date() for entry in data_entries]) + timedelta(days=30)
    # api_url = f"https://openexchangerates.org/api/time-series.json?app_id=2d6c79cb6f4e4c349d2cc3590b3ac10f&base={base_currency}&start={start_date}&end={end_date}"
    # print('---------> ' + str(start_date))
    # print('---------> ' + str(end_date))
    # response = requests.get(api_url)
    # data = response.json()
    # print('Status ---------> ' + str(response.status_code))
    # print('---------> ' + str(data))
#----------------------------------------------------------------------------------------------

# <!-------------------------- End of File ------------------------------->