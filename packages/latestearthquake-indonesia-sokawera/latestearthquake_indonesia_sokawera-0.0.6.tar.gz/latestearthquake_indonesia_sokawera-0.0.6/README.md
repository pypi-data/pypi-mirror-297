# Latest Indonesia Earthquake
This package will get the latest earthquake from BMKG | Meteorological, Climatological, and Geophysical Agency

## HOW IT WORK?
This package will scrape from [BMKG](https://bmkg.go.id/) to get latest quake happened in Indonesia.

This package will use BeautifulSoup4 and Requests, to produce output in the form of JSON that is ready to be used in web of mobile applications

## HOW TO USE
```
from gempaterkini import ekstraksi_data, tampilkan_data

if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)

```
# Author
Pri Anton Subardio, Prita dan Hugo AB