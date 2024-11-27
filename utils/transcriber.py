import os
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm
import re


class Transcriber:
    def __init__(self, input_dir, output_file, language="ru-RU"):
        self.input_dir = input_dir
        self.output_file = output_file
        self.language = language
        self.recognizer = sr.Recognizer()
        self.supported_formats = ('.wav', '.mp3', '.flac', '.ogg')
        self.temp_folder = r".\temp"

    def transcribe_file(self, file_path):
        """Обрабатывает один файл и возвращает его транскрипцию."""
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio_data, language=self.language)
        except sr.UnknownValueError:
            return "[Не удалось распознать]"
        except Exception as e:
            return f"[Ошибка: {e}]"

    def windows_sort_key(self, line):
        """
        Формирует ключ для сортировки строк в стиле Windows.
        Разбивает строку на числовые и текстовые компоненты.
        """
        # Извлекаем имя файла до пробела
        filename = line.split(" - ", 1)[0]
        return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', filename)]

    def sort_transribe_lines_in_file(self, filepath):
        # Чтение файла
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Сортировка строк
        sorted_lines = sorted(lines, key=self.windows_sort_key)

        # Запись отсортированных строк обратно в файл
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines(sorted_lines)

    def run(self):
        """Транскрибирует все файлы в заданной директории."""
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        all_files = [
            file
            for root, _, files in os.walk(self.input_dir)
            for file in files
        ]

        with open(self.output_file, "w", encoding="utf-8") as output:
            for file_name in tqdm(all_files, desc="Обработка файлов", unit="file"):
                file_path = os.path.join(self.input_dir, file_name)

                if not file_name.lower().endswith(self.supported_formats):
                    continue

                if not file_path.lower().endswith('.wav'):
                    audio = AudioSegment.from_file(file_path)
                    temp_export_path = os.path.join(self.temp_folder, f"{os.path.splitext(file_name)[0]}.wav")
                    audio.export(temp_export_path, format="wav")
                    file_path = temp_export_path
                
                transcription = self.transcribe_file(file_path)
                
                if file_path == temp_export_path:
                    os.remove(temp_export_path)

                # Запись в файл, выравнивание строки
                padded_file_name = file_name.ljust(20)
                output.write(f"{padded_file_name}\t{transcription}\n")

        self.sort_transribe_lines_in_file(self.output_file)
        print(f"Транскрипция завершена. Результаты сохранены в {self.output_file}")
