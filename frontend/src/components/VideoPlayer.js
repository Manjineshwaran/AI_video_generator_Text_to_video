import React from 'react';

const VideoPlayer = ({ videoPath }) => {
  if (!videoPath) return null;

  // videoPath is now just the filename
  console.log('VideoPlayer - videoPath:', videoPath);
  console.log('VideoPlayer - test video URL:', `http://localhost:8000/test-video/${encodeURIComponent(videoPath)}`);
  console.log('VideoPlayer - streaming URL:', `http://localhost:8000/stream-video/${encodeURIComponent(videoPath)}`);
  console.log('VideoPlayer - static URL:', `http://localhost:8000/static/videos/${encodeURIComponent(videoPath)}`);
  console.log('VideoPlayer - download URL:', `http://localhost:8000/download-video?path=${encodeURIComponent(videoPath)}`);

  return (
    <div className="video-player">
      <h3>Your Generated Video</h3>
      {/* <video 
        controls 
        width="100%" 
        crossOrigin="anonymous"
        onError={(e) => {
          console.error('Video loading error:', e);
          console.error('Video element error details:', e.target.error);
          console.error('Video src:', e.target.src);
        }}
        onLoadStart={() => console.log('Video loading started')}
        onLoadedData={() => console.log('Video data loaded')}
      >
        <source src={`http://localhost:8000/test-video/${encodeURIComponent(videoPath)}`} type="video/mp4" />
        <source src={`http://localhost:8000/stream-video/${encodeURIComponent(videoPath)}`} type="video/mp4" />
        <source src={`http://localhost:8000/static/videos/${encodeURIComponent(videoPath)}`} type="video/mp4" />
        <source src={`http://localhost:8000/download-video?path=${encodeURIComponent(videoPath)}`} type="video/mp4" />
        Your browser does not support the video tag.
      </video> */}
      <div className="video-actions">
        <a 
          href={`http://localhost:8000/download-video?path=${encodeURIComponent(videoPath)}&download=true`} 
          download
          className="download-btn"
        >
          Download Video
        </a>
      </div>
    </div>
  );
};

export default VideoPlayer;