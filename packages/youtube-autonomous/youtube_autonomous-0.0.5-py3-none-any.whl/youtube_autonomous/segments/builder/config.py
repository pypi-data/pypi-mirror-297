MAX_DURATION_PER_IMAGE = 5
"""
The amount of seconds that an image can be used to build a 
video by applying some effect on it.
"""
MIN_DURATION_PER_IMAGE = 2
"""
The minimum amount of seconds that an image must last when 
treating ai_images segment building to ensure that a new
image is needed. If the value is lower than this one, the
previous image will stay longer to fit this short period of
time.
"""
MAX_DURATION_PER_YOUTUBE_SCENE = 5
"""
The maximum number of seconds that we can extract consecutively 
from a YouTube video (related to avoiding copyright issues).
"""