# Class that implements anisotropic DFs of the Osipkov-Merritt type
import numpy
from scipy import integrate, special, interpolate
from ..util import conversion
from ..potential import evaluatePotentials, evaluateDensities
from .sphericaldf import anisotropicsphericaldf, sphericaldf
from .eddingtondf import eddingtondf

# This is the general Osipkov-Merritt superclass, implementation of general
# formula can be found following this class
class _osipkovmerrittdf(anisotropicsphericaldf):
    """General Osipkov-Merritt superclass with useful functions for any DF of the Osipkov-Merritt type."""
    def __init__(self,pot=None,denspot=None,ra=1.4,rmax=None,
                 scale=None,ro=None,vo=None):
        """
        NAME:

            __init__

        PURPOSE:

            Initialize a DF with Osipkov-Merritt anisotropy

        INPUT:

            pot= (None) Potential instance or list thereof

            denspot= (None) Potential instance or list thereof that represent the density of the tracers (assumed to be spherical; if None, set equal to pot)

            ra - anisotropy radius (can be a Quantity)
          
            scale - Characteristic scale radius to aid sampling calculations. 
                Not necessary, and will also be overridden by value from pot 
                if available.

           ro=, vo= galpy unit parameters

        OUTPUT:

            None

        HISTORY:

            2020-11-12 - Written - Bovy (UofT)

        """
        anisotropicsphericaldf.__init__(self,pot=pot,denspot=denspot,rmax=rmax,
                                        scale=scale,ro=ro,vo=vo)
        self._ra= conversion.parse_length(ra,ro=self._ro)
        self._ra2= self._ra**2.

    def _call_internal(self,*args):
        """
        NAME:

            _call_internal

        PURPOSE:

            Evaluate the DF for an Osipkov-Merritt-anisotropy DF

        INPUT:

            E - The energy

            L - The angular momentum

        OUTPUT:

            fH - The value of the DF

        HISTORY:

            2020-11-12 - Written - Bovy (UofT)

        """
        E, L, _= args
        return self.fQ(-E-0.5*L**2./self._ra2)

    def _sample_eta(self,r,n=1):
        """Sample the angle eta which defines radial vs tangential velocities"""
        # cumulative distribution of x = cos eta satisfies
        # x/(sqrt(A+1 -A* x^2)) = 2 b - 1 = c
        # where b \in [0,1] and A = (r/ra)^2
        # Solved by
        # x = c sqrt(1+[r/ra]^2) / sqrt( [r/ra]^2 c^2 + 1 ) for c > 0 [b > 0.5]
        # and symmetric wrt c
        c= numpy.random.uniform(size=n)
        x= c*numpy.sqrt(1+r**2./self._ra2)/numpy.sqrt(r**2./self._ra2*c**2.+1)
        x*= numpy.random.choice([1.,-1.],size=n)
        return numpy.arccos(x)

    def _p_v_at_r(self,v,r):
        """p( v*sqrt[1+r^2/ra^2*sin^2eta] | r) used in sampling """
        if hasattr(self,'_logfQ_interp'):
            return numpy.exp(\
                    self._logfQ_interp(-evaluatePotentials(self._pot,r,0,
                                                       use_physical=False)\
                                   -0.5*v**2.))*v**2.
        else:
            return self.fQ(-evaluatePotentials(self._pot,r,0,
                                               use_physical=False)\
                           -0.5*v**2.)*v**2.

    def _sample_v(self,r,eta,n=1):
        """Generate velocity samples"""
        # Use super-class method to obtain v*[1+r^2/ra^2*sin^2eta]
        out= super(_osipkovmerrittdf,self)._sample_v(r,eta,n=n)
        # Transform to v
        return out/numpy.sqrt(1.+r**2./self._ra2*numpy.sin(eta)**2.)

    def _vmomentdensity(self,r,n,m):
         if m%2 == 1 or n%2 == 1:
             return 0.
         return 2.*numpy.pi*integrate.quad(lambda v: v**(2.+m+n)
                                    *self.fQ(-evaluatePotentials(self._pot,r,0,
                                                         use_physical=False)
                                             -0.5*v**2.),
                             0.,self._vmax_at_r(self._pot,r))[0]\
            *special.gamma(m/2.+1.)*special.gamma((n+1)/2.)/\
            special.gamma(0.5*(m+n+3.))/(1+r**2./self._ra2)**(m/2+1)
    
