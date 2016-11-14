from io import BytesIO
from math import fabs, cos, pi

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas 
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, Spacer


def process(data):
    prod = data.get('producao')
    dens = data.get('densidade')
    freq = data.get('frequencia')
    turno = data.get('turno')
    rcu = data.get('rcu')
    inclinacao = data.get('inclinacao')
    pc = data.get('p1')
    pf = data.get('p2')

    vfogo = prod / (52 * dens * freq)
    pmh = vfogo / (7 * turno)

    d = select_diameter(rcu, pmh)
    h = select_height(d)
    b, s, t, j, lf = select_geom(rcu, d)
    l = h / cos(inclinacao * pi / 90) + (1 - inclinacao / 100) * j
    lc = l - t - lf

    cf = pf * pi * d**2 / 4000
    qf = cf * lf
    cc = pc * pi * d**2 / 4000
    qc = cc * lc
    qt = qf + qc

    vr = b * s * h
    n = vfogo / vr
    r = vr / l
    ce = qt / vr


class Test(object):

    def __init__(self):
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()

    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height - y * unit
        return x, y
    
    def run(self):
        self.doc = SimpleDocTemplate('test.pdf')
        self.story = [Spacer(1, 2.5*inch)]
        self.createLineItems()

        self.doc.build(self.story, onFirstPage=self.createDocument)
        print("Finished")

    def createDocument(self, canvas, doc):

        self.c = canvas
        normal = self.styles["Normal"]

        header_text = "<b>This is a test header</b>"
        p = Paragraph(header_text, normal)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(100, 12, mm))

        ptext = """Lorem ipsum dolor sit amet, consectetur adipisicing elit"""

        p = Paragraph(ptext, style=normal)
        p.wrapOn(self.c, self.width-50, self.height)
        p.drawOn(self.c, 30, 700)

        ptext = """Lorem ipsum dolor sit amet, consectetur adipisicing elit"""

        p = Paragraph(ptext, style=normal)
        p.wrapOn(self.c, self.width-50, self.height)
        p.drawOn(self.c, 30, 600)

        ptext = """Lorem ipsum dolor sit amet, consectetur adipisicing elit"""

    def createLineItems(self):

        text_data = ["Line", "DOS", "Procedure<br/>/Modifier",
                     "Description", "Units", "Billed<br/>Charges",
                     "Type1<br/>Reductions", "Type2<br/>Reductions",
                     "Type3<br/>Reductions", "Allowance",
                     "Qualify<br/>Code"]
        d = []
        font_size = 8
        centered = ParagraphStyle(name="centered", aligment=TA_CENTER)

        for text in text_data:
            ptext = "<font size=%s><b>%s</b></font>" % (font_size, text)
            p = Paragraph(ptext, centered)
            d.append(p)

        data = [d]
        
        line_num = 1

        formatted_line_data = []

        for x in range(200):
            line_data = [str(line_num), "04/12/2013", "73090", 
                                          "Test Reflexes", "1", "131.00", "0.00", 
                                          "0.00", "0.00", "0.00", "1234"]


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        p = canvas.Canvas(response)

        p.drawString(100, 100, "Hello world.")
        
        p.showPage()
        p.save()
        return response

def select_diameter(rcu, pmh):
    ds = 65, 89, 150
    if rcu < 120:
        rcus = 190, 250, 550
    else:
        rcus = 60, 110, 270

    pair = dict(zip(rcus, ds))
    calc = {fabs(value-pmh): value for value in pair.keys()}
    choosed_rcu = calc.get(min(calc.keys()))
    return pair.get(choosed_rcu)


def select_height(d):
    if 64 < d < 90:
        return 9
    elif 100 < d < 151:
        return 12.5


def select_geom(rcu, d):
    if rcu <= 70:
        geom = 39, 51, 35, 10, 30
    elif 70 < rcu < 120:
        geom = 37, 47, 34, 11, 35
    elif 120 <= rcu <= 180:
        geom = 35, 43, 32, 12, 40
    elif rcu > 180:
        geom = 33, 38, 30, 12, 46

    return (x * d / 1000 for x in geom)
