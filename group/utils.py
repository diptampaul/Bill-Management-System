from bill.models import Bill
from .models import Group_Details, Group_Members, AdminBillClear

def get_bills(group_id):
    #Getting pending bills
    pending_bills = []
    for bill in Bill.objects.filter(status='P').filter(gid = group_id):
        #Corresponding name of mid
        m_username = Group_Members.objects.get(mid = bill.mid).m_name
        pending_bills.append({'file': str(bill.photo).split("bills/")[-1], 'billed_for': bill.billed_for, 'amount': bill.amount, 'upvote': bill.upvote, 'created_at': bill.created, 'id': bill.bid, 'm_user': m_username})
    #Getting Approved bills
    approved_bills = []
    #Getting each individuals dues
    total_paid_list = {}
    for bill in Bill.objects.filter(status='A').filter(gid = group_id):
        m_username = Group_Members.objects.get(mid = bill.mid).m_name
        approved_bills.append({'file': str(bill.photo).split("bills/")[-1], 'billed_for': bill.billed_for, 'amount': bill.amount, 'created_at': bill.created, 'id': bill.bid, 'm_user': m_username})
        if m_username not in total_paid_list:
            total_paid_list[m_username] = bill.amount
        else:
            total_paid_list[m_username] = total_paid_list[m_username] + bill.amount
    due_list = []
    for member in Group_Members.objects.filter(gid = group_id):
        due_list.append([member.mid,member.m_name, member.wallet_balance, 0])
    for k,v in total_paid_list.items():
        shared_amount = (v/len(due_list))
        for item in due_list:
            if k != item[1]:
                item[3] = item[3] + float(shared_amount)
    #Getting the completed bills
    completed_bills = []
    for bill in Bill.objects.filter(status='C').filter(gid = group_id):
        #Corresponding name of mid
        m_username = Group_Members.objects.get(mid = bill.mid).m_name
        completed_bills.append({'file': str(bill.photo).split("bills/")[-1], 'billed_for': bill.billed_for, 'amount': bill.amount, 'upvote': bill.upvote, 'created_at': bill.created, 'id': bill.bid, 'm_user': m_username})
    
    modified_due_list = []
    for member in due_list:
        modified_due_list.append({'name': member[1], 'amount': round(member[3],2), 'id' : member[0], 'wallet': member[2], 'size': len(due_list)})
        
    return pending_bills, approved_bills, modified_due_list, completed_bills

def update_upvotes(bid):
    bill_obj = Bill.objects.get(bid = bid)
    bill_obj.upvote = int(bill_obj.upvote) + 1
    bill_obj.save()

def convert_pending_to_approve(group_id):
    threshold = int(Group_Details.objects.get(gid = group_id).g_members) // 2
    for bill in Bill.objects.filter(status='P').filter(gid = group_id):
        if bill.upvote >= threshold:
            bill.status = 'A'
            #Reduce the shared amount from the user wallet
            # member_obj = Group_Members.objects.get(mid = bill.mid)
            # member_obj.wallet_balance = float(member_obj.wallet_balance) - round((bill.amount / len(Group_Members.objects.filter(gid = group_id))),2)
            # member_obj.save()
            bill.save()
            
def update_payout_to_admin_panel(payout_detail):
    send_to_admin = AdminBillClear()
    send_to_admin.cleared_bill_ids = payout_detail['bill_ids']
    send_to_admin.mid = payout_detail['mid']
    send_to_admin.user_name = payout_detail['payee_name']
    send_to_admin.bill_amount = payout_detail['total_payout_amount']
    send_to_admin.payout_method = payout_detail['payout_method']
    send_to_admin.payout_details = payout_detail['pds']
    send_to_admin.save()
    print(f"PAYOUT SENT TO ADMIN SUCCESSFULLY FOR {payout_detail['payee_name']}")