import requests
import ssl
import urllib.parse
import datetime
import concurrent.futures
from collections import defaultdict
import pickle
import json

ssl._create_default_https_context = ssl._create_unverified_context

headers = {'Host': 'rdeapps.stanford.edu',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/x-www-form-urlencoded',
'Content-Length': '2436',
'Origin': 'null',
'Connection': 'keep-alive',
'Cookie': '_ga=GA1.2.703481378.1600222041; ASP.NET_SessionId_Menu=cehqbzlzcrt2pbcjkrjt2k3u; __AntiXsrfToken=60480e29a8b344739e0d51989e5afee1',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1'}

payload = urllib.parse.parse_qs('__EVENTTARGET=GetMenu&__EVENTARGUMENT=&__VIEWSTATE=sZkCJiqUWHbwPwasAIvqexhIMdshkpUlA8G0S4A7odkYpEScZc09oPCbajJS2TbfKjkHLvJkrI9MB8G%2Fuei0aYMn2QBmc%2BudV%2BD%2Fwdem8NAASKC5ixWeQMHuLSfQgrtsRzGJ60y23S7uV%2FKFANN72Y86XILqVa%2FG7w3mlzAzBZkJ2ILt3r46FXObE5S%2BB8PfmLMCRCDX%2BoImvCeYBZJFJs9rIIm8FcsBu9RmECWaI54VpspG74Q%2BXGPpOH%2FnouAPgbxEJFR2H2eAETdpN1vwOlzxhR1BO%2BEAU4uz0tZIF5m5FsJF%2BOU8qp7BVrFsOevsWBmfVSVhgMEA3XOQtarJvuEKiIaB3q57bQ38kWT8RHvb680POcQtaiQAS787p0eVNAd9GLZS6JLbWp7gNySWg93oG4qbHSTdz%2BWgjpurMGXsFrKlPqtBULx0FeTHxsVe5tyos0wdX5bqCjJeYUaipbNZJ1kbF%2FGDrwBbwRIaarPj1Ztjo0yoV77zEbAuEXdSQv15RCIk9N60rE%2BrkhQCi2xyToTq%2FEvUncYLgVonSAzW%2BKY1kbaHvaL9L70174kppjFNNRTXTISNH3tG8DkfLQKVACH076jAJ%2FSxSc1tKuzBF%2B5qQkHSoS9O6UrQHG%2Bmnm6XlSVgnDEGQC0kfJdEOH7ncx0mrmgY8z%2BB8dEIGzTKdz3d1%2BcSNC3xrX7WAMPl4g1Gejk3SFG5gsCp9LEN8FihPasG9dFyz8nSz%2F3J5IgG71D%2BiaXReqd2%2FrUqNEDSDhwdnlIK8wWhAE6zomKpQCV%2FMi6XfKHsZ7HOTUSeXYZ4Y2NLdQko1mNE2hZM%2FbjnmOcYK%2Ft0TbYvWMIpO%2B7bpXvdj%2FS4Rhv1S7dUGA8vQCn3PbDjClagOkonDHRQY2bz%2BKfbs6ZAcryuHOydjV3thr7AVY0EgvLDl%2BefJ%2B1s5IV%2F56JOC5e2amXNvUgoaVAahlrtwI0o1v906AujohCWxWTx%2B440GDqjHKmZBGXIoft5yY320YsGjVo37fnv99N0qVD3%2FLaofxD0k3Bwyr02Exqt2Hdf0yzDEieI2U4R2xZuLA2fpc2yOQocuAlFKeJT8%2BsYMV%2F%2Ba3hNmCTuZp6InsGN%2B5ggnjCogiv3VTcysmC9OyM3reRSbIYLmI6Dj0Qs9aJUymJZGxKFKOKRDLrNd0L36IcCVgTUdo2%2FYnN1wxBSgUYxhthobQ7%2FDDNrJAJhk5C5an3MaYO7WfMgFbbCTF22vk4obC4MkKEB0XeE7WfMVYHSjbzuoRwQMF14KlQe5tRubMIzxgIvt%2Fqzo6VJjYOwauiQADasPkExXCRImAv18Sr0igDuryWhOPaB77nF1TEZCYjAWPPuFJLRDkCG7A%3D%3D&__VIEWSTATEGENERATOR=5ABBD323&__EVENTVALIDATION=hBPn1Tqa%2BCSuDDVsxuLcxKRgHgrkDOLd2OBCYrCB%2FDGHQ5NJHjL71aHxKsV%2B98JCW54A8bJqwDUaHaaizjP6oH3OVc%2BrF8w%2FA00XqTfDxCw0x5jrhHqOwRbXCMkpuT1GZwF%2FD3r%2FlHqo0fSFbBRWwv5G5lYEyelOL2QzROXkcKSixPPDrhUHDitPsQCWsACLUYV3wOTRGPMKJKw9HHgAq1NRRcS7zaEpzovExxJ3us7tPZviz2Gl%2FBufprkiNn9sMFCGe0g5QtetC1AH%2Fa50cMBNp6MrQTGLxSctmM70Peb5MWanC0ZDtEWWPt4m4J20GuV2w2UEGZA%2Fs2DgecCm1akWurgyGFwhRWfS3joUGBUX7bRI5T9CIvWdvOLlBbXjvoxs9wtNZT2arNt3o7AlVBSFVpZDq46l183Ay6oJ%2BCQ1XRURlAvfnJWulZxSn889stYfBSRpyh4Y31zGK47%2FQzdg54%2FZMaJCCRbyKONQDmEf6LUAAihdu%2F9jfJim2Q2PHIrAld4%2BeFKQHH2ZcA%2BtbgbXHCTpfypUfhckw7%2BVgTuWRQFx6bN6qu1QD%2B1TgToa8GUlxmwRvF14DCqxj%2BH0NVI4NbVNtfcQqXdLoEMlAHDZS8T5FdiKDDVXhldG0oKE3CFWS%2BHHh5jcTYpVawTg3YqRhSIwYC%2FwB4AzmgyHB60LUvizAPL795suhoSegEA0&ctl00%24MainContent%24lstLocations=FlorenceMoore&ctl00%24MainContent%24lstDay=9%2F21%2F2021&ctl00%24MainContent%24lstMealType=Lunch')


def req_meal(loc, day, meal):
    print(loc, day, meal)
    '''print(payload["ctl00$MainContent$lstLocations"])
    print(payload['ctl00$MainContent$lstDay'])
    print(payload['ctl00$MainContent$lstMealType'])'''
    payload["ctl00$MainContent$lstLocations"] = [loc]
    payload['ctl00$MainContent$lstDay'] = [day]
    payload['ctl00$MainContent$lstMealType'] = [meal]

    return requests.post('https://rdeapps.stanford.edu/dininghallmenu/', headers=headers, data=urllib.parse.urlencode(payload, doseq=True))


date = f'{datetime.datetime.now().month}/{datetime.datetime.now().day}/{datetime.datetime.now().year}'
options = [[i.split('value="')[1].split('">')[0] for i in j.split('<option')[1:]] for j in
           req_meal('', date, '').text.split('<select')[1:]]

combos = [(l, d, m) for d in options[1] if d != '' for m in options[2] if m != '' for l in options[0] if l != '']
# print(combos)

'''for day in options[1]:
    for meal in options[2]:
        if meal == '':
            continue
        for loc in options[0]:
            if loc == '':
                continue
            print(day, meal, loc)
            print([i.split('</span>')[0] for i in req_meal(loc, day, meal).text.split('clsLabel_Name">')[1:]])
        exit(0)'''

data = defaultdict(lambda: defaultdict(list))
'''for combo in combos[20:25]:
    meal = [i.split('</span>')[0] for i in req_meal(*combo).text.split('clsLabel_Name">')[1:]]
    data[(combo[1], combo[2])][tuple(meal)].append(combo[0])'''

print(combos)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Start the load operations and mark each future with its URL
    future_to_day = {executor.submit(req_meal, *c): c for c in combos}
    for future in concurrent.futures.as_completed(future_to_day):
        combo = future_to_day[future]
        try:
            data1 = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (combo, exc))
        else:
            meal = [i.split('</span>')[0] for i in data1.text.split('clsLabel_Name">')[1:]]
            data[(combo[1], combo[2])][tuple(meal)].append(combo[0])

print()
all_specials = {}
for time in data:
    common = sorted(list(data[time].keys()), key=lambda x: len(data[time][x]))[-1]
    for x in data[time]:
        specials = []
        # print(x)
        # print(data[time][x])
        for food in x:
            if food not in common:
                specials.append(food)
        if len(specials) > 0:
            print(time)
            print(data[time][x])
            print(specials)
            print()
            for i in data[time][x]:
                all_specials[(i, *time)] = specials

all_specials_list = sorted([[k, all_specials[k]] for k in all_specials], key=lambda x: combos.index(x[0]))
with open('specials.json', 'w') as f:
    json.dump(all_specials_list, f)
