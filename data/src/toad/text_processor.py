import sys
import re
from unicodedata import normalize

sys.path.append("/content/src/glow-tts")
from text import symbols as glowtts_symbols

sys.path.remove("/content/src/glow-tts")

sys.path.append("/content/src/g2pK")
import g2pk

sys.path.remove("/content/src/g2pK")

symbols = set(glowtts_symbols)

g2p = g2pk.G2p()


def normalize_text(text):
    text = simple_replace(text)
    text = g2p.idioms(text)
    text = g2pk.english.convert_eng(text, g2p.cmu)
    text = g2pk.utils.annotate(text, g2p.mecab)
    text = g2pk.numerals.convert_num(text)
    text = re.sub("/[PJEB]", "", text)
    text = eng_cap(text)

    text = normalize("NFD", text)
    for pos, char in enumerate(text):
        if char not in symbols:
            text = text[:pos] + " " + text[pos + 1 :]
    text = normalize("NFC", text)
    return text


def split_text(text):
    texts = []
    pi = 0
    for ci in range(len(text)):
        if text[ci] in ",;:":
            # replace character to dot
            text = text[:ci] + "." + text[ci + 1 :]
            continue
        if text[ci] in ".!?\n":
            texts.append(text[pi : ci + 1])
            pi = ci + 1
    texts.append(text[pi:])
    return texts


def eng_cap(text):
    text = re.sub(r"(a|A)", "에이", text)
    text = re.sub(r"(b|B)", "비", text)
    text = re.sub(r"(c|C)", "씨", text)
    text = re.sub(r"(d|D)", "디", text)
    text = re.sub(r"(e|E)", "이", text)
    text = re.sub(r"(f|F)", "에프", text)
    text = re.sub(r"(g|G)", "쥐", text)
    text = re.sub(r"(h|H)", "에이치", text)
    text = re.sub(r"(i|I)", "아이", text)
    text = re.sub(r"(j|J)", "제이", text)
    text = re.sub(r"(k|K)", "케이", text)
    text = re.sub(r"(l|L)", "엘", text)
    text = re.sub(r"(m|M)", "엠", text)
    text = re.sub(r"(n|N)", "엔", text)
    text = re.sub(r"(o|O)", "오", text)
    text = re.sub(r"(p|P)", "피", text)
    text = re.sub(r"(q|Q)", "큐", text)
    text = re.sub(r"(r|R)", "알", text)
    text = re.sub(r"(s|S)", "에스", text)
    text = re.sub(r"(t|T)", "티", text)
    text = re.sub(r"(u|U)", "유", text)
    text = re.sub(r"(v|V)", "브이", text)
    text = re.sub(r"(w|W)", "더블유", text)
    text = re.sub(r"(x|X)", "엑스", text)
    text = re.sub(r"(y|Y)", "와이", text)
    text = re.sub(r"(z|Z)", "지", text)

    return text


def simple_replace(text):
    # 중복된 문장 부호는 마지막 문장부호로 변경
    text = re.sub(r"[.?!]+\?", "?", text)
    text = re.sub(r"[.?!]+!", "!", text)
    text = re.sub(r"[.?!]+\.", "books", text)

    # 기본 자모음
    text = re.sub(r"ㄱ", "기역", text)
    text = re.sub(r"ㄴ", "니은", text)
    text = re.sub(r"ㄷ", "디귿", text)
    text = re.sub(r"ㄹ", "리을", text)
    text = re.sub(r"ㅁ", "미음", text)
    text = re.sub(r"ㅂ", "비읍", text)
    text = re.sub(r"ㅅ", "시옷", text)
    text = re.sub(r"ㅇ", "이응", text)
    text = re.sub(r"ㅈ", "지읒", text)
    text = re.sub(r"ㅊ", "치읓", text)
    text = re.sub(r"ㅋ", "키읔", text)
    text = re.sub(r"ㅌ", "티읕", text)
    text = re.sub(r"ㅍ", "피읖", text)
    text = re.sub(r"ㅎ", "히읗", text)
    text = re.sub(r"ㄲ", "쌍기역", text)
    text = re.sub(r"ㄸ", "쌍디귿", text)
    text = re.sub(r"ㅃ", "쌍비읍", text)
    text = re.sub(r"ㅆ", "쌍시옷", text)
    text = re.sub(r"ㅉ", "쌍지읒", text)
    text = re.sub(r"ㄳ", "기역시옷", text)
    text = re.sub(r"ㄵ", "니은지읒", text)
    text = re.sub(r"ㄶ", "니은히읗", text)
    text = re.sub(r"ㄺ", "리을기역", text)
    text = re.sub(r"ㄻ", "리을미음", text)
    text = re.sub(r"ㄼ", "리을비읍", text)
    text = re.sub(r"ㄽ", "리을시옷", text)
    text = re.sub(r"ㄾ", "리을티읕", text)
    text = re.sub(r"ㄿ", "리을피읍", text)
    text = re.sub(r"ㅀ", "리을히읗", text)
    text = re.sub(r"ㅄ", "비읍시옷", text)
    text = re.sub(r"ㅏ", "아", text)
    text = re.sub(r"ㅑ", "야", text)
    text = re.sub(r"ㅓ", "어", text)
    text = re.sub(r"ㅕ", "여", text)
    text = re.sub(r"ㅗ", "오", text)
    text = re.sub(r"ㅛ", "요", text)
    text = re.sub(r"ㅜ", "우", text)
    text = re.sub(r"ㅠ", "유", text)
    text = re.sub(r"ㅡ", "으", text)
    text = re.sub(r"ㅣ", "이", text)
    text = re.sub(r"ㅐ", "애", text)
    text = re.sub(r"ㅒ", "얘", text)
    text = re.sub(r"ㅔ", "에", text)
    text = re.sub(r"ㅖ", "예", text)
    text = re.sub(r"ㅘ", "와", text)
    text = re.sub(r"ㅙ", "왜", text)
    text = re.sub(r"ㅚ", "외", text)
    text = re.sub(r"ㅝ", "워", text)
    text = re.sub(r"ㅞ", "웨", text)
    text = re.sub(r"ㅟ", "위", text)
    text = re.sub(r"ㅢ", "의", text)

    return text


def process_text(text):
    texts = split_text(text)
    results = []
    for text in texts:
        text = simple_replace(text.strip())
        text = normalize_text(text)
        if text:
            results.append(text)
    return results
