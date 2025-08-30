from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import re

class YouTubeTranscriptInput(BaseModel):
    youtube_url: str = Field(..., description="YouTube video URL")

class YouTubeTranscriptTool(BaseTool):
    name: str = "YouTube Transcript Tool"
    description: str = "Extract transcript from YouTube videos for fact-checking"
    args_schema: Type[BaseModel] = YouTubeTranscriptInput

    def _run(self, youtube_url: str) -> str:
        try:
            video_id = self._extract_video_id(youtube_url)
            if not video_id:
                return "Invalid YouTube URL format"

            from youtube_transcript_api import YouTubeTranscriptApi
            
            api = YouTubeTranscriptApi()
            
            try:
                transcript = api.get_transcript(video_id)
                full_transcript = " ".join([entry['text'] for entry in transcript])
                return f"YouTube Video Transcript (ID: {video_id}):\n\n{full_transcript}"
            except Exception as e:
                return f"Error accessing video {video_id}: {str(e)}"
                
        except Exception as e:
            return f"Error processing YouTube URL: {str(e)}"

    def _extract_video_id(self, url: str) -> str:
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
