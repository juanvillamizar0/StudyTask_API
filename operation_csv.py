import csv
import os


def read_csv(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(file_path: str, data: list, fieldnames: list) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def create_record(file_path: str, record: dict, fieldnames: list) -> dict:
    data = read_csv(file_path)
    data.append(record)
    write_csv(file_path, data, fieldnames)
    return record


def find_records(file_path: str) -> list:
    return read_csv(file_path)


def find_record_by_id(file_path: str, record_id: int) -> dict | None:
    data = read_csv(file_path)

    for record in data:
        if int(record["id"]) == record_id:
            return record

    return None


def update_record(file_path: str, record_id: int, new_record: dict, fieldnames: list) -> dict | None:
    data = read_csv(file_path)

    for index, record in enumerate(data):
        if int(record["id"]) == record_id:
            data[index] = new_record
            write_csv(file_path, data, fieldnames)
            return new_record

    return None


def kill_record(file_path: str, record_id: int, fieldnames: list) -> bool:
    data = read_csv(file_path)
    new_data = [record for record in data if int(record["id"]) != record_id]

    if len(new_data) == len(data):
        return False

    write_csv(file_path, new_data, fieldnames)
    return True