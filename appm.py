from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import uuid

app = Flask(__name__)

# Configuración de la carpeta donde se guardarán los archivos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renderiza la página principal."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Recibe los archivos desde el frontend y los guarda localmente."""
    if 'files' not in request.files:
        return jsonify({"error": "No se enviaron archivos."}), 400

    uploaded_files = request.files.getlist('files')
    file_paths = []
    for file in uploaded_files:
        if not allowed_file(file.filename):
            return jsonify({"error": f"El archivo {file.filename} no es permitido."}), 400

        # Genera un nombre único para evitar conflictos
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_paths.append(filename)

    return jsonify({"message": "¡Archivos subidos correctamente!", "files": file_paths}), 200

@app.route('/files', methods=['GET'])
def list_files():
    """Lista los archivos guardados en el servidor."""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Descarga un archivo del servidor."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
