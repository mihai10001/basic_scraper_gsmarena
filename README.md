# Unobstructive scraper for building a database

### Small scraper for building a mobile device database
### It is used togheter with a web application personal project, for a phone guide website (specifically, for displaying entries in the device database).
### I intend by no means to steal or distribute any data I gathered/ will gather. It is intended for the web application project only, which is kept private (the site won't get published).

**There are 3 major steps in the implementation, each assigned to a function:**

- The first function reads all known brands from a list of brands.
- For every brand, it returns a list of the latest 40 devices (by release date) from that brand (checks only first page of results).
- For each devices, it only scrapes a slight portion of information:
  - Release date
  - Brand
  - Name
  - Processor
  - Rating
  - Price

After scraping the information for one device, it stores it into the database, and sleeps for 0.1 seconds (in case I am sending too many requests to the server).
In the implementation, I have used libraries such as urllib to open URLs, and the well known Python library BeautifulSoup for parsing the HTML.
If you've got this far with the reading, feel free to reuse my code in your project, or message me if you find that there could be important improvements considered.