from .models import Account

def account_processor(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    return {
        'user_account': account
    }



