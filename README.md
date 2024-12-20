# flickr-pubdomain
Some code to download Public Domain imagers from FLICKR that have safety on, descriptions (or more than 1 or 2 word titles), and geocoordinates


https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=cb966d0ee9e1164724681ec61bfe2346&license=7&safe_search=1&content_types=0&extras=description%2C+license%2C+date_upload%2C+date_taken%2C+owner_name%2C+icon_server%2C+original_format%2C+last_update%2C+geo%2C+tags%2C+machine_tags%2C+o_dims%2C+views%2C+media%2C+url_o&format=rest

https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=cb966d0ee9e1164724681ec61bfe2346&license=10&safe_search=1&content_types=0&extras=description%2C+license%2C+date_upload%2C+date_taken%2C+owner_name%2C+icon_server%2C+original_format%2C+last_update%2C+geo%2C+tags%2C+machine_tags%2C+o_dims%2C+views%2C+media%2C+url_o&page=4&format=json&nojsoncallback=1

https://www.flickr.com/services/api/flickr.photos.search.htm

https://www.flickr.com/services/api/flickr.photos.search.htm

https://www.flickr.com/services/api/explore/flickr.photos.licenses.getInfo


```xml
<?xml version="1.0" encoding="utf-8" ?>
<rsp stat="ok">
  <licenses>
    <license id="0" name="All Rights Reserved" url="" />
    <license id="4" name="Attribution License" url="https://creativecommons.org/licenses/by/2.0/" />
    <license id="6" name="Attribution-NoDerivs License" url="https://creativecommons.org/licenses/by-nd/2.0/" />
    <license id="3" name="Attribution-NonCommercial-NoDerivs License" url="https://creativecommons.org/licenses/by-nc-nd/2.0/" />
    <license id="2" name="Attribution-NonCommercial License" url="https://creativecommons.org/licenses/by-nc/2.0/" />
    <license id="1" name="Attribution-NonCommercial-ShareAlike License" url="https://creativecommons.org/licenses/by-nc-sa/2.0/" />
    <license id="5" name="Attribution-ShareAlike License" url="https://creativecommons.org/licenses/by-sa/2.0/" />
    <license id="7" name="No known copyright restrictions" url="https://www.flickr.com/commons/usage/" />
    <license id="8" name="United States Government Work" url="https://www.usa.gov/government-copyright" />
    <license id="9" name="Public Domain Dedication (CC0)" url="https://creativecommons.org/publicdomain/zero/1.0/" />
    <license id="10" name="Public Domain Mark" url="https://creativecommons.org/publicdomain/mark/1.0/" />
  </licenses>
</rsp>

```