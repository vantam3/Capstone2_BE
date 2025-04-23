import subprocess

def convert_webm_to_mp3(input_path, output_path):
    try:
        # ✅ Đường dẫn chính xác tới ffmpeg.exe trên máy bạn
        ffmpeg_path = "C:/Users/tranv/ffmpeg/ffmpeg-n7.1-latest-win64-gpl-7.1/bin/ffmpeg.exe"

        print("🔧 Running ffmpeg...")
        print("📥 Input:", input_path)
        print("📤 Output:", output_path)

        result = subprocess.run(
            [ffmpeg_path, "-y", "-i", input_path, output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print("❌ FFmpeg failed:", result.stderr)
            return False

        print("✅ Convert thành công!")
        return True

    except Exception as e:
        print("❌ Convert error:", e)
        return False
