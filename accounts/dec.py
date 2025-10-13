
def login_not_required(view_func):
    view_func.login_exempt = True
    return view_func