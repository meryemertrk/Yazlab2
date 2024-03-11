from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup as bs
from .models import Makale  # Makale modelini içe aktarın

def home(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        return redirect('search', search_query=search_query)
    return render(request, 'home.html')

def search(request, search_query=None):
    if not search_query:
        search_query = request.POST.get('search', '')

    # Birinci arama sorgusu
    url = f'https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q={search_query}'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result_lists = soup.find_all('div', {'class': 'gs_ri'})
    find_result = []
    for r in result_lists:
        title = r.find('h3', class_='gs_rt').text.strip()
        authors = r.find('div', class_='gs_a').text.strip()
        descriptions = r.find('div', class_='gs_rs').text.strip()
        pdf_link = r.find('a').get('href') if r.find('a') else None

        # MongoDB'ye kaydetme
        makalebilgi = Makale(baslik=title, yazarlar=authors, aciklamalar=descriptions, pdf_linki=pdf_link)
        makalebilgi.save(using='makalebilgi')  # 'makalebilgi' veritabanına kaydetme

        find_result.append((title, authors, descriptions, pdf_link))

    # İkinci arama sorgusu
    search_query2 = request.POST.get('search2', '')
    url2 = f'https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q={search_query2}'
    res2 = requests.get(url2)
    soup2 = bs(res2.text, 'html.parser')
    result_lists2 = soup2.find_all('div', {'class': 'gs_ri'})
    find_result2 = []
    for r in result_lists2:
        title = r.find('h3', class_='gs_rt').text.strip()
        authors = r.find('div', class_='gs_a').text.strip()
        descriptions = r.find('div', class_='gs_rs').text.strip()
        pdf_link = r.find('a').get('href') if r.find('a') else None

        # MongoDB'ye kaydetme
        makalebilgi = Makale(baslik=title, yazarlar=authors, aciklamalar=descriptions, pdf_linki=pdf_link)
        makalebilgi.save(using='makalebilgi')  # 'makalebilgi' veritabanına kaydetme

        find_result2.append((title, authors, descriptions, pdf_link))

    context = {'find_result': find_result, 'find_result2': find_result2}
    return render(request, 'search.html', context)



