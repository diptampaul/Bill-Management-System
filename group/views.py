from django.shortcuts import render
from bill.models import Bill
from .models import Group_Details, Group_Members
from .utils import get_bills, update_upvotes, convert_pending_to_approve
import mimetypes
import os
from django.http.response import HttpResponse

#REMAINING  reduce the bill amount/4 from the wallet after getting approval, change the dues list with wallet and all the other things, add bill clear option to approved bills (if all members has sufficient amount in wallet), add each member/group ewallet, add clear from wallet in the individual due section, add wallet balance to individual members, 

# Create your views here.
def group(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
        #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #logged in to billed dashboard
                    pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
def bill_upvote(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
        bill_ids =  request.POST.getlist('billids') #To fetch list of values from checklist
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Update the upvoted bills
                    for id in bill_ids:
                        update_upvotes(int(id))
                    #Converting pending bills into approved bills if condition matches
                    convert_pending_to_approve(str(gd.gid))
                    pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                    #Pending Dues for each person
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
def add_bill_home(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Get all users of that group
                    member_details = []
                    for member in Group_Members.objects.filter(gid = gd.gid):
                        member_details.append({'id': member.mid, 'name': member.m_name, 'wallet': member.wallet_balance})
                    return render(request, 'group/add_bill.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
def bill_added(request):
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Take all the inputs
                    file_path = request.FILES['upload']
                    amount = request.POST['amount']
                    billed_for =  request.POST['billed_for']
                    billed_by =  request.POST['billed_by']  #Returns the member id
                    #save the bill file
                    with open(f"{BASE_DIR}/media/bills/{str(file_path)}", 'wb+') as destination:
                        for chunk in file_path.chunks():
                            destination.write(chunk)
                    #Check if the billed amount / total member is less than the billed by wallet amount
                    try:
                        if float(amount) > Group_Members.objects.get(mid = billed_by).wallet_balance:
                            pass
                            #Wallet condition is not applicable as of now as we will check it before approving any bill
                            # member_details = []
                            # for member in Group_Members.objects.filter(gid = gd.gid):
                            #     member_details.append({'id': member.mid, 'name': member.m_name, 'wallet': member.wallet_balance})
                            # return render(request, 'group/add_bill.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'WUSER': True})
                    except:
                        member_details = []
                        for member in Group_Members.objects.filter(gid = gd.gid):
                            member_details.append({'id': member.mid, 'name': member.m_name, 'wallet': member.wallet_balance})
                        return render(request, 'group/add_bill.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'INVALID': True})
                    #add new bill
                    bill_obj = Bill()
                    bill_obj.photo = f"bills/{file_path}"
                    bill_obj.bid = len(Bill.objects.all()) + 1
                    bill_obj.billed_for = billed_for
                    bill_obj.amount = amount
                    bill_obj.status = 'P'
                    bill_obj.upvote = 0
                    bill_obj.gid = gd.gid
                    bill_obj.mid = billed_by
                    bill_obj.save()
                
                    pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
    
    
    
    
    
def bills_download(request, filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/bills/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')