import io,pathlib,json,html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
ROOT=pathlib.Path(__file__).resolve().parent
def packet():
 pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
 qs=json.loads((ROOT/'problem_questions.json').read_text(encoding='utf-8'))
 out=io.BytesIO();c=canvas.Canvas(out,pagesize=A4);w,h=A4
 style=ParagraphStyle('question',fontName='STSong-Light',fontSize=12,leading=20)
 for i,q in enumerate(qs):
  c.setFont('STSong-Light',17);c.drawString(36,h-46,'COMP9020 · Problem Set 4 · '+q['label'])
  text=q['prompt'].replace('ℤ','Z (integers)').replace('ℝ','R (reals)').replace('⊨',' entails ').replace('∉',' not in ').replace('∈',' in ')
  for symbol,plain in {'−':'-', '≤':' <= ', '≥':' >= ', '≠':' != ', '∩':' intersection ', '∪':' union ', '⇒':' => ', '←':' converse ', '⌊':'floor(', '⌋':')', '∅':'empty set', '⊆':' subset of ', '≡':' congruent to ', 'φ':'phi', 'ψ':'psi', 'ν':'nu', 'ω':'omega', 'χ':'chi', 'Σ':'Sigma', '¬':' not ', '²':'^2', '·':' ', '′':"'"}.items():text=text.replace(symbol,plain)
  p=Paragraph(html.escape(text),style);_,height=p.wrap(w-72,160);p.drawOn(c,36,h-78-height)
  c.setFont('STSong-Light',9);c.drawString(36,h-104-height,'个人整理题目／补充检查项；完整题干与图请对照原题。此PDF不含答案。')
  for y in range(90,int(h-140-height),24):
   c.setStrokeColorRGB(.86,.89,.9);c.line(36,y,w-36,y)
  c.setFillColorRGB(.25,.3,.35);c.drawString(36,48,'My working / 我的解题过程');c.drawRightString(w-36,48,f'{i+1}/{len(qs)}')
  c.showPage()
 c.save();return out.getvalue()
