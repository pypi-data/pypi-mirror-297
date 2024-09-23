from __future__ import annotations
__all__ = ['planks_law_sr', 'planks_law_sr_deriv_T', 'planks_law_sr_deriv_lambda', 'planks_law_sr_nm', 'planks_law_sr_um', 'stefan_boltzmann_law', 'stefan_boltzmann_law_surface', 'wiens_displacement_law_T', 'wiens_displacement_law_lambda']
def planks_law_sr(T: float, lambda: float) -> float:
    """
        Calculates the spectral radiance using Planck's Law for a black body.

        This function computes the spectral radiance of a black body as a function
        of temperature (T) and wavelength (lambda) in units of W/(sr m^2)/m.

        :param T: Temperature in Kelvin.
        :param lambda: Wavelength in meters.
        :return: Spectral radiance in W/(sr m^2)/m.
    """
def planks_law_sr_deriv_T(T: float, lambda: float) -> float:
    """
        Computes the partial derivative of Planck's Law w.r.t. temperature.

        This function calculates the partial derivative of the spectral radiance
        formula (Planck's Law) with respect to temperature (T).

        :param T: Temperature in Kelvin.
        :param lambda: Wavelength in meters.
        :return: Partial derivative of spectral radiance w.r.t. temperature.
    """
def planks_law_sr_deriv_lambda(T: float, lambda: float) -> float:
    """
        Computes the partial derivative of Planck's Law w.r.t. wavelength.

        This function calculates the partial derivative of the spectral radiance
        formula (Planck's Law) with respect to wavelength (lambda).

        :param T: Temperature in Kelvin.
        :param lambda: Wavelength in meters.
        :return: Partial derivative of spectral radiance w.r.t. wavelength.
    """
def planks_law_sr_nm(T: float, lambda: float) -> float:
    """
        Calculates the spectral radiance using Planck's Law for a black body.

        This function computes the spectral radiance of a black body as a function
        of temperature (T) and wavelength (lambda) in units of W/(sr m^2)/nm.

        :param T: Temperature in Kelvin.
        :param lambda: Wavelength in nanometers.
        :return: Spectral radiance in W/(sr m^2)/nm.
    """
def planks_law_sr_um(T: float, lambda: float) -> float:
    """
        Calculates the spectral radiance using Planck's Law for a black body.

        This function computes the spectral radiance of a black body as a function
        of temperature (T) and wavelength (lambda) in units of W/(sr m^2)/um.

        :param T: Temperature in Kelvin.
        :param lambda: Wavelength in micrometers.
        :return: Spectral radiance in W/(sr m^2)/um.
    """
def stefan_boltzmann_law(T: float) -> float:
    """
        Applies the Stefan-Boltzmann law to compute energy radiated per unit area.

        This function computes the total energy radiated per unit surface area of a
        black body across all wavelengths per unit time as a function of temperature (T).

        :param T: Temperature in Kelvin.
        :return: Total energy radiated per unit area (W/m^2).
    """
def stefan_boltzmann_law_surface(T: float, A: float, epsilon: float) -> float:
    """
        Applies the Stefan-Boltzmann law to compute energy radiated from a surface.

        This function computes the total energy per unit time radiated from a surface
        of area A (in m^2) with a given emissivity and temperature (T) using the
        Stefan-Boltzmann law.

        :param T: Temperature in Kelvin.
        :param A: Surface area in square meters.
        :param epsilon: Emissivity of the surface (0 <= epsilon <= 1).
        :return: Total energy radiated from the surface (W).
    """
def wiens_displacement_law_T(lambda: float) -> float:
    """
        Applies Wien's displacement law to compute temperature from wavelength.

        This function computes the temperature (T) in Kelvin for a given wavelength
        (lambda) in meters using Wien's displacement law.

        :param lambda: Wavelength in meters.
        :return: Temperature in Kelvin.
    """
def wiens_displacement_law_lambda(T: float) -> float:
    """
        Applies Wien's displacement law to compute wavelength from temperature.

        This function computes the wavelength (lambda) in meters for a given temperature
        (T) in Kelvin using Wien's displacement law.

        :param T: Temperature in Kelvin.
        :return: Wavelength in meters.
    """
