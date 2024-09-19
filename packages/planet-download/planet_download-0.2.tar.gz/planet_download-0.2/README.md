# Planet Image Download Using Planet API
This Github repository helps to dowload the planet scope image using the api provided by planet scope.

### How to use this package
Clone this repository and use it like example below:
We need three things to use the package:
1. Spatial extent or bounding box
2. Dates (dates is in list, we provide base year and target year )
3. Planet Api Key

```python
from planet_image_acquisition.planet_image_acquisition import get_planet_image
spatial_extent = (120.527,16.342,120.652,16.464) # xmin,ymin,xmax,ymax
dates = [2018,2019] # Should be provided in list format
api = '' # Provide the planet api key for your account

base,target=get_planet_image(spatial_extent,dates,api)
```

### Temporal Resolution for Planet Scope Image
We can download planet scope image from the year 2018. For the year 2018 and 2019, we can only download 6 months composite.
For 2020 we can download planet image of 6 monthe composite (2019-12_2020-05), 2 months composite (2020-06_2020-08),and all
other from this point is a one month composite

Years and Image composite for the respective year is given as below. One should provide dates like below inorder to download
planet image. I this package we only provide the year other logic is handled in date_logic python file.


| **Year**   | **Image Composite**      |
| --- | --- |
| 2018   | 2017-12_2018-05, 2018-06_2018-11 |
| 2019   | 2018-12_2019-05, 2019-06_2019-11 |
| 2020   | 2019-12_2020-05, 2020-06_2020-08, 2020-09, 2020-10, 2020-11, 2020-12 |
| 2021   | 2021-01, 2021-02, 2021-03, .... , 2021-12 |
| 2022   | 2022-01, 2022-02, 2022-03, .... , 2022-12 |
| 2023   | 2023-01, 2023-02, 2023-03, .... , 2023-12 |
| 2024   | 2024-01, 2024-02, 2024-03, .... , 2024-12 |


