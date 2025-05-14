import os
from pathlib import Path
import requests
import hashlib
import random
import time

from faster_whisper import WhisperModel


# ============================================
# 配置部分
# ============================================


# 文件设置

# 要生成字幕的文件
video_dir = "D:\\dev\\tools\\bin\BBDown\Blender"  # ← 替换为你自己的目录
# 后缀
file_postfix = ".mp4"


# Faster-Whisper设置
device = "cuda"  # cpu cuda
compute_type = "int8_float16"  # int8_float16 int8 float16
model_size = "large-v3"  # 模型

# === 配置你自己的百度翻译 API Key 和 Secret ===
APP_ID = "xxxxxxxxxxxxxxx"  # ← 在这里填入你的百度翻译 APP ID
SECRET_KEY = "xxxxxxxxxxx"  # ← 在这里填入你的百度翻译密钥


# 模型
model = WhisperModel(model_size, device=device, compute_type=compute_type)

# 如果用cuda并且报错Could not locate cudnn_ops64_9.dll. Please make sure it is in your library path!
# 就设置一下你的CUDA的bin
os.add_dll_directory("C:\\Program Files\\NVIDIA\\CUDNN\\v9.10\\bin\\12.9")


# 百度翻译函数
def translate_baidu(text, from_lang="en", to_lang="zh"):
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    salt = str(random.randint(32768, 65536))
    sign = APP_ID + text + salt + SECRET_KEY
    sign = hashlib.md5(sign.encode()).hexdigest()

    params = {
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appid": APP_ID,
        "salt": salt,
        "sign": sign,
    }

    for attempt in range(3):
        try:
            response = requests.get(url, params=params, timeout=5)
            result = response.json()
            if "trans_result" in result:
                return result["trans_result"][0]["dst"]
            else:
                print("翻译失败:", result)
        except Exception as e:
            print("请求失败:", e)
        time.sleep(1)
    return text


# 生成英文字幕
def generate_en_sub(file_path, en_sub_path):
    print(file_path)
    segments, info = model.transcribe(
        file_path,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    print(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )
    # === 写入 .srt 文件 ===

    with open(en_sub_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            start = segment.start
            end = segment.end
            text = segment.text.strip()

            def fmt(t):
                h, r = divmod(t, 3600)
                m, s = divmod(r, 60)
                return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")

            f.write(f"{i}\n{fmt(start)} --> {fmt(end)}\n{text}\n\n")

    print(f"✅ 英文字幕已保存到: {en_sub_path}")


# 翻译成中文字幕
def translate_cn_sub(en_sub_path, cn_sub_path):
    # 开始翻译
    # === 逐行翻译 .srt 文件 ===
    with open(en_sub_path, "r", encoding="utf-8") as fin, open(
        cn_sub_path, "w", encoding="utf-8"
    ) as fout:
        block = []
        for line in fin:
            if line.strip() == "":
                if len(block) >= 3:
                    idx = block[0]
                    timecode = block[1]
                    text = " ".join(block[2:])
                    translated = translate_baidu(text.strip())
                    fout.write(f"{idx}\n{timecode}\n{translated}\n\n")
                else:
                    fout.write("\n")
                block = []
            else:
                block.append(line.strip())
    print(f"✅ 已保存翻译中文字幕：{cn_sub_path}")


def parse_srt(path):
    with open(path, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
        result = []
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                idx = lines[0]
                timecode = lines[1]
                text = " ".join(lines[2:])
                result.append((idx, timecode, text))
        return result


# 合并为一个字幕文件
def combine_subs(en_sub_path, cn_sub_path, combine_file_path):
    en_srt = parse_srt(en_sub_path)
    zh_srt = parse_srt(cn_sub_path)
    with open(
        combine_file_path,
        "w",
        encoding="utf-8",
    ) as out:
        for (idx, timecode, en_text), (_, _, zh_text) in zip(en_srt, zh_srt):
            out.write(f"{idx}\n{timecode}\n{en_text}\n{zh_text}\n\n")
    print(f"✅ 字幕合并完成：{combine_file_path}")


# 生成原英文字幕
def generate_sub(file_dir, file_path):
    # 得到文件名

    filename_without_postfix = Path(file_path).stem
    en_sub_filename = os.path.join(file_dir, f"{filename_without_postfix}.en.srt")
    cn_sub_filename = os.path.join(file_dir, f"{filename_without_postfix}.cn.srt")
    cn_en_sub_file = os.path.join(file_dir, f"{filename_without_postfix}.srt")

    generate_en_sub(file_path, en_sub_filename)

    translate_cn_sub(en_sub_filename, cn_sub_filename)

    combine_subs(en_sub_filename, cn_sub_filename, cn_en_sub_file)


if __name__ == "__main__":
    for filename in os.listdir(video_dir):
        if filename.endswith(file_postfix):
            # print(os.path.join(video_dir, filename))
            generate_sub(video_dir, os.path.join(video_dir, filename))
