from django.shortcuts import render
from bill.models import Bill
from .models import Group_Details, Group_Members
from .utils import get_bills, update_upvotes, convert_pending_to_approve
import mimetypes
import os
from django.http.response import HttpResponse

#REMAINING    Adding new bills, change the dues list with wallet and all the other things, add bill clear option to approved bills (if all members has sufficient amount in wallet), add each member/group ewallet, add clear from wallet in the individual due section, add wallet balance to individual members, 

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
        bill_ids =  request.POST.getlist('billids')            #To fetch list of values from checklist
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