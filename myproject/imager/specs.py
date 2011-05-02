from imagekit.specs import ImageSpec
from imagekit import processors

# define the thumbnail resize processor
class ResizeThumb(processors.Resize):
	width = 100
	height = 75
	crop = True

# define a display size resize processor
class ResizeDisplay(processors.Resize):
	width = 600

# adjustment processor to enhance small images
class EnhanceThumb(processors.Adjustment):
	contrast = 1.2
	sharpness = 1.1

# define thumbnail spec
class Thumbnail(ImageSpec):
	access_as = 'thumbnail_image'
	pre_cache = True
	processors = [ResizeThumb, EnhanceThumb]

# define display spec
class Display(ImageSpec):
	increment_count = True
	processors = [ResizeDisplay]
