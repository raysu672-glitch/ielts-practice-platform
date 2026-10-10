#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phonics.py — 拼读规则打标 + 简易音节切分（构建期，不入运行时）。

写入 words.phonics（JSON 规则 id 列表）、words.syll（hap·py 式切分）、
words.irr（同形异音/视读词，不进互锁练词）。

打标规则（三重过滤，缺一不可）：
  1) 拼写正则命中（rules[].match）
  2) 音标校验命中（rules[].ipa）：读词音标必须含 any 之一、且不含 none 之一
     —— 这一层把 his→c_s、change→c_g、machine→dig_ch、you→ou/ow、walk→c_l、
        knee→c_k、write→c_w、hour→c_h、now→oa/ow 之类的误标自动剔除。
  3) 非不规则：不在 IRR_WORDS 里

硬保护：任何出现在 rules[].examples 里的词永不被标为 irr（验收：例词必然可参与互锁）。

用法：
  python scripts/build_phonics.py            # 干跑，只审计不落库
  python scripts/build_phonics.py --apply    # 正式写入 words 表

db.ensure_ready() 在全新安装（words 刚导入、尚无 phonics 标签）时会自动调用
tag_words()，保证新库不会缺拼读数据。
"""
import argparse
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_PLATFORM_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DATA = os.path.join(_PLATFORM_ROOT, 'sources', 'danci', 'data')
RULES = os.path.join(DATA, 'phonics_rules.json')
DB = os.path.join(_PLATFORM_ROOT, 'data', 'vocab.db')

# ---------------------------------------------------------------------------
# 不规则词表 = 同形异音（heteronyms）+ 纯视读词。
# 只收「拼写无法提示读音」的词；凡能由某条规则解释的（如 have 的 h/v、come 的 k）
# 一律不收，交给音标校验层去处理（它们自然通不过不符合的规则）。
# ---------------------------------------------------------------------------
IRR_WORDS = {
    # --- 同形异音：同一拼写两种读法，朗读时无法由规则判定 ---
    'live', 'read', 'lead', 'close', 'use', 'present', 'record', 'object', 'subject',
    'produce', 'increase', 'decrease', 'refuse', 'excuse', 'desert', 'contract', 'content',
    'permit', 'progress', 'project', 'protest', 'survey', 'suspect', 'transfer', 'minute',
    'bow', 'tear', 'wind', 'row', 'wound', 'dove', 'bass', 'separate', 'alternate',
    'appropriate', 'delegate', 'estimate', 'graduate', 'intimate', 'moderate', 'associate',
    'advocate', 'duplicate', 'elaborate', 'invalid', 'rebel', 'convict', 'exploit',
    'address', 'concert', 'conflict', 'contest', 'contrast', 'convert', 'digest', 'escort',
    'export', 'extract', 'impact', 'import', 'insult', 'perfume', 'reject', 'sow',
    # --- 视读词：拼写完全不提示读音（且不作为任何规则例词）---
    'one', 'once', 'two', 'who', 'whom', 'whose', 'whole', 'eye', 'because',
    'friend', 'great', 'break', 'bread', 'ready', 'women', 'woman',
    'many', 'any', 'again', 'said', 'says', 'was', 'were', 'are',
    'answer', 'queue', 'beauty', 'beautiful', 'ocean', 'sure', 'sugar', 'iron',
}

# ECDICT 音标里混入的非 IPA 写法 → 统一归一化，便于子串匹配
_TRANS = str.maketrans({
    'ә': 'ə',   # U+04D9 西里尔 schwa
    'ɡ': 'g',   # U+0261 脚本 g
    'є': 'e',   # U+0454
    '’': '',
    '`': '',
    "'": '',
    ' ': '',
    '.': '',
    ',': '',
    '[': '',
    ']': '',
    'ˈ': '',
})


def norm_ipa(p: str) -> str:
    """归一化音标：统一特殊字符、去重音与分隔符，只保留可匹配的连续串。"""
    if not p:
        return ''
    return (p or '').strip().translate(_TRANS)


def ipa_ok(ipa: str, cond: dict) -> bool:
    """音标校验：含 any 之一（若给了 any），且不含 none 之一（若给了 none）。"""
    if not cond:
        return True
    any_list = cond.get('any') or []
    none_list = cond.get('none') or []
    if any_list and not any(x in ipa for x in any_list):
        return False
    if none_list and any(x in ipa for x in none_list):
        return False
    return True


def syllabify(word: str) -> str:
    """极简英文音节切分：按元音核切开，中间辅音倾向给后一音节。

    词尾沉默 e 先摘掉再切（make 不该切成 ma·ke），只切出一个音节就返回原词。
    """
    w = word.lower()
    if len(w) <= 3 or ' ' in w or '-' in w:
        return word
    # 词尾沉默 e：前一字符是辅音时视为不发音，不参与切分
    if len(w) >= 4 and w.endswith('e') and w[-2] not in 'aeiou':
        w = w[:-1]
    vowels = set('aeiouy')
    parts = []
    i = 0
    n = len(w)
    while i < n:
        j = i
        while j < n and w[j] not in vowels:
            j += 1
        if j >= n:
            if parts:
                parts[-1] += w[i:]
            else:
                parts.append(w[i:])
            break
        k = j
        while k < n and w[k] in vowels:
            k += 1
        m = k
        while m < n and w[m] not in vowels:
            m += 1
        if m < n and m > k:
            split = k + max(0, (m - k) - 1)
            parts.append(w[i:split])
            i = split
        else:
            parts.append(w[i:m] if m > i else w[i:])
            i = m if m > i else n
    parts = [p for p in parts if p]
    if len(parts) <= 1:
        return word
    return '·'.join(parts)


def load_rules(path: str = RULES) -> list:
    with open(path, encoding='utf-8') as f:
        return json.load(f)['rules']


def tag_words(conn: sqlite3.Connection, rules_path: str = RULES) -> dict:
    """给 words 打 phonics/syll/irr 标签（不 commit，由调用方决定）。

    可重复执行（幂等）。返回统计数字典。
    """
    rules = load_rules(rules_path)

    # 例词集合：硬保护，永不标 irr
    example_words = set()
    for r in rules:
        for ex in r.get('examples', []):
            example_words.add(ex.lower())

    compiled = []
    for r in rules:
        if r['id'] == 'review_mix':
            continue  # 综合复习不用于打标
        compiled.append((r['id'], re.compile(r['match'], re.I), r.get('ipa') or {}))

    rows = conn.execute('SELECT id, word, p FROM words').fetchall()

    tagged = syll_n = irr_n = no_ipa = 0
    for row in rows:
        wid, w, p = row[0], row[1], row[2]
        lw = (w or '').lower()
        ipa = norm_ipa(p)
        if not ipa:
            no_ipa += 1

        # irr：同形异音/视读词，且绝不包含任何规则例词
        is_irr = lw in IRR_WORDS and lw not in example_words
        conn.execute('UPDATE words SET irr=? WHERE id=?', ('1' if is_irr else None, wid))
        if is_irr:
            irr_n += 1

        ids = []
        if not is_irr and ' ' not in lw and '&' not in lw:
            for rid, cre, cond in compiled:
                if cre.search(lw) and ipa_ok(ipa, cond):
                    ids.append(rid)

        syl = syllabify(w or '')
        syl = syl if '·' in syl else None
        if syl:
            syll_n += 1
        conn.execute('UPDATE words SET phonics=?, syll=? WHERE id=?',
                     (json.dumps(ids, ensure_ascii=False), syl, wid))
        if ids:
            tagged += 1

    return {'total': len(rows), 'tagged': tagged, 'syll': syll_n,
            'irr': irr_n, 'no_ipa': no_ipa, 'rules': len(compiled)}


# ---------------------------------------------------------------------------
# 审计（只读，供人工/CI 查验）
# ---------------------------------------------------------------------------
SUSPECT = {
    'c_s': ['is', 'his', 'has', 'was', 'these', 'those'],
    'c_g': ['change', 'page', 'large', 'huge', 'age', 'orange'],
    'dig_ch': ['machine', 'chemistry', 'stomach', 'character', 'school'],
    'dig_ng': ['change', 'orange', 'danger'],
    'c_w': ['write', 'wrong', 'who', 'two', 'answer', 'know'],
    'c_l': ['walk', 'talk', 'half', 'could', 'would'],
    'c_k': ['know', 'knee', 'knife', 'knight', 'knot'],  # knock 词尾 ck 真实发 /k/，不算误标
    'c_h': ['hour', 'honest', 'what', 'when'],
    'vt_ou_ow': ['you', 'should', 'could', 'would', 'four', 'your', 'group', 'though', 'through'],
    'vt_oa_ow': ['now', 'how', 'brown', 'town', 'down'],
    'v_u': ['put', 'full', 'pull'],
    'v_o': ['come', 'done', 'love', 'some', 'go'],
    'v_a': ['was', 'many', 'are'],
    'v_i': ['find', 'nice', 'time', 'police'],
    'magic_a': ['have', 'are', 'warm'],
    'vt_ea': ['bread', 'head', 'great', 'break'],
    'vt_oo': ['blood', 'flood'],
}


def audit(conn: sqlite3.Connection, rules_path: str = RULES) -> bool:
    """打印审计报告。返回 True 表示全部通过。"""
    rules = load_rules(rules_path)
    conn.row_factory = sqlite3.Row

    print('例词体检（须为族长、未被标 irr、且被本规则命中）：')
    problems = []
    n_ex = 0
    for r in rules:
        if r['id'] == 'review_mix':
            continue  # 综合复习伪规则，不参与打标
        for ex in r.get('examples', []):
            n_ex += 1
            row = conn.execute(
                'SELECT is_head, irr, phonics FROM words WHERE lower(word)=lower(?)', (ex,)).fetchone()
            if row is None:
                problems.append((r['id'], ex, '库里没有'))
            elif row['is_head'] != 1:
                problems.append((r['id'], ex, '不是族长'))
            elif row['irr'] == '1':
                problems.append((r['id'], ex, '被标 irr'))
            elif ('"%s"' % r['id']) not in (row['phonics'] or ''):
                problems.append((r['id'], ex, '未被本规则命中'))
    if problems:
        for rid, ex, why in problems:
            print('  %-12s %-10s %s' % (rid, ex, why))
    print('  例词 %d 个，问题 %d 个 %s' % (n_ex, len(problems), '✓' if not problems else '← 需修'))

    print()
    print('误匹配抽查（应全为 0）：')
    fp = 0
    for rid, ws in SUSPECT.items():
        hits = []
        for s in ws:
            row = conn.execute('SELECT phonics FROM words WHERE lower(word)=?', (s,)).fetchone()
            if row and row['phonics'] and ('"%s"' % rid) in row['phonics']:
                hits.append(s)
        if hits:
            fp += len(hits)
            print('  %-10s 误标 %d 个: %s' % (rid, len(hits), ', '.join(hits)))
    print('  误标合计：%d %s' % (fp, '✓' if fp == 0 else '← 需修'))

    return not problems and fp == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='正式写入数据库（默认只干跑审计）')
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding='utf-8')
    sys.path.insert(0, os.path.dirname(HERE))
    from vocab import db as _db

    conn = _db.init_db(DB)
    conn.row_factory = sqlite3.Row

    st = tag_words(conn)
    print('words=%d  有音标=%d  无音标(不打标)=%d'
          % (st['total'], st['total'] - st['no_ipa'], st['no_ipa']))
    print('打标(至少命中1条规则)=%d  有音节切分=%d  irr=%d  规则数=%d'
          % (st['tagged'], st['syll'], st['irr'], st['rules']))
    print()

    ok = audit(conn)

    print()
    if args.apply:
        conn.commit()
        print('已写入数据库 ✓')
    else:
        conn.rollback()
        print('（干跑：未写入数据库。确认无误后加 --apply）')
    conn.close()
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
