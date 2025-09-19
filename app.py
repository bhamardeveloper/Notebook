from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    
with app.app_context():
    db.create_all()
    
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([
        {"id": note.id, "title": note.title, "content": note.content} for note in notes
    ])


@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "title": new_note.title, "content": new_note.content}), 201


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.json
    note.title = data['title']
    note.content = data['content']
    db.session.commit()
    return jsonify({"id": note.id, "title": note.title, "content": note.content})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"})



if __name__ == '__main__':
    app.run(debug=True, port=5001)