class osipkovmerrittdf(_osipkovmerrittdf):
    """Class that implements anisotropic DFs of the Osipkov-Merritt type with radially varying anisotropy
    
    .. math::

        \\beta(r) = \\frac{1}{1+r_a^2/r^2}

    with :math:`r_a` the anistropy radius.

    """
    def __init__(self,pot=None,denspot=None,ra=1.4,rmax=1e4,
                 scale=None,ro=None,vo=None):
        """
        NAME:

            __init__

        PURPOSE:

            Initialize a DF with Osipkov-Merritt anisotropy

        INPUT:

            pot= (None) Potential instance or list thereof

            denspot= (None) Potential instance or list thereof that represent the density of the tracers (assumed to be spherical; if None, set equal to pot)

            ra - anisotropy radius (can be a Quantity)
          
           rmax= (1e4) when sampling, maximum radius to consider (can be Quantity)

            scale - Characteristic scale radius to aid sampling calculations. 
                Not necessary, and will also be overridden by value from pot 
                if available.

           ro=, vo= galpy unit parameters

        OUTPUT:

            None

        HISTORY:

            2021-02-07 - Written - Bovy (UofT)

        """
        _osipkovmerrittdf.__init__(self,pot=pot,denspot=denspot,ra=ra,
                                   rmax=rmax,ro=ro,vo=vo)
        # Because f(Q) is the same integral as the Eddington conversion, but
        # using the augmented density rawdensx(1+r^2/ra^2), we use a helper
        # eddingtondf to do this integral, hacked to use the augmented density
        self._edf= eddingtondf(pot=self._pot,denspot=self._denspot,scale=scale,
                               rmax=rmax,ro=ro,vo=vo)
        self._edf._dnudr= \
           (lambda r: self._denspot._ddensdr(r)*(1.+r**2./self._ra2) \
                   +2.*self._denspot.dens(r,0,use_physical=False)*r/self._ra2)\
           if not isinstance(self._denspot,list) \
           else (lambda r: numpy.sum([p._ddensdr(r) for p in self._denspot])\
                *(1.+r**2./self._ra2)\
                +2.*evaluateDensities(self._denspot,r,0,use_physical=False)\
                *r/self._ra2)
        self._edf._d2nudr2= \
           (lambda r: self._denspot._d2densdr2(r)*(1.+r**2./self._ra2) \
                    +4.*self._denspot._ddensdr(r)*r/self._ra2 \
                    +2.*self._denspot.dens(r,0,use_physical=False)/self._ra2)\
           if not isinstance(self._denspot,list) \
           else (lambda r: numpy.sum([p._d2densdr2(r) for p in self._denspot])\
                *(1.+r**2./self._ra2)\
                +4.*numpy.sum([p._ddensdr(r) for p in self._denspot])\
                    *r/self._ra2 \
                +2.*evaluateDensities(self._denspot,r,0,use_physical=False)\
                /self._ra2)

    def sample(self,R=None,z=None,phi=None,n=1,return_orbit=True):
        # Slight over-write of superclass method to first build f(Q) interp
        # No docstring so superclass' is used
        if not hasattr(self,'_logfQ_interp'):
            Qs4interp= numpy.hstack((numpy.linspace(1e-5,0.5,101,
                                                    endpoint=False),
                                     sorted(1.-numpy.geomspace(1e-4,0.5,101))))
            Qs4interp= -(Qs4interp*(self._edf._Emin-self._edf._potInf)
                        +self._edf._potInf)
            fQ4interp= numpy.log(self.fQ(Qs4interp))
            iindx= True^numpy.isnan(fQ4interp)
            self._logfQ_interp= interpolate.InterpolatedUnivariateSpline(\
                                        Qs4interp[iindx],fQ4interp[iindx],k=3)
        return sphericaldf.sample(self,R=R,z=z,phi=phi,n=n,
                                  return_orbit=return_orbit)

   
    def fQ(self,Q):
        """
        NAME:

            fQ

        PURPOSE

            Calculate the f(Q) portion of an Osipkov-Merritt Hernquist distribution function

        INPUT:

            Q - The Osipkov-Merritt 'energy' E-L^2/[2ra^2] (can be Quantity)

        OUTPUT:

            fQ - The value of the f(Q) portion of the DF

        HISTORY:

            2021-02-07 - Written - Bovy (UofT)

        """
        return self._edf.fE(-Q)
