from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, HttpResponseRedirect
from django.db.models import Q
from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context, Template, loader
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings
from django.utils import timezone
from django.db.models import F
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import datetime as dt
import json
import re
import os
import urllib.request
import urllib.parse
import threading
import uuid
import time
from random import shuffle, randint
import sys
import math
import smtplib

from bs4 import BeautifulSoup

from Main.handlers.utilities import get_remote_IP, check_recaptcha
from Main.handlers.settings import MAX_COMPANIES, get_DEBUG, is_bot
from Main.API.manager import api
from Main.handlers.view import view_handler, add_error, add_success
from Main.models import Companies, Tokens, CAE, Visits, Messages


def error500(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'error500.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies}, status="500")

#def error404(request):
#    random = randint(1, MAX_COMPANIES)
#    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

#    return render(request, '404.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies}, status="404")

# Create your views here.
@csrf_exempt
def v1_req(request):
    return redirect('index')

@csrf_exempt
def api_req(request, endpoint, action=""):
    result = api(request, endpoint, action)

    willCallback = request.GET.get('callback', "")

    if(willCallback == ""):
        return JsonResponse(result.getResult(), status=result.getCode())
    else:
        dict = {
            "callback": willCallback,
            "response": json.dumps(result.getResult())
        }
        return render(request, 'api_callback.html', dict, status=result.getCode())

def index(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()
    a = '''
    import xlrd

    start_time = time.time()

    tmp_all = []

    for fn in os.listdir('/root/workspace/extractor/result3/'):
        print(fn)

        book = xlrd.open_workbook("/root/workspace/extractor/result3/" + fn)
        sh = book.sheet_by_index(0)

        for line in range(1, sh.nrows):
            tmp_all.append(
                {
                    "identifier": str(sh.cell_value(rowx=line, colx=1)),
                    "name": str(sh.cell_value(rowx=line, colx=0)),
                    "cae": str(sh.cell_value(rowx=line, colx=2)),
                    "cae_text": str(sh.cell_value(rowx=line, colx=3)),
                    "state": str(sh.cell_value(rowx=line, colx=5)),
                    "city": str(sh.cell_value(rowx=line, colx=6)),
                    "started_at": str(sh.cell_value(rowx=line, colx=4)),
                    "active": bool(sh.cell_value(rowx=line, colx=7)),
                }
            )


    shuffle(tmp_all)
    print("Empresas baralhadas")

    a = 0
    b = 0
    total = str(len(tmp_all))

    for line in tmp_all:
        b += 1
        try:
            Companies.objects.create(
                identifier=line["identifier"],
                name=line["name"],
                cae=line["cae"],
                state=line["state"],
                city=line["city"],
                started_at=line["started_at"],
                active=line["active"]
            )

            CAE.objects.create(
                pk=line["cae"],
                text=line["cae_text"]
            )

        except:
            a = a+1
            pass

        sys.stdout.write("\r" + str(b) + " empresas de " + str(total) + " carregadas")
        sys.stdout.flush()

    sys.stdout.write("\r" + str(b) + " empresas de " + total + " carregadas\n")
    sys.stdout.flush()

    print("Não foi possivel carregar " + str(a) + " empresas")

    print("--- %s seconds ---" % (time.time() - start_time))'''



    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'index.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies})

def company(request, nif):

    company = get_object_or_404(Companies, identifier=nif)

    structured_data = {
        "@context": "http://schema.org",
        "@type": "Organization",
        "legalName": company.name,
        "taxID": company.identifier,
        "address": [{
            "@type": "PostalAddress",
            "addressCountry": "PT"
        }]
    }

    if company.website:
        structured_data.update(
            {
                "url": company.website
            }
        )
    else:
        structured_data.update(
            {
                "url": "https://www.getcompany.info/" + str(company.identifier) + "/"
            }
        )

    if company.address:
        structured_data["address"][0].update({
            "streetAddress": company.address
        })

    if company.phone:
        structured_data.update({
            "contactPoint": [{
                "@type": "ContactPoint",
                "telephone": "+351" + str(company.phone),
                "contactType": "customer service"
            }],
            "telephone": "+351" + str(company.phone)
        })

        if company.fax:
            structured_data["contactPoint"][0].update(
                {
                    "faxNumber": "+351" + str(company.fax)
                }
            )

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):

        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()

        company.visits_bots += 1
        company.save()

        #random = randint(1, MAX_COMPANIES)
        #random_companies = Companies.objects.filter(id__gt=random, active=True, cae=company.cae).exclude(state="")[:8]

        return render(request, 'company-bots.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "company": company, "title": str(company.name + " " + company.identifier + " - GetCompany.info"), "structured_data": json.dumps(structured_data)})

    if company.error_crawling == True or company.already_crawled == False:
        t = threading.Thread(target=Crawl_Company,
                                    args=[nif])
        t.setDaemon(True)
        t.start()

    tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
    tmp_model.usersVisits=F('usersVisits')+1
    tmp_model.save()

    company.visits_users += 1
    company.save()

    current_hash = str(uuid.uuid4())[:32]

    free_id = False


    max_tries = 10
    tries = 0


    while not free_id:

        if tries > max_tries:
            return 504

        tries += 1

        if Tokens.objects.filter(id=current_hash).exists():

            current_hash = str(uuid.uuid4())[:32]
        else:
            free_id = True

    Tokens.objects.create(pk=current_hash, company_id=company.pk)

    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True, cae=company.cae).exclude(state="")[:8]

    return render(request, 'company.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "company": company, "random_companies": random_companies, "token": current_hash, "title": str(company.name + " " + company.identifier + " - GetCompany.info"), "structured_data": json.dumps(structured_data)})

def redirectCompany(request, nif):
    return HttpResponseRedirect("/" + str(nif) + "/")

def docs(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'documentation.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies})

def contact(request):
    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    if request.method == "POST":
        try:

            grecaptcharesponse = request.POST.get("g-recaptcha-response", '')

            if (grecaptcharesponse.strip() == ''):
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "Captcha é obrigatorio"})

            name = request.POST["name"].strip()
            email = request.POST["email"].strip()
            message = request.POST["message"].strip()
            company = request.POST.get("company", '').strip()
            subject = request.POST["subject"]

            # Verify if the recaptcha is valid
            data = urllib.parse.urlencode({"secret": "6LcMFykTAAAAADsrJh8PGYKt_wJlhH67d7HgtKQT", "response": grecaptcharesponse, "remoteip": get_remote_IP(request)})
            binary_data = data.encode('utf-8')
            u = urllib.request.urlopen("https://www.google.com/recaptcha/api/siteverify", binary_data)
            result = u.read()
            recaptcha_result = json.loads(result.decode('utf-8'))

            if recaptcha_result["success"] == False:
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "Captcha não é valido, tente novamente"})

            if subject not in ["1", "2", "3"]:
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "Ocorreu um erro, tente novamente"})

            if len(name) < 1:
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "O nome é obrigatorio"})

            if len(email) < 1:
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "O email é obrigatorio"})

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "O email não é valido"})

            if len(message) < 1:
                return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "A mensagem é obrigatoria"})

            if len(name) > 50:
                name = name[0:50]

            if len(email) > 50:
                email = email[0:50]

            if len(message) > 1000:
                message = message[0:1000]

            if len(company) > 50:
                company = company[0:50]

            Messages.objects.create(
                name=name,
                email=email,
                message=message,
                company=company,
                subject=subject,
                ip=get_remote_IP(request),
                useragent=request.META['HTTP_USER_AGENT']
                )

            t = loader.get_template('emails/contact.html')
            output = t.render({
                "name": name,
                "email": email,
                "message": message,
                "company": company,
                "subject": subject,
                "ip": get_remote_IP(request),
                "useragent": request.META['HTTP_USER_AGENT']
            })

            msg = EmailMultiAlternatives("GetCompany.Info - " + str(name), output, "geral@getcompany.info", ["g4bryrm98@hotmail.com"])
            msg.attach_alternative(output, 'text/html')
            msg.send(True)

            return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "success": "Mensagem enviada, aguarde resposta nos proximos dias"})

        except:
            return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies, "error": "Ocorreu um erro, tente novamente"})

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    return render(request, 'contact.html', {"is_bot": is_bot(request), "debug": get_DEBUG() , "random_companies": random_companies})

