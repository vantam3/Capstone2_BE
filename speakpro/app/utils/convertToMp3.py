from gtts import gTTS
from django.core.files import File
import os
from app.models import Audio
from django.conf import settings

def generate_audio_for_text(speaking_text):
    try:
        # Decode binary content to text
        text = speaking_text.content.decode() if isinstance(speaking_text.content, bytes) else str(speaking_text.content)
        tts = gTTS(text=text, lang=speaking_text.language or 'en')

        filename = f"{speaking_text.id}_audio.mp3"
        temp_path = os.path.join(settings.MEDIA_ROOT, "temp", filename)

        os.makedirs(os.path.dirname(temp_path), exist_ok=True)  # đảm bảo thư mục tồn tại
        tts.save(temp_path)

        with open(temp_path, "rb") as f:
            audio = Audio(speaking_text=speaking_text)
            audio.audio_file.save(filename, File(f), save=True)

        os.remove(temp_path)  # xoá file tạm sau khi lưu vào model

    except Exception as e:
        print(f"[❌ Error generating audio] {e}")
