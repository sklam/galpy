# Tests of integrating orbits in non-inertial frames
import pytest
import numpy
from galpy import potential
from galpy.orbit import Orbit
from galpy.util import coords

def test_lsrframe_scalaromegaz():
    # Test that integrating an orbit in the LSR frame is equivalent to 
    # normal orbit integration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    omega= lp.omegac(1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    framepot= potential.NonInertialFrameForce(Omega=omega)
    dp_frame= potential.DehnenBarPotential(omegab=1.8-omega,rb=0.5,Af=0.03)
    diskframepot= lp+dp_frame+framepot
    # Now integrate the orbit of the Sun in both the inertial and the lsr frame
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot)
        # Non-inertial frame
        op= Orbit([o.R(),o.vR(),o.vT()-omega*o.R(),o.z(),o.vz(),o.phi()])
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.R(ts)*numpy.cos(o.phi(ts)-omega*ts)
        o_ys= o.R(ts)*numpy.sin(o.phi(ts)-omega*ts)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) <tol, 'Integrating an orbit in the rotating LSR frame does not agree with the equivalent orbit in the intertial frame for integration method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in the rotating LSR frame does not agree with the equivalent orbit in the intertial frame for integration method {}'.format(method)
    check_orbit(method='odeint',tol=1e-6)
    check_orbit(method='dop853_c',tol=1e-9)
    return None
    
def test_lsrframe_vecomegaz():
    # Test that integrating an orbit in the LSR frame is equivalent to 
    # normal orbit integration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    omega= lp.omegac(1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    framepot= potential.NonInertialFrameForce(Omega=numpy.array([0.,0.,omega]))
    dp_frame= potential.DehnenBarPotential(omegab=1.8-omega,rb=0.5,Af=0.03)
    diskframepot= lp+dp_frame+framepot
    # Now integrate the orbit of the Sun in both the inertial and the lsr frame
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot)
        # Non-inertial frame
        op= Orbit([o.R(),o.vR(),o.vT()-omega*o.R(),o.z(),o.vz(),o.phi()])
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.R(ts)*numpy.cos(o.phi(ts)-omega*ts)
        o_ys= o.R(ts)*numpy.sin(o.phi(ts)-omega*ts)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in the rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in the rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-6)
    check_orbit(method='dop853_c',tol=1e-9)
    return None    
        
def test_accellsrframe_scalaromegaz():
    # Test that integrating an orbit in an LSR frame that is accelerating
    # is equivalent to normal orbit integration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    omega= lp.omegac(1.)
    omegadot= 0.02
    diskpot= lp
    framepot= potential.NonInertialFrameForce(Omega=omega,Omegadot=omegadot)
    diskframepot= lp+framepot
    # Now integrate the orbit of the Sun in both the inertial and the lsr frame
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot)
        # Non-inertial frame
        op= Orbit([o.R(),o.vR(),o.vT()-omega*o.R(),o.z(),o.vz(),o.phi()])
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.R(ts)*numpy.cos(o.phi(ts)-omega*ts-omegadot*ts**2./2.)
        o_ys= o.R(ts)*numpy.sin(o.phi(ts)-omega*ts-omegadot*ts**2./2.)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in the acceleratingly-rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in the acceleratingly-rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-6)
    check_orbit(method='dop853_c',tol=1e-9)
    return None   

def test_accellsrframe_vecomegaz():
    # Test that integrating an orbit in an LSR frame that is accelerating
    # is equivalent to normal orbit integration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    omega= lp.omegac(1.)
    omegadot= 0.02
    diskpot= lp
    framepot= potential.NonInertialFrameForce(Omega=numpy.array([0.,0.,omega]),
                                              Omegadot=numpy.array([0.,0.,omegadot]))
    diskframepot= lp+framepot
    # Now integrate the orbit of the Sun in both the inertial and the lsr frame
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot)
        # Non-inertial frame
        op= Orbit([o.R(),o.vR(),o.vT()-omega*o.R(),o.z(),o.vz(),o.phi()])
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.R(ts)*numpy.cos(o.phi(ts)-omega*ts-omegadot*ts**2./2.)
        o_ys= o.R(ts)*numpy.sin(o.phi(ts)-omega*ts-omegadot*ts**2./2.)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in the acceleratingly-rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in the acceleratingly-rotating LSR frame does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-6)
    check_orbit(method='dop853_c',tol=1e-9)
    return None      

