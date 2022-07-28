from bill.models import Bill
from .models import Group_Details, Group_Members

def get_bills(group_id):
    #Getting pending bills
    pending_bills = []
    for bill in Bill.objects.filter(status='P').filter(gid = group_id):
        member_id = bill.mid
        #Corresponding name of mid
        m_username = Group_Members.objects.get(mid = member_id).m_name
        pending_bills.append({'file': str(bill.photo).split("bills/")[-1], 'billed_for': bill.billed_for, 'amount': bill.amount, 'upvote': bill.upvote, 'created_at': bill.created, 'id': bill.bid, 'm_user': m_username})
    #Getting Approved bills
    approved_bills = []
    #Getting each individuals dues
    total_paid_list = {}
    for bill in Bill.objects.filter(status='A').filter(gid = group_id):
        member_id = bill.mid
        m_username = Group_Members.objects.get(mid = member_id).m_name
        approved_bills.append({'file': str(bill.photo).split("bills/")[-1], 'billed_for': bill.billed_for, 'amount': bill.amount, 'created_at': bill.created, 'id': bill.bid, 'm_user': m_username})
        if m_username not in total_paid_list:
            total_paid_list[m_username] = bill.amount
        else:
            total_paid_list[m_username] = total_paid_list[m_username] + bill.amount

    due_list = {}
    for member in Group_Members.objects.filter(gid = group_id):
        due_list[member.m_name] = 0
    for k,v in total_paid_list.items():
        shared_amount = v/len(due_list)
        for k1, v1 in due_list.items():
            if k != k1:
                due_list[k1] = due_list[k1] + shared_amount 
        
    return pending_bills, approved_bills, due_list

def update_upvotes(bid):
    bill_obj = Bill.objects.get(bid = bid)
    bill_obj.upvote = int(bill_obj.upvote) + 1
    bill_obj.save()

def convert_pending_to_approve(group_id):
    threshold = int(Group_Details.objects.get(gid = group_id).g_members) // 2
    for bill in Bill.objects.filter(status='P').filter(gid = group_id):
        if bill.upvote >= threshold:
            bill.status = 'A'
            bill.save()