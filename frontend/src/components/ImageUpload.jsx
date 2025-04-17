import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import '../styles/ImageUpload.css';

const ImageUpload = ({ onImageUpload }) => {
  const [previewUrl, setPreviewUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check if file is an image
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    // Create preview URL
    const reader = new FileReader();
    reader.onload = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);

    // Pass file to parent component
    onImageUpload(file);
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleCancelUpload = () => {
    setPreviewUrl(null);
    fileInputRef.current.value = '';
    onImageUpload(null);
  };

  return (
    <div className="image-upload">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        ref={fileInputRef}
        className="file-input"
      />
      
      {!previewUrl ? (
        <button 
          type="button" 
          onClick={handleButtonClick}
          className="upload-button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          Upload Image
        </button>
      ) : (
        <div className="preview-container">
          <img src={previewUrl} alt="Preview" className="image-preview" />
          <button 
            type="button" 
            onClick={handleCancelUpload}
            className="cancel-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

ImageUpload.propTypes = {
  onImageUpload: PropTypes.func.isRequired
};

export default ImageUpload;
