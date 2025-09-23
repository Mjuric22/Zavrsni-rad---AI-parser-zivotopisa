# CV Parser - Pametni CV Parser i Generator

Pametna aplikacija koja spaja **DocStrange** (OCR) + **OpenAI** (LLM) + **Web interfejs** za obradu CV-ova i generiranje strukturiranih profila kandidata.

## 🚀 Funkcionalnosti

- **📄 OCR obrada**: Izvlači podatke iz PDF, DOCX, slika pomoću DocStrange
- **🤖 AI obrada**: Koristi OpenAI GPT-4o-mini za strukturiranje podataka
- **🎨 Web interfejs**: Drag-and-drop upload, pregled rezultata
- **📥 Export**: Preuzimanje u Markdown, HTML formatima
- **📋 Strukturirani profil**: Ime, kontakt, sažetak, iskustvo, obrazovanje, vještine

## 📋 Potrebni paketi

```bash
pip install -r cv_requirements.txt
```

## 🔑 Konfiguracija

### OpenAI API ključ

**SIGURNO - Nema hardcodiranih ključeva u kodu!**

Aplikacija će vas sigurno pitati za API ključ pri pokretanju:

1. **Automatski unos** - Aplikacija će vas pitati za ključ pri pokretanju
2. **Environment varijabla** (opcionalno):
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

**✅ Sigurno za GitHub** - API ključ se neće spremiti u datoteku!

## 🏃‍♂️ Pokretanje

```bash
python cv_parser_app.py
```

**Prvi put:**
1. Aplikacija će vas pitati za OpenAI API ključ
2. Unesite svoj ključ (počinje s `sk-`)
3. Aplikacija će testirati ključ
4. Ako je valjan, aplikacija će se pokrenuti

**Sljedeći puti:**
- Ako imate `OPENAI_API_KEY` varijablu okruženja, aplikacija će je koristiti
- Inače će vas ponovno pitati za ključ

Aplikacija će se pokrenuti na: **http://localhost:5000**

## 📖 Kako koristiti

1. **Upload CV**: Povucite CV datoteku ili kliknite za odabir
2. **Obrađi CV**: Kliknite "Obrađi CV" dugme
3. **Pregledaj rezultate**: 
   - **Obrađeni profil**: Strukturirani Markdown profil
   - **Izvorni podaci**: Raw JSON podaci
   - **Originalni tekst**: Izvorni tekst iz dokumenta
4. **Export**: Preuzmite u Markdown ili HTML formatu

## 🎯 Podržani formati

- **PDF**: .pdf
- **Word**: .docx, .doc
- **Slike**: .png, .jpg, .jpeg, .tiff, .bmp

## 🔧 API endpoints

- `POST /api/upload-cv` - Upload i obrada CV-a
- `GET /api/health` - Status aplikacije

## 📝 Primjer prompta za OpenAI

```
Ti si asistent za kreiranje kandidatskih profila.
Dobit ćeš JSON s podacima iz životopisa.

Tvoj zadatak:
- Formatiraj ih kao uredan **Markdown dokument**.
- Uključi sekcije:
  - # Ime Prezime
  - ## Kontakt
  - ## Sažetak (150 riječi)
  - ## Radno iskustvo
  - ## Obrazovanje
  - ## Vještine

Vrati ISKLJUČIVO Markdown, bez koda ili dodatnih objašnjenja.
```

## 🎨 Izgled rezultata

```markdown
# Ivan Horvat

## Kontakt
- 📍 Zagreb
- 📧 ivan@mail.com
- 📱 +38591111222

## Sažetak
Ivan je softver inženjer s 5 godina iskustva u razvoju web aplikacija...

## Radno iskustvo
- **Software Developer**, ACME d.o.o. (01/2019 – 06/2021)

## Obrazovanje
- mag. inf., FOI Varaždin (2014 – 2018)

## Vještine
Python · SQL · Machine Learning
```

## 🛠️ Tehnologije

- **Backend**: Python, Flask
- **OCR**: DocStrange (Cloud mode)
- **AI**: OpenAI GPT-4o-mini
- **Frontend**: HTML, CSS, JavaScript
- **Export**: Markdown, HTML

## 📁 Struktura fajlova

```
cv_parser_app.py          # Glavna aplikacija
templates/
  cv_parser.html          # HTML template
static/
  cv_styles.css           # CSS stilovi
  cv_script.js            # JavaScript funkcionalnost
cv_requirements.txt       # Python dependencies
CV_PARSER_README.md       # Dokumentacija
```

## 🚨 Napomene

- **OpenAI API**: Potreban je valjan API ključ (unosi se sigurno pri pokretanju)
- **Sigurnost**: API ključ se neće spremiti u datoteku - sigurno za GitHub!
- **DocStrange**: Koristi Cloud mode za najbolji kvalitet
- **Veličina datoteke**: Maksimalno 50MB
- **Internet**: Potreban za DocStrange Cloud i OpenAI API

## 🔄 Workflow

1. **Upload** → CV datoteka
2. **DocStrange** → OCR + izvlačenje podataka
3. **OpenAI** → Strukturiranje i formatiranje
4. **Web UI** → Pregled i export rezultata

## 💡 Moguća poboljšanja

- [ ] PDF export funkcionalnost
- [ ] Batch obrada više CV-ova
- [ ] Custom prompti za različite tipove dokumenata
- [ ] Integracija s drugim LLM-ovima
- [ ] Database za čuvanje rezultata
- [ ] User authentication
- [ ] API rate limiting
