from .download import download_planet_images
from .date_logic import create_dates
from .raster_analysis import mosaic, composite_mosaic_image, clip_raster
from .vector_analysis import make_shapefile
import rasterio

def get_planet_image(spatial_extent, date_list, api_key):
    xmin, ymin, xmax, ymax = spatial_extent
    shapefile = make_shapefile(xmin, ymin, xmax, ymax)
    dates = create_dates(date_list)
    downloaded_image_dir = download_planet_images(shapefile, dates, api_key)
    mosaicked_image_folder = mosaic(downloaded_image_dir, dates)
    base_composite, target_composite = composite_mosaic_image(mosaicked_image_folder, date_list)
    base_clipped = clip_raster(base_composite, shapefile)
    target_clipped = clip_raster(target_composite, shapefile)
    base_image = rasterio.open(base_clipped)
    target_image = rasterio.open(target_clipped)

    return base_image, target_image




spatial_extent = (120.527,16.342,120.652,16.464)
dates = [2018,2019]
api = 'PLAKc718f94526fd4f15970f4ae2cf4c4076'

base,target=get_planet_image(spatial_extent,dates,api)
print(base,'base\n')
print(target,'target')

# python setup.py sdist bdist_wheel
#  twine upload dist/*

