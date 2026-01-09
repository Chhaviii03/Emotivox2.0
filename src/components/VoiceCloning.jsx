import { useState, useEffect } from "react";
import { FaUpload, FaMicrophone, FaPause, FaPlay, FaDownload } from "react-icons/fa";
import Header from "./Header";

const VoiceCloning = () => {
  // Get API URL from environment variable or use localhost as fallback
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
  
  const [text, setText] = useState("");
  const [audioFiles, setAudioFiles] = useState([]);
  const [audioFile, setAudioFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "audio/wav") {
      setAudioFile(file);
    } else {
      alert("Please upload a valid WAV file.");
    }
  };

  const handleGenerateSpeech = async () => {
    if (!text.trim()) {
      alert("Please enter text for voice cloning.");
      return;
    }
    if (!audioFile) {
      alert("Please upload a reference audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("text", text);
    formData.append("voiceFiles", audioFile);

    try {
      const response = await fetch(`${API_URL}/clone`, {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        const url = data.download_url;
        setAudioUrl(url);
        loadAudioList();
      } else {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }));
        alert(`Error: ${errorData.error || "Something went wrong!"}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert(`Failed to connect to backend. Please check if the server is running at ${API_URL}`);
    }
  };

  const loadAudioList = async () => {
    try {
      const response = await fetch(`${API_URL}/list-outputs`);
      if (response.ok) {
        const files = await response.json();
        setAudioFiles(files);
      } else {
        console.error("Failed to load audio files");
      }
    } catch (error) {
      console.error("Error loading audio list:", error);
    }
  };

  useEffect(() => {
    loadAudioList();
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 to-gray-700 p-6">
      <Header />
      <div className="w-full max-w-xl bg-gray-800 p-6 rounded-2xl shadow-xl">
        <h2 className="text-4xl font-bold text-center text-white mb-6">Voice Cloning</h2>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text here..."
          className="w-full h-32 p-4 text-lg text-white bg-gray-700 border border-gray-600 rounded-lg focus:outline-none mb-4"
        />
        <div className="flex items-center gap-4 mb-4">
          <input type="file" accept=".wav" onChange={handleFileUpload} className="hidden" id="file-upload" />
          <label htmlFor="file-upload" className="px-4 py-2 bg-purple-600 text-white rounded-full cursor-pointer hover:bg-purple-700">
            <FaUpload className="inline mr-2" />Upload WAV File
          </label>
          <button
            onClick={handleGenerateSpeech}
            className="px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700"
          >
            Clone Voice
          </button>
        </div>

        {audioUrl && (
          <div className="mt-4">
            <audio controls src={audioUrl} className="w-full"></audio>
          </div>
        )}

  
      </div>
    </div>
  );
};

export default VoiceCloning;
