from django.shortcuts import render
from group.models import Group_Details, Group_Members
from group.utils import get_bills
from .models import GroupMemberPayout
from .utils import get_payout_update, account_number_validation, upi_validation
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        pass
    return render(request, 'index.html',{})

#REgister and login view pending


def add_member(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
        m_name = request.POST['m_name']
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #If member list is full throw error
                    max_limit = int(gd.g_members)
                    all_users = Group_Members.objects.filter(gid = gd.gid)
                    if(len(all_users) == max_limit):
                        return HttpResponse("GROUP IS FULL .... !  CONTACT DIPTAM")
                    #else add the member
                    group_member = Group_Members()
                    group_member.gid = gd.gid
                    group_member.mid = int(f"{gd.gid}{len(all_users) + 1}")
                    group_member.m_name = m_name
                    group_member.save()
                    pending_bills, approved_bills, dues, completed_bills = get_bills(str(gd.gid))
                    return render(request, 'group/group.html', {'g_name': g_det, 'g_password': g_password, 'pending_bills': pending_bills, 'approved_bills': approved_bills, 'member_added': True, 'dues': dues, 'completed_bills': completed_bills})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
def add_payment(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Get all users payout details of that group
                    member_details = get_payout_update(gd.gid)
                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})
    
def add_successful_payment(request):
    if request.method == 'POST':
        g_det = request.POST['g_det']
        g_password = request.POST['g_password']
         #Checking the group id and password
        group_details = Group_Details.objects.all()
        for gd in group_details:
            if str(gd.gid) == g_det or gd.g_name == g_det:
                if gd.g_password == g_password:
                    #Get all users payout details of that group
                    member_details = get_payout_update(gd.gid)
                    #take all the input fields for all the members in list
                    member_ids = request.POST.getlist('member_id')
                    preferred_payout_mode = request.POST.getlist('payment_mode')
                    account_numbers = request.POST.getlist('account_number')
                    ifscs = request.POST.getlist('ifsc')
                    holder_names = request.POST.getlist('holder_name')
                    wallet_nos = request.POST.getlist('wallet_no')
                    wallet_types = request.POST.getlist('wallet_type')
                    upi_ids = request.POST.getlist('upi')
                    if len(member_ids) == len(preferred_payout_mode) == len(account_numbers) == len(ifscs) == len(holder_names) == len(wallet_nos) == len(wallet_types) == len(upi_ids):
                        #if all are equal continue with the functions, else return INVALID inputs 
                        #start the loop
                        for i in range(len(member_ids)):
                            if preferred_payout_mode[i] == 'N':
                                continue
                            #If the member already added payout details then update else add
                            try:
                                payout_obj = GroupMemberPayout.objects.filter(mid = member_ids[i])[0]
                            except:
                                payout_obj = GroupMemberPayout()
                                payout_obj.mid = member_ids[i]
                            payout_obj.receiving_preference = preferred_payout_mode[i]
                            if preferred_payout_mode[i] == 'B':
                                #Data validation for account number
                                validation_status, wrong_fields = account_number_validation(account_numbers[i])
                                if validation_status:
                                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_format': True, 'wrong_fields': wrong_fields})
                                if account_numbers[i] != '' and ifscs[i] != '' and holder_names[i] != '':
                                    payout_obj.account_number = account_numbers[i]
                                    payout_obj.account_name = holder_names[i]
                                    payout_obj.ifsc_code = ifscs[i]
                                else:
                                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_payment_mode': True})
                            elif preferred_payout_mode[i] == 'U':
                                validation_status, wrong_fields = upi_validation(upi_ids[i])
                                if validation_status:
                                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_format': True, 'wrong_fields': wrong_fields})
                                if upi_ids[i] != '':
                                    payout_obj.upi = upi_ids[i]
                                else:
                                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_payment_mode': True})
                            elif preferred_payout_mode[i] == 'W':
                                if wallet_nos[i] != '' and wallet_types[i] != '':
                                    payout_obj.wallet_number = wallet_nos[i]
                                    payout_obj.wallet_type = wallet_types[i]
                                else:
                                    return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_payment_mode': True})
                            else:
                                return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_input': True})
                            payout_obj.save()
                            print("Payout Addition Success")
                            member_details = get_payout_update(gd.gid)
                        return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details})
                    else:
                        return render(request, 'group/member_payment_add.html', {'g_name': g_det, 'g_password': g_password, 'member_details': member_details, 'wrong_input': True})
        return render(request, 'index.html', {"INVALID": True})
    else:
        return render(request, 'index.html', {})