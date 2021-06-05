from urllib.request import urlopen

url = "http://www.koeri.boun.edu.tr/scripts/lst9.asp"


def getAllData(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("latin-1")

    return html


def parseAllData(data):
    start_index = data.find("<pre>") + len("<pre>")
    end_index = data.find("</pre>")
    data = (data[start_index:end_index])[585:]

    return data.splitlines()


def parseData(data):
    location_end_index = 0
    type_start_index = 0

    # default date YYYY-MM-DD
    date = data[0:10]
    # DD-MM-YYYY
    date = date[8:10] + "." + date[5:8] + date[0:4]

    time = data[11:19]
    latitude = data[21:28]
    longitude = data[31:38]
    depth = data[46:49]
    md = data[55:59]
    ml = data[60:65]
    mv = data[65:71]

    for i in range(71, len(data)):
        if (data[i] == " ") and (data[i + 1] == " "):
            location_end_index = i
            break

    location = data[71:location_end_index]

    for i in range(location_end_index, len(data)):
        if i != " ":
            type_start_index = i
            break

    type = data[type_start_index:].split()[0].replace("Ý", "I")

    return [date, time, latitude, longitude, depth, md, ml, mv, location, type]


def googleMapsLink(latitude, longitude):
    #googpe maps dev. sayfasında ayrıca farklı ayarlar var. Daha sonra ekleme yapmak için fonk. halinde yazdım.
    url = "https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," + str(longitude)

    return url

def getInfo(data):
    earthquake = parseData(data)
    googleMapUrl = googleMapsLink(earthquake[2],earthquake[3])

    info = ("DEPREM BILGISI\n" +
            "Tarih: " + earthquake[0] + " Saat: " + earthquake[1] + "\n" +
            "Yer: " + earthquake[8] + " @ " + googleMapUrl + "\n" +
            "Buyukluk: " + earthquake[6] + "Derinlik: "+ earthquake[4] + " km" + "\n")

    return info

#ornek uygulama

all_data = getAllData(url)
data = parseAllData(all_data)
print(getInfo(data[1]))
