import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def save_avatar(file_storage, filename_prefix='avatar'):
    if not file_storage:
        return None
    if not allowed_file(file_storage.filename):
        return None
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    out_name = f"{filename_prefix}_{os.urandom(6).hex()}.{ext}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, out_name)
    file_storage.save(path)
    # повертаємо шлях відносно статичних файлів
    return f"/static/img/{out_name}"
