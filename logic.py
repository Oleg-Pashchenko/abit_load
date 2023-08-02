from records_loader import Record


def compare_data(records: list[Record], positions_count: dict, mode):
    for record_id in range(len(records)):

        if mode == 'Original' and not (records[record_id].doc_type == 'Оригинал' or records[record_id].epgu):
            continue  # Если не оригинал и не епгу не смотрим

        if mode == 'Copies' and not (records[record_id].doc_type == 'Копия' and not records[record_id].epgu):
            continue  # Тут смотрим только на случай копий

        if records[record_id].max_priority == 0:  # если еще не изменяли
            snils = records[record_id].snils
            matching_records = [rec for rec in records if rec.snils == snils]  # находим все заявки пользователя по снилсу
            sorted_records = sorted(matching_records, key=lambda rec: rec.priority)  # сортируем их по возрастанию приоритета
            priority = 1
            for i, rec in enumerate(sorted_records):
                if positions_count[rec.direction] > 0:  # если места на направлении остались
                    positions_count[rec.direction] -= 1
                    for ii, recc in enumerate(sorted_records):
                        records[records.index(recc)].max_priority = priority
                    break
                else: # Если заполнено
                    priority += 1
    return records


def check_results(records: list[Record]):
    count = 0
    snils = []
    for record in records:
        if record.max_priority != record.max_priority_to_check:
            if record.snils not in snils:
                snils.append(record.snils)
                print('Error:', record)
                count += 1
    print(count)