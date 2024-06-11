import io, uuid
from PIL import Image

def upload_image(bucket, image: Image.Image) -> str:
    image_name = f"{uuid.uuid4()}.png"    
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)    
    
    blob = bucket.blob(image_name)
    blob.upload_from_file(image_buffer, content_type='image/png')
    
    blob.make_public()
    return blob.public_url
