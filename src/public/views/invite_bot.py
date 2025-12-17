from django.http import HttpResponseRedirect


def invite_bot(request):
    redirect_url = "https://discord.com/api/oauth2/authorize?" \
                   "client_id=187636051135823872&" \
                   "permissions=741735489&" \
                   "redirect_uri=https%3A%2F%2Fduckhunt.me%2Fdocs%2Fbot-administration%2Fadmin-quickstart&" \
                   "scope=applications.commands%20bot"

    return HttpResponseRedirect(redirect_url)
