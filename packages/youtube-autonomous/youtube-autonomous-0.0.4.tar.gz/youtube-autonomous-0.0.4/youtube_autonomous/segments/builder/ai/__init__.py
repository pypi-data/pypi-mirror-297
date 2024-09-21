from youtube_autonomous.segments.builder.ai.enums import ImageEngine
from yta_multimedia.image.generation.ai.prodia import generate_image_with_prodia
from yta_multimedia.experimental.image.generation.ai.flux import generate_dev as generate_image_with_flux
from yta_general_utils.temp import create_temp_filename


def create_ai_image(prompt: str, output_filename: str = None, image_engine: ImageEngine = ImageEngine.DEFAULT):
    """
    Creates an AI image with the provided 'prompt' and stores it locally
    as 'output_filename' (if it is not provided it will generate a 
    temporary file) with the also provided 'image_engine'.

    This method returns the 'output_filename' of the generated image.
    """
    if not prompt:
        raise Exception('No "prompt" provided.')
    
    if not output_filename:
        output_filename = create_temp_filename('ai.png')

    if not image_engine:
        image_engine = ImageEngine.DEFAULT

    if image_engine == ImageEngine.PRODIA:
        generate_image_with_prodia(prompt, output_filename)
    elif image_engine == ImageEngine.FLUX:
        generate_image_with_flux(prompt, output_filename)

    return output_filename