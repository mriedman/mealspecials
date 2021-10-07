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
'Cookie': '_ga=GA1.2.703481378.1600222041; ASP.NET_SessionId_Menu=jtqm40qlia3wuvsvzmws0iu2; __AntiXsrfToken=60480e29a8b344739e0d51989e5afee1; MealType=Lunch; DiningHall=FlorenceMoore',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1'}

now = datetime.datetime.now()
payload = urllib.parse.parse_qs(f'__EVENTTARGET=GetMenu&__EVENTARGUMENT=&__VIEWSTATE=X4yQsTr5grPbEINwO%2BvB3AjGDr8kbRg1lU9Qejlsy9tqgfDVcWIF7F%2BK5n3lte5Hss2OCq41YdtEhZ8H4HeklOCNeCANWmrhDTG71naSuUr%2FolV%2FtUEP7wYdMjRBMmnPtaS2BHYkSSixXa5W0osIE0egxcuEFc3UghvFO8cgK5Bz0xqxqvHGJlJ4h3KQkzyykqat1U%2FpBdJqfaLRUMDBYqdPd%2F7ZeWxjQqN3UiFad%2FF%2Fe0HOkGzbm0c3mRLl9JBtxHHqhaZIvBO9rUMAJkF%2FSUU%2F%2FV3qD2EGo19USazoz6nSpnC9IiL95AyTHb%2FHVxJtJOZT9NvXWtYjD3zBzSjz1Dzi%2FYSe0y2PFo79iwKmHL%2F%2Bf6nlAwZ4eKwfCyUsl%2FcHpN4Vb%2FAJU4eWBmXqhnBe%2FB3NZFIz3L%2FGe4%2F%2BALwD%2FrQy47MSjvdNDecjRsd%2FqOASFCs5K8AqSiBn37MuUWL6lbrLGht54Bs6PWfyYEdrsZPucDW7lUDqO7bnSIogr8fOmBIhg6zq6XBtzqsV87EfJXZ2C1mJ%2BAqEaTwyJ6WOPKSxLUe%2Fc4GC5pXZBY2hJivPritMrkJ7G%2BBpMAe5W11gOuQQeU96x%2BhiK5h%2BfIOVGMjP7GHJ1PA0mfzs%2BkNCbeoRwMvEQ7Isvn74by%2Figxn3aOVEyrtPookOLq%2Bgu2KNQtPeNx8IptVgy4E3uXUkQe%2FkgCNBnf2A%2F7ZdIzJ%2Fj1rzJWbSLSM6OaWqOvimSOlGTJpeK2vPrlOPFoFUmwDfWhB%2FLymInYKuUVuS4YVACS15D4Il9wx39Sv48TilCkrpXlP%2BwR470TTPzKp%2Bgjlrv55S%2BezsdQWQxvEh45jLTFFTzLs3uukbue1o7s%2Bce%2FyThSOFBDlrwYvSpaBepx378pjDDZrycUx56lotTr0BC4lOA6VYG5GyTRzKGGdG0dHj2hng%2BPEAhcCtzaRvMvrTZQckxgJ11ZHGzTWwufpk6VufCC2M5%2Fpu4EOT%2F3pAfUHrxdyIQlSfFKODNFhW6noUt8faaklPwOUiKYTeYNYijUBG9ei02AimQPhG%2FerEEDhFAyrtgA0zzNuAZcJFVX6TJpJx9fHERrAftlqduyu9C0MIJ2IIO%2BcjhqrIgCDwSin40sg2sWyd%2FUWNiAeaNM6mbDFwS317obWkdyCBBOd71mF2iJPeSfYfIlkUmqWh0tCZo4BQUXRQUuNawgatE61ZRNObkLX4YeCIRYky8822LF2Dv0FQ9GYpRLuB7OAh1siMzXyBD0%2Bz%2BihUD1bD7E6P1%2FK25%2FaZQbJoN4nNl3U3o3W5bnik0u8a9TnweDk%2F5Vixpr18DhJ5gCgMc1h8AT95pJP%2B&__VIEWSTATEGENERATOR=5ABBD323&__EVENTVALIDATION=sIxY77Gqu0OoviDcp6cv03p0WxM9PDmqSTqNnhMeMbOw6Ct%2FYudniRtUywFmKEnhIqcN1%2BJO3sRcE14dJEB8x6jKR3mdSVmyhtnymTCO%2B3Ypy4Fb4lx07GEerNYOM78pnCQlVllzWVHUR1S%2FlNwq%2BijjcShG54EtoWxWoh44W%2FvX7C3PkCiSPv8fuCGztzGESlZ8HPp1G%2FP%2FuMTulWcaext4BkeRUzELTw4lcVrvWY%2B4IfMoog129TYz%2FUaxmrgiGEencUqBl%2BRORl4uVRy8%2FeXwIAuUiBDWHSt6Q%2FJeFjZ%2FBozxnYrIopn014RdxtH8pVteDJwZoyDHUNJK%2BsuCIMDpY%2BXBIkCwfu4SiapQC%2FUhkmksYRI6AivNSDX4mYUXVDl09k0Fs0lh%2BKNz%2BcbMnK9euZleKCazCV8%2B89PdtQiRTOtYwTMyJAdWlc%2F4sPoLc%2Ff%2F3CnArSzXhBvuqV7%2B9WVbeGU4oHOOWUIKa5wyIbO5DwYBblIdoNrFFTlbIp4NrTVQqGOkEb1%2F3FGkZ%2F2ajTjwGf%2FmkUppIF%2FuctRy9oX5a8HVe6a2qKaPFL2zSdKIARDBif6JM8IyJCFjqh%2B%2FkTYDag4P7D%2F41QOa0wRSqCmIpfLYSndVdGPvol7J3EsEvuNTCbDghFdUWjSQZp51vSchCoibEsiT6Iib0fvDX1M%3D&ctl00%24MainContent%24lstLocations=FlorenceMoore&ctl00%24MainContent%24lstDay=10%2F7%2F2021&ctl00%24MainContent%24lstMealType=Dinner')


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
