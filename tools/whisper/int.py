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

en_srt = parse_srt("D:\\dev\\tools\\bin\\BBDown\\Blender\\[P01]1 1. Course Introduction.en.srt")
zh_srt = parse_srt("D:\\dev\\tools\\bin\\BBDown\\Blender\\[P01]1 1. Course Introduction.zh.srt")

with open("D:\\dev\\tools\\bin\\BBDown\\Blender\\[P01]1 1. Course Introduction.srt", "w", encoding="utf-8") as out:
    for (idx, timecode, en_text), (_, _, zh_text) in zip(en_srt, zh_srt):
        out.write(f"{idx}\n{timecode}\n{en_text}\n{zh_text}\n\n")

print("✅ 合并完成：bilingual.srt")