from django.shortcuts import render
from group.models import Group_Details, Group_Members
from group.utils import get_bills
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