def status(request):

    try:
        pw = request.GET["pw"]
    except:
        return render(request, '404.html', {"is_bot": is_bot(request), "debug": get_DEBUG()})

    if(pw == "justdoit"):

        dic = {
            "legend": '<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>',
            "labels": [],
            "uservisits": [],
            "botvisits": [],
            "companiesCrawled": []
        }

        counter = Visits.objects.all().count()
        counter -= 30

        visitas = Visits.objects.all().order_by('-id')[:30]

        for visit in visitas:
            dic["labels"].append(str(visit.date)[:10])
            dic["uservisits"].append(visit.usersVisits)
            dic["botvisits"].append(visit.botsVisits)
            dic["companiesCrawled"].append(visit.companiesCrawled)

        final_dict = {
            "legend": dic["legend"],
            "labels": json.dumps(dic["labels"]),
            "uservisits": json.dumps(dic["uservisits"]),
            "botvisits": json.dumps(dic["botvisits"]),
            "companiesCrawled": json.dumps(dic["companiesCrawled"]),
            "is_bot": is_bot(request),
            "debug": get_DEBUG()
        }

        return render(request, 'status.html', final_dict)

    else:
        return render(request, '404.html', {"is_bot": is_bot(request), "debug": get_DEBUG()})


def about(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    return render(request, 'about.html', {})

def terms(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    return render(request, 'terms.html', {})

def sitemapmain(request):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    companies_per_sitemap = 30000

    total_companies = Companies.objects.all().count()

    sitemaps = math.ceil(total_companies/companies_per_sitemap)

    result = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for i in range(0, sitemaps):
        result += '<sitemap><loc>https://www.getcompany.info/companies-' + str(i) + '.xml</loc></sitemap>'

    result += '</sitemapindex>'

    return HttpResponse(result, content_type='text/xml; charset=UTF-8')

def sitemap_companies(request, id):

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.botsVisits=F('botsVisits')+1
        tmp_model.save()
    else:
        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.usersVisits=F('usersVisits')+1
        tmp_model.save()

    companies_per_sitemap = 30000

    skip = int(id) * companies_per_sitemap
    get = skip + companies_per_sitemap

    total_companies = Companies.objects.all()[skip:get]

    result = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for company in total_companies:
        result += '<url><loc>https://www.getcompany.info/' + company.identifier + '/</loc><lastmod>' + str(company.updated_at)[:10] + '</lastmod></url>'

    result += '</urlset>'

    return HttpResponse(result, content_type='text/xml; charset=UTF-8')

def Crawl_Company(nif):
    try:
        fp = urllib.request.urlopen(str("https://www.gescontact.pt/" + nif))
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")

        fp.close()
    except:
        company = Companies.objects.get(identifier=nif)

        company.already_crawled = True
        company.error_crawling = True

        company.save()

    else:

        soup = BeautifulSoup(mystr, "html.parser");
        data = soup.find('div', attrs={"class": "post-content box mark-links entry-content"});

        data2 = data.find_all('p')

        state = "Sintra"

        address = None
        address_l2 = None
        phone = None
        mobile = None
        fax = None
        email = None

        info = False
        about = None
        products = None
        brands = None
        tags = None

        links = False
        website = None
        facebook = None
        twitter = None
        linkedin = None
        googleplus = None

        active_tab = None

        x = 0
        for i in data2:
            x += 1

            tmp = i.get_text().strip()

            if(x == 4):
                address_l2 = str(tmp.strip())
                pass

            if(tmp.startswith("Morada:")):
                address = str(tmp.replace("Morada: ", "").strip())
                pass

            if(tmp.endswith(state)):
                address_l2 = str(tmp.strip())
                pass

            if(tmp.startswith("Telefone:")):
                phone = str(tmp[:19].replace("Telefone: ", "").strip())
                pass

            if(tmp.startswith("Telemóvel:")):
                mobile = str(tmp[:20].replace("Telemóvel: ", "").strip())
                pass

            if(tmp.startswith("Fax:")):
                fax = str(tmp[:14].replace("Fax: ", "").strip())
                pass

            if(tmp.startswith("E-mail:")):
                tmp2 = str(tmp.replace("E-mail:", "").strip())
                if(tmp2 == ""):
                    email = None
                else:
                    email = tmp2
                pass

            if(tmp.startswith("Apresentação:")):
                info = True
                about = str(tmp.replace("Apresentação: ", "").strip())
                if active_tab == None:
                    active_tab = 1
                pass

            if(tmp.startswith("Produtos e Serviços:")):
                info = True
                products = str(tmp.replace("Produtos e Serviços: ", "").strip())
                if active_tab == None:
                    active_tab = 2
                pass

            if(tmp.startswith("Marcas:")):
                info = True
                brands = str(tmp.replace("Marcas: ", "").strip())
                if active_tab == None:
                    active_tab = 3
                pass

            if(tmp.startswith("Etiquetas:")):
                info = True
                tags = str(tmp.replace("Etiquetas: ", "").strip())
                if active_tab == None:
                    active_tab = 4
                pass

            if(tmp.startswith("Website:")):
                links = True
                website = str(tmp.replace("Website: ", "").strip())
                pass

            if(tmp.startswith("Facebook:")):
                links = True
                facebook = str(tmp.replace("Facebook: ", "").strip())
                pass

            if(tmp.startswith("Twitter:")):
                links = True
                twitter = str(tmp.replace("Twitter: ", "").strip())
                pass

            if(tmp.startswith("LinkedIn:")):
                links = True
                linkedin = str(tmp.replace("LinkedIn: ", "").strip())
                pass

            if(tmp.startswith("Google + :")):
                links = True
                googleplus = str(tmp.replace("Google + : ", "").strip())
                pass

        company = Companies.objects.get(identifier=nif)

        company.address = address
        company.address_l2 = address_l2
        company.phone = phone
        company.mobile = mobile
        company.fax = fax
        company.email = email
        company.info = info
        company.about = about
        company.products = products
        company.brands = brands
        company.tags = tags
        company.links = links
        company.website = website
        company.facebook = facebook
        company.twitter = twitter
        company.linkedin = linkedin
        company.googleplus = googleplus
        company.active_tab = active_tab

        company.updated_at = timezone.now()

        company.already_crawled = True
        company.error_crawling = False

        company.save()

        tmp_model = Visits.objects.get_or_create(date=str(dt.datetime.now())[:10])[0]
        tmp_model.companiesCrawled=F('companiesCrawled')+1
        tmp_model.save()