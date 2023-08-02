from records_loader import Record, read_excel_files_to_records
import logic
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

records, positions_count = read_excel_files_to_records()
positions_count_view = dict(positions_count)
records.sort(key=lambda x: (x.priority, -x.scores), reverse=False)

records: list[Record] = logic.compare_data(records, positions_count, 'Original')
#records: list[Record] = logic.compare_data(records, positions_count, 'Copies')

for record in records:
    if record.snils == '138-736-426 91':
        print(record)
print('\n\n')

logic.check_results(records)


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    unique_directions = set(record.direction for record in records)
    return render_template('index.html', directions=unique_directions)


@app.route('/table/<string:direction>')
def show_table(direction):
    filtered_records = [record for record in records if record.direction == direction]
    return render_template('table.html', records=filtered_records, positions_count=positions_count_view[direction])


if __name__ == '__main__':
    app.run(port=8000, debug=True)