def test_arbitraryaxisrotation_nullpotential():
    # Test that integrating an orbit in a frame rotating around an
    # arbitrary axis works
    # Start with a test where there is no potential, so a static 
    # object should remain static
    np= potential.NullPotential()
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,method='odeint',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=np,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the inertial frame
        # and then as seen by the rotating observer
        o= Orbit([1.,0.,0.,0.,0.,0.])
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,np,method=method)
        # Non-inertial frame
        # First compute initial condition
        Rp,phip,zp= rotate_and_omega(o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)
        vRp,vTp,vzp= rotate_and_omega_vec(o.vR(),o.vT(),o.vz(),
                                          o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)    
        op= Orbit([Rp,vRp,vTp,zp,vzp,phip])
        op.integrate(ts,RotatingPotentialWrapperPotential(pot=np,rot=rot,omega=omega)
            +potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot))),
            method=method)
        # Compare
        # Orbit in the inertial frame
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        o_vRs= o.vR(ts)
        o_vTs= o.vT(ts)
        o_vzs= o.vz(ts)
        # and that computed in the non-inertial frame converted back to inertial
        op_xs, op_ys, op_zs= [], [], []
        op_vRs, op_vTs, op_vzs= [], [], []
        for ii,t in enumerate(ts):
            xyz= rotate_and_omega(op.x(t),op.y(t),phi=op.z(t),t=t,
                                  rot=rot,omega=omega,rect=True)
            op_xs.append(xyz[0])
            op_ys.append(xyz[1])
            op_zs.append(xyz[2])
            vRTz= rotate_and_omega_vec(op.vR(t),op.vT(t),op.vz(t),
                                       op.R(t),op.z(t),phi=op.phi(t),
                                       t=t,rot=rot,omega=omega)
            op_vRs.append(vRTz[0])
            op_vTs.append(vRTz[1])
            op_vzs.append(vRTz[2])
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vRs-op_vRs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vTs-op_vTs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vzs-op_vzs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(zvec=[0.,1.,1.],omega=1.3,method='odeint',tol=1e-5)
    check_orbit(zvec=[2.,0.,1.],omega=-1.1,method='dop853',tol=1e-4)
    check_orbit(zvec=[2.,3.,1.],omega=0.9,method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_arbitraryaxisrotation():
    # Test that integrating an orbit in a frame rotating around an
    # arbitrary axis works
    lp= potential.MiyamotoNagaiPotential(normalize=1.,a=1.,b=0.2)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,method='odeint',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=diskpot,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the inertial frame
        # and then as seen by the rotating observer
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        # First compute initial condition
        Rp,phip,zp= rotate_and_omega(o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)
        vRp,vTp,vzp= rotate_and_omega_vec(o.vR(),o.vT(),o.vz(),
                                          o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)    
        op= Orbit([Rp,vRp,vTp,zp,vzp,phip])
        op.integrate(ts,RotatingPotentialWrapperPotential(pot=diskpot,rot=rot,omega=omega)
            +potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot))),
            method=method)
        # Compare
        # Orbit in the inertial frame
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        o_vRs= o.vR(ts)
        o_vTs= o.vT(ts)
        o_vzs= o.vz(ts)
        # and that computed in the non-inertial frame converted back to inertial
        op_xs, op_ys, op_zs= [], [], []
        op_vRs, op_vTs, op_vzs= [], [], []
        for ii,t in enumerate(ts):
            xyz= rotate_and_omega(op.x(t),op.y(t),phi=op.z(t),t=t,
                                  rot=rot,omega=omega,rect=True)
            op_xs.append(xyz[0])
            op_ys.append(xyz[1])
            op_zs.append(xyz[2])
            vRTz= rotate_and_omega_vec(op.vR(t),op.vT(t),op.vz(t),
                                       op.R(t),op.z(t),phi=op.phi(t),
                                       t=t,rot=rot,omega=omega)
            op_vRs.append(vRTz[0])
            op_vTs.append(vRTz[1])
            op_vzs.append(vRTz[2])
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vRs-op_vRs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vTs-op_vTs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vzs-op_vzs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(zvec=[0.,1.,1.],omega=1.3,method='odeint',tol=1e-5)
    check_orbit(zvec=[2.,0.,1.],omega=-1.1,method='dop853',tol=1e-4)
    check_orbit(zvec=[2.,3.,1.],omega=0.9,method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_arbitraryaxisrotation_omegadot_nullpotential():
    # Test that integrating an orbit in a frame rotating around an
    # arbitrary axis works, where the frame rotation is changing in time
    # Start with a test where there is no potential, so a static 
    # object should remain static
    np= potential.NullPotential()
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,omegadot=0.1,method='odeint',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=np,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the inertial frame
        # and then as seen by the rotating observer
        o= Orbit([1.,0.,0.,0.,0.,0.])
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,np,method=method)
        # Non-inertial frame
        # First compute initial condition, no need to specify omegadot, bc t=0
        Rp,phip,zp= rotate_and_omega(o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)
        vRp,vTp,vzp= rotate_and_omega_vec(o.vR(),o.vT(),o.vz(),
                                          o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)    
        op= Orbit([Rp,vRp,vTp,zp,vzp,phip])
        # Omegadot is just a scaled version of Omega
        op.integrate(ts,RotatingPotentialWrapperPotential(pot=np,rot=rot,omega=omega,
                                                          omegadot=omegadot)
            +potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot)),
                Omegadot=numpy.array(derive_noninert_omega(omega,rot=rot))*omegadot/omega),
            method=method)
        # Compare
        # Orbit in the inertial frame
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        o_vRs= o.vR(ts)
        o_vTs= o.vT(ts)
        o_vzs= o.vz(ts)
        # and that computed in the non-inertial frame converted back to inertial
        op_xs, op_ys, op_zs= [], [], []
        op_vRs, op_vTs, op_vzs= [], [], []
        for ii,t in enumerate(ts):
            xyz= rotate_and_omega(op.x(t),op.y(t),phi=op.z(t),t=t,
                                  rot=rot,omega=omega,omegadot=omegadot,rect=True)
            op_xs.append(xyz[0])
            op_ys.append(xyz[1])
            op_zs.append(xyz[2])
            vRTz= rotate_and_omega_vec(op.vR(t),op.vT(t),op.vz(t),
                                       op.R(t),op.z(t),phi=op.phi(t),
                                       t=t,rot=rot,omega=omega,omegadot=omegadot)
            op_vRs.append(vRTz[0])
            op_vTs.append(vRTz[1])
            op_vzs.append(vRTz[2])
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vRs-op_vRs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vTs-op_vTs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vzs-op_vzs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(zvec=[0.,1.,1.],omega=1.3,method='odeint',tol=1e-5)
    check_orbit(zvec=[2.,0.,1.],omega=-1.1,method='dop853',tol=1e-4)
    check_orbit(zvec=[2.,3.,1.],omega=0.9,method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_arbitraryaxisrotation_omegadot():
    # Test that integrating an orbit in a frame rotating around an
    # arbitrary axis works, where the frame rotation is changing in time
    # Start with a test where there is no potential, so a static 
    # object should remain static
    lp= potential.MiyamotoNagaiPotential(normalize=1.,a=1.,b=0.2)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,omegadot=0.03,method='odeint',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=diskpot,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the inertial frame
        # and then as seen by the rotating observer
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        # First compute initial condition, no need to specify omegadot, bc t=0
        Rp,phip,zp= rotate_and_omega(o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)
        vRp,vTp,vzp= rotate_and_omega_vec(o.vR(),o.vT(),o.vz(),
                                          o.R(),o.z(),phi=o.phi(),t=0.,rot=rot,omega=-omega)    
        op= Orbit([Rp,vRp,vTp,zp,vzp,phip])
        # Omegadot is just a scaled version of Omega
        op.integrate(ts,RotatingPotentialWrapperPotential(pot=diskpot,rot=rot,omega=omega,
                                                          omegadot=omegadot)
            +potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot)),
                Omegadot=numpy.array(derive_noninert_omega(omega,rot=rot))*omegadot/omega),
            method=method)
        # Compare
        # Orbit in the inertial frame
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        o_vRs= o.vR(ts)
        o_vTs= o.vT(ts)
        o_vzs= o.vz(ts)
        # and that computed in the non-inertial frame converted back to inertial
        op_xs, op_ys, op_zs= [], [], []
        op_vRs, op_vTs, op_vzs= [], [], []
        for ii,t in enumerate(ts):
            xyz= rotate_and_omega(op.x(t),op.y(t),phi=op.z(t),t=t,
                                  rot=rot,omega=omega,omegadot=omegadot,rect=True)
            op_xs.append(xyz[0])
            op_ys.append(xyz[1])
            op_zs.append(xyz[2])
            vRTz= rotate_and_omega_vec(op.vR(t),op.vT(t),op.vz(t),
                                       op.R(t),op.z(t),phi=op.phi(t),
                                       t=t,rot=rot,omega=omega,omegadot=omegadot)
            op_vRs.append(vRTz[0])
            op_vTs.append(vRTz[1])
            op_vzs.append(vRTz[2])
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vRs-op_vRs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vTs-op_vTs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_vzs-op_vzs)) < tol, 'Integrating an orbit in a rotating frame around an arbitrary axis does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(zvec=[2.,0.,1.],omega=-1.1,method='dop853',tol=1e-5)
    return None

