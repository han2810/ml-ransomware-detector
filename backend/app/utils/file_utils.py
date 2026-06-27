from pathlib import Path

from werkzeug.utils import secure_filename


def validate_and_normalize(uploaded_file, allowed_extensions):
    if uploaded_file is None:
        return None, "Thieu multipart field 'file'."
    filename = secure_filename(Path(uploaded_file.filename or "").name)
    if not filename:
        return None, "Chua chon file upload."
    if Path(filename).suffix.lower() not in allowed_extensions:
        return None, "Dinh dang file khong duoc ho tro."
    return filename, None

