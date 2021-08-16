import re
import requests
import urllib


def get_domain_listings(url):
    query_url = 'http://web.archive.org/web/timemap/?url=' +\
                urllib.parse.quote(url, safe='') +\
                '&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=\u0021statuscode%3A%5B45%5D..&limit=100000'
    query_headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://web.archive.org/web/*/flatplanetcafe.net/*',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    results = requests.get(query_url, query_headers).json()

    return structure_url_listings(results)


def structure_url_listings(listings):
    headers = listings[0]
    rows = listings[1:]

    structured = {}
    for row in rows:
        entry = structure_url_entry(headers, row)
        structured[clean_url(entry['original'])] = entry

    return structured


def structure_url_entry(headers, row):
    structured = {}

    for i in range(len(headers)):
        structured[headers[i]] = row[i]

    return structured


def clean_url(url):
    pattern = '^(([a-zA-Z]+:)?//)?([^:/]+)(:[0-9]+)?(/.*)?$'
    match = re.match(pattern, url)
    if match:
        domain_name = match.group(3)
        if domain_name[0:4] == 'www.':
            domain_name = domain_name[4:]
        path = match.group(5)
        return domain_name + path
        return match.group()
    else:
        return url


def get_url_listings(url, year):
    query_url = 'http://web.archive.org/__wb/calendarcaptures/2?url=' +\
                urllib.parse.quote(url, safe='') +\
                '&date=' +\
                str(year) +\
                '&groupby=day'
    headers = {

    }
    results = requests.get(query_url, headers)

    return url

# curl 'http://web.archive.org/__wb/calendarcaptures/2?url=http%3A%2F%2Fflatplanetcafe.net%3A80%2Fimages%2Fbtnflatliners.jpg&date=2002&groupby=day' \
#   -H 'Connection: keep-alive' \
#   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36' \
#   -H 'Accept: */*' \
#   -H 'Referer: http://web.archive.org/web/2002*/http://flatplanetcafe.net:80/images/btnflatliners.jpg' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Cookie: wayback.collectionid=web; wayback.archivalhost=https%3A%2F%2Ftheanarchistlibrary.org; wayback.timestamp=20200216155815; wayback.initiatingpage=https%3A%2F%2Fweb.archive.org%2Fweb%2F20200216155815%2Fhttps%3A%2F%2Ftheanarchistlibrary.org%2Flibrary%2Fanonymous-desert; JSESSIONID=810F42CFB556A69B8496C843443CDA0D; csm-hit=tb:s-NBBNN6Q4Q7ZY5SKKD02G|1600198319103&t:1600198319103; PHPSESSID=sbat7m6vf3l39sv5o9t66njtd7; logged-in-sig=1631748150+1600212150+xG7o9vnTNNIvjvYjsFEsS9MP2%2BKIGaqFfcVpeR6qG7E%2FJvllC1O02APg55TX%2BxtKlQCsSHVQDFo4h3cmg5yw%2BrTRxXpNv5KHx7bGRWU%2FSxcAqemAbbdCcJ9jHnG90XuC5slnUq8v9eXD31VVGub7Ew0Mu1MqYq1yYzm69RIwwac%3D; logged-in-user=beka%40gothdyke.mom; __mmapiwsid=b02f2975-cb37-470f-8cc9-d24ecaa5f732:eeb8c20050290cb31242e5ec43d4b84859b54aff; _ga=GA1.2.2128881681.1616089784; __utma=198155069.1121135315.1318874675.1318874675.1318874675.1; __utmc=198155069; __utmz=198155069.1318874675.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); collections=cdl%2Camericana' \
#   --compressed \
#   --insecure


if __name__ == '__main__':
    results = get_domain_listings('http://flatplanetcafe.net')
    for url in results.keys():
        print(url)
