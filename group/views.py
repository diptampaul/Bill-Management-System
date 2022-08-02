from django.shortcuts import render
from bill.models import Bill
from user.models import GroupMemberPayout
from .models import Group_Details, Group_Members
from .utils import get_bills, update_upvotes, convert_pending_to_approve, update_payout_to_admin_panel
import mimetypes
import os
from django.http.response import HttpResponse

#REMAINING then move/send the billed amount to the admin db, make a admin panel to clear the bills, add clear from wallet in the individual due section, group the payout details for same user to find the total amount

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
                    #----------Pending
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
    

def bill_clear(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    bill_ids =  request.POST.getlist('billids') 
                    print(bill_ids)
                    payout_details = []
                    insufficent_balance_members = []
                    for bill_id in bill_ids:
                        bill_obj = Bill.objects.get(bid = bill_id)
                        #Check if the billed member added his wallet details or not, otherwise money couldn't be transferred hence throw error
                        try:
                            payout_obj = GroupMemberPayout.objects.get(mid = bill_obj.mid)
                        except:
                            payee = Group_Members.objects.get(mid = bill_obj.mid).m_name
                            pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                            return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'money_send_failed': True, 'payee': payee})
                        #Check if shared amount is present everyone's wallet, else return cannot be cleared.
                        all_members = Group_Members.objects.filter(gid = gd.gid)
                        for member in all_members:
                            if bill_obj.mid != member.mid:
                                if round((bill_obj.amount / len(all_members)),2) > member.wallet_balance:
                                    print(round((bill_obj.amount / len(all_members)),2))
                                    if len(insufficent_balance_members) == 0:
                                        insufficent_balance_members.append({'name': member.m_name, 'need_to_load': (round((bill_obj.amount / len(all_members)),2) - float(member.wallet_balance))})
                                    else:
                                        changed = False
                                        for insufficent_balance_member in insufficent_balance_members:
                                            if insufficent_balance_member['name'] == member.m_name:
                                                insufficent_balance_member['need_to_load'] = insufficent_balance_member['need_to_load'] + (round((bill_obj.amount / len(all_members)),2))
                                                changed = True
                                        if changed:
                                            continue
                                        else:
                                            insufficent_balance_members.append({'name': member.m_name, 'need_to_load': (round((bill_obj.amount / len(all_members)),2) - float(member.wallet_balance))})
                        if len(insufficent_balance_members) > 0:
                            continue
                        else:
                            #Now clear the bills  and reduce the shared amount from every payee except the biller
                            for member in all_members:
                                if bill_obj.mid != member.mid:
                                    member.wallet_balance = member.wallet_balance - round((bill_obj.amount / len(all_members)),2)
                                    member.save()
                            bill_obj.status = 'C'
                            #Add details of all the payouts  i.e. Payee Name, Payout Method, Total Amount Send, 
                            total_payout_amount = bill_obj.amount - round((bill_obj.amount / len(all_members)),2)
                            preferred_payment = payout_obj.receiving_preference
                            if preferred_payment == 'B':
                                payout_method = 'Bank Transfer'
                                pds = f"Account No: {payout_obj.account_number} \nIFSC: {payout_obj.ifsc_code} \nHolder Name:{payout_obj.account_name}"
                            elif preferred_payment == 'W':
                                payout_method = 'Wallet Transfer'
                                pds = f"Wallet No: {payout_obj.wallet_number} \nWallet Type: {payout_obj.wallet_type}"
                            elif preferred_payment == 'U':
                                payout_method = 'UPI Transfer'
                                pds = f"Account No: {payout_obj.upi}"
                            payee_name = Group_Members.objects.get(mid = bill_obj.mid).m_name
                            #Sum up the total amount for all the payees
                            if len(payout_details) == 0:
                                payout_details.append({'payee_name': payee_name, 'payout_method': payout_method, 'pds': pds, 'total_payout_amount': total_payout_amount, 'bill_ids': str(bill_obj.bid), 'mid': bill_obj.mid})
                            else:
                                added = False
                                for payout_detail in payout_details:
                                    if payout_detail['payee_name'] == payee_name:
                                        #Sum the total value
                                        payout_detail['total_payout_amount'] = payout_detail['total_payout_amount'] + total_payout_amount
                                        payout_detail['bill_ids'] = payout_detail['bill_ids'] + ',' +  str(bill_obj.bid)
                                        added = True
                                if added:
                                    continue
                                payout_details.append({'payee_name': payee_name, 'payout_method': payout_method, 'pds': pds, 'total_payout_amount': total_payout_amount, 'bill_ids': str(bill_obj.bid), 'mid': bill_obj.mid})
                            bill_obj.save() 
                                
                    if len(insufficent_balance_members) > 0:
                        pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                        #If one more bills are cleared, then send mail and show the warnings else show the error only.
                        if len(payout_details) > 0:
                            #Add to admin DB to send the money
                            print("Added to Admin DB, need to check and clear")
                            for payout_detail in payout_details:
                                update_payout_to_admin_panel(payout_detail=payout_detail)
                            return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'money_send_partially': True, 'payout_details': payout_details, 'insufficent_balance_members': insufficent_balance_members})
                        
                        return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'insufficent_balance_members_par': insufficent_balance_members})
                    #Add to admin DB to send the money
                    print("Added to Admin DB, need to check and clear")
                    for payout_detail in payout_details:
                        update_payout_to_admin_panel(payout_detail=payout_detail)
                    pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'dues': dues, 'completed_bills': completed_bills, 'money_send': True, 'payout_details': payout_details})
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