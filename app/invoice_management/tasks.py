# tasks.py

# from celery import shared_task
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from cm_backend.celery import app
from django.db.models import Q
import sys
import traceback

from common.services import send_mail
from app.user_authentication.models import *
from app.invoice_management.models import *
from app.contract_management.models import *
from app.space_management.models import *
from .models import *
from celery import shared_task
from cm_backend import settings
# from django.core.mail import send_mail
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from celery import app
from datetime import timedelta,date
import datetime
from django.utils import timezone
from twilio.rest import Client as smsauth
from twilio.base.exceptions import TwilioRestException
from cm_backend import settings
from cm_backend.celery import app
from django.db.models import F, Sum
from django.template.loader import render_to_string



@app.task(name= 'generate_bills')
def generate_bills():

    try:
        today = date.today()

        contracts = Contract.objects.filter(is_active = True, status=1)

        for contract in contracts:
            contract_date = contract.valid_from
            print("contract date is:",contract_date)
            
            if contract_date.day == today.day:
                print(f"Contract ID: {contract.id}")
                print(f"Created Date: {contract_date}")
                # print(f"Exceed Date: {exceed_date}")
                due_date = today + timedelta(days=14)
                print(f"Due date is: {due_date}")
                customer = contract.customer
                space = contract.space
                rent = contract.space.rent_price
                print(f"Customer is:{customer}")
                print(f"Space is:{space}")
                print(f"Rent is:{rent}")
                elect_charge = contract.space.building.electricity_charge
                print(elect_charge)
                water_charge = contract.space.building.water_charge
                print(water_charge)
                maintenance = contract.space.building.maintenance_charge
            
                one_month_ago = today - relativedelta(months=1)
                month = one_month_ago.strftime("%m")  # Get the month as a zero-padded string
                year = one_month_ago.strftime("%Y")  # Get the year as a four-digit string
                code = contract.space.code
                invoice = f"KMRL{year}{month}{code}"
                print(f"Rent is:{invoice}")

                utility_readings = UtilityReading.objects.filter(year=year, month=month, is_approved=True, space=space)
                print(utility_readings)
                if utility_readings.exists():
                    elect_reading = utility_readings[0].electricity_reading
                    print(f"Electricity Reading: {elect_reading}")

                    wat_reading = utility_readings[0].water_reading
                    print(f"Water Reading: {wat_reading}")

                    electricity = elect_charge * elect_reading
                    print(f"Electricity Cost: {electricity}")

                    water = water_charge * wat_reading
                    print(f"Water Cost: {water}")

                    total_amount = electricity+water+maintenance+rent
                    print(total_amount)

                    existing_invoice = Invoice.objects.filter(customer=customer, space=space, month=month, year=year)

                    if existing_invoice.exists():
                        print(f"Invoice already exists: {existing_invoice.first()}")
                    else:
                        invoice_obj = Invoice.objects.create(
                            customer=customer,
                            space=space,
                            payment_status=1,
                            rent_amount=rent,
                            water_charge=water,
                            electricity_charge=electricity,
                            maintenance_charge=maintenance,
                            total_amount=total_amount,
                            due_date=due_date,
                            invoice_number=invoice,
                            year=year,
                            month=month
                        )
                        print("New invoice created:", invoice_obj)
                else:
                    print('utlity reading not taken. canot generate bill')

        late_fees = 100
        Invoice.objects.filter(Q(payment_status=1) & Q(due_date__lt=today)).update(late_fee=late_fees)
        Invoice.objects.filter(Q(payment_status=1) & Q(due_date__lt=today)).filter(is_null=True).update(late_fee=late_fees,total_amount=F('total_amount') + late_fees)    

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        msg = err

def send_payment_reminder_mail(invoice, color_code):
    type = "due_date_mail"
    notification_obj = Notification_Content.objects.get(notification_type=type)
    content = notification_obj.content
    print(content)
    
    mail = invoice.customer.email
    print(mail)
    previous_month = invoice.due_date - timedelta(days=invoice.due_date.day)
    month = previous_month.strftime("%B")
    name= invoice.customer.get_full_name()
    due_date= invoice.due_date
    total_bill_amount= invoice.total_amount
    space_code = invoice.space.code
    building = invoice.space.building.name
    year = invoice.year
    print(f"..space code..{space_code}")
    print(f".building..{building}")
    data = {
            'name': name,
            'month': month,
            'due_date': due_date,
            'total_bill_amount': total_bill_amount,
            'space_code' : space_code,
            'building' : building,
            'year' : year
        }
    for key, value in data.items():
        placeholder = f"<<{key}>>"
        content = content.replace(placeholder, str(value))
    formatted_content = content.format(
                                        name= name,
                                        month= month,
                                        due_date= due_date,
                                        total_bill_amount= total_bill_amount,
                                        space_code = space_code,
                                        building = building,
                                        year = year
                                    )
    print(formatted_content)
    msg = render_to_string(str(settings.BASE_DIR)+'/templates/email_templates/reminder.html',
                                                {
                                                    'color_code': color_code,
                                                    'content': formatted_content
                                                })

    send_mail(mail,'Rent Payment Reminder.!!!',msg)
    print("Reminder mail has been sent")

