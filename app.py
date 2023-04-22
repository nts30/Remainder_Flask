from datetime import datetime
from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = f'{uuid4()}'

reminders = []

@app.route('/delete/<int:index>', methods=['POST'])
def remove_reminder(index):
    reminders.pop(index)
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        reminder_text = request.form['reminder']
        reminder_date = request.form['date']
        reminder_time = request.form['time']
        date_str = f'{reminder_date} {reminder_time}'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        reminders.append(
            {
                'text': reminder_text,
                'time': date_obj
            }

        )
        return redirect(url_for('home'))
    now = datetime.now()
    upcoming_reminders = []
    for index, reminder in enumerate(reminders):
        if reminder['time'] > now:
            reminder['index'] = index
            upcoming_reminders.append(reminder)

    return render_template('home.html', upcoming_reminders=upcoming_reminders)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
