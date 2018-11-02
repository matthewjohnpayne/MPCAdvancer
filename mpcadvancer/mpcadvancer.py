# -*- coding: utf-8 -*-
# mpcadvancer/mpcadvancer/mpcadvancer.py

'''
--------------------------------------------------------------
Main mpcadvancer module.

Oct 2018
Matt Payne

To contain all (high-level) functions required to advance orbits
Currently just sketching out framework

Needs to advance various types of initial conditions (ICs):
(i) single orbits, (ii) tangents, (iii) "uncertainty region"

Will be dependent on lower-level advancement routines, such as
(i) kepcart; (ii) nbody; (iii) chebyshev

Has some heritage from hack-work done by Payne to help Veres

# Anticipated Standard functionalities: few/none exist as-of Oct 27th, 2018
# advance_cartesian_states_2body   # Advance cartesian states to requested TDBs using Keplerian (2-body)
# advance_cartesian_states_nbody   # Advance cartesian states to requested TDBs using N-Body method

--------------------------------------------------------------
'''


# Import third-party packages
# --------------------------------------------------------------
import sys
import numpy as np


# Import neighboring packages
# --------------------------------------------------------------



# Class(es) / Routines for advancing orbits
# --------------------------------------------------------------


class ORBIT_ICs:
    ''' 
    To contain the initial condition specification
    for one-or-many initial conditions to be advanced
    
    Needs to be able to load / accept some specification of 
    (i) initial common time
    (ii) one-or-many initial Keplerian / Cartesian ICs
    
    I think we want to be able to input/use either
    (a) single nominal orbit
    (b) variations for differentials 
    (c) some form of uncertainty-region specification/object(s)
    
    Want it to contain any/many reformating and/or 
    transformation options necessary to ensure
    that the ORBIT_ICs object contains the correct
    input format assumed by ADVANCE class, i.e.
    (i) cartesian HELIOCENTRIC ECLIPTIC CARTESIAN ICs
       --- Much / all of this will relate to the "cartState" in mpcutilities.classes
    (ii) common initial time, iTDB

    '''

    # Add some content ...



class TARGET_STATES:
    '''
    To contain the results from ADVANCER for each of the target times
    
    Need to think more about the form(s) this will take
    
    I assume it will contain convenience functions to help reformat, etc
    '''

    def __init__(self,  ):
        '''
        Intend that this be initialized using output from ADVANCE
        at grid of times
        '''
        # Add some content ...
        pass




    def createFunctionalRepresentation():
        '''
        Creates a functional approximation to TARGET_STATES
        Allows interpolation at arbitrary time (accurate within targetTDBs)
        Primary use-case would be for stars from NBody ...
        ... but it could be used for 2Body (however wasteful that might be, it'll be useful for testing and development)
        
        This could be chebyshev
        
        Need to think in more detail about ...
        (i) is this ever going to be used over multiple nights, or just single-night validity ?
        
        Parameters
        ----------
        
        Returns
        -------
        
        Examples
        --------
        >>> import mpcadvancer
        >>> ics = ORBIT_ICs(something)
        >>> a   = ADVANCE(ics)
        >>> t   = a.nbody(targetTDBs)
        >>> f   = t.createFunctionalRepresentation()
        '''



class ADVANCE:
    '''
    Advances ORBIT_ICs to requested TDBs, returns TARGET_STATES
    
    Assumes ORBIT_ICs contain 
    (i) cartesian HELIOCENTRIC ECLIPTIC CARTESIAN ICs;
    (ii) common initial time, iTDB
    
    Provides top-level-wrappers around various methods to advance orbits
    (a) keplerian; (b) n-body; (c) polynomial (e.g. cheby)
    
    Need to think about uniform-versus-nonuniform target-times:
    - fitting observations will require non-uniform
    - for n-body, suspect passing to cheby/poly-func will be easiest
    
    Returns
    -------
    
    Examples
    --------
    >>> import mpcadvancer
    >>> ics = ORBIT_ICs(something)
    >>> a   = ADVANCE(ics)
    >>> t   = a.twobody(targetTDBs)
    '''



    def __init__(self, orbit_ics ):
        '''
        Must initialize with a valid ORBIT_ICs object
        
        Parameters
        ----------
        orbit_ics   :   ORBIT_ICs-class

        '''

        # Add assertions to assure contents
        #  - after development-phase, could disable assertions
        assert hasattr(orbit_ics, 'cartStateArray') # <<-- This might change 
        assert hasattr(orbit_ics, 'iTDB')
        assert hasattr(orbit_ics, 'ICtype')
        # Will require additional attributed in future ...



    def twobody(targetTDBs):
        '''
        Implements universal-kepler-stepper to advance orbit(s)
        
        Parameters
        ----------
        targetTDBs       : list of floats
            Epochs at which to generate output.
            Length = N_T
        
        Returns
        -------
        targets          : TARGET_STATES-object
            Contains the output coordinates in 
            HELIOCENTRIC ECLIPTIC CARTESIANS as specified in 
            the TARGET_STATES class
        
        Examples
        --------
        >>> ...
        
        '''
    
        # For nominal-only orbit:
        # - use universal_stepper with var=tangent=False
        if orbit_ics.ICtype == "Nominal"        :
            # Temporary hack.
            # Using a slower indirect method
            # Should be replaced by a method that does direct advance of cartesians using f & g
            #targetTDBs, targetStateArrays = advance_cartesian_states_2body_INDIRECT(cartStateArray, iTDB , targetTDBs)
            #targetTangent = False
            fakeOutput = None
    
        # For nominal + tangent:
        # - use universal_stepper with var=tangent=True
        elif orbit_ics.ICtype == "Tangent"      :
            fakeOutput = None
    
        # For uncertainty-region:
        # - not sure yet ...
        elif orbit_ics.ICtype == "Uncertainty"  :
            fakeOutput = None

        # Shouldn't be able to get here ...
        else:
            sys.exit("orbit_ics.ICtype of unknown type: $r"%orbit_ics.ICtype)

        # Might need to do some work to create the output TARGET_STATES-object
        targets = TARGET_STATES(fakeOutput)
        
        return targets



    def nbody(targetTDBs, nbodyPARAMS):
        '''
        Implements N-body method to advance orbit(s)
        
        Parameters
        ----------
        targetTDBs          : list of floats
            Epochs at which to generate output.
            Length = N_T
        nbodyPARAMS         : dictionary
            We'll need to do something to specify the various
            parameters needed by the n-body integrator
        
        Returns
        -------
        targets          : TARGET_STATES-object
            Contains the output coordinates in
            HELIOCENTRIC ECLIPTIC CARTESIANS as specified in
            the TARGET_STATES class
        
        Examples
        --------
        >>> ...
        
        '''
            
        # For nominal-only orbit:
        if orbit_ics.ICtype == "Nominal"        :
            fakeOutput = None

        # For nominal + tangent:
        elif orbit_ics.ICtype == "Tangent"      :
            fakeOutput = None

        # For uncertainty-region:
        elif orbit_ics.ICtype == "Uncertainty"  :
            fakeOutput = None

        # Shouldn't be able to get here ...
        else:
            sys.exit("orbit_ics.ICtype of unknown type: $r"%orbit_ics.ICtype)


        # Might need to do some work to create the output TARGET_STATES-object
        targets = TARGET_STATES(fakeOutput)

        return targets

















