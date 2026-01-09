from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
from TTS.api import TTS
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)
# Allow all origins for now - you can restrict to your Netlify URL in production
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize the TTS model lazily to avoid timeout on startup
tts = None

def get_tts_model():
    global tts
    if tts is None:
        print("Loading TTS model... This may take a few minutes on first load.")
        try:
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True)
            tts.to("cpu")
            print("TTS model loaded successfully!")
        except Exception as e:
            print(f"Error loading TTS model: {str(e)}")
            raise
    return tts

OUTPUT_FOLDER = "outputs"
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/clone', methods=['POST'])
def clone_voice():
    try:
        text = request.form.get('text')
        files = request.files.getlist('voiceFiles')

        if not text or not files:
            return jsonify({"error": "Missing text or voice files"}), 400

        # Get TTS model (lazy loading)
        model = get_tts_model()

        # Clear the outputs folder before generating a new audio
        try:
            for file in os.listdir(OUTPUT_FOLDER):
                file_path = os.path.join(OUTPUT_FOLDER, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        except Exception as e:
            print(f"Error clearing outputs folder: {e}")

        # Save and merge voice samples
        voice_paths = []
        for f in files:
            path = f"{OUTPUT_FOLDER}/user_voice_{uuid.uuid4().hex}.wav"
            f.save(path)
            voice_paths.append(path)

        combined = AudioSegment.empty()
        for path in voice_paths:
            combined += AudioSegment.from_wav(path)

        merged_path = f"{OUTPUT_FOLDER}/merged_reference_{uuid.uuid4().hex}.wav"
        combined.export(merged_path, format="wav")

        # Generate cloned voice
        output_filename = f"output_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        model.tts_to_file(text=text, speaker_wav=merged_path, language="en", file_path=output_path)

        # Clean up individual voice samples
        for path in voice_paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error removing {path}: {e}")
        try:
            os.remove(merged_path)
        except Exception as e:
            print(f"Error removing merged file: {e}")

        # Return a URL to download the file
        base_url = request.host_url.rstrip('/')
        download_url = f"{base_url}/outputs/{output_filename}"
        return jsonify({"download_url": download_url}), 200
    except Exception as e:
        print(f"Error in clone_voice: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Route to serve output audio
@app.route('/outputs/<filename>')
def serve_output_file(filename):
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404

# Route to list all generated audio files
@app.route('/list-outputs', methods=['GET'])
def list_outputs():
    try:
        files = os.listdir(OUTPUT_FOLDER)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint for Render
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running"}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Emotivox 2.0 Backend API",
        "endpoints": {
            "health": "/health",
            "clone": "/clone (POST)",
            "list_outputs": "/list-outputs (GET)",
            "download": "/outputs/<filename> (GET)"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
