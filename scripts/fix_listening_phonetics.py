#!/usr/bin/env python3
"""修复「听力词汇」词表里的 phonetic（音标）与词形不符问题。

背景
----
`l` -> `I` 的字体/编码事故（连带 `ʃ/ð/ʒ/ɔ:` -> `∫/δ/3/J:`）污染了词表，
后续多次「修拼写」的脚本只改 word、重建了部分音频，**没修 phonetic**。
后来又被一次自动化改写（把音标改成美式记法）批量替换了 559 条，替换过程
里留下了若干重音记号错位（如 `air quality` 的 `/ɛr kˈwɑləti/`）。

结果就是学生看到的三种「对不上」：
  1. 单词改了、音标没跟着改（flourishing 的音标还是 flourishment 的）；
  2. 音标里残留 `I/∫/δ/3` 等污染字符；
  3. 重音记号被挪到词首辅音之后（music -> /mˈjuzɪk/）。

本脚本一次性处理：污染符号替换 + 个别错位条目 + 词形与音标/词义不符的条目。

用法
----
  python scripts/fix_listening_phonetics.py            # 仅预览（默认）
  python scripts/fix_listening_phonetics.py --apply    # 实际写回
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html",
    ROOT / "sources" / "tinglidanciceshi" / "listening.html",
]

# ① 污染符号批量替换（顺序敏感，J: 必须先于 I）
BATCH: list[tuple[str, str]] = [
    ("J:", "ɔ:"),   # 'pIæt,fJ:rmz -> 'plæt,fɔ:rmz
    ("δ", "ð"),     # 希腊 delta -> eth
    ("∫", "ʃ"),     # 积分号 -> esh
    ("3", "ʒ"),     # 数字 3（当 ʒ 用）
    ("I", "l"),     # 大写 I -> 小写 l
    ("ε", "ɛ"),     # 希腊 epsilon -> IPA open-e
    ("'", "ˈ"),     # ASCII 单引号 -> IPA 主重音
    (",", "ˌ"),     # ASCII 逗号   -> IPA 次重音
    (":", "ː"),     # ASCII 冒号   -> IPA 长音符
    ("oʊ", "əʊ"),   # 美式记法 -> 英式（音频为 en-GB）
]

# ② 词形本身错了（音标/词义指向另一个词）
RENAME: dict[str, str] = {
    # 原 graduai（逐渐的 /ˈɡrædʒuəl/）被前一次修复错改成 graduate，应为 gradual
    "graduate": "gradual",
    # 原 paining（疼痛 /ˈpeɪnɪŋ/）被前一次修复错改成 painting，应为 pain
    "painting": "pain",
}

# ③ 批量替换后仍不对的条目：词 -> 正确音标
SPECIAL: dict[str, str] = {
    "flourishing": "/ˈflʌrɪʃɪŋ/",     # 原为 flourishment 的音标
    "breathing": "/ˈbri:ðɪŋ/",
    "explode": "/ɪk'spləud/",
    "apology": "/ə ˈpɒlədʒi/",
    "length": "/leŋθ/",
    "labels": "/ˈleɪbəlz/",
    "publishing": "/ˈpʌblɪʃɪŋ/",
    "shipping": "/ˈʃɪpɪŋ/",
    "touching": "/ˈtʌtʃɪŋ/",
    "weekend": "/ˌwi:kˈend/",
    "unanswered": "/ʌnˈɑ:nsəd/",
    "weather": "/ˈweðə(r)/",
    "loyalty": "/ˈlɔɪəlti/",
    "legroom": "/ˈleɡru:m/",
    "lost": "/lɒst/",
    "alter": "/ˈɔ:ltə(r)/",
    "tolerance": "/ˈtɒlərəns/",
    "shoppers": "/ˈʃɒpəz/",
    "wheelchair": "/ˈwi:ltʃeə(r)/",
    "undergraduate": "/ˌʌndərˈɡrædʒuət/",
    # 音标倒退（被自动化改写改坏，回退到正确形式）
    "painting class": "/ˈpeɪntɪŋ klæs/",
    "face painting": "/feɪs ˈpeɪntɪŋ/",
    "young graduates": "/ˌjʌŋ ˈɡrædʒuəts/",
    "air quality": "/ɛr ˈkwɑləti/",
    "background music": "/ˈbækgraʊnd ˈmjuzɪk/",
    "future career": "/ˈfjuʧər kəˈrɪr/",
    "interview questions": "/ˈɪntərvju ˈkwɛsʧənz/",
    "live music": "/lɪv ˈmjuzɪk/",
    "local museum": "/ˈloʊkəl ˈmjuziəm/",
    "music festival": "/ˈmjuzɪk ˈfɛstɪvəl/",
    "music videos": "/ˈmjuzɪk ˈvɪdioʊz/",
    "non-smoking room": "/ˌnɑnˈsmoʊkɪŋ rum/",
    "sleeping bag": "/ˈslipɪŋ bæg/",
    "sleeping pills": "/ˈslipɪŋ pɪlz/",
    "smaller areas": "/ˈsmɔlər ˈɛriəz/",
    "smaller one": "/ˈsmɔlər wən/",
    "space museum": "/speɪs ˈmjuziəm/",
    "swimming pool": "/ˈswɪmɪŋ pul/",
    "swimming suit": "/ˈswɪmɪŋ sut/",
    "think quickly": "/θɪŋk ˈkwɪkli/",
    "write music": "/raɪt ˈmjuzɪk/",
    "hardworking": "/ˌhɑːdˈwɜːkɪŋ/",
    "overdue books": "/ˌoʊvərˈdu bʊks/",
    "part-time": "/ˌpɑrtˈtaɪm/",
    "self-centered": "/ˌsɛlfˈsɛntərd/",
    "unhealthy": "/ʌnˈhɛlθi/",
    "hairdresser": "/ˈhɛrdrɛsər/",
    "electronic card": "/ɪˌlɛkˈtrɑnɪk kɑrd/",
    "electronic directory": "/ɪˌlɛkˈtrɑnɪk dɪˈrɛktəri/",
    # 改名后仍需单独修音标
    "pain": "/peɪn/",
    "gradual": "/ˈɡrædʒuəl/",
    # 词形/音标不符（部分自导入期就存在）
    "hair": "/heə(r)/",
    "teeth": "/ti:θ/",
    "remote": "/rɪˈməʊt/",
}

# ④ 词义与词形不符（多为改名后遗留）
MEANING: dict[str, str] = {
    "hair": "头发",
    "weather": "天气",
    "eye contact": "眼神交流",
    "remote": "偏远的",
}

# ⑤ 全量校对（2026-09-19）新增：按错误类别整理
SPECIAL_FULL: dict[str, str] = {
    # --- A. θ 被写成 ə（18 条）---
    "bath": "/bɑ:θ/",
    "bathrooms": "/ˈbɑ:θru:mz/",
    "birth": "/bɜːθ/",
    "healthcare": "/ˈhelθkeə(r)/",
    "healthy": "/ˈhelθi/",
    "hothouse": "/ˈhɒθhaʊs/",
    "math": "/mæθ/",
    "mathematics": "/ˌmæθəˈmætɪks/",
    "methods": "/ˈmeθədz/",
    "monthly": "/ˈmʌnθli/",
    "myth": "/mɪθ/",
    "northeast": "/ˌnɔ:θˈi:st/",
    "theatre": "/ˈθɪətə(r)/",
    "theme": "/θi:m/",
    "therapy": "/ˈθerəpi/",
    "thunderstorm": "/ˈθʌndəstɔ:m/",
    "thursday": "/ˈθɜːzdeɪ/",
    "wealthy": "/ˈwelθi/",
    # --- B. d 被写成 ɒ（20 条）---
    "aging": "/ˈeɪdʒɪŋ/",
    "argentina": "/ˌɑ:dʒənˈti:nə/",
    "biological": "/ˌbaɪəˈlɒdʒɪkl/",
    "change": "/tʃeɪndʒ/",
    "drama": "/ˈdrɑ:mə/",
    "engineering": "/ˌendʒɪˈnɪərɪŋ/",
    "fluids": "/ˈflu:ɪdz/",
    "gardening": "/ˈɡɑ:dnɪŋ/",
    "gene": "/dʒi:n/",
    "general": "/ˈdʒenərəl/",
    "germs": "/dʒɜ:mz/",
    "jazz": "/dʒæz/",
    "joint": "/dʒɔɪnt/",
    "journals": "/ˈdʒɜ:nəlz/",
    "management": "/ˈmænɪdʒmənt/",
    "microbiology": "/ˌmaɪkrəʊbaɪˈɒlədʒi/",
    "orange": "/ˈɒrɪndʒ/",
    "originality": "/əˌrɪdʒəˈnæləti/",
    "stage": "/steɪdʒ/",
    "trends": "/trendz/",
    # --- C. ŋ 写成 n / ɡ（8 条）---
    "link": "/lɪŋk/",
    "monkeys": "/ˈmʌŋkiz/",
    "hungry": "/ˈhʌŋɡri/",
    "vetting": "/ˈvetɪŋ/",
    "weeding": "/ˈwi:dɪŋ/",
    "strangers": "/ˈstreɪndʒəz/",
    "dangerous": "/ˈdeɪndʒərəs/",
    # --- D. 字母组合未转成 IPA ---
    "coconut": "/ˈkəʊkənʌt/",
    "horsehair": "/ˈhɔ:sheə(r)/",
    "protein": "/ˈprəʊti:n/",
    "worksheet": "/ˈwɜːkʃi:t/",
    # --- E. 音标串位（音标属于别的词）---
    "politician": "/ˌpɒlɪˈtɪʃn/",
    # --- F. 其它零散 ---
    "geese": "/gi:s/",
    "agriculture": "/ˈæɡrɪkʌltʃə(r)/",
    # --- G. 音标内嵌空格（单词内部被空格断开）---
    "adults": "/əˈdʌlts/",
    "airline": "/ˈeəlaɪn/",
    "antiseptic": "/ˌæntiˈseptɪk/",
    "arrangement": "/əˈreɪndʒmənt/",
    "attack": "/əˈtæk/",
    "balcony": "/ˈbælkəni/",
    "benefits": "/ˈbenɪfɪts/",
    "cabin": "/ˈkæbɪn/",
    "calculating": "/ˈkælkjəleɪtɪŋ/",
    "calculation": "/ˌkælkjəˈleɪʃn/",
    "cashier": "/kæˈʃɪə(r)/",
    "cement": "/sɪˈment/",
    "circles": "/ˈsɜːkəlz/",
    "coloured": "/ˈkʌləd/",
    "colours": "/ˈkʌləz/",
    "commitment": "/kəˈmɪtmənt/",
    "comprehension": "/ˌkɒmprɪˈhenʃn/",
    "concert": "/ˈkɒnsət/",
    "concrete": "/ˈkɒŋkri:t/",
    "confidence": "/ˈkɒnfɪdəns/",
    "confirmation": "/ˌkɒnfəˈmeɪʃn/",
    "decline": "/dɪˈklaɪn/",
    "defense": "/dɪˈfens/",
    "degrees": "/dɪˈɡri:z/",
    "demand": "/dɪˈmɑ:nd/",
    "designers": "/dɪˈzaɪnəz/",
    "difficult": "/ˈdɪfɪkəlt/",
    "distribute": "/dɪˈstrɪbju:t/",
    "domestic": "/dəˈmestɪk/",
    "double": "/ˈdʌbəl/",
    "downhill": "/ˈdaʊnhɪl/",
    "editor": "/ˈedɪtə(r)/",
    "fear": "/fɪə(r)/",
    "fishing": "/ˈfɪʃɪŋ/",
    "garbage": "/ˈɡɑ:bɪdʒ/",
    "global": "/ˈɡləʊbəl/",
    "graphics": "/ˈɡræfɪks/",
    "identification": "/aɪˌdentɪfɪˈkeɪʃn/",
    "immigration": "/ˌɪmɪˈɡreɪʃn/",
    "impossible": "/ɪmˈpɒsəbl/",
    "independent": "/ˌɪndɪˈpendənt/",
    "interaction": "/ˌɪntərˈækʃn/",
    "international": "/ˌɪntəˈnæʃənəl/",
    "isolation": "/ˌaɪsəˈleɪʃn/",
    "metals": "/ˈmetəlz/",
    "microfilm": "/ˈmaɪkrəʊfɪlm/",
    "migrate": "/maɪˈɡreɪt/",
    "minivan": "/ˈmɪnɪvæn/",
    "noticeboard": "/ˈnəʊtɪsbɔːd/",
    "objectives": "/əbˈdʒektɪvz/",
    "observation": "/ˌɒbzəˈveɪʃn/",
    "overfishing": "/ˌəʊvəˈfɪʃɪŋ/",
    "painkiller": "/ˈpeɪnkɪlə(r)/",
    "painters": "/ˈpeɪntəz/",
    "pennies": "/ˈpeniz/",
    "performance": "/pəˈfɔ:məns/",
    "released": "/rɪˈli:st/",
    "rubbish": "/ˈrʌbɪʃ/",
    "satisfaction": "/ˌsætɪsˈfækʃn/",
    "scientific": "/ˌsaɪənˈtɪfɪk/",
    "sculptures": "/ˈskʌlptʃəz/",
    "silence": "/ˈsaɪləns/",
    "slaves": "/sleɪvz/",
    "specific": "/spəˈsɪfɪk/",
    "stabilize": "/ˈsteɪbəlaɪz/",
    "surface": "/ˈsɜ:fɪs/",
    "technical": "/ˈteknɪkəl/",
    # --- H. 主重音位置错误 / 剩余内嵌空格（第二轮）---
    "reinforce": "/ˌriːɪnˈfɔːs/",
    "medication": "/ˌmedɪˈkeɪʃn/",
    "undeveloped": "/ˌʌndɪˈveləpt/",
    "tutorials": "/ˈtjuːtɔːriəlz/",
    "translator": "/trænzˈleɪtə(r)/",
    "resources": "/rɪˈsɔːsɪz/",
    "processing": "/ˈprəʊsesɪŋ/",
    "kilometers": "/kɪˈlɒmɪtəz/",
    "insurance": "/ɪnˈʃʊərəns/",
    "indoor": "/ɪnˈdɔː(r)/",
    "european": "/ˌjʊərəˈpiːən/",
    "emergency": "/ɪˈmɜːdʒənsi/",
    "effectiveness": "/ɪˈfektɪvnəs/",
    "duration": "/djuˈreɪʃn/",
    "documentation": "/ˌdɒkjʊˈmenteɪʃn/",
    "democratic": "/ˌdeməˈkrætɪk/",
    "decrease": "/dɪˈkriːs/",
    "tomatoes": "/təˈmɑːtəʊz/",
    "morality": "/ˈmɒrəlɪti/",
    "ingredients": "/ɪnˈɡriːdiənts/",
    "jet engine": "/dʒet ˈendʒɪn/",
    "baseball coach": "/ˈbeɪsbɔːl koʊtʃ/",
    # --- I. 二合元音写错（oɪ 应为 ɔɪ；au 应为 aʊ）---
    "boiler": "/ˈbɔɪlə(r)/",
    "choice": "/tʃɔɪs/",
    "toilet": "/ˈtɔɪlət/",
    "voices": "/ˈvɔɪsɪz/",
    "accountants": "/əˈkaʊntənts/",
    "amount": "/əˈmaʊnt/",
    "compounds": "/ˈkɒmpaʊndz/",
    "crown": "/kraʊn/",
    "outline": "/ˈaʊtlaɪn/",
    "pounds": "/paʊndz/",
    "town": "/taʊn/",
    "warehouse": "/ˈweəhaʊs/",
    "waterpower": "/ˈwɔːtəpaʊə(r)/",
    # --- J. 包裹符号缺失 / 重音错位 ---
    "challenge": "/ˈtʃælɪndʒ/",
    "cooperation loan": "/kəʊˌɒpəˈreɪʃn ləʊn/",
}

POLLUTED = re.compile(r"[I∫δ]|(?<![0-9])3(?![0-9])|J:")


def scrub(ph: str) -> str:
    for a, b in BATCH:
        ph = ph.replace(a, b)
    return ph


def normalize(ph: str) -> str:
    """方括号当斜杠、斜杠内侧多余空格。"""
    out = ph.strip()
    if out.startswith("[") and out.endswith("]"):
        out = "/" + out[1:-1].strip() + "/"
    m = re.match(r"^/\s*(.*?)\s*/$", out)
    if m:
        out = "/" + m.group(1) + "/"
    return out


VOW_R = set("aæeioəɪʊɛɒʌɑɔɜu")


def rhotic(ph: str) -> str:
    """英式非儿化（对齐 listening.html / en-GB 音频）。

    r 只在元音前发音；词尾的 -er/-or/-ar 写成 (r)；
    ɪr/ɛr/ʊr（r 后非元音）转为 ɪə/eə/ʊə；其余非元音前的 r 直接删除。
    """
    n = len(ph)
    out: list[str] = []
    i = 0
    while i < n:
        if ph[i] == "(" and i + 2 < n and ph[i + 1] == "r" and ph[i + 2] == ")":
            out.append("(r)")
            i += 3
            continue
        ch = ph[i]
        if ch != "r":
            out.append(ch)
            i += 1
            continue
        nxt = ph[i + 1] if i + 1 < n else ""
        prev = ph[i - 1] if i > 0 else ""
        if nxt in VOW_R:
            out.append("r")
        elif prev == "ə":
            if nxt in ("/", "]", "", " "):
                out.append("(r)")
        elif prev in "ɪɛʊ":
            out.append("ə")
        i += 1
    return "".join(out)


def fix_file(path: Path, apply: bool) -> int:
    raw = io.open(path, encoding="utf-8").read()
    m = re.search(r"const ALL_WORDS = (\[[\s\S]*?\]);", raw)
    if not m:
        print(f"  跳过（无 ALL_WORDS）: {path.name}")
        return 0

    words = json.loads(m.group(1))
    changed: list[tuple[str, str, str]] = []
    for w in words:
        word, old = w["word"], w.get("phonetic", "")

        if word in RENAME:
            w["word"] = RENAME[word]

        if word in MEANING:
            w["meaning"] = MEANING[word]

        if not old:
            continue
        # 优先级：本轮全量校对 > 上轮定点修复 > 通用清洗；所有结果都过一遍记号规范化
        new = SPECIAL_FULL.get(word)
        if new is None:
            new = SPECIAL.get(word)
        if new is None:
            new = normalize(scrub(old))
        else:
            new = normalize(scrub(new))
        new = rhotic(new)
        if new != old:
            w["phonetic"] = new
            changed.append((w["word"], old, new))

    print(f"\n=== {path.name}：需修 {len(changed)} 条 ===")
    for word, old, new in changed:
        print("  %-24s %-30s -> %s" % (word, old, new))

    if not changed:
        return 0

    if apply:
        blob = json.dumps(words, ensure_ascii=False, separators=(",", ":"))
        path.write_text(raw[: m.start(1)] + blob + raw[m.end(1):], encoding="utf-8")
        print(f"  已写回 {path}")
    return len(changed)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="修复听力词表 phonetic 字段")
    ap.add_argument("--apply", action="store_true", help="实际写回（默认仅预览）")
    args = ap.parse_args()

    total = sum(fix_file(p, args.apply) for p in TARGETS if p.is_file())
    print(f"\n合计 {total} 条" + ("（已写回）" if args.apply else "（预览，未写回）"))

    if args.apply:
        for p in TARGETS:
            if not p.is_file():
                continue
            ws = json.loads(re.search(
                r"const ALL_WORDS = (\[[\s\S]*?\]);",
                io.open(p, encoding="utf-8").read()).group(1))
            left = [w["word"] for w in ws if POLLUTED.search(w.get("phonetic", ""))]
            print(f"  复查 {p.name}: 残留污染 {len(left)} 条 {left[:8] if left else ''}")


if __name__ == "__main__":
    main()
