# Ordflätelösaren – GitHub Codespaces

En Streamlit-app som läser ett bokstavsrutnät från en bild, låter dig rätta OCR-resultatet, söker efter ord och markerar dem i en bild.

## Starta i GitHub Codespaces

1. Skapa ett nytt GitHub-repository, till exempel `ordflata-losare`.
2. Ladda upp alla filer och mappar från det här projektet till repositoryts rot. Se till att `.devcontainer/devcontainer.json` följer med.
3. På GitHub, öppna repositoryt och välj **Code → Codespaces → Create codespace on main**.
4. Codespaces bygger miljön och installerar Python-paketen samt Tesseract OCR.
5. Appen startar automatiskt. När Codespaces frågar om port `8501`, öppna den i webbläsaren. Vanligtvis öppnas fliken automatiskt.

## Om appen inte startar automatiskt

Öppna terminalen i Codespaces och kör:

```bash
python -m pip install --user -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Använd fliken **Ports** i VS Code och öppna port `8501`.

## Användning

1. Ladda upp en PNG-, JPG- eller WEBP-bild.
2. Välj antal rader och kolumner.
3. Kontrollera och vid behov rätta bokstäverna som OCR läst av.
4. Skriv orden ett per rad.
5. Klicka **Hitta och markera ord**.
6. Ladda ner resultatbilden.

## Begränsningar

- Standardinställningen är 10 × 10 rutor.
- OCR-beskärningen antar att rutnätet upptar cirka 68 % av bildens bredd till vänster. Om layouten är annorlunda kan du behöva beskära bilden före uppladdning eller justera `crop_grid()` i `app.py`.
- Ord får gå i åtta riktningar och svänga. En ruta får inte användas två gånger inom samma ord.
- OCR kan göra misstag; kontrollera alltid rutnätet innan du söker.
