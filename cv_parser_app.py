import os
import json
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from openai import OpenAI
from docstrange import DocumentExtractor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 

openai_client = None


OPENAI_API_KEY = None

def get_api_key_from_user():
    """Sigurno dobivanje API ključa od korisnika."""
    print("\n" + "="*60)
    print("🔑 KONFIGURACIJA OPENAI API KLJUČA")
    print("="*60)
    print("Za rad aplikacije potreban je OpenAI API ključ.")
    print("Možete ga dobiti na: https://platform.openai.com/api-keys")
    print("\n⚠️  VAŽNO: API ključ se neće spremiti u datoteku - sigurno je!")
    print("="*60)
    
    while True:
        api_key = input("\n🔑 Unesite svoj OpenAI API ključ: ").strip()
        
        if not api_key:
            print("❌ API ključ ne može biti prazan!")
            continue
            
        if not api_key.startswith('sk-'):
            print("❌ API ključ mora počinjati s 'sk-'")
            continue
            
        if len(api_key) < 20:
            print("❌ API ključ je prekratak!")
            continue
            
        # Testiraj ključ
        try:
            test_client = OpenAI(api_key=api_key)
            # Jednostavan test poziv
            test_client.models.list()
            print("✅ API ključ je valjan!")
            return api_key
        except Exception as e:
            print(f"❌ API ključ nije valjan: {str(e)}")
            retry = input("Želite li pokušati ponovno? (d/n): ").strip().lower()
            if retry not in ['d', 'da', 'y', 'yes']:
                return None

def initialize_openai():
    """Initialize OpenAI client with API key."""
    global openai_client, OPENAI_API_KEY
    
    # Prvo pokušaj iz varijable okruženja
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            openai_client = OpenAI(api_key=api_key)
            print("✅ OpenAI API konfiguriran iz varijable okruženja")
            return True
        except Exception as e:
            print(f"⚠️ Greška s API ključem iz okruženja: {e}")
    
    # Ako nema ključa u okruženju, traži od korisnika
    api_key = get_api_key_from_user()
    if api_key:
        try:
            openai_client = OpenAI(api_key=api_key)
            OPENAI_API_KEY = api_key
            # Postavi kao environment varijablu za ovu sesiju
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ OpenAI API konfiguriran iz korisničkog unosa")
            return True
        except Exception as e:
            print(f"❌ Greška pri inicijalizaciji OpenAI klijenta: {e}")
            return False
    
    return False

