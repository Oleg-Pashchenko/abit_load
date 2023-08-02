import dataclasses
import os

import pandas as pd


@dataclasses.dataclass
class Record:
    snils: str  # Снилс
    doc_type: str  # Документ является оригиналом или копией
    scores: int  # Суммарно баллов
    priority: int  # Приоритет человека для данного направления
    max_priority: int  # Приоритет выставленный системой
    max_priority_to_check: int # Приоритет для проверки себя
    epgu: bool  # Статус добавления заявки через систему ЕПГУ
    direction: str  # Направление подготовки


def read_to_exclude():
    df = pd.read_excel('exclude.xlsx')
    ans = []
    for index, row in df.iterrows():
        ans.append(row[2])
    return ans

def read_excel_files_to_records():
    to_exclude = read_to_exclude()

    records = []
    positions_count = {}
    directory = 'test_data'
    for filename in os.listdir(directory):
        if filename.endswith(".xls"):
            file_path = os.path.join(directory, filename)
            df = pd.read_excel(file_path, engine='xlrd')

            for index, row in df.iterrows():
                if index == 3:
                    direction = row[0]
                if index == 10:
                    positions_count[direction] = int(row[0].split('Всего мест: ')[1].split('.')[0])
                if index > 12 and row[2] not in to_exclude:
                    record = Record(
                        snils=row[2],
                        doc_type=row[14],
                        scores=int(row[11]),
                        priority=int(row[4]),
                        max_priority=0,
                        max_priority_to_check=int(row[3]),
                        epgu=False if 'nan' in str(row[15]) else True,
                        direction=direction
                    )
                    records.append(record)

    return records, positions_count

