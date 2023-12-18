import json
import csv
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

res = []
for i in range(len(data[0]["days"])):
    date = data[0]["days"][i]['datetime']
    data_j = data[0]["days"][i]['hours']
    for row in data_j:
        row['name'] = 'Hà Nội, Giải Phóng'
        if 'datetime' in row:
            row['datetime'] = str(date) + 'T' + str(row['datetime'])
        if 'source' in row:
            del row['source']
        if 'stations' in row:
            del row['stations']
        if 'datetimeEpoch' in row:
            del row['datetimeEpoch']
        if 'pressure' in row:
            row['sealevelpressure'] = row.pop('pressure')
        if 'preciptype' in row and row['preciptype'] == ['rain']:
            row['preciptype'] = 'rain'
        res.append(row)

csv_file_path = 'dataCurrent.csv'
with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    # Tạo đối tượng writer CSV
    fieldnames = res[0].keys() if res else []
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if res:
        writer.writeheader()

        # Ghi từng dòng vào file CSV
        writer.writerows(res)
