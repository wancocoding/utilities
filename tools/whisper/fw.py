from faster_whisper import WhisperModel

# === 配置区域 ===
audio_file = "D:\\dev\\tools\\bin\BBDown\Blender\\[P01]1 1. Course Introduction.mp4"  # 修改为你的音频或视频文件名
# model_size = "medium"          # 可选：tiny, base, small, medium, large-v2
device = "cpu"                 # 或 "cuda"
output_srt = "D:\\dev\\tools\\bin\BBDown\Blender\\[P01]1 1. Course Introduction.en.srt"

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))


# === 写入 .srt 文件 ===
with open(output_srt, "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments, 1):
        start = segment.start
        end = segment.end
        text = segment.text.strip()

        def fmt(t):
            h, r = divmod(t, 3600)
            m, s = divmod(r, 60)
            return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace('.', ',')

        f.write(f"{i}\n{fmt(start)} --> {fmt(end)}\n{text}\n\n")

print(f"✅ 字幕已保存到: {output_srt}")

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))