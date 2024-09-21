
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from FlowCyPy.units import Quantity, meter, watt, distance, power, joule, second, particle
from FlowCyPy.utils import PropertiesReport
import numpy as np


config_dict = dict(
    arbitrary_types_allowed=True,
    kw_only=True,
    slots=True,
    extra='forbid'
)


@dataclass(config=config_dict)
class Source(PropertiesReport):
    """
    optical_power : Quantity
        The optical power of the laser (in watts).
    wavelength : Quantity
        The wavelength of the laser (in meters).
    """
    optical_power: Quantity
    wavelength: Quantity
    numerical_aperture: float
    name: str = 'Laser source'

    @field_validator('optical_power')
    def validate_sampling_freq(cls, value):
        """
        Validates that the optical power is provided in watts.

        Args:
            value (Quantity): The optical power to validate.

        Returns:
            Quantity: The validated optical power.

        Raises:
            ValueError: If the optical power is not in watts.
        """
        if not value.check('watt'):
            raise ValueError(f"optical_power must be in watt, but got {value.units}")
        return value

    @field_validator('wavelength')
    def validate_sampling_freq(cls, value):
        """
        Validates that the wavelength is provided in meters.

        Args:
            value (Quantity): The wavelength to validate.

        Returns:
            Quantity: The validated wavelengths.

        Raises:
            ValueError: If the wavelength is not in meters.
        """
        if not value.check('meter'):
            raise ValueError(f"optical_power must be in meter, but got {value.units}")
        return value

    def __post_init__(self) -> None:
        """
        Initialize additional parameters after class instantiation by assigning physical units to parameters.
        """
        # Calculate Gaussian beam waist at the focus
        self.waist = self.wavelength / (np.pi * self.numerical_aperture)


        h = 6.62607015e-34 * joule * second  # Planck constant
        c = 3e8 * meter / second  # Speed of light

        self.frequency = c / self.wavelength
        self.photon_energy = (h * self.frequency).to(joule) / particle
