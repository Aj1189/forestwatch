import boto3
import os
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import io

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
        region_name=current_app.config['S3_REGION']
    )

def add_watermark(image_file):
    # Load image from file storage
    image_file.seek(0)
    img = Image.open(image_file).convert("RGBA")
    watermark_text = "ForestWatch"
    
    # Make transparent overlay with watermark
    txt_overlay = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_overlay)

    font_size = max(16, img.size[0] // 20)
    font_path = os.path.join(current_app.root_path, "static", "fonts", "arial.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.size[0] - text_width) // 2
    y = (img.size[1] - text_height) // 2
    draw.text((x, y), watermark_text, font=font, fill=(255,255,255,128))


    watermarked = Image.alpha_composite(img, txt_overlay).convert("RGB")

    # Save to memory buffer
    output = io.BytesIO()
    watermarked.save(output, format="JPEG")
    output.seek(0)
    return output

def upload_to_s3(file, key):
    s3 = get_s3_client()
    bucket = current_app.config['S3_BUCKET']

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    key = f"complaints/{key}.{ext}"

    # Apply watermark
    watermarked_file = add_watermark(file)

    s3.upload_fileobj(
        watermarked_file, bucket, key,
        ExtraArgs={'ContentType': 'image/jpeg', 'ACL': 'public-read'}
    )
    return f"https://{bucket}.s3.amazonaws.com/{key}"

def delete_from_s3(file_url):
    s3 = get_s3_client()
    bucket = current_app.config['S3_BUCKET']
    key = file_url.split(f"https://{bucket}.s3.amazonaws.com/")[-1]
    s3.delete_object(Bucket=bucket, Key=key)

def update_s3_file(old_file_url, new_file):
    delete_from_s3(old_file_url)
    return upload_to_s3(new_file)
