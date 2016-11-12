from math import fabs, cos, pi


class Bancada(object):

    def __init__(self, data):
        self.prod = data.get('producao')
        self.dens = data.get('densidade')
        self.freq = data.get('frequencia')
        self.turno = data.get('turno')
        self.rcu = data.get('rcu')
        self.inclinacao = data.get('inclinacao')
        self.pc = data.get('p1') self.pf = data.get('p2')

    @property
    def vfogo(self):
        return self.prod / (52 * self.dens * self.freq)

    @property
    def pmh(self):
        return self.vfogo / (7 * self.turno)

    @property
    def d(self):
        ds = 65, 89, 150
        if self.rcu < 120:
            rcus = 190, 250, 550
        else:
            rcus = 60, 110, 270

        pair = dict(zip(rcus, ds))
        calc = {fabs(value-self.pmh): value for value in pair.keys()}
        choosed_rcu = calc.get(min(calc.keys()))
        return pair.get(choosed_rcu)

    @property
    def h(self):
        if 64 < self.d < 90:
            return 9
        elif 100 < self.d < 151:
            return 12.5

    def _switch(self):
        return {
            self.rcu <= 70: (39, 51, 35, 10, 30),
            70 < self.rcu < 120: (37, 47, 34, 11, 35),
            120 <= self.rcu <= 180: (35, 43, 32, 12, 40),
            self.rcu > 180: (33, 38, 30, 12, 46),
        }[True]

    @property
    def b(self):
        return self._switch[0] * self.d / 1000 
    @property
    def s(self):
        return self._switch[1] * self.d / 1000

    @property
    def t(self):
        return self._switch[2] * self.d / 1000

    @property
    def j(self):
        return self._switch[3] * self.d / 1000

    @property
    def lf(self):
        return self._switch[4] * self.d / 1000

    @property
    def l(self):
        upper = self.h / cos(self.inclinacao * pi / 90)
        bottom = (1 - self.inclinacao / 100) * self.j
        return upper + bottom

    @property
    def lc(self):
        return self.l - self.t- self.lf

    @property
    def cf(self):
        return self.pf * pi * self.d**2 / 4000

    @property
    def qf(self): 
        return self.cr * self.lf

    @property
    def cc(self):
        return self.cc
        # cc = pc * pi * d**2 / 4000
        # qc = cc * lc
        # qt = qc + qf

        # vr = b * s * h
        # n = vfogo / vr
        # r = vr / l
        # ce = qt / vr

    @property
    def l(self):
    def draw(self):
        pass
