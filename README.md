# Ordflätelösaren

En liten lokal webbapp som:
- tar emot en pusselbild,
- försöker läsa bokstäverna med OCR,
- låter dig rätta OCR-resultatet,
- söker efter orden med svängar och diagonaler,
- markerar hittade ord i en bild som kan laddas ned.

## Installera

Kräver Python 3.10 eller senare och Tesseract OCR.

### 1. Installera Tesseract OCR

- **Windows:** installera Tesseract OCR från dess officiella installationspaket och se till att `tesseract.exe` finns i PATH.
- **macOS:** `brew install tesseract`
- **Ubuntu/Debian:** `sudo apt install tesseract-ocr`

Om Tesseract inte känner igen svenska bokstäver med standardinställningarna kan du även installera svenska språkdata. Appen begränsar dock OCR till latinska versaler inklusive ÅÄÖ.

### 2. Installera Python-paketen

Öppna en terminal i mappen och kör:

```bash
python -m pip install -r requirements.txt
```

### 3. Starta appen

```bash
streamlit run app.py
```

Appen öppnas i webbläsaren. Ladda upp bilden, kontrollera bokstäverna som OCR läst av och klicka på **Hitta och markera ord**.

## Antaganden och begränsningar

- Standardinställningen är 10 rader × 10 kolumner.
- Appen utgår från att bokstäver får angränsa i åtta riktningar, även diagonalt.
- Varje ruta får användas högst en gång i samma ord.
- Den första versionen antar att rutnätet ligger i bildens vänstra 68 %. Om layouten skiljer sig mycket från det, beskära bilden först så att rutnätet ligger till vänster, eller ändra `crop_grid()` i `app.py`.
- OCR är inte felfri. Granska alltid rutnätet i redigeringsrutan innan sökningen.
- För svåra pussel med många möjliga vägar kan sökningen ta längre tid; den här versionen är avsedd för vanliga ordflätor.
