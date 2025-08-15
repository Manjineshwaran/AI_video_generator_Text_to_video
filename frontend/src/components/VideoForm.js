import React, { useState } from 'react';
import { toast } from 'react-toastify';
import api from '../services/api';
import Loader from './Loader';

const VideoForm = ({ onVideoGenerated }) => {
  const [formData, setFormData] = useState({
    prompt: '',
    duration: 3,
    fps: 12
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' || name === 'fps' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await api.generateVideo(formData);
      toast.success('Video generated successfully!');
      onVideoGenerated(response.video_path);
    } catch (error) {
      toast.error('Failed to generate video. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="video-form">
      <div className="form-group">
        <label htmlFor="prompt">Video Prompt</label>
        <textarea
          id="prompt"
          name="prompt"
          value={formData.prompt}
          onChange={handleChange}
          required
          placeholder="Describe the video you want to generate..."
        />
      </div>
      
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="duration">Duration (seconds)</label>
          <input
            type="number"
            id="duration"
            name="duration"
            min="1"
            max="60"
            value={formData.duration}
            onChange={handleChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="fps">Frames per second</label>
          <input
            type="number"
            id="fps"
            name="fps"
            min="1"
            max="60"
            value={formData.fps}
            onChange={handleChange}
          />
        </div>
      </div>
      
      <button type="submit" disabled={isLoading} className="generate-btn">
        {isLoading ? <Loader size="small" /> : 'Generate Video'}
      </button>
    </form>
  );
};

export default VideoForm;