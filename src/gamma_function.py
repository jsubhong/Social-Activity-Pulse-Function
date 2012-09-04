#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
from base_function import base_function
import scipy.special

class func(base_function):
    """ This is the gamma distribution function and associated unilities for evaluating and fitting. """
    
    def __init__(self, _x0 = 0., _a = 2., _b = 3., _A0 = 1.):
        self.x0 = float(_x0)
        self.a = float(_a)
        self.b= float(_b)
        self.A0 = float(_A0)

    def eval(self, x, baseline=None):
        arg = (x - self.x0)
        if arg < 0:
            return [0.0]
        c = self.b**(-self.a)
        return [self.A0 * c * arg**(self.a - 1.) * math.exp(-arg/self.b)/scipy.special.gamma(self.a)]

    def setParList(self, par):
        [self.x0, self.a, self.b, self.A0] = par

    def getParList(self):
        return [self.x0, self.a, self.b, self.A0]

    def guessFromData(self, x, y):
        # find x at max y
        ymax = -99999999999
        for i in range(0,len(y)):
            if y[i] > ymax:
                ymax = y[i]
                xmax = x[i]
        xrange = (x[-1] - x[0])
        b = 0.5 * xrange 
        a =  (xmax/b) + 1
        A = ymax/4.
        x0 = x[0] 
        res = [x0, a, b, A]
        return res

   # Attributes of the fitted curve

    def getAvgT(self):
        ta = self.a * self.b
        return ta + self.x0, self.eval(ta + self.x0)[0]

    def getPeakValue(self):
        aMin1 = self.a - 1.
        print self.A0*math.exp(-aMin1)*((aMin1/self.b)**aMin1)/scipy.special.gamma(self.a)
        # This is numerically unstable for alpha ~ 1 - rapid rise, long tail
        print self.A0*(3.*self.a**2 - 2.*self.a)/(self.b**aMin1)
    
    def getPeakTime(self):
        peak = self.b * (self.a - 1)
        return peak + self.x0, self.eval(peak + self.x0)[0]

    def getHalfLife(self):
        #
        # This isn't working!!!
        #
        ta, fa = self.getAvgT()
        tg = 0
        # predjudice result for t > tpeak
        t = ta
        eps = math.pow(10, (-8. + math.log10(t)))
        while abs(tg - t) > eps:
            tg = t
            t = self.tUpdater(tg)
            print "<<<",tg,t,self.eval(t)[0],">>>"
        #return t+self.x0,self.eval(t + self.x0)[0]
        return -1,-1

    def tUpdater(self, t):
        k = (self.b/2.)**(1./(self.a-1.)) * (self.a - 1.)/math.exp(1)
        r = self.b*(self.a - 1.)
        return r * math.log(t/k)
 
    # Output
    
    def __repr__(self):
        res =  "\n#  x0=%f\n#  a=%f\n#  b=%f\n#  A0=%f\n"%tuple(self.getParList())
        res += "#  tOffset=%f\n"%self.x0
        res += "#  tavg=%f   f(tavg)=%fi\n"%self.getAvgT()
        res += "#  tpeak=%f   f(tpeak)=%f\n"%self.getPeakTime()  
        res += "#  t1/2life=%f   f(t1/2Life)=%f\n"%self.getHalfLife()
        return res

#########################
if __name__ == '__main__':
    # simple demos
    #pf = func(_x0 = 4, _a=1., _b=2., _A0=1)
    pf = func(_x0 = 4, _a=3., _b=1., _A0=1)
    pf.printPoints(0, 12.)
    print pf