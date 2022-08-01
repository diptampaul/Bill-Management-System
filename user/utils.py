from group.models import Group_Members
from .models import GroupMemberPayout

def get_payout_update(group_id):
    member_details = []
    for member in Group_Members.objects.filter(gid = group_id):
        member_details.append({'id': member.mid, 'name': member.m_name, 'wallet': member.wallet_balance})
    #Check every users corresponding payment details as of preference
    for member in member_details:
        payment_obj = GroupMemberPayout.objects.filter(mid = member['id'])
        if len(payment_obj) == 0:
            member['payment_added']= False
        else:
            member['payment_added']= True
            payment_obj = payment_obj[0]
            preferred_payment = payment_obj.receiving_preference
            if preferred_payment == 'B':
                member['payment_mode'] = 'Bank Transfer'
                member['payment_details'] = [payment_obj.account_number, payment_obj.ifsc_code, payment_obj.account_name]
            elif preferred_payment == 'W':
                member['payment_mode'] = 'Wallet Transfer'
                if payment_obj.wallet_type == 'P':
                    member['payment_details'] = ['Paytm Pay', payment_obj.wallet_number]
                else:
                    member['payment_details'] = ['Google Pay', payment_obj.wallet_number]
            elif preferred_payment == 'U':
                member['payment_mode'] = 'UPI Transfer'
                member['payment_details'] = [payment_obj.upi]
    print(member_details)
    return member_details

def account_number_validation(account_no):
    validation_status, wrong_fields = False, []
    try:
        converted = int(account_no)
    except:
        validation_status = True
        wrong_fields.append({'field': 'acc', 'value': account_no})
    return validation_status, wrong_fields

def upi_validation(upi_id):
    validation_status, wrong_fields = False, []
    if '@' not in upi_id:
        validation_status = True
        wrong_fields.append({'field': 'upi', 'value': upi_id})
    return validation_status, wrong_fields