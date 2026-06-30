import csv


class CSVReader:

    @staticmethod
    def read_csv(file_path):
        data = []

        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

        return data