@app.task(name='send_payment_alert_email')
def send_payment_alert_email():
    try:
        
        type = "due_date_mail"
        notification_obj = Notification_Content.objects.get(notification_type=type)
        content = notification_obj.content
        # print(content)
        pending_invoices = Invoice.objects.filter(payment_status=1,is_active=True)
        # pending_invoices = pending_invoices.annotate(
        #     latefee_bill_amount=Sum(F('total_amount')+ F('late_fee'))
        # )
        current_date = timezone.now().date()
        print(current_date)
        for invoice in pending_invoices:
            due_date = invoice.due_date
            print(due_date)
            five_days_before = due_date - timedelta(days=5)
            print(five_days_before)
            three_days_before = due_date - timedelta(days=3)
            one_day_before = due_date - timedelta(days=1)
            if current_date == five_days_before:
                send_payment_reminder_mail(invoice, 'green')
            elif current_date == three_days_before:
                send_payment_reminder_mail(invoice, 'yellow')
            elif current_date == one_day_before:
                send_payment_reminder_mail(invoice, 'red')
            elif current_date >= invoice.due_date:
                previous_month = invoice.due_date - timedelta(days=invoice.due_date.day)
                month = previous_month.strftime("%B")
                mail = invoice.customer.email
                name= invoice.customer.get_full_name()
                total_bill_amount= invoice.total_amount
                due_date= invoice.due_date
                space_code = invoice.space.code
                building = invoice.space.building.name
                year = invoice.year
                type = "late_fee_mail"
                notification_obj = Notification_Content.objects.get(notification_type=type)
                content = notification_obj.content
                data = {
                        'name': name,
                        'total_bill_amount': total_bill_amount,
                        'due_date': due_date,
                        'space_code' : space_code,
                        'building' : building,
                        'month' : month,
                        'year' : year
                    }
                for key, value in data.items():
                    placeholder = f"<<{key}>>"
                    content = content.replace(placeholder, str(value))
                formatted_content = content.format(
                                                    name= name,
                                                    total_bill_amount= total_bill_amount,
                                                    due_date= due_date,
                                                    space_code = space_code,
                                                    building = building,
                                                    month = month,
                                                    year = year
                                                )

                print(formatted_content)
                # print(mail)
                msg = render_to_string(str(settings.BASE_DIR)+'/templates/email_templates/late_fee_reminder.html', {
                'content': formatted_content
                })
                send_mail(mail,'Rent Payment Reminder.!!!',msg)
                print("Reminder mail has been sent")
            else:
                print('No Mails')
                pass
    except Exception as e:
        print(e)


def send_invoice_reminder(invoice, message, client, from_number):
    phonenumber = invoice.customer.phonenumber
    message_result = client.messages.create(to=phonenumber, from_=from_number, body=message)
    print(message_result)
    print("Reminder SMS has been sent")


@app.task(name='send_payment_alert_sms')
def send_payment_alert_sms():
    try:
        ACCOUNT_SID = 'ACa0ed2062f098fa6b10897d833b82e236'
        ACCOUNT_TOKEN = '0fcc3c35a70fb56fc1080524e567d666'
        client = smsauth(ACCOUNT_SID, ACCOUNT_TOKEN)
        from_number = '+12294596943'
        pending_invoices = Invoice.objects.filter(payment_status=1,is_active=True)
        print(pending_invoices)
        current_date = timezone.now().date()
        for invoice in pending_invoices:
            due_date = invoice.due_date
            five_days_before = due_date - timedelta(days=5)
            three_days_before = due_date - timedelta(days=3)
            one_day_before = due_date - timedelta(days=1)
            previous_month = invoice.due_date - timedelta(days=invoice.due_date.day)
            month = previous_month.strftime("%B")
            name= invoice.customer.get_full_name()
            due_date= invoice.due_date
            total_bill_amount= invoice.total_amount
            space_code = invoice.space.code
            building = invoice.space.building.name
            year = invoice.year
            
            type = "due_date_sms"
            notification_obj = Notification_Content.objects.get(notification_type=type)
            content = notification_obj.content
            data = {
                    'name': name,
                    'month': month,
                    'due_date': due_date,
                    'total_bill_amount': total_bill_amount,
                    'space_code' : space_code,
                    'building' : building,
                    'year' : year
                    }
            for key, value in data.items():
                placeholder = f"<<{key}>>"
                content = content.replace(placeholder, str(value))
            formatted_content = content.format(
                                                name= name,
                                                month= month,
                                                due_date= due_date,
                                                total_bill_amount= total_bill_amount,
                                                space_code = space_code,
                                                building = building,
                                                year = year
                                            )
            print(formatted_content)
            msg = formatted_content

            type = "late_fee_sms"
            notification_obj = Notification_Content.objects.get(notification_type=type)
            content = notification_obj.content
            data = {
                    'name': name,
                    'month': month,
                    'due_date': due_date,
                    'total_bill_amount': total_bill_amount,
                    'space_code' : space_code,
                    'building' : building,
                    'year' : year 
                    }
            for key, value in data.items():
                placeholder = f"<<{key}>>"
                content = content.replace(placeholder, str(value))
            formatted_content_msg1 = content.format(
                                                name= name,
                                                month= month,
                                                due_date= due_date,
                                                total_bill_amount= total_bill_amount,
                                                space_code = space_code,
                                                building = building,
                                                year = year
                                            )
            print(formatted_content_msg1)
            msg1 = formatted_content_msg1
            
            if current_date == five_days_before:
               send_invoice_reminder(invoice, msg, client, from_number)
            elif current_date == three_days_before:
               send_invoice_reminder(invoice, msg, client, from_number)
            elif current_date == one_day_before:
                send_invoice_reminder(invoice, msg, client, from_number)
            elif current_date >= invoice.due_date:
               send_invoice_reminder(invoice, msg1, client, from_number)
            else:
                print('No sms')
                pass
    except TwilioRestException as err:
        print("TwilioRestException",err)
    except Exception as e:
        print('Error in sms sending : ', e)


