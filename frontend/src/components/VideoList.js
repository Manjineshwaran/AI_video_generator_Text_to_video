import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

const VideoList = () => {
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await api.listVideos();
        setVideos(response.videos);
      } catch (error) {
        toast.error('Failed to load videos');
        console.error('Error:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchVideos();
  }, []);

  if (isLoading) {
    return <div>Loading videos...</div>;
  }

  if (videos.length === 0) {
    return <div>No videos found. Generate some first!</div>;
  }

  return (
    <div className="video-list">
      <h2>Your Generated Videos</h2>
      <div className="video-grid">
        {videos.map((video, index) => (
          <div key={index} className="video-item">
            <video controls width="100%" crossOrigin="anonymous">
              <source src={`http://localhost:8000/test-video/${encodeURIComponent(video)}`} type="video/mp4" />
              <source src={`http://localhost:8000/stream-video/${encodeURIComponent(video)}`} type="video/mp4" />
              <source src={`http://localhost:8000/static/videos/${encodeURIComponent(video)}`} type="video/mp4" />
              <source src={`http://localhost:8000/download-video?path=${encodeURIComponent(video)}`} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <div className="video-meta">
              <span>{video}</span>
              <a 
                href={`http://localhost:8000/download-video?path=${encodeURIComponent(video)}&download=true`} 
                download
                className="download-btn"
              >
                Download
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoList;