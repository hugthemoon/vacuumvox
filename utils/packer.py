import os
import tarfile
from pydub import AudioSegment
from tqdm import tqdm
import shutil

class Packer:
    def __init__(self, input_dir, output_file, codec="libmp3lame", frequency=22050, bitrate="256k", channels=1):
        self.input_dir = input_dir
        self.output_file = output_file
        self.codec = codec
        self.frequency = frequency
        self.bitrate = bitrate
        self.channels = channels
        self.temp_output_dir = "./temp"
        self.tar_file = "temp_archive.tar"

    def convert_to_mp3(self, file_path, output_path):
        """Конвертирует один файл в MP3."""
        try:
            audio = AudioSegment.from_file(file_path)
            audio = audio.set_frame_rate(self.frequency).set_channels(self.channels).set_sample_width(2)
            audio.export(output_path, format="mp3", codec=self.codec, bitrate=self.bitrate)
        except Exception as e:
            print(f"Ошибка при обработке {file_path}: {e}")

    def create_tar(self, files_to_pack):
        """Упаковывает в .tar архив."""
        with tarfile.open(self.tar_file, "w") as tar:
            for file_name in tqdm(files_to_pack, desc="Упаковка", unit="file"):
                file_path = os.path.join(self.temp_output_dir, file_name)
                if os.path.isfile(file_path):
                    tar.add(file_path, arcname=file_name)

    def compress_with_gzip(self):
        """Создаем сжатый архив .tgz из .tar."""
        with tarfile.open(self.tar_file, "r") as f_in:  # Открываем временный .tar архив
            with tarfile.open(self.output_file, "w:gz") as f_out:  # Открываем .tgz архив для записи
                # Копируем все содержимое .tar в .tgz
                for member in f_in.getmembers():
                    f_out.addfile(member, f_in.extractfile(member))
        
        # Удаляем временный .tar файл после сжатия
        os.remove(self.tar_file)

    def run(self):
        """Конвертирует файлы в MP3, упаковывает их в tar, а затем сжимает в tgz."""

        if not os.path.exists(self.temp_output_dir):
            os.makedirs(self.temp_output_dir)

        # Список всех файлов для обработки
        all_files = [
            file
            for root, _, files in os.walk(self.input_dir)
            for file in files
        ]

        # Прогресс-бар для конвертации
        for file_name in tqdm(all_files, desc="Конвертация", unit="file"):
            file_path = os.path.join(self.input_dir, file_name)
            output_path = os.path.join(self.temp_output_dir, f"{os.path.splitext(file_name)[0]}.mp3")
            self.convert_to_mp3(file_path, output_path) 

        # Список файлов в временной папке
        temp_files = os.listdir(self.temp_output_dir)

        # Создание tar архива
        self.create_tar(temp_files)

        # Сжатие tar в tgz
        self.compress_with_gzip()

        # Удаляем временную папку
        shutil.rmtree(self.temp_output_dir)

        print(f"Файлы из {self.input_dir} успешно конвертированы и упакованы в {self.output_file}.")
