from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, HttpResponseRedirect
from django.db.models import Q
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, Template, loader
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings

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

from bs4 import BeautifulSoup

from Main.handlers.utilities import get_remote_IP, check_recaptcha
from Main.handlers.settings import MAX_COMPANIES
from Main.API.manager import api
from Main.handlers.view import view_handler, add_error, add_success
from Main.models import Companies, Tokens, CAE

def error404(request):
    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'error404.html', {"random_companies": random_companies}, status="404")

def error500(request):
    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'error500.html', {"random_companies": random_companies}, status="500")

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

    return render(request, 'index.html', {"random_companies": random_companies})

def company(request, nif):

    try:
        company = Companies.objects.get(identifier=nif)
    except Companies.DoesNotExist:
        return redirect('404')

    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):

        company.visits_bots += 1
        company.save()

        random = randint(1, MAX_COMPANIES)
        random_companies = Companies.objects.filter(id__gt=random, active=True, cae=company.cae).exclude(state="")[:8]

        return render(request, 'company-bots.html', {"company": company, "random_companies": random_companies, "title": str(company.name + " " + company.identifier + " - GetCompany.info")})

    t = threading.Thread(target=Crawl_Company,
                                args=[nif])
    t.setDaemon(True)
    t.start()

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

    return render(request, 'company.html', {"company": company, "random_companies": random_companies, "token": current_hash, "title": str(company.name + " " + company.identifier + " - GetCompany.info")})

def redirect(request, nif):
    return HttpResponseRedirect("/c/" + str(nif) + "/")

def docs(request):
    random = randint(1, MAX_COMPANIES)
    random_companies = Companies.objects.filter(id__gt=random, active=True).exclude(state="")[:8]

    return render(request, 'documentation.html', {"random_companies": random_companies})

def about(request):
    a = '''start = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    final = '</urlset>'


    total = Companies.objects.count()

    companies = Companies.objects.all()

    count = 0
    total_count = 0

    current_sitemap_text = start
    current_sitemap_count = 0

    for company in companies:
        sys.stdout.write("\r" + str(total_count))
        sys.stdout.flush()

        count += 1
        total_count += 1

        current_sitemap_text += '\
              <url>\
                <loc>https://www.getcompany.info/c/' + company.identifier + '/</loc>\
                <changefreq>monthly</changefreq>\
                <priority>1</priority>\
              </url>'

        if count > 50000:

            current_sitemap_text += final

            with open(os.path.join(settings.BASE_DIR, "/static/sitemaps/companies-" + str(current_sitemap_count) + ".xml")) as myfile:
                myfile.write(current_sitemap_text)

            count = 0
            current_sitemap_text = start
            current_sitemap_count = 0'''

    b = '''
    for i in range(0,20):

        result = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

        skip = i * 45000
        get = skip + 45000
        print("skip " + str(skip))
        print("get " + str(get))

        companies = Companies.objects.all()[skip:get]

        for company in companies:
            result += '<url><loc>https://www.getcompany.info/c/' + company.identifier + '/</loc><changefreq>monthly</changefreq><priority>1</priority></url>'


        result += '</urlset>'

        with open("/root/workspace/Old/11/companies-" + str(i) + ".xml", "w") as myfile:
            myfile.write(result)

        del result'''

    return render(request, 'about.html', {})

def terms(request):

    return render(request, 'terms.html', {})

def sitemapmain(request):

    companies_per_sitemap = 30000

    total_companies = Companies.objects.all().count()

    sitemaps = math.ceil(total_companies/companies_per_sitemap)

    result = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for i in range(0, sitemaps):
        result += '<sitemap><loc>https://www.getcompany.info/companies-' + str(i) + '.xml</loc></sitemap>'

    result += '</sitemapindex>'

    return HttpResponse(result, content_type='application/xml')

def sitemap_companies(request, id):

    companies_per_sitemap = 30000

    skip = int(id) * companies_per_sitemap
    get = skip + companies_per_sitemap

    total_companies = Companies.objects.all()[skip:get]

    result = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for company in total_companies:
        result += '<url><loc>https://www.getcompany.info/' + company.identifier + '/</loc><lastmod>' + str(company.updated_at)[:10] + '</lastmod></url>'

    result += '</urlset>'

    return HttpResponse(result, content_type='application/xml')

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

        company.already_crawled = True

        company.save()