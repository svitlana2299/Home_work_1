from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
import zipfile
import tarfile
import gzip


def handle_media(filename: Path, target_folder: Path) -> None:
    # отримуємо нову назву файлу без розширення
    target_folder.mkdir(exist_ok=True, parents=True)
    new_filename = target_folder / normalize(filename.stem)
    new_filename = new_filename.with_suffix(
        filename.suffix)  # додаємо розширення
    filename.replace(new_filename)


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    # отримуємо нову назву файлу без розширення
    new_filename = target_folder / normalize(filename.stem)
    new_filename = new_filename.with_suffix(
        filename.suffix)  # додаємо розширення
    filename.replace(new_filename)


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_name = normalize(filename.stem)
    folder_for_file = target_folder / folder_name
    folder_for_file.mkdir(exist_ok=True, parents=True)
    # Визначаємо формат архіву та розпаковуємо його
    try:
        if filename.suffix == '.zip':
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(folder_for_file)
        elif filename.suffix == '.gz':
            with gzip.open(filename, 'rb') as gz_file:
                with open(folder_for_file / filename.stem, 'wb') as extracted_file:
                    shutil.copyfileobj(gz_file, extracted_file)
        elif filename.suffix == '.tar':
            with tarfile.open(filename, 'r') as tar_ref:
                tar_ref.extractall(folder_for_file)
        else:
          # Якщо формат архіву невідомий, виводимо повідомлення та повертаємо None
            print(f"Unknown archive format: {filename.suffix}")
            return None

    except (shutil.ReadError, tarfile.TarError, gzip.BadGzipFile) as e:
        # Якщо сталася помилка при розпаковуванні архіву, виводимо повідомлення та повертаємо None
        print(f"Could not extract archive {filename}: {e}")
        return None
    filename.unlink()
    # Переносимо файли з розпакованої теки в цільову теку
    for file in folder_for_file.iterdir():
        if file.is_file():
            new_path = target_folder / 'archives' / \
                folder_name / file.name.replace(file.suffix, '')
            file.replace(new_path)


def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f'Sorry, we can not delete the folder: {folder}')


def main(folder: Path) -> None:
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in parser.DOC_DOCUMENT:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENT:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENT:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'PPTX')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')

    for file in parser.AMR_ARCIVES:
        handle_media(file, folder / 'archives' / 'AMR')
    for file in parser.ZIP_ARCIVES:
        handle_media(file, folder / 'archives' / 'ZIP')
    for file in parser.GZ_ARCIVES:
        handle_media(file, folder / 'archives' / 'GZ')

    for file in parser.MY_OTHER:
        handle_media(file, folder / 'other')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    folder_for_scan = Path(sys.argv[1])
    main(folder_for_scan.resolve())
