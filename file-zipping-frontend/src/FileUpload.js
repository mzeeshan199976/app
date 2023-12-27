// FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import { useSpring, animated } from 'react-spring';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const FileUpload = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [progress, setProgress] = useState(0);
  const [showProgress, setShowProgress] = useState(false);

  const animationProps = useSpring({
    opacity: showProgress ? 1 : 0,
    transform: showProgress ? 'translateY(0)' : 'translateY(-100px)',
  });

  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files);
  };

  const handleUpload = async () => {
    setShowProgress(true);

    const formData = new FormData();
    for (const file of selectedFiles) {
      formData.append('files', file);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5050/zip-files/', formData, {
        onUploadProgress: (progressEvent) => {
          const progressPercentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(progressPercentage);
        },
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading files:', error);
    } finally {
      setShowProgress(false);
    }
  };

  return (
    <div className="file-upload-container">
      <h3>Upload Files</h3>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload} className="btn btn-primary">
        Upload
      </button>

      <animated.div style={animationProps} className="progress-container">
        <div className="progress">
          <div
            className="progress-bar progress-bar-striped progress-bar-animated"
            role="progressbar"
            style={{ width: `${progress}%` }}
            aria-valuenow={progress}
            aria-valuemin="0"
            aria-valuemax="100"
          >
            {progress}%
          </div>
        </div>
      </animated.div>
    </div>
  );
};

export default FileUpload;
