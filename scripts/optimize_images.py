import os
from PIL import Image

MAX_DIM = 1920
QUALITY = 82

def process_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        return

    orig_size = os.path.getsize(file_path)
    
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            
            # Downscale if excessively large
            if width > MAX_DIM or height > MAX_DIM:
                if width > height:
                    new_w = MAX_DIM
                    new_h = int(height * (MAX_DIM / width))
                else:
                    new_h = MAX_DIM
                    new_w = int(width * (MAX_DIM / height))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # WebP path
            base_path = os.path.splitext(file_path)[0]
            webp_path = base_path + '.webp'
            
            # Save WebP
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img.save(webp_path, 'WEBP', quality=QUALITY, optimize=True)
            else:
                rgb_img = img.convert('RGB')
                rgb_img.save(webp_path, 'WEBP', quality=QUALITY, optimize=True)

            # Re-save original format compressed
            if ext in ['.jpg', '.jpeg']:
                rgb_img = img.convert('RGB') if img.mode != 'RGB' else img
                rgb_img.save(file_path, 'JPEG', quality=QUALITY, optimize=True)
            elif ext == '.png':
                if img.mode == 'P':
                    img = img.convert('RGBA')
                img.save(file_path, 'PNG', optimize=True)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return

    new_orig_size = os.path.getsize(file_path)
    webp_size = os.path.getsize(webp_path)
    print(f"Processed: {os.path.basename(file_path)}")
    print(f"  Original: {orig_size / 1024 / 1024:.2f} MB -> Compressed: {new_orig_size / 1024:.1f} KB | WebP: {webp_size / 1024:.1f} KB")

def main():
    root_dir = r"c:\wamp64\www\Portfolio"
    uploads_dir = os.path.join(root_dir, "Uploads")
    
    print("--- Processing Root Images ---")
    for f in os.listdir(root_dir):
        fp = os.path.join(root_dir, f)
        if os.path.isfile(fp):
            process_image(fp)

    print("\n--- Processing Uploads Directory Images ---")
    for f in os.listdir(uploads_dir):
        fp = os.path.join(uploads_dir, f)
        if os.path.isfile(fp):
            process_image(fp)

if __name__ == "__main__":
    main()
