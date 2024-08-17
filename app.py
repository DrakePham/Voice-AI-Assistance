from flask import Flask, render_template, request, jsonify
from voice_command import respond_to_command

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    command_text = request.form.get('command')
    response = respond_to_command(command_text)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
