from math import fabs, cos, pi

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def processed(data):
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

    return [
        ['producao', prod],
        ['densidade', dens],
        ['frequencia', freq],
        ['turno', turno],
        ['rcu', rcu],
        ['inclinacao', inclinacao],
        ['pc', pc],
        ['pf', pf],
        ['vfogo', vfogo],
        ['pmh', pmh],
        ['D diâmetro dos furos (cm ou pol)', d],
        ['H altura da bancada (m)', h],
        ['A afastamento (m)', b],
        ['E espaçamento (m)', s],
        ['t', t],
        ['j', j],
        ['lf', lf],
        ['l', l],
        ['lc', lc],
        ['cf', cf],
        ['qf', qf],
        ['cc', cc],
        ['qc', qc],
        ['qt', qt],
        ['vr', vr],
        ['n', n],
        ['r', r],
        ['ce', ce],
    ]


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


def export(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response)

    draw_image(p, data)
    draw_table(p, data)

    p.showPage()
    p.save()
    return response


def draw_image(p, data):
    pass


def draw_table(p, data):
    # Set new origin
    p.translate(inch, inch)
    p.setFont("Helvetica", 14)

    for i, row in enumerate(data[::-1]):
        # First column
        p.rect(0, i*0.3*inch, 3*inch, 0.3*inch, fill=0)
        # First column contents
        p.drawString(0.1*inch, (0.1+i*0.3)*inch, row[0])
        # Second column
        p.rect(3*inch, i*0.3*inch, 1*inch, 0.3*inch, fill=0)
        # Second column contents
        p.drawString(3.1*inch, (0.1+i*0.3)*inch, str(round(row[1], 2)))
