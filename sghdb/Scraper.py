import requests,csv,exceptions
import xml.etree.ElementTree as ET

blcode = []
postalcodes = []
codes = {}
data = []
try:
    for i in range(300,500):
        u = 'https://services2.hdb.gov.sg/web/ej03/svy21kml/flats/flats-kml-%s.kml'%i
        r_kml = requests.get(u).text
        root_kml = ET.fromstring(r_kml)
        for p in root_kml:
            BL = p[0].text
            ZIP = p[2].text
            blcode.append(BL)
            postalcodes.append(ZIP)
            codes.update({BL:ZIP})
            address = 'https://services2.hdb.gov.sg/webapp/BC16AWPropInfoXML/BC16SRetrievePropInfoXML?sysId=FI10&bldngGL=%s'%BL
            r_address = requests.get(address).text
            root_address = ET.fromstring(r_address)
            if root_address[4].text == ZIP:
                lease = 'https://services2.hdb.gov.sg/webapp/BB14ALeaseInfo/BB14SGenerateLeaseInfoXML?postalCode=%s'%ZIP
                r_lease = requests.get(lease).text
                root_lease = ET.fromstring(r_lease)
                if len(root_lease)>3:
                #if root_lease[3] is not None:
                    temp = [root_address[2].text,root_address[3].text,root_address[4].text,root_lease[3].text]
                    temp = [e.strip() for e in temp]
                    data.append(temp)
                    print data

except:
    pass
finally:
    with open(r"C:\Users\Winrock\Desktop\sghdb\Scraper.csv", mode='wb') as filee:
        writerr = csv.writer(filee)
        writerr.writerows(data)
    
