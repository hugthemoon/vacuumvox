import argparse
from utils.transcriber import Transcriber
from utils.packer import Packer
import os

def add_ffmpeg_to_path():
    # Путь к директории с ffmpeg
    ffmpeg_dir = r"%localAppData%\ffmpegio\ffmpeg-downloader\ffmpeg\bin"

    # Проверяем, есть ли уже ffmpeg в PATH
    if ffmpeg_dir not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

def main():
    parser = argparse.ArgumentParser(description="Утилита для сборки озвучки для робота пылесоса. Позволяет сделать транскрипцию аудио файлов, конвертировать в нужный формат и упаковать в tar.gz архив.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда transcribe
    transcribe_parser = subparsers.add_parser("transcribe", help="Транскрибировать аудиофайлы.")
    transcribe_parser.add_argument("--input", required=True, help="Путь к папке с аудиофайлами.")
    transcribe_parser.add_argument("--out", required=True, help="Путь к выходному текстовому файлу.")
    transcribe_parser.add_argument("--lang", default="ru-RU", help="Язык распознавания (по умолчанию: 'ru-RU').")

    # Подкоманда pack
    pack_parser = subparsers.add_parser("pack", help="Конвертировать и упаковать файлы.")
    pack_parser.add_argument("--input", required=True, help="Путь к папке с исходными файлами.")
    pack_parser.add_argument("--out", required=True, help="Путь к выходному файлу архива (.tgz).")
    pack_parser.add_argument("--codec", default="libmp3lame", help="Кодек (по умолчанию mp3: 'libmp3lame').")
    pack_parser.add_argument("--frequency", type=int, default=22050, help="Частота дискретизации (по умолчанию: 22050).")
    pack_parser.add_argument("--bitrate", default="256k", help="Битрейт (по умолчанию: '256k').")
    pack_parser.add_argument("--channels", type=int, default=1, help="Количество каналов (по умолчанию: 1).")

    args = parser.parse_args()

    if args.command == "transcribe":
        transcriber = Transcriber(args.input, args.out, args.lang)
        transcriber.run()
    elif args.command == "pack":
        packer = Packer(args.input, args.out, args.codec, args.frequency, args.bitrate, args.channels)
        packer.run()

if __name__ == "__main__":
    try:
        add_ffmpeg_to_path()
        main()
    except KeyboardInterrupt:
        print("Прервано пользователем.")
