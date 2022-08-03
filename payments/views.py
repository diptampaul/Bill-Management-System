from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from group.models import Group_Details, Group_Members
from .utils import get_razorpay_client, razorpay_initial_object
from group.utils import get_bills
from .models import PaymentInitialized, PaymentHistory

# Create your views here.
def top_up_wallet(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Get razorpay client
                    razorpay_client = get_razorpay_client()
                    #Take all the inputs
                    try:
                        member_id = request.POST.getlist('member_id')[0]
                    except:
                        return HttpResponseBadRequest()
                    amount = request.POST['amount']
                    if amount < 10:
                        return HttpResponseBadRequest()
                    member_details = Group_Members.objects.get(mid = member_id)
                    context = razorpay_initial_object(razorpay_client, float(str(amount)+"00"))
                    #Store into payment initialized table
                    payment_initialized_obj = PaymentInitialized()
                    payment_initialized_obj.order_id = context['razorpay_order_id']
                    payment_initialized_obj.mid = member_id
                    payment_initialized_obj.actual_amount = amount
                    payment_initialized_obj.amount = float(str(amount)+"00")
                    payment_initialized_obj.gid = str(gd.gid)
                    payment_initialized_obj.g_password = g_password
                    payment_initialized_obj.save()
                    return render(request, 'payment/initiate.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'context': context, 'amount': amount})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
    
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        print("POST REQUEST")
        try:
            print("Client setup done")
           #Get razorpay client
            razorpay_client = get_razorpay_client()
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print(params_dict)
            
            #Try to load the saved data in temporary table, if not found throw error
            try:
                payment_initialized_obj = PaymentInitialized.objects.get(order_id = razorpay_order_id)
            except:
                return render(request, 'payment/paymentfailed.html')

            #loading the neccessary things
            gid = payment_initialized_obj.gid
            g_password = payment_initialized_obj.g_password
            g_det = Group_Details.objects.get(gid = gid).g_name
            pending_bills, approved_bills, dues, completed_bills = get_bills(gid)
            
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                print("Inside if")
                amount = payment_initialized_obj.amount  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    
                    #Save in the payment history table
                    payment_history_obj = PaymentHistory()
                    payment_history_obj.order_id = razorpay_order_id
                    payment_history_obj.payment_id = payment_id
                    payment_history_obj.mid = payment_initialized_obj.mid
                    payment_history_obj.amount = payment_initialized_obj.actual_amount
                    payment_history_obj.save()
                    
                    #increase the wallet balance
                    group_member_obj = Group_Members.objects.get(mid = payment_initialized_obj.mid)
                    group_member_obj.wallet_balance = float(group_member_obj.wallet_balance) + float(payment_initialized_obj.actual_amount)
                    group_member_obj.save()
                    
                    # render success page on successful caputre of payment
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'payment_success': True, 'topup_amount': payment_initialized_obj.actual_amount})
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'payment_failed': True})
            else:
                # if signature verification fails.
                return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'payment_failed': True})
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()