import traceback
from pathlib import Path
import csv


class Logger:

    def __init__(self,):
        self.log_directory = Path(__file__).parent

    def log(self,
            user_prompt: str,
            system_prompt: str,
            answer,
            file_name: str
            ):

        try:
            file_path = self.log_directory / file_name

            file_exists = file_path.exists()

            with open(
                    file_path,
                    mode="a",
                    newline="",
                    encoding="utf-8"
            ) as csv_file:

                writer = csv.writer(csv_file)

                if not file_exists:
                    writer.writerow([
                        "system_prompt",
                        "user_prompt",
                        "output"
                    ])

                writer.writerow([
                    system_prompt,
                    user_prompt,
                    answer
                ])

        except Exception as e:
            print("error in logging ")
            print(traceback.format_exc())
