#!/bin/bash
# 听力基础词汇音频重命名（拼写修正后同步服务器文件名）
# 用法（SSH 登录服务器后）：
#   cd /var/www/ielts && bash scripts/rename_basic_words_audio_server.sh
# 或仅在本目录执行：
#   AUDIO_DIR=/var/www/ielts/sources/tinglidanciceshi/audio/basic_words bash rename_basic_words_audio_server.sh

set -euo pipefail

AUDIO_DIR="${AUDIO_DIR:-/var/www/ielts/sources/tinglidanciceshi/audio/basic_words}"

if [[ ! -d "$AUDIO_DIR" ]]; then
  echo "错误：目录不存在: $AUDIO_DIR" >&2
  exit 1
fi

cd "$AUDIO_DIR"

rename_one() {
  local old="$1.mp3"
  local new="$2.mp3"
  if [[ ! -f "$old" ]]; then
    echo "跳过（源文件不存在）: $old"
    return 0
  fi
  if [[ -f "$new" ]]; then
    echo "跳过（目标已存在）: $new"
    return 0
  fi
  mv -- "$old" "$new"
  echo "OK: $old -> $new"
}

rename_one "air-condition" "air conditioning"
rename_one "bottie water" "bottle water"
rename_one "businessmanagement" "business management"
rename_one "butterfiies" "butterflies"
rename_one "cabie" "cable"
rename_one "ciothing sections" "clothing sections"
rename_one "compiaints" "complaints"
rename_one "compiete" "complete"
rename_one "compiex" "complex"
rename_one "compuisory" "compulsory"
rename_one "computerprogrammer" "computer programmer"
rename_one "contact detaiis" "contact details"
rename_one "desk iamp" "desk lamp"
rename_one "disable people" "disabled people"
rename_one "eniargement" "enlargement"
rename_one "entertainmentindustry" "entertainment industry"
rename_one "equai" "equal"
rename_one "famiiy" "family"
rename_one "fiashiight" "flashlight"
rename_one "fiavor" "flavor"
rename_one "fiute" "flute"
rename_one "flourishment" "flourishing"
rename_one "french styie" "french style"
rename_one "gioves" "gloves"
rename_one "graduai" "graduate"
rename_one "iand" "land"
rename_one "ianes" "lanes"
rename_one "iaptops" "laptops"
rename_one "iaw department" "law department"
rename_one "iegroom" "legroom"
rename_one "ieisure" "leisure"
rename_one "iength" "length"
rename_one "infiuence" "influence"
rename_one "informai" "informal"
rename_one "ioans" "loans"
rename_one "iookout point" "lookout point"
rename_one "iost" "lost"
rename_one "iungs" "lungs"
rename_one "journaiism" "journalism"
rename_one "knowiedge sharing" "knowledge sharing"
rename_one "laboratories report" "laboratory report"
rename_one "marine piants" "marine plants"
rename_one "modei" "model"
rename_one "moraiity" "morality"
rename_one "paining" "painting"
rename_one "painting ciass" "painting class"
rename_one "personai alarm" "personal alarm"
rename_one "personalinformation" "personal information"
rename_one "popuiar" "popular"
rename_one "practicai course" "practical course"
rename_one "presenting result" "presenting results"
rename_one "reaiism" "realism"
rename_one "reguiar" "regular"
rename_one "reieased" "released"
rename_one "ring abell" "ring a bell"
rename_one "seif-iocking" "self-locking"
rename_one "shaiiow" "shallow"
rename_one "steei" "steel"
rename_one "symboi" "symbol"
rename_one "tempie waiis" "temple walls"
rename_one "tities" "titles"
rename_one "transiation" "translation"
rename_one "window iocks" "window locks"

echo "完成。当前 mp3 数量: $(find . -maxdepth 1 -name '*.mp3' | wc -l)"
