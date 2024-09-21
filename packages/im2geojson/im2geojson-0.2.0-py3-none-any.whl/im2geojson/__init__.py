"""

Parse GeoJSON from image metadata.

<br>


Quick Start
-----------


Import im2geojson and initialise by passing the directory of images:


```python
>>> from im2geojson import ImageToGeoJSON

# For example: if your current directory is named `parent` and this contains a folder of images: `my_images`,
# Initialise with `input_directory`:
>>> input_directory = './my_images'
>>> im2geojson = ImageToGeoJSON(input_directory=input_directory)

# Start image processing:
>>> im2geojson.start()
```
```s
Running...
Finished in 0.31 seconds
```
<br>


Summary
-------

```python
>>> im2geojson.summary
```
```s
'1 out of 6 images processed successfully'
```
<br>


Output
------

```json
// my_images.geojson
{
    "type": "FeatureCollection", 
    "title": "my_images", 
    "features": 
    [
        {
            "type": "Feature", 
            "geometry": 
            {
                "type": "Point", 
                "coordinates": [115.095269, -8.631053]
            }, 
            "properties": 
            {
                "datetime": "2023-05-05 06:19:24", 
                "filename": "EXIF.jpg"
            }
        }
    ], 
    "properties": 
    {
        "parent": "parent"
    }
}
```
<br>


Errors
------

```python
>>> im2geojson.error_dictionary
```
```s
{'my_images/MISSING_EXIF.jpg': 'AttributeError: image does not have attribute gps_latitude',
 'my_images/MISSING_DATETIME.jpg': 'AttributeError: image does not have attribute datetime_original',
 'my_images/CORRUPTED_DATETIME.jpg': "ValueError: time data 'corrupted' does not match format '%Y:%m:%d %H:%M:%S'",
 'my_images/CORRUPTED_EXIF.jpg': 'ValueError: Invalid GPS Reference X, Expecting N, S, E or W',
 'my_images/NO_EXIF.jpg': "'No metadata.'"}
```
<br>
<br>

   
***

<br>

"""

import logging

logging.getLogger('im2geojson').addHandler(logging.NullHandler())


from im2geojson.im2geojson import ImageToGeoJSON

__all__ = ['ImageToGeoJSON']

