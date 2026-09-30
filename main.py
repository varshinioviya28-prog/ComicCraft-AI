from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uuid, html

BASE = Path(__file__).resolve().parent.parent
STATIC = BASE/'static'; TEMPLATES = BASE/'templates'; GENERATED = BASE/'data'/'generated'
GENERATED.mkdir(parents=True, exist_ok=True)
app = FastAPI(title='ComicCraft - AI Comic Story Creator', version='1.0.0')
app.mount('/static', StaticFiles(directory=STATIC), name='static')
app.mount('/generated', StaticFiles(directory=GENERATED), name='generated')
templates=Jinja2Templates(directory=str(TEMPLATES))

class ComicRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str='Forest'
    tone: str='Light-hearted'
    art_style: str='Comic Book'

def panel_svg(title, name, setting, style, n, scene, caption, narration):
    palettes={'Forest':('#dff3e4','#8bc6a7','#234f3d'),'School':('#e8f0ff','#9bb6e8','#233a68'),'Space':('#101735','#493a8c','#f4f2ff'),'City':('#f4e7da','#c99770','#4a3023')}
    bg,accent,ink=palettes.get(setting,palettes['Forest'])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560"><defs><linearGradient id="g{n}" x1="0" x2="0" y1="0" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{accent}"/></linearGradient></defs><rect width="900" height="560" rx="18" fill="url(#g{n})"/><circle cx="760" cy="105" r="58" fill="#fff" opacity=".65"/><g fill="{ink}" opacity=".82"><path d="M80 430 Q130 200 180 430Z"/><path d="M180 440 Q235 150 290 440Z"/><path d="M650 440 Q710 170 770 440Z"/></g><g transform="translate(395 255)"><ellipse cx="0" cy="95" rx="75" ry="105" fill="#f07835"/><circle cx="0" cy="0" r="72" fill="#f28a42"/><path d="M-58-40 L-48-112 L-5-70 L45-112 L58-38Z" fill="#e7682e"/><circle cx="-24" cy="-3" r="8" fill="#222"/><circle cx="24" cy="-3" r="8" fill="#222"/><path d="M-18 25 Q0 42 18 25" fill="none" stroke="#222" stroke-width="7" stroke-linecap="round"/><path d="M70 70 Q150 10 120 130 Q100 155 70 118" fill="#e96e31"/></g><rect x="26" y="25" width="400" height="70" rx="14" fill="white" opacity=".92"/><text x="48" y="58" font-family="Arial" font-size="23" font-weight="700" fill="{ink}">Panel {n}: {html.escape(title[:30])}</text><text x="48" y="82" font-family="Arial" font-size="14" fill="{ink}">{html.escape(name[:20])} • {html.escape(setting)} • {html.escape(style)}</text><rect x="40" y="470" width="820" height="62" rx="12" fill="white" opacity=".92"/><text x="58" y="495" font-family="Arial" font-size="15" font-style="italic" fill="#333">{html.escape(caption[:105])}</text><text x="58" y="518" font-family="Arial" font-size="13" fill="#555">{html.escape(narration[:140])}</text></svg>'''

def generate(req):
    prompt=req.story_prompt.strip() or 'A small adventure'; name=req.character_name.strip() or 'Alex'
    scenes={
      'Forest':[('The Forest Edge',f'{name} discovers a mysterious path at the edge of the forest.'),('Into the Deep Woods',f'{name} follows a glowing trail and hears a friendly voice between the trees.'),('The Hidden Secret',f'{name} reaches a quiet clearing and finds the source of the strange light.'),('A New Beginning',f'{name} returns home carrying a small reminder of the adventure.')],
      'School':[('A Strange Morning',f'{name} notices something unusual in the school hallway.'),('The Mystery',f'{name} and a friend search the classroom for clues.'),('The Big Reveal',f'The mystery turns into a fun surprise for everyone.'),('Best Day Ever',f'{name} leaves school smiling after the unexpected adventure.')],
      'Space':[('Mission Start',f'{name} launches into space on a tiny exploration ship.'),('Unknown Signal',f'A mysterious signal appears beyond the nearest planet.'),('The Discovery',f'{name} finds a friendly floating world hidden in the stars.'),('Homeward',f'{name} heads home with a story nobody will forget.')],
      'City':[('The City Trail',f'{name} spots a mysterious clue in a busy city street.'),('Chasing Clues',f'{name} follows clues through shops, parks and bright streets.'),('The Secret',f'The final clue reveals a surprising friend waiting nearby.'),('New Adventure',f'{name} heads home already planning the next adventure.')]
    }.get(req.setting,[])
    panels=[]
    captions=['Wind moves softly through the scene.','A curious sound breaks the silence.','Everything feels possible for a moment.','The adventure ends, but the story continues.']
    for i,(title,scene) in enumerate(scenes,1):
        cap=captions[i-1]; narration=f'{scene} Tone: {req.tone}. Story idea: {prompt[:70]}.'
        fn=f'{uuid.uuid4().hex}.svg'; (GENERATED/fn).write_text(panel_svg(title,name,req.setting,req.art_style,i,scene,cap,narration),encoding='utf-8')
        panels.append({'panel':i,'title':title,'scene':scene,'caption':cap,'narration':narration,'image_url':f'/generated/{fn}','image_prompt':f'{req.art_style} illustration of {name} in {req.setting}: {scene}'})
    return {'title':'Your Comic Preview','character':name,'setting':req.setting,'tone':req.tone,'art_style':req.art_style,'story_prompt':prompt,'panels':panels}

@app.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse('index.html',{'request':request})
@app.post('/generate',response_class=HTMLResponse)
def generate_page(request:Request,story_prompt:str=Form(...),character_name:str=Form(...),setting:str=Form('Forest'),tone:str=Form('Light-hearted'),art_style:str=Form('Comic Book')):
    comic=generate(ComicRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style)); return templates.TemplateResponse('preview.html',{'request':request,'comic':comic})
@app.post('/generate-comic/json')
def generate_json(req:ComicRequest): return generate(req)
@app.get('/test-image')
def test_image():
    p=GENERATED/'test-image.svg'; p.write_text(panel_svg('Test Image','ComicCraft','Forest','Comic Book',1,'Local image generation works.','The image endpoint is working.','No external image service is required.'),encoding='utf-8'); return FileResponse(p,media_type='image/svg+xml')
@app.get('/export-success',response_class=HTMLResponse)
def success(request:Request): return templates.TemplateResponse('success.html',{'request':request})
@app.get('/health')
def health(): return {'status':'ok','project':'ComicCraft','version':'1.0.0'}
@app.post('/download-pdf')
def download_pdf(req:ComicRequest):
    try:
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from svglib.svglib import svg2rlg
    except ImportError: return JSONResponse({'error':'Install requirements first.'},status_code=500)
    comic=generate(req); out=GENERATED/f'comiccraft_{uuid.uuid4().hex[:8]}.pdf'; styles=getSampleStyleSheet(); story=[Paragraph('ComicCraft — AI Comic Story',styles['Title']),Spacer(1,12)]
    for p in comic['panels']:
        story += [Paragraph(f"Panel {p['panel']}: {p['title']}",styles['Heading2']),Paragraph(p['scene'],styles['Italic']),Spacer(1,7)]
        drawing=svg2rlg(str(GENERATED/Path(p['image_url']).name)); drawing.width=6.5*inch; drawing.height=4.05*inch; story += [drawing,Spacer(1,7),Paragraph('<b>Caption:</b> '+p['caption'],styles['Normal']),Paragraph('<b>Narration:</b> '+p['narration'],styles['Normal']),Spacer(1,14)]
    SimpleDocTemplate(str(out),pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36).build(story); return FileResponse(out,media_type='application/pdf',filename=out.name)
