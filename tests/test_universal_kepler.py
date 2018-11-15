# /mpcadvancer/tests/test_universal_kepler.py

"""
 
--------------------------------------------------------------

Nov 2018

Payne

Test the functions that perform universal kepler steps
(i.e. that do orbit advance)

*** MORE TESTING OF THE ACCURACY OF THE CODE IS REQUIRED ***

--------------------------------------------------------------

"""


# Import third-party packages
# --------------------------------------------------------------
#import unittest
import numpy as np

# Importing of local modules/packages required for this test
# --------------------------------------------------------------
import mpcutilities.classes as Classes
import mpcutilities.phys_const as PHYS
import mpcutilities.kepcart as kc
#import mpcadvancer.mpcadvancer as MPCA


# Import the specific package/module/function we are testing
# --------------------------------------------------------------
import mpcadvancer.mpcuniversal_stepper as MPCU


# Basic test(s) of the kepcart package
# ----------------------------------------------------------

def test_universal_step_call():
    '''
    Test the method of calling universal_step
    '''
    # Specify input cartesian state
    S      = Classes.CartState(4.54505776553499E-01, 2.65897829531622E+00, 1.27589977852726E-04, -1.04016715229021E-02, 1.01504237291145E-03, 1.94860821131980E-03)
    # Specify timestep
    dt = 1.0 # [days]
    
    # Simple (nominal) evolution (no evaluation of Partials)
    finalCartState, cartPartial = MPCU.universal_step(PHYS.GMsun , dt, S, False)

    # Test returned quantities from simple advance
    assert False, "Doomed to fail ... "

    # Evolution of Nominal & Partials
    finalCartState, cartPartial = MPCU.universal_step(PHYS.GMsun , dt, S, True)

    # Test returned quantities from advance of partials
    assert False, "Doomed to fail ... "

"""
def test_universal_step_against_keplerian_advance():
    '''
    Test the accuracy of calling universal_step by comparing it to 
    orbital advance using mean-anomaly (requires Cart-to-Kep conversion)
    '''
    # Specify input cartesian state
    S      = Classes.CartState(4.54505776553499E-01, 2.65897829531622E+00, 1.27589977852726E-04, -1.04016715229021E-02, 1.01504237291145E-03, 1.94860821131980E-03)
    # Specify timestep
    dt = 1.0 # [days]
    
    # Simple (nominal) evolution (no evaluation of Partials) using universal_step
    finalCartState, cartPartial = MPCU.universal_step(PHYS.GMsun , dt, S, False)
    
    # Conversion of input cartesian state to keplerian
    els    = kc.cart2kep(PHYS.GMsun , S)

    # Evolution of Keplerian meananomaly is linear with time
    a,e,i,O,o,M = els
    n = np.sqrt(PHYS.GMsun/(a**3))
    dM = n * dt

    # Convert back to Cartesian
    finalCartStateAlternative  = kc.kep2cartState(PHYS.GMsun , a,e,i,O,o,M+dM)

    # Compare results
    assert np.allclose(
                       np.array(finalCartState.x, finalCartState.y, finalCartState.z, finalCartState.xd, finalCartState.yd, finalCartState.zd),
                       np.array(finalCartStateAlternative.x, finalCartStateAlternative.y, finalCartStateAlternative.z, finalCartStateAlternative.xd, finalCartStateAlternative.yd, finalCartStateAlternative.zd),
                       ), "Problem with the comparison of finalCartState (%f %f %f %f %f %f) and finalCartStateAlternative (%f %f %f %f %f %f)" %(finalCartState.x, finalCartState.y, finalCartState.z, finalCartState.xd, finalCartState.yd, finalCartState.zd, finalCartStateAlternative.x, finalCartStateAlternative.y, finalCartStateAlternative.z, finalCartStateAlternative.xd, finalCartStateAlternative.yd, finalCartStateAlternative.zd)
    

def test_universal_step_against_NBODY():
    '''
    Test the accuracy of calling universal_step by comparing it to
    orbital advance using some code in REBOUND
    '''
    pass



def test_universal_step_partialDeriv():
    '''
    Test the method of calling universal_step and evaluating partial derivatives
    '''
    # Specify input cartesian state
    S      = Classes.CartState(4.54505776553499E-01, 2.65897829531622E+00, 1.27589977852726E-04, -1.04016715229021E-02, 1.01504237291145E-03, 1.94860821131980E-03)
    # Specify timestep
    dt = 1.0 # [days]
    
    # Specify the input tangent vectors to evaluate
    pass
    
    # Evolution of Nominal & Partials
    finalCartState, cartPartial = MPCU.universal_step(PHYS.GMsun , dt, S, True)
    
    # Test returned quantities from advance of partials
    assert False, "Doomed to fail ... "

"""






