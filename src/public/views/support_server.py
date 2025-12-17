from django.http import HttpResponseRedirect


def support_server(request):
    redirect_url = "https://discord.gg/2BksEkV"

    return HttpResponseRedirect(redirect_url)
