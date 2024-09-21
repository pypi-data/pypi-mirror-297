import numpy as np
from FlowCyPy import Scatterer, Detector, Source
from FlowCyPy import ureg
from PyMieSim.single.scatterer import Sphere as PMS_SPHERE
from PyMieSim.single.source import Gaussian as PMS_GAUSSIAN
from PyMieSim.single.detector import Photodiode as PMS_PHOTODIODE
from FlowCyPy.units import meter, watt, degree


def compute_detected_signal(source: Source, detector: Detector, scatterer: Scatterer) -> float:
    """
    Empirical model for scattering intensity based on particle size, granularity, and detector angle.

    This function models forward scatter (FSC) as proportional to the particle's size squared and
    side scatter (SSC) as proportional to the granularity and modulated by angular dependence
    (sin^n(theta)). Granularity is a dimensionless measure of the particle's internal complexity or
    surface irregularities:

    - A default value of 1.0 is used for moderate granularity (e.g., typical white blood cells).
    - Granularity values < 1.0 represent smoother particles with less internal complexity (e.g., bacteria).
    - Granularity values > 1.0 represent particles with higher internal complexity or surface irregularities (e.g., granulocytes).

    Parameters
    ----------
    detector : Detector
        The detector object containing phi_angle (in radians).
    particle_size : float
        The size of the particle (in meters).
    granularity : float, optional
        A measure of the particle's internal complexity or surface irregularities (dimensionless).
        Default is 1.0.
    A : float, optional
        Empirical scaling factor for angular dependence. Default is 1.5.
    n : float, optional
        Power of sine function for angular dependence. Default is 2.0.

    Returns
    -------
    float
        The detected scattering intensity for the given particle and detector.
    """
    pms_source = PMS_GAUSSIAN(
        wavelength=source.wavelength.to(meter).magnitude,
        polarization=0,
        optical_power=source.optical_power.to(watt).magnitude,
        NA=source.numerical_aperture
    )

    size_list = scatterer.dataframe['Size'].pint.to(meter).values.numpy_data
    ri_list = scatterer.dataframe['RefractiveIndex'].values.numpy_data
    couplings = np.empty_like(size_list)

    for index, (size, ri) in enumerate(zip(size_list, ri_list)):

        pms_scatterer = PMS_SPHERE(
            diameter=size,
            index=ri,
            medium_index=scatterer.medium_refractive_index,
            source=pms_source
        )

        pms_detector = PMS_PHOTODIODE(
            NA=detector.numerical_aperture,
            gamma_offset=detector.gamma_angle.to(degree).magnitude,
            phi_offset=detector.phi_angle.to(degree).magnitude,
            polarization_filter=None,
            sampling=detector.sampling
        )

        couplings[index] = pms_detector.coupling(pms_scatterer)


    return couplings * ureg.watt