"""
def advance_cartesian_states_2body_INDIRECT(cartStateArray, iTDB , targetTDBs):
    '''
    Temporary hack.
    Using a slower indirect method to advance input cartesian states to requested TDBs ...
    ... using Keplerian (2-body) method
    Should be replaced by a method that does direct advance of cartesians using f & g
    
    Parameters
    ----------
    cartStateArray      : "CartStateArray" Object-type as defined in MPCFormat.
    Set of HELIOCENTRIC ECLIPTIC CARTESIAN initial conditions.
    Length = N_s
    N.B. Heliocentric cartesians converson routines in MPCFormat
    iTDB                : float
    The initial epoch, in TDB-units, for the coordinates in cartStateArray
    N.B. Time-conversions can be done using routines in MPCUtilities
    targetTDBs          : list of floats
    Epochs at which to generate output.
    Length = N_T
    
    Returns
    -------
    targetTDBs          : list of floats
    Echo of input List/Array of Epochs at which output is generated.
    targetStateArrays   : Array of StateArrays
    Contains the output coordinates in HELIOCENTRIC ECLIPTIC CARTESIANS
    Has dimensions N_t * N_s
    
    Examples
    --------
    >>> ...
    
    '''
    
    # Because this is the clunky "INDIRECT" version ...
    # ... we convert input cartesian states to keplerian elements
    # N.B.  [angles in radians] , Mean motions, n, [radians/day]
    
    #a, e, incl, longnode, argperi, meananom =   kc.keplerians(len(state_epoch_array), PHYS.GMsun , SA_ )
    a, e, incl, longnode, argperi, meananom =   MPCFormat.cart2kep(len(state_epoch_array), PHYS.GMsun , cartStateArray )
    n = np.sqrt(PHYS.GMsun/(a**3))
    
    # For convenience, repeat(tile) for each time of interest so that they form single long arrays
    N_t      = len(targetTDBs)
    a        = np.tile(a,         N_t)
    e        = np.tile(e,         N_t )
    incl     = np.tile(incl,      N_t )
    longnode = np.tile(longnode,  N_t )
    argperi  = np.tile(argperi,   N_t )
    meananom = np.tile(meananom,  N_t )
    n        = np.tile(n,         N_t )
    
    # Calculate MeanAnomalies at times
    dt             = np.array(targetTDBs) - iTDB
    MAs_at_ObsTime = meananom  + n * dt
    
    # Heliocentric cartesians for those shifted meananomalies
    #posns, vels           = kc.cartesian_vectors(len(MAs_at_ObsTime), PHYS.GMsun,    a, e, incl, longnode, argperi,    MAs_at_ObsTime)
    posns, vels           = MPCFormat.kep2cart_vectors(len(MAs_at_ObsTime), PHYS.GMsun,    a, e, incl, longnode, argperi,    MAs_at_ObsTime)
    posns, vels           = np.array(posns).reshape((-1,3)), np.array(vels).reshape((-1,3))
    
    # Populate the output
    # - inefficient, but then the whole function is unnecessary, so futile to optimize
    targetStateArrays           = (MPCFormat.CartState*len(posns))()
    for i,xyz,uvw in zip( range(len(posns)) , posns, vels  ):
        targetStateArrays[i].state.x, targetStateArrays[i].state.y, targetStateArrays[i].state.z    = np.split(xyz,3)
        targetStateArrays[i].state.xd, targetStateArrays[i].state.yd, targetStateArrays[i].state.zd = np.split(uvw,3)
    
    return targetTDBs , targetStateArrays
"""







