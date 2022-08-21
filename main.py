from pathlib import Path
import asyncio
from aiopath import AsyncPath
import shutil
import sys
import file_parser as parser
from normalize import normalize


async def handle_media(filename: Path, target_folder: Path):
    filename = AsyncPath(filename)
    target_folder = AsyncPath(target_folder)
    await target_folder.mkdir(exist_ok=True, parents=True)
    await filename.replace(target_folder / normalize(filename.name))


async def handle_other(filename: Path, target_folder: Path):
    filename = AsyncPath(filename)
    target_folder = AsyncPath(target_folder)
    await target_folder.mkdir(exist_ok=True, parents=True)
    await filename.replace(target_folder / normalize(filename.name))


async def handle_archive(filename: Path, target_folder: Path):
    filename = AsyncPath(filename)
    target_folder = AsyncPath(target_folder)
    await target_folder.mkdir(exist_ok=True, parents=True)
    await filename.replace(target_folder / (normalize(filename.name[:-len(filename.suffix)]) + filename.suffix))

    try:
        shutil.unpack_archive(str(filename.resolve()), str(filename.resolve()))
    except shutil.ReadError:
        print(f'{filename} не є архівом!')
        filename.rmdir()
        return None
    await filename.unlink()


async def handle_folder(folder: Path):
    folder = AsyncPath(folder)
    try:
        await folder.rmdir()
    except OSError:
        print(f'Не вдалося видалити папку {folder}')


async def main(folder: Path):
    await parser.scan(folder)

    for file in parser.JPEG_IMAGES:
        await handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        await handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        await handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        await handle_media(file, folder / 'images' / 'SVG')
    for file in parser.MP3_AUDIO:
        await handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        await handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        await handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        await handle_media(file, folder / 'audio' / 'AMR')
    for file in parser.AVI_VIDEO:
        await handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        await handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        await handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        await handle_media(file, folder / 'video' / 'MKV')
    for file in parser.DOC_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        await handle_media(file, folder / 'documents' / 'PPTX')
    for file in parser.OTHER_FILES:
        await handle_other(file, folder / 'other_files')
    for file in parser.ARCHIVES:
        await handle_archive(file, folder / 'archives')

    for folder in parser.FOLDERS[::-1]:
        await handle_folder(folder)


if __name__ == '__main__':
    if sys.argv[1]:
        folder = Path(sys.argv[1])
        if folder.is_dir():
            asyncio.run(main(folder))
        else:
            print(f'{folder} не є папкою!')
