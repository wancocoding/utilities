import requests
import hashlib
import random
import time

# === 配置你自己的百度翻译 API Key 和 Secret ===
APP_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"  # ← 在这里填入你的百度翻译 APP ID
SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxx"  # ← 在这里填入你的百度翻译密钥

# === 要翻译的原始英文字幕文件 ===
input_srt = "D:\\dev\\tools\\bin\\BBDown\\Blender\\[P01]1 1. Course Introduction.en.srt"
output_srt = (
    "D:\\dev\\tools\\bin\\BBDown\\Blender\\[P01]1 1. Course Introduction.zh.srt"
)


# === 翻译函数 ===
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


# === 逐行翻译 .srt 文件 ===
with open(input_srt, "r", encoding="utf-8") as fin, open(
    output_srt, "w", encoding="utf-8"
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

print(f"✅ 已保存翻译字幕：{output_srt}")
