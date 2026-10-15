import streamlit as st
from PIL import Image, ImageDraw
import pytesseract
import re
import io

st.set_page_config(page_title="Ordflätelösaren", page_icon="🔎", layout="wide")
st.title("🔎 Ordflätelösaren")
st.write("Ladda upp en bild med ett bokstavsrutnät. Programmet läser bokstäverna, hittar orden och markerar dem i bilden.")

with st.sidebar:
    st.header("Rutnät")
    rows = st.number_input("Antal rader", min_value=1, max_value=40, value=10)
    cols = st.number_input("Antal kolumner", min_value=1, max_value=40, value=10)

uploaded = st.file_uploader("Ladda upp pusselbild", type=["png", "jpg", "jpeg", "webp"])
default_words = """GUSTAV
VASATIDEN
VASA
STATSKYRKA
ÄRKEBISKOP
PÅVE
PROTESTANT
KATOLIK
REFORMERA
KLOSTER"""
words_text = st.text_area("Ord att hitta (ett ord per rad)", value=default_words, height=210)

def normalize(s):
    return re.sub(r"[^A-ZÅÄÖ]", "", s.upper())

def crop_grid(image, rcount, ccount):
    # Standardlayout: rutnätet upptar den vänstra delen av bilden.
    w, h = image.size
    grid_img = image.crop((0, 0, int(w * 0.68), h))
    gw, gh = grid_img.size
    cells = []
    for r in range(rcount):
        row = []
        for c in range(ccount):
            x0, x1 = int(c * gw / ccount), int((c + 1) * gw / ccount)
            y0, y1 = int(r * gh / rcount), int((r + 1) * gh / rcount)
            cell = grid_img.crop((x0, y0, x1, y1))
            cw, ch = cell.size
            cell = cell.crop((int(cw * .12), int(ch * .08), int(cw * .88), int(ch * .82)))
            row.append(cell)
        cells.append(row)
    return grid_img, cells

def ocr_cell(cell):
    cell = cell.convert("L").resize((cell.width * 5, cell.height * 5))
    cell = cell.point(lambda p: 255 if p > 130 else 0)
    text = pytesseract.image_to_string(
        cell,
        config="--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    )
    text = normalize(text)
    return text[0] if text else ""

def find_word(grid, word):
    R, C = len(grid), len(grid[0])
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    def dfs(r, c, i, path, used):
        if grid[r][c] != word[i]:
            return None
        path = path + [(r, c)]
        used = used | {(r, c)}
        if i == len(word) - 1:
            return path
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in used:
                found = dfs(nr, nc, i + 1, path, used)
                if found:
                    return found
        return None

    if not word or not grid or not grid[0]:
        return None
    for r in range(R):
        for c in range(C):
            found = dfs(r, c, 0, [], set())
            if found:
                return found
    return None

if uploaded:
    original = Image.open(uploaded).convert("RGB")
    grid_img, cells = crop_grid(original, int(rows), int(cols))
    st.subheader("1. Kontrollera OCR-resultatet")
    try:
        initial_grid = [[ocr_cell(cell) for cell in row] for row in cells]
    except Exception as exc:
        st.error(f"Kunde inte köra OCR: {exc}")
        initial_grid = [["" for _ in range(int(cols))] for _ in range(int(rows))]

    initial_text = "\n".join(" ".join(ch if ch else "?" for ch in row) for row in initial_grid)
    grid_text = st.text_area(
        "Rutnät — en rad per rad, bokstäver separerade med mellanslag",
        value=initial_text,
        height=min(350, int(rows) * 30 + 40)
    )
    parsed = []
    for line in grid_text.splitlines():
        vals = [normalize(x)[:1] for x in line.split()]
        if vals:
            parsed.append(vals)

    if len(parsed) != int(rows) or any(len(row) != int(cols) for row in parsed):
        st.warning(f"Rutnätet måste ha exakt {int(rows)} rader och {int(cols)} kolumner. Skriv ett mellanslag mellan varje bokstav.")
    else:
        words = [normalize(w) for w in words_text.splitlines() if normalize(w)]
        if st.button("Hitta och markera ord", type="primary"):
            results = {word: find_word(parsed, word) for word in words}
            found_count = sum(path is not None for path in results.values())
            st.subheader("2. Resultat")
            st.write(f"Hittade **{found_count} av {len(words)} ord**.")
            for word, path in results.items():
                if path:
                    coords = " → ".join(f"({r+1},{c+1})" for r, c in path)
                    st.success(f"{word}: {coords}")
                else:
                    st.error(f"{word}: hittades inte. Kontrollera bokstäverna och reglerna.")

            marked = grid_img.copy()
            draw = ImageDraw.Draw(marked, "RGBA")
            gw, gh = marked.size
            palette = [
                (255,65,65,105), (40,130,255,105), (40,190,100,105),
                (255,165,0,115), (170,80,220,105), (0,190,190,105),
                (245,80,160,105), (150,150,30,110), (80,90,210,105),
                (210,110,60,105)
            ]
            for idx, (word, path) in enumerate(results.items()):
                if not path:
                    continue
                color = palette[idx % len(palette)]
                for r, c in path:
                    x0, x1 = c * gw / cols, (c + 1) * gw / cols
                    y0, y1 = r * gh / rows, (r + 1) * gh / rows
                    draw.rounded_rectangle(
                        (x0 + 2, y0 + 2, x1 - 2, y1 - 2),
                        radius=7, fill=color,
                        outline=(color[0], color[1], color[2], 255), width=3
                    )
            st.image(marked, caption="Varje ord har en egen färg", use_container_width=True)
            buf = io.BytesIO()
            marked.save(buf, format="PNG")
            st.download_button(
                "Ladda ner markerad bild",
                data=buf.getvalue(),
                file_name="ordflata_losning.png",
                mime="image/png"
            )
else:
    st.info("Ladda upp en pusselbild för att börja.")
    st.markdown(
        "**Så fungerar det:** OCR läser bokstäverna i rutorna. En sökalgoritm provar intilliggande rutor "
        "i åtta riktningar, inklusive diagonaler och svängar. Du kan rätta OCR-resultatet innan sökningen."
    )
