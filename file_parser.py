import sys
from pathlib import Path

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_ARCIVES = []
ZIP_ARCIVES = []
GZ_ARCIVES = []
TAR_ARCIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENT,
    'DOCX': DOCX_DOCUMENT,
    'TXT': TXT_DOCUMENT,
    'PDF': PDF_DOCUMENT,
    'XLSX': XLSX_DOCUMENT,
    'PPTX': PPTX_DOCUMENT,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_ARCIVES,
    'ZIP': ZIP_ARCIVES,
    'GZ': GZ_ARCIVES,
    'TAR': TAR_ARCIVES,
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():

        if item.is_dir():

            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
                FOLDERS.append(item)
                scan(item)  # сканування вкладенної папка РЕКУРСІЯ
            continue  # перехід до наступного елемента в папці
        ext = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях файлу
        if not ext:
            MY_OTHER.append(full_name)
        else:
            try:
                cotainer = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                cotainer.append(full_name)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(full_name)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder: {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f"Images jpeg: {JPEG_IMAGES}")
    print(f"Images png: {PNG_IMAGES}")
    print(f"Images jpg: {JPG_IMAGES}")
    print(f"Images svg: {SVG_IMAGES}")
    print(f"Video avi: {AVI_VIDEO}")
    print(f"Video mp4: {MP4_VIDEO}")
    print(f"Video mov: {MOV_VIDEO}")
    print(f"Video mkv: {MKV_VIDEO}")
    print(f"Document doc: {DOC_DOCUMENT}")
    print(f"Document docx: {DOCX_DOCUMENT}")
    print(f"Document txt: {TXT_DOCUMENT}")
    print(f"Document pdf: {PDF_DOCUMENT}")
    print(f"Document xlsx: {XLSX_DOCUMENT}")
    print(f"Document pptx: {PPTX_DOCUMENT}")
    print(f"Audio mp3: {MP3_AUDIO}")
    print(f"Audio ogg: {OGG_AUDIO}")
    print(f"Audio wav: {WAV_AUDIO}")
    print(f"Arcives amr: {AMR_ARCIVES}")
    print(f"Arcives zip: {ZIP_ARCIVES}")
    print(f"Arcives gz: {GZ_ARCIVES}")
    print(f"Arcives tar: {TAR_ARCIVES}")
    print('*' * 25)
    print(f'UNKNOWN: {UNKNOWN}')
