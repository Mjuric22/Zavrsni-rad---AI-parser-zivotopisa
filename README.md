# CV Parser - Pametni CV Parser i Generator Profila Kandidata

**Napravio: Matej Jurić**  
**Godina: 2025**

## 🚀 Opis

CV Parser je pametna aplikacija koja kombinira DocStrange (OCR) s OpenAI GPT-4o-mini za automatsku analizu i strukturiranje životopisa. Aplikacija izvlači podatke iz CV-ova, obrađuje ih pomoću AI-a i generira profesionalne profile kandidata s Hiring Manager perspektivom.

## 📁 Struktura projekta

```
docstrange-main/
├── cv_parser_app.py          # Glavna Flask aplikacija
├── templates/
│   └── cv_parser.html        # HTML template
├── static/
│   ├── cv_styles.css         # CSS stilovi
│   └── cv_script.js          # JavaScript funkcionalnost
├── docstrange/               # DocStrange biblioteka za OCR
├── cv_requirements.txt       # Python dependencies
├── CV_PARSER_README.md       # Detaljna dokumentacija
└── README.md                 # Ovaj fajl
```

## 🏃‍♂️ Brzo pokretanje

1. **Instaliraj dependencies:**
```bash
   pip install -r cv_requirements.txt
```

2. **Pokreni aplikaciju:**
```bash
   python cv_parser_app.py
   ```

3. **Unesi OpenAI API ključ** kad te aplikacija pita

4. **Otvori** http://localhost:5000 u pregledniku

## 🔑 Sigurnost

- **Nema hardcodiranih API ključeva** u kodu
- **Sigurno za GitHub** - API ključ se unosi pri pokretanju
- **Neće se spremiti** u datoteku

## 📖 Detaljna dokumentacija

Za potpunu dokumentaciju, pogledajte [CV_PARSER_README.md](CV_PARSER_README.md)

## 🎯 Funkcionalnosti

- **📄 OCR obrada**: PDF, DOCX, slike
- **🤖 AI analiza**: OpenAI GPT-4o-mini
- **👔 Hiring Manager perspektiva**: Stroga procjena kandidata
- **📋 Strukturirani profil**: Ime, kontakt, sažetak, iskustvo, obrazovanje, vještine
- **🎯 Pozicijski fokus**: Prilagođena procjena za različite tipove pozicija
- **📊 Preporuka**: Jasna preporuka (PREPORUČUJEM/NEPREPORUČUJEM)
- **💾 Izvoz**: HTML format za preuzimanje
- **🌐 Web sučelje**: Moderno i intuitivno korisničko sučelje

---

**Napravio: Matej Jurić | 2025**
