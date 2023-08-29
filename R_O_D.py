import streamlit as st
from pytube import YouTube
import os
import requests
from io import BytesIO

def main():
    st.title("R-O-D YT Video/Audio")

    path = st.text_input('Enter URL of any YouTube video')

    download_type = st.selectbox(
        'Select type of download',
        ('video', 'audio')
    )

    if download_type == 'video':
        video_formats = ['webm', 'mp4', 'mkv']
        selected_format = st.selectbox(
            'Select video format',
            video_formats
        )
        video_resolutions = ['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']
        selected_resolution = st.selectbox(
            'Select video resolution',
            video_resolutions
        )
    elif download_type == 'audio':
        audio_formats = ['mp3', 'wav']
        selected_format = st.selectbox(
            'Select audio format',
            audio_formats
        )
        audio_qualities = ['128kbps', '160kbps', '192kbps']
        selected_quality = st.selectbox(
            'Select audio quality',
            audio_qualities
        )

    if st.button("Download"):
        try:
            video = YouTube(path)
            st.write("Title of Video: " + video.title)
            #st.write("Number of Views: " + str(video.views))

            if download_type == 'audio':
                audio_streams = video.streams.filter(only_audio=True, file_extension='mp4')
                if len(audio_streams) > 0:
                    audio_stream = audio_streams[0]
                    audio_url = audio_stream.url
                    download_content(audio_url, f"{video.title}.{selected_format}")
                else:
                    st.error(f"No audio streams available for download with format {selected_format}.")
            elif download_type == 'video':
                available_streams = video.streams.filter(res=selected_resolution, file_extension=selected_format)
                if available_streams:
                    # Choose the best stream based on resolution
                    video_stream = max(available_streams, key=lambda x: int(x.resolution[:-1]))
                    video_url = video_stream.url
                    download_content(video_url, f"{video.title}.{selected_format}")
                else:
                    st.error(f"No video stream available for download with resolution {selected_resolution} and format {selected_format}.")
        except Exception as e:
            st.error("An error occurred: " + str(e))

    if st.button("Show Available Streams"):
        try:
            video = YouTube(path)
            st.write("Title of Video: " + video.title)
            #st.write("Number of Views: " + str(video.views))
            st.write("Available Streams:")
            for stream in video.streams:
                st.write(f"Quality: {stream.resolution}, Format: {stream.subtype}, Type: {stream.type}")
        except Exception as e:
            st.error("An error occurred: " + str(e))

    st.sidebar.text("Made by Dinesh_R 😉😎")
    st.sidebar.text("Contact: developer458809@gmail.com✔ ")

def download_content(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        buffer = BytesIO()
        for chunk in response.iter_content(chunk_size=1024):
            buffer.write(chunk)
        st.success(f"Downloading {filename}...")
        st.write(f"{filename} downloaded successfully!")
        st.download_button(label=f"Click to download {filename}", data=buffer.getvalue(), file_name=filename)

if __name__ == '__main__':
    main()
