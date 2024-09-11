from django.shortcuts import render,redirect
from .models import Flight_schedule, Subscription, Query
from .form import QueryForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
# not sure if we need these as the queries have already been handled
#from .models import Inquiry
#from .forms import InquiryForm
from azure.communication.email import EmailClient
from django.conf import settings
# Create your views here.


def index(request):
    flights = Flight_schedule.objects.all()
    return render(request, 'index.html',{'flights':flights})

def query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print("Query form not saved")
    return render(request, 'query.html')

@csrf_exempt
def submit_enquiry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        message = data.get('message')
        # 保存数据到数据库
        enquiry = Query(email=email, query=message)
        enquiry.save()
        return JsonResponse({'message': 'Enquiry submitted successfully'})
    return JsonResponse({'error': '仅支持POST请求'}, status=400)

@csrf_exempt
def get_today_flights(request):
    if request.method == 'GET':
        flights = Flight_schedule.objects.all().filter(date=date.today())
        flight_list = []
        for flight in flights:
            flight_list.append({
                'flight_id': flight.flight_id,
                'location': flight.location,
                'time': flight.time,
                'date': flight.date,
                'status': flight.status,
            })
        return JsonResponse({'flights': flight_list})
    return JsonResponse({'error': '仅支持GET请求'}, status=400)

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        flight_id = data.get('flight_id')
        time_before = data.get('notification_time')
        flight_date = data.get('flight_date')
        flight = Flight_schedule.objects.get(flight_id=flight_id)

        print(time_before)
        print(flight.time)


        notification_time = subtract_hours_from_time(time_before, flight.time)
        # Save data to the database
        subscription = Subscription(email=email, date=flight_date, time=notification_time, flight_id_id=flight.flight_id)
        subscription.save()
        return JsonResponse({'message': '订阅成功'})
    return JsonResponse({'error': '仅支持POST请求'}, status=400)



@csrf_exempt
def get_query(request):
    if request.method == 'GET':
        # only get messages with status = false i.e. not completed messages
        queries = Query.objects.filter(status=0)
        # queries = Query.objects.all()
        query_list = []
        for query in queries:
            query_list.append({
                'id': query.query_id,
                'email': query.email,
                'query': query.query,
            })
        return JsonResponse({'queries': query_list})
    return JsonResponse({'error': '仅支持GET请求'}, status=400)


# Backend end point to handle POST request
@csrf_exempt
def send_reply_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            to_email = data.get('to_email')
            reply_message = data.get('reply_message')

            # Call your send_email function
            send_email(to_email, reply_message)

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# changes message's status to true, i.e. status = 1
@csrf_exempt
def dismiss_message(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        message_id = data.get('messageId')
        print(f"Message ID received: {message_id}")

        # Fetch the message object
        message = Query.objects.get(query_id=message_id)

        # Update the message as completed (assuming you have a `completed` field)
        message.status = True
        message.save()

        return JsonResponse({'status': 'success', 'message': 'Message dismissed successfully'})
    except Query.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def subtract_hours_from_time(hours_to_subtract_str, time_obj):
    #TODO: handle edge case midnight flight
    # Convert the hours string to an integer
    hours_to_subtract = int(hours_to_subtract_str)

    # Combine the time with a dummy date to make subtraction easier
    datetime_obj = datetime.combine(datetime.today(), time_obj)

    # Subtract the hours using timedelta
    new_datetime_obj = datetime_obj - timedelta(hours=hours_to_subtract)

    # Extract the new time and return it
    return new_datetime_obj.time()

# Hiru's work form here below... I don't think we need all of it
"""
def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submit_inquiry')  # Redirect after POST
    else:
        form = InquiryForm()
    return render(request, 'submit_inquiry.html', {'form': form})


def admin_dashboard(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'admin_dashboard.html', {'inquiries': inquiries})


def reply_inquiry(request, pk):
    inquiry = Inquiry.objects.get(pk=pk)
    if request.method == 'POST':
        reply_message = request.POST['reply']
        inquiry.reply = reply_message
        inquiry.save()

        # Send the email to the user
        send_email(inquiry.email, reply_message)

        return redirect('admin_dashboard')
    return render(request, 'reply_inquiry.html', {'inquiry': inquiry})
"""

def send_email(to_email, reply_message):
    try:
        print("sending message in django to:" +to_email +"message is : " + reply_message)
        connection_string = settings.AZURE_EMAIL_CONNECTION_STRING
        sender_address = settings.AZURE_EMAIL_SENDER_ADDRESS

        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": sender_address,
            "recipients": {
                "to": [{"address": to_email}],
            },
            "content": {
                "subject": "Reply to your inquiry",
                "plainText": reply_message,
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

        if result["status"] == "Succeeded":
            print(f"Successfully sent the email (operation id: {result['id']})")
        else:
            raise RuntimeError(f"Failed to send email: {result['error']}")

    except Exception as ex:
        print(f"Error sending email: {ex}")
