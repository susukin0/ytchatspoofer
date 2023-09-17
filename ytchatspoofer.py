import re
from googleapiclient.discovery import build
import time

# YouTube API anahtarınızı buraya ekleyin
api_key = 'YOUR_API_KEY'

# YouTube URL'sinden video ID'sini çıkaran fonksiyon
def extract_video_id(youtube_url):
    video_id_match = re.search(r'v=([a-zA-Z0-9_-]+)', youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

# YouTube canlı yayının chat ID'sini almak için fonksiyon
def get_live_chat_id(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()
    live_chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    return live_chat_id

# Canlı yayın chat'inden belirli bir terimi kontrol eden fonksiyon
def check_messages_for_term(chat_id, term):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.liveChatMessages().list(
        liveChatId=chat_id,
        part='snippet',
        maxResults=5
    ).execute()
    
    messages = response['items']
    
    for message in messages:
        if term.lower() in message['snippet']['textMessageDetails']['messageText'].lower():
            return message['snippet']['textMessageDetails']['messageText']
    
    return None

# YouTube API'sini oluşturun
youtube = build('youtube', 'v3', developerKey=api_key)

# YouTube canlı yayını URL'sini belirtin
youtube_url = "https://www.youtube.com/watch?v=VIDEO_ID"

# Video ID'sini çıkarın
video_id = extract_video_id(youtube_url)

if video_id:
    # Canlı yayının chat ID'sini alın
    chat_id = get_live_chat_id(video_id)
    print(f"Canlı yayının chat ID'si: {chat_id}")
    
    # Belirli bir terimi kontrol et
    term_to_check = "makarna"  # İzlemek istediğiniz terim
    result = None
    
    while not result:
        result = check_messages_for_term(chat_id, term_to_check)
        if not result:
            print(f"Couldn't Find The Word. Suspended 5 Seconds...")
            time.sleep(5)
    
    print(f"Bildirim: {result}")
else:
    print("Video ID bulunamadı.")