def extract_cv_data(file_path: str) -> Dict[str, Any]:
    try:
        # Use cloud mode for best quality
        extractor = DocumentExtractor()
        result = extractor.extract(file_path)
        
        # Extract as structured JSON
        json_data = result.extract_data()
        
        return {
            'success': True,
            'raw_data': json_data,
            'markdown': result.extract_markdown(),
            'text': result.extract_text()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_cv_with_openai(raw_data: Dict[str, Any], position_type: str = "general") -> str:
    if not openai_client:
        return "OpenAI API ključ nije konfiguriran"
    
    # Position-specific instructions
    position_instructions = {
        "tech": "Fokusiraj se na tehničke vještine, programiranje, tehnologije, projekte i inovacije. Ocijeni njegovu sposobnost rješavanja problema i prilagođavanja novim tehnologijama. BUDI STROŽI - nedostaci u tehničkim vještinama su kritični.",
        "management": "Naglasak na vođenje timova, strateško razmišljanje, rezultate, komunikacijske vještine i sposobnost donošenja odluka. Ocijeni njegovu sposobnost upravljanja ljudima i projektima. BUDI STROŽI - loše vođenje timova je neprihvatljivo.",
        "sales": "Fokusiraj se na prodajne rezultate, komunikacijske vještine, izgradnju odnosa s klijentima, postizanje ciljeva i prodajne tehnike. BUDI STROŽI - nedostaci u prodajnim rezultatima su kritični.",
        "marketing": "Naglasak na kreativnost, analitičke vještine, poznavanje digitalnih platformi, kampanje, brand management i rezultate marketinga. BUDI STROŽI - nedostaci u kreativnosti ili analizi su problematični.",
        "finance": "Fokusiraj se na financijske vještine, analizu, računovodstvo, risk management, compliance i numeričke sposobnosti. BUDI STROŽI - greške u financijama su neprihvatljive.",
        "hr": "Naglasak na ljudske vještine, komunikaciju, rješavanje konflikata, organizacijske vještine i razumijevanje ljudskih resursa. BUDI STROŽI - nedostaci u komunikaciji su kritični.",
        "design": "Fokusiraj se na kreativnost, dizajnerske vještine, portfolio, estetiku, inovacije i vizualne sposobnosti. BUDI STROŽI - nedostaci u kreativnosti su problematični.",
        "general": "Općenita procjena kandidata s naglaskom na ključne kvalifikacije, iskustvo i potencijal za različite pozicije. BUDI STROŽI - nedostaci u osnovnim vještinama su kritični."
    }
    
    position_focus = position_instructions.get(position_type, position_instructions["general"])
    
    prompt = f"""
Ti si STROGI i iskusan Hiring Manager s 10+ godina iskustva u regrutaciji i procjeni kandidata.
Dobit ćeš JSON s podacima iz životopisa kandidata.

VAŽNO: BUDI STROŽI I KRITIČAN - ne budi samo pozitivan!

Tvoj zadatak:
- Formatiraj podatke kao uredan **Markdown dokument**.
- Uključi sekcije:
  - # Ime Prezime
  - ## Kontakt
  - ## Sažetak (150 riječi) - NAPRAVI STROGI OSVRT KAO HIRING MANAGER
  - ## Radno iskustvo
  - ## Obrazovanje
  - ## Vještine

VAŽNO za sekciju "Sažetak":
- Ponašaj se kao STROGI Hiring Manager koji procjenjuje kandidata
- Napiši detaljni, profesionalni osvrt o kandidatu (150 riječi)
- Uključi: ključne kvalifikacije, iskustvo, vještine, potencijal
- Koristi profesionalni ton kao da pišeš za kolege u HR-u
- BUDI STROŽI - spomeni i nedostatke ako ih ima
- Budi objektivan i kritičan, ne samo pozitivan
- NA KRAJU MORAŠ NAPISATI: "PREPORUČUJEM/NEPREPORUČUJEM kandidata za poziciju"

SPECIJALNE INSTRUKCIJE ZA TIP POZICIJE ({position_type.upper()}):
{position_focus}

Primjer sažetka:
"Kandidat s 5+ godina iskustva u razvoju web aplikacija, specijaliziran za Python i React. Dokazao sposobnost vođenja timova i implementacije složenih projekata. Izvrsne komunikacijske vještine i sposobnost rada u multikulturalnom okruženju. Međutim, nedostaje mu iskustvo s cloud tehnologijama i DevOps praksama koje su ključne za moderni razvoj. Iako ima solidne tehničke vještine, potrebno je dodatno obučavanje za napredne koncepte. PREPORUČUJEM kandidata za poziciju Senior Developer-a s uvjetom dodatnog obučavanja."

DODATNE INSTRUKCIJE:
- BUDI STROŽI I KRITIČAN - ne budi samo pozitivan
- Ako kandidat ima nedostatke, spomeni ih jasno i objektivno
- Naglasi jedinstvene kvalitete kandidata
- Ocijeni njegovu prikladnost za različite tipove pozicija
- Koristi profesionalni HR terminologiju
- NA KRAJU UVJEK NAPIŠI: "PREPORUČUJEM" ili "NEPREPORUČUJEM" kandidata
- Objasni zašto preporučuješ ili ne preporučuješ kandidata
- Ako ima nedostatke, spomeni ih jasno i objasni zašto su problematični
- BUDI STROŽI - nedostaci u ključnim vještinama mogu biti razlog za NEPREPORUČUJEM

Vrati ISKLJUČIVO Markdown, bez koda ili dodatnih objašnjenja.
"""
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Ulazni JSON:\n{json.dumps(raw_data, indent=2, ensure_ascii=False)}"}
            ],
            temperature=0.1,  # Vrlo niska temperatura za strože rezultate
            max_tokens=2000,   # Više tokena za detaljniji profil
            top_p=0.8         # Fokusiraniji i stroži odgovor
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Greška pri obradi s OpenAI: {str(e)}"

@app.route('/')
def index():
    """Main page."""
    return render_template('cv_parser.html')

@app.route('/api/upload-cv', methods=['POST'])
def upload_cv():
    """Upload and process CV."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'Nema datoteke'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nema odabrane datoteke'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Get position type from form data
            position_type = request.form.get('position_type', 'general')
            
            # Extract data with DocStrange
            extraction_result = extract_cv_data(tmp_path)
            
            if not extraction_result['success']:
                return jsonify({'error': f'Greška pri izvlačenju: {extraction_result["error"]}'}), 500
            
            # Process with OpenAI if available
            processed_markdown = ""
            if openai_client:
                processed_markdown = process_cv_with_openai(extraction_result['raw_data'], position_type)
            else:
                processed_markdown = extraction_result['markdown']
            
            return jsonify({
                'success': True,
                'raw_data': extraction_result['raw_data'],
                'processed_markdown': processed_markdown,
                'original_markdown': extraction_result['markdown'],
                'text': extraction_result['text'],
                'file_name': file.filename
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        return jsonify({'error': f'Nepredviđena greška: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    openai_status = "konfiguriran" if openai_client else "nije konfiguriran"
    return jsonify({
        'status': 'zdrav',
        'openai_status': openai_status,
        'docstrange_status': 'dostupan'
    })

if __name__ == '__main__':
    print("🚀 Pokretanje CV Parser aplikacije...")
    print("📝 Napravio: Matej Jurić | Godina: 2025")
    print("="*60)
    
    # Initialize OpenAI
    if initialize_openai():
        print("\n🎉 Aplikacija je spremna!")
        print("📝 Otvorite http://localhost:5000 u pregledniku")
        print("="*60)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("\n❌ Aplikacija se ne može pokrenuti bez valjanog OpenAI API ključa!")
        print("💡 Možete postaviti OPENAI_API_KEY varijablu okruženja ili pokrenuti aplikaciju ponovno.")
        input("\nPritisnite Enter za izlaz...")