def test_linacc_constantacc_z():
    # Test that a linearly-accelerating frame along the z direction works
    # with a constant acceleration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    az= 0.02
    intaz= lambda t: 0.02*t**2./2.
    framepot= potential.NonInertialFrameForce(RTacm=[0.,0.,az])
    diskframepot= AcceleratingPotentialWrapperPotential(pot=diskpot,
                                                        a=[lambda t: 0.,
                                                           lambda t: 0.,
                                                           intaz])\
                    +framepot
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        op= o()
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        op_zs= op.z(ts)+intaz(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-9)
    check_orbit(method='dop853',tol=1e-9)
    check_orbit(method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_linacc_constantacc_xyz():
    # Test that a linearly-accelerating frame along the z direction works
    # with a constant acceleration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    ax,ay,az= -0.03,0.04,0.02
    inta= [lambda t: -0.03*t**2./2.,lambda t: 0.04*t**2./2.,lambda t: 0.02*t**2./2.]
    framepot= potential.NonInertialFrameForce(RTacm=[ax,ay,az])
    diskframepot= AcceleratingPotentialWrapperPotential(pot=diskpot,a=inta)\
                    +framepot
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        op= o()
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        op_xs= op.x(ts)+inta[0](ts)
        op_ys= op.y(ts)+inta[1](ts)
        op_zs= op.z(ts)+inta[2](ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-5)
    check_orbit(method='dop853',tol=1e-9)
    check_orbit(method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_linacc_changingacc_z():
    # Test that a linearly-accelerating frame along the z direction works
    # with a changing acceleration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    az= lambda t: 0.02+0.03*t/20.
    intaz= lambda t: 0.02*t**2./2.+0.03*t**3./6./20.
    framepot= potential.NonInertialFrameForce(RTacm=[lambda t: 0.,lambda t: 0.,az])
    diskframepot= AcceleratingPotentialWrapperPotential(pot=diskpot,
                                                        a=[lambda t: 0.,
                                                           lambda t: 0.,
                                                           intaz])\
                    +framepot
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        op= o()
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        op_xs= op.x(ts)
        op_ys= op.y(ts)
        op_zs= op.z(ts)+intaz(ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-9)
    check_orbit(method='dop853',tol=1e-9)
    check_orbit(method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_linacc_changingacc_xyz():
    # Test that a linearly-accelerating frame along the z direction works
    # with a changing acceleration
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    ax,ay,az= lambda t: -0.03-0.03*t/20., \
            lambda t: 0.04+0.08*t/20., \
            lambda t: 0.02+0.03*t/20.
    inta= [lambda t: -0.03*t**2./2.-0.03*t**3./6./20.,
           lambda t: 0.04*t**2./2.+0.08*t**3./6./20.,
           lambda t: 0.02*t**2./2.+0.03*t**3./6./20.]
    framepot= potential.NonInertialFrameForce(RTacm=[ax,ay,az])
    diskframepot= AcceleratingPotentialWrapperPotential(pot=diskpot,
                                                        a=inta)\
                    +framepot
    def check_orbit(method='odeint',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # Inertial frame
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot,method=method)
        # Non-inertial frame
        op= o()
        op.integrate(ts,diskframepot,method=method)
        # Compare
        o_xs= o.x(ts)
        o_ys= o.y(ts)
        o_zs= o.z(ts)
        op_xs= op.x(ts)+inta[0](ts)
        op_ys= op.y(ts)+inta[1](ts)
        op_zs= op.z(ts)+inta[2](ts)
        assert numpy.amax(numpy.fabs(o_xs-op_xs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_ys-op_ys)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
        assert numpy.amax(numpy.fabs(o_zs-op_zs)) < tol, 'Integrating an orbit in a linearly-accelerating frame with constant acceleration does not agree with the equivalent orbit in the intertial frame for method {}'.format(method)
    check_orbit(method='odeint',tol=1e-5)
    check_orbit(method='dop853',tol=1e-9)
    check_orbit(method='dop853_c',tol=1e-5) # Lower tol, because diff integrators for inertial and non-inertial, bc wrapper not implemented in C
    return None

def test_python_vs_c_arbitraryaxisrotation():
    # Integrate an orbit in both Python and C to check that they match
    # We don't need to known the true answer here
    lp= potential.MiyamotoNagaiPotential(normalize=1.,a=1.,b=0.2)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,
                    py_method='dop853',c_method='dop853_c',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=diskpot,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the rotating frame in Python
        o= Orbit()
        o.turn_physical_off()
        # Rotating frame in Python
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot+potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot))),
                method=py_method)
        # In C
        op= o()
        op.integrate(ts,diskpot+potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot))),
                method=c_method)
        assert numpy.amax(numpy.fabs(o.x(ts)-op.x(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.y(ts)-op.y(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.z(ts)-op.z(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vx(ts)-op.vx(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vy(ts)-op.vy(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vz(ts)-op.vz(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        return None
    check_orbit()
    return None

def test_python_vs_c_arbitraryaxisrotation_omegadot():
    # Integrate an orbit in both Python and C to check that they match
    # We don't need to known the true answer here
    lp= potential.MiyamotoNagaiPotential(normalize=1.,a=1.,b=0.2)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    def check_orbit(zvec=[1.,0.,1.],omega=1.3,omegadot=0.03,
                    py_method='dop853',c_method='dop853_c',tol=1e-9):
        # Set up the rotating frame's rotation matrix
        rotpot= potential.RotateAndTiltWrapperPotential(pot=diskpot,zvec=zvec)
        rot= rotpot._rot
        # Now integrate an orbit in the rotating frame in Python
        o= Orbit()
        o.turn_physical_off()
        # Rotating frame in Python
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot+potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot)),
                Omegadot=numpy.array(derive_noninert_omega(omega,rot=rot))*omegadot/omega),
                method=py_method)
        # In C
        op= o()
        op.integrate(ts,diskpot+potential.NonInertialFrameForce(\
                Omega=numpy.array(derive_noninert_omega(omega,rot=rot)),
                Omegadot=numpy.array(derive_noninert_omega(omega,rot=rot))*omegadot/omega),
                method=c_method)
        # Compare
        assert numpy.amax(numpy.fabs(o.x(ts)-op.x(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.y(ts)-op.y(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.z(ts)-op.z(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vx(ts)-op.vx(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vy(ts)-op.vy(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vz(ts)-op.vz(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        return None
    check_orbit(tol=1e-8)
    return None

def test_python_vs_c_linacc_changingacc_xyz():
    # Integrate an orbit in both Python and C to check that they match
    # We don't need to known the true answer here
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    dp= potential.DehnenBarPotential(omegab=1.8,rb=0.5,Af=0.03)
    diskpot= lp+dp
    ax,ay,az= lambda t: -0.03-0.03*t/20., \
            lambda t: 0.04+0.08*t/20., \
            lambda t: 0.02+0.03*t/20.
    inta= [lambda t: -0.03*t**2./2.-0.03*t**3./6./20.,
           lambda t: 0.04*t**2./2.+0.08*t**3./6./20.,
           lambda t: 0.02*t**2./2.+0.03*t**3./6./20.]
    framepot= potential.NonInertialFrameForce(RTacm=[ax,ay,az])
    def check_orbit(py_method='dop853',c_method='dop853_c',tol=1e-9):
        o= Orbit()
        o.turn_physical_off()
        # In Python
        ts= numpy.linspace(0.,20.,1001)
        o.integrate(ts,diskpot+framepot,method=py_method)
        # In C
        op= o()
        op.integrate(ts,diskpot+framepot,method=c_method)
        # Compare
        assert numpy.amax(numpy.fabs(o.x(ts)-op.x(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.y(ts)-op.y(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.z(ts)-op.z(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vx(ts)-op.vx(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vy(ts)-op.vy(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        assert numpy.amax(numpy.fabs(o.vz(ts)-op.vz(ts))) <tol, 'Integrating an orbit in a rotating frame in Python does not agree with integrating the same orbit in C; using methods {} and {}'.format(py_method,c_method)
        return None
    check_orbit(tol=1e-10)
    return None

# Utility wrappers and other functions
from galpy.potential.WrapperPotential import parentWrapperPotential
from galpy.potential.Potential import _evaluateRforces, _evaluatephiforces, _evaluatezforces
class AcceleratingPotentialWrapperPotential(parentWrapperPotential):
    def __init__(self,amp=1.,pot=None,
                 a=[lambda t: 0., lambda t: 0., lambda t: 0.],
                 ro=None,vo=None):
        # a = accelerated x
        # that is
        # x -> x + a(t)
        # so a isn't really a...
        self._a= a
        
    def _Rforce(self,R,z,phi=0.,t=0.):
         Fxyz= self._force_xyz(R,z,phi=phi,t=t)
         return numpy.cos(phi)*Fxyz[0]+numpy.sin(phi)*Fxyz[1]

    def _phiforce(self,R,z,phi=0.,t=0.):
        Fxyz= self._force_xyz(R,z,phi=phi,t=t)
        return R*(-numpy.sin(phi)*Fxyz[0] + numpy.cos(phi)*Fxyz[1])

    def _zforce(self,R,z,phi=0.,t=0.):
        return self._force_xyz(R,z,phi=phi,t=t)[2]

    def _force_xyz(self,R,z,phi=0.,t=0.):
        """Get the rectangular forces in the transformed frame"""
        x,y,_= coords.cyl_to_rect(R,phi,z)
        xp= x+self._a[0](t)
        yp= y+self._a[1](t)
        zp= z+self._a[2](t)
        Rp,phip,zp= coords.rect_to_cyl(xp,yp,zp)
        Rforcep= _evaluateRforces(self._pot,Rp,zp,phi=phip,t=t)
        phiforcep= _evaluatephiforces(self._pot,Rp,zp,phi=phip,t=t)
        zforcep= _evaluatezforces(self._pot,Rp,zp,phi=phip,t=t)
        xforcep= numpy.cos(phip)*Rforcep-numpy.sin(phip)*phiforcep/Rp
        yforcep= numpy.sin(phip)*Rforcep+numpy.cos(phip)*phiforcep/Rp
        return numpy.array([xforcep,yforcep,zforcep])

# Functions and wrappers for rotation around an arbitrary axis
# Rotation happens around an axis that is rotated by rot
# So transformation from rotating to inertial is
# rot.T x omega-rotation x rot
def rotate_and_omega(R,z,phi=0.,t=0.,rot=None,omega=None,omegadot=None,rect=False):
    # From the rotating frame to the inertial frame
    if rect:
        x,y,z= R,z,phi
    else:
        x,y,z= coords.cyl_to_rect(R,phi,z)
    xyzp= numpy.dot(rot,numpy.array([x,y,z]))
    Rp,phip,zp = coords.rect_to_cyl(xyzp[0],xyzp[1],xyzp[2])
    phip+= omega*t
    if not omegadot is None:
        phip+= omegadot*t**2./2.
    xp,yp,zp= coords.cyl_to_rect(Rp,phip,zp)
    xyz= numpy.dot(rot.T,numpy.array([xp,yp,zp]))
    if rect:
        R,phi,z= xyz[0],xyz[1],xyz[2]
    else:
        R,phi,z= coords.rect_to_cyl(xyz[0],xyz[1],xyz[2])
    return R,phi,z
def rotate_and_omega_vec(vR,vT,vz,R,z,phi=0.,t=0.,rot=None,omega=None,omegadot=None):
    # From the rotating frame to the inertial frame, for vectors
    x,y,z= coords.cyl_to_rect(R,phi,z)
    vx,vy,vz= coords.cyl_to_rect_vec(vR,vT,vz,phi=phi)
    xyzp= numpy.dot(rot,numpy.array([x,y,z]))
    Rp,phip,zp = coords.rect_to_cyl(xyzp[0],xyzp[1],xyzp[2])
    vxyzp= numpy.dot(rot,numpy.array([vx,vy,vz]))
    vRp,vTp,vzp = coords.rect_to_cyl_vec(vxyzp[0],vxyzp[1],vxyzp[2],xyzp[0],xyzp[1],xyzp[2])
    phip+= omega*t
    vTp+= omega*Rp
    if not omegadot is None:
        phip+= omegadot*t**2./2.
        vTp+= omegadot*t*Rp
    xp,yp,zp= coords.cyl_to_rect(Rp,phip,zp)
    vxp,vyp,vzp= coords.cyl_to_rect_vec(vRp,vTp,vzp,phi=phip)
    xyz= numpy.dot(rot.T,numpy.array([xp,yp,zp]))
    vxyz= numpy.dot(rot.T,numpy.array([vxp,vyp,vzp]))
    vR,vT,vz= coords.rect_to_cyl_vec(vxyz[0],vxyz[1],vxyz[2],xyz[0],xyz[1],xyz[2])
    return vR,vT,vz
def derive_noninert_omega(omega,rot=None,
                          x=1.,y=2.,z=3.,
                          x2=-1.,y2= 2.,z2= -5.,
                          t=0.):
    # Numerically compute Omega of the non-inertial frame
    # Need to use the rotation of two arbitrary (non-parallel) vectors
    # To fully describe the rotation
    # Then can solve for it
    # See https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Conversion_formulae_for_derivatives
    # Let's begin
    # Compute d r / d t, numerically
    eps= 1e-6
    r11= rotate_and_omega(x,y,phi=z,t=t,rot=rot,omega=omega,rect=True)
    r12= rotate_and_omega(x,y,phi=z,t=t+eps,rot=rot,omega=omega,rect=True)
    dr1dt= (numpy.array(r12)-numpy.array(r11))/eps
    r21= rotate_and_omega(x2,y2,phi=z2,t=t,rot=rot,omega=omega,rect=True)
    r22= rotate_and_omega(x2,y2,phi=z2,t=t+eps,rot=rot,omega=omega,rect=True)
    dr2dt= (numpy.array(r22)-numpy.array(r21))/eps
    # Solve
    #dxdt= -omegaz * y + omegay * z
    #dydt=  omegaz * x - omegax * z
    #dzdt= -omegay * x + omegax * y
    # with the two given points. Use
    # dy1dt= omegaz * x1 - omegax * z1
    # dy2dt= omegaz * x2 - omegax * z2
    # dy1dt * x2 - dy2dt * x1 = -omegax * ( z1 * x2 - z2 * x1)
    # and
    # dx1dt= -omegaz * y1 + omegay * z1
    # dx2dt= -omegaz * y2 + omegay * z2
    # dx1dt * y2 - dx2dt * y1 =  omegay * ( z1 * y2 - z2 * y1 )
    # dx1dt * z2 - dx2dt * z1 = -omegaz * ( y1 * z2 - y2 * z1 )
    omegax= -(dr1dt[1]*r21[0] - dr2dt[1]*r11[0])/(r11[2]*r21[0] - r21[2] * r11[0])
    omegay=  (dr1dt[0]*r21[1] - dr2dt[0]*r11[1])/(r11[2]*r21[1] - r21[2] * r11[1])
    omegaz= -(dr1dt[0]*r21[2] - dr2dt[0]*r11[2])/(r11[1]*r21[2] - r21[1] * r11[2])
    return (omegax,omegay,omegaz)
    
class RotatingPotentialWrapperPotential(parentWrapperPotential):
    def __init__(self,amp=1.,pot=None,rot=None,omega=None,omegadot=None,ro=None,vo=None):
        # Frame rotates as rot.T x omega-rotation x rot, see transformations above
        self._rot= rot
        self._omega= omega
        self._omegadot= omegadot
        
    def _Rforce(self,R,z,phi=0.,t=0.):
         Fxyz= self._force_xyz(R,z,phi=phi,t=t)
         return numpy.cos(phi)*Fxyz[0]+numpy.sin(phi)*Fxyz[1]

    def _phiforce(self,R,z,phi=0.,t=0.):
        Fxyz= self._force_xyz(R,z,phi=phi,t=t)
        return R*(-numpy.sin(phi)*Fxyz[0] + numpy.cos(phi)*Fxyz[1])

    def _zforce(self,R,z,phi=0.,t=0.):
        return self._force_xyz(R,z,phi=phi,t=t)[2]

    def _force_xyz(self,R,z,phi=0.,t=0.):
        """Get the rectangular forces in the transformed frame"""
        Rp, phip, zp= rotate_and_omega(R,z,phi=phi,t=t,
                                       rot=self._rot,omega=self._omega,
                                       omegadot=self._omegadot)
        Rforcep= _evaluateRforces(self._pot,Rp,zp,phi=phip,t=t)
        phiforcep= _evaluatephiforces(self._pot,Rp,zp,phi=phip,t=t)
        zforcep= _evaluatezforces(self._pot,Rp,zp,phi=phip,t=t)
        xforcep= numpy.cos(phip)*Rforcep-numpy.sin(phip)*phiforcep/Rp
        yforcep= numpy.sin(phip)*Rforcep+numpy.cos(phip)*phiforcep/Rp
        # Now figure out the inverse rotation matrix to rotate the forces
        # The way this is written, we effectively compute the transpose of the
        # rotation matrix, which is its inverse
        inv_rot= numpy.array([\
           list(rotate_and_omega(1.,0.,phi=0.,t=t,rot=self._rot,omega=self._omega,omegadot=self._omegadot,rect=True)),
           list(rotate_and_omega(0.,1.,phi=0.,t=t,rot=self._rot,omega=self._omega,omegadot=self._omegadot,rect=True)),
           list(rotate_and_omega(0.,0.,phi=1.,t=t,rot=self._rot,omega=self._omega,omegadot=self._omegadot,rect=True))])
        return numpy.dot(inv_rot,
                         numpy.array([xforcep,yforcep,zforcep]))
