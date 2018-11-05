# /mpcutilities/mpcutilities/universal-kepler.py
"""
# --------------------------------------------------------------
# Nov 2018
# Payne 
#
# Use C to do fast universal kepler step (advance cartesian state)
#
# --------------------------------------------------------------
"""

# Import third-party packages
# --------------------------------------------------------------
import os
import numpy as np
from ctypes import *

# Importing of local modules/packages
# --------------------------------------------------------------
import mpcutilities.classes     as Classes

# Import local files / dirs  
# --------------------------------------------------------------
lib = CDLL(os.path.join(os.path.dirname(__file__), 'universal_step.so'))


# Define "kepcart" routines
# --------------------------------------------------------------


THIS PYTHON WRAPPER OF universal_step IS HEAVILY INCOMPLETE 


def universal_step(GM, dt, inputCartState, evalPartial):
    """
    Take a kepler step in universal variables
    For evolution of a SINGLE body's cartesian state
    by a SINGLE timestep
    
    *** USES A CALL TO C-CODE***
    
    Parameters
    ----------
    GM              : float,
        Constant
    dt              : float
        Time step (days?)
    inputCartState       : "CartState" Object-type as defined in MPCFormat.
        Probably assumes HELIOCENTRIC ECLIPTIC CARTESIAN initial conditions
    evalPartial     : Boolean
        Whether or not to evaluate partial-derivative matrix
    
    Returns
    -------
    finalCartState  : "CartState"   Object-type as defined in ...
        Cartesian state at time dt (evolved from input cartState)
    finalCartPartial: "CartPartial" Object-type as defined in ...
        Partial derivatives of finalCartState w.r.t. components of input cartState
        *** AM PASSING THIS BACK AS ZEROES IF PARTIALS ARE NOT EVALUATED ***
    
    Examples
    --------
    >>> ...
    
    """
    
    
    
    finalCartState  = Classes.CartState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cartPartial     = Classes.CartPartial(0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    _universal_step          = lib.universal_step
    _universal_step.argtypes = (c_double, c_double, inputCartState, POINTER(Classes.CartState), c_bool, POINTER(Classes.CartPartial))
    _universal_step.restype  = None
    
    return_value = _universal_step(GM, dt, inputCartState,
                                   byref(finalCartState),
                                   evalPartial,
                                   byref(cartPartial),
                                   )
                                   
    return finalCartState, cartPartial




def universal_steps(GM, timeArray, inputCartState, evalPartial, timeSteps=False):
    """
    Version of universal_step that takes a kepler step in universal variables
    For evolution of a SINGLE body's cartesian state
    by MULTIPLE timesteps
    
    *** USES A CALL TO C-CODE***
    
    Parameters
    ----------
    GM              : float,
        Constant
    dtArray         : ndarray
        Used to specify integration timesteps
        See "timeSteps" below for further detail
    inputCartState  : "CartState" Object-type as defined in MPCFormat.
        Probably assumes HELIOCENTRIC ECLIPTIC CARTESIAN initial conditions
    evalPartial     : Boolean
        Whether or not to evaluate partial-derivative matrix
    timeSteps       : Boolean, optional
        If timeSteps == False (default):
            # => timeArray assumed absolute (with cartState @ t=0) 
            # => Need to derive timesteps
            # e.g. timeArray = [2,3,4]  => dtArray = [2,1,1]
        If timeSteps == True:
            # => timeArray defines individual step sizes
            # e.g. timeArray = [1,1,1]  => dtArray = [1,1,1]
    Returns
    -------
   
    
    Examples
    --------
    >>> ...
    
    """

    # Ensure it is an array
    timeArray = np.array(timeArray)
    # Make into individual timesteps (if not already input like that)
    if timeSteps:
        dtArray = timeArray
    else:
        dtArray = timeArray - np.append( [0], timeArray[:-1])

    # Convenient arrays to hold the output
    num                 = len(dtArray)
    finalStateArray     = Classes.CartState * num
    finalPartialArray   = Classes.CartState * num

    # Make repeated calls to universal_step
    for i, dt in enumerate(dtArray):
        if i ==0 :
            finalStateArray[i],finalPartialArray[i] = universal_step(GM, dt, inputCartState,       evalPartial)
        else:
            finalStateArray[i],finalPartialArray[i] = universal_step(GM, dt, finalStateArray[i-1], evalPartial)

    return finalStateArray,finalPartialArray





def universal_multistep(GM, dt, inputCartStateArray, evalPartial):
    """
    Version of universal_step that takes a kepler step in universal variables
    For the evolution of MULTIPLE cartesian states
    by a SINGLE timestep
    
    *** USES A CALL TO C-CODE***
        
    My tentative idea is that this could also be used to handle propagation of the
    *** UNCERTAINTY *** regions
    My working hypothesis is that this is going to be
    evaluated/propagated using a "bundle" of orbits
    I.e. This will be passed in as an "inputCartStateArray", the same as for any
    generic collection of states
    
    
    Parameters
    ----------
    GM                      : float,
        Constant
    dt                      : float
        Time step (days?)
    inputCartStateArray     : "CartStateArray" Object-type as defined in MPCFormat.
        Probably assumes HELIOCENTRIC ECLIPTIC CARTESIAN initial conditions
    
    Returns
    -------
    finalCartStateArray     : "CartStateArray"   Object-type as defined in ...
        Array of cartesian states at time dt (evolved from input cartStateArray)
    finalCartPartialArray   : "CartPartialArray" Object-type as defined in ...
        Partial derivatives of finalCartStates w.r.t. components of input cartState
        *** AM PASSING THIS BACK AS ZEROES IF PARTIALS ARE NOT EVALUATED ***
    
    Examples
    --------
    >>> ...
    
    """
    
    # Convenient arrays to hold the output
    num                 = len(inputCartStateArray)
    finalStateArray     = Classes.CartState * num
    finalPartialArray   = Classes.CartState * num
    
    
    _universal_step          = lib.universal_step
    _universal_step.argtypes = (c_double, c_double, inputCartState, POINTER(Classes.CartState), c_bool, POINTER(Classes.CartPartial))
    _universal_step.restype  = None
    
    # Loop over each of the input cartesian states (i.e. orbits)
    for i, inputCartState in enumerate(inputCartStateArray):
        # To be passed in byref
        finalCartState      = Classes.CartState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        finalcartPartial    = Classes.CartPartial(0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        return_value = _universal_step(GM, dt, inputCartState,  byref(finalCartState), evalPartial, byref(finalcartPartial))
        finalStateArray[-1] = finalCartState
        finalPartialArray[-1] =
    return finalStateArray, finalPartialArray



def universal_multisteps(GM, timeArray, inputCartStateArray, evalPartial,timeSteps=False):
    """
    Version of universal_step that takes a kepler step in universal variables
    For the evolution of MULTIPLE cartesian states
    by MULTIPLE timesteps
    
    *** USES A CALL TO C-CODE***
    
    Parameters
    ----------
    GM                      : float,
        Constant
    dtArray         : ndarray
        Used to specify integration timesteps
        See "timeSteps" below for further detail
    inputCartStateArray     : "CartStateArray" Object-type as defined in MPCFormat.
        Probably assumes HELIOCENTRIC ECLIPTIC CARTESIAN initial conditions
    evalPartial     : Boolean
        Whether or not to evaluate partial-derivative matrix
    timeSteps       : Boolean, optional
        If timeSteps == False (default):
            # => timeArray assumed absolute (with cartState @ t=0)
            # => Need to derive timesteps
            # e.g. timeArray = [2,3,4]  => dtArray = [2,1,1]
        If timeSteps == True:
            # => timeArray defines individual step sizes
            # e.g. timeArray = [1,1,1]  => dtArray = [1,1,1]
    
    Returns
    -------
    finalCartStateArray     : "CartStateArray"   Object-type as defined in ...
    Array of cartesian states at time dt (evolved from input cartStateArray)
    finalCartPartialArray   : "CartPartialArray" Object-type as defined in ...
    Partial derivatives of finalCartStates w.r.t. components of input cartState
    *** AM PASSING THIS BACK AS ZEROES IF PARTIALS ARE NOT EVALUATED ***
    
    Examples
    --------
    >>> ...
    
    """
    # Ensure it is an array
    timeArray = np.array(timeArray)
    # Make into individual timesteps (if not already input like that)
    if timeSteps:
        dtArray = timeArray
    else:
        dtArray = timeArray - np.append( [0], timeArray[:-1])

    # Convenient arrays to hold the output
    numT                 = len(dtArray)
    numS                 = len(inputCartStateArray)
    finalStateArray     = Classes.CartState * numS * numT
    finalPartialArray   = Classes.CartState * numS * numT

    # Make repeated calls to universal_multistep
    for i, dt in enumerate(dtArray):
        if i ==0 :
            interimStateArray, interimPartialArray = universal_multistep(GM, dt, inputCartStateArray, evalPartial)
        else:
            interimStateArray, interimPartialArray = universal_multistep(GM, dt, interimStateArray,   evalPartial)

        for j, _  in zip(interimStateArray, interimPartialArray):
            finalStateArray[i*numS+j],finalPartialArray[i*numS+j] = _[0],_[1]

    return finalStateArray, finalPartialArray




