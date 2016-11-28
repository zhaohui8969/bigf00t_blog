def check_login(request):
    if request.user.is_superuser:
        return True
    return False