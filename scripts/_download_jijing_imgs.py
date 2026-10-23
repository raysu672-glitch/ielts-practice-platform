import json
import os
import urllib.request

BASE = "https://ai-oss3.oss-cn-shenzhen.aliyuncs.com/exam/"
OUT = os.path.join(os.path.dirname(__file__), "..", "sources", "jianyazhenti", "exam-data", "jijing")
os.makedirs(OUT, exist_ok=True)

files = {
    1255: "9408f25e6bc047e2b1bb297022119a65.png",
    1240: "587aa1e722444e658ca712023576ad20.png",
    1196: "8a513a41b77e4ffdaf001bf78d53356c.jpg",
    1171: "b8d05ad89cd54b02b32bb9b1f2ea923d.jpg",
    1106: "e79fa4282b34401fa5e2336c38890833.png",
    1082: "7f4b8eb48d684e22ac2833384b8a46c6.png",
    1063: "7e6757b9189248b0be997c67bc5521f2.png",
    1057: "56da71e4f853478f9f046f069097e8e1.png",
    1055: "07a6013b0cae451f8a1a46ca9af963c9.png",
    1048: "4c134343c099468c9da06c30c40ccfd7.png",
    1046: "62ac8d764c0c410495cbeb5033e0380a.png",
    1039: "dc678e144f7c4d3d91db0496cf17999f.png",
    1037: "3e9bcd47704b4082ace0ea2fbde24c83.png",
    1007: "ce8bfd90db75410a90247d41a2d5f219.png",
    1005: "503c40e2e06045e5b8487d4c3b5b071a.png",
    960: "a06fd8b8ad7046b7a29962159bfa03a6.png",
    958: "c06a5e0548194f7ba7e016d178d1745c.png",
    956: "c892302cdf194472ba0c7da009582d24.png",
    954: "c8ea8524cbf8440bb884c371cf3669c7.png",
}

results = []
for sid, fn in files.items():
    ext = os.path.splitext(fn)[1]
    dest = os.path.join(OUT, f"{sid}{ext}")
    url = BASE + fn
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, "wb") as f:
            f.write(data)
        results.append({"id": sid, "ok": True, "bytes": len(data), "file": os.path.basename(dest)})
    except Exception as e:
        results.append({"id": sid, "ok": False, "err": str(e)})

print(json.dumps(results, ensure_ascii=False, indent=2))