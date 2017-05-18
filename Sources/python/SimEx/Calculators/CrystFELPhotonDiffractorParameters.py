##########################################################################
#                                                                        #
# Copyright (C) 2016-2017 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

""" Module that holds the CrystFELPhotonDiffractorParameters class.  """
import os

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Utilities.EntityChecks import checkAndSetInstance

class CrystFELPhotonDiffractorParameters(AbstractCalculatorParameters):
    """
    Class representing parameters for the CrystFELPhotonDiffractor calculator.
    """
    def __init__(self,
                uniform_rotation=None,
                number_of_diffraction_patterns=None,
                powder=None,
                intensities_file=None,
                crystal_size_range=None,
                poissonize=None,
                number_of_background_photons=None,
                suppress_fringes=None,
                beam_parameter_file=None,
                beam_geometry_file=None,
                number_of_MPI_processes=None,
                **kwargs,
                ):
        """
        Constructor for the CrystFELPhotonDiffractorParameters.

        :param uniform_rotation: Whether to perform uniform sampling of rotation space.
        :type uniform_rotation: bool, default True

        :param powder: Whether to sum all patterns to generate a simulated powder diffraction pattern.
        :type powder: bool

        :param intensities_file: Location of file that contains intensities and phases at reciprocal lattice points. See CrystFEL documentation for more info. Default: Constant intensities and phases across entire sample.
        :type intensities_file: str

        :param crystal_size_range: (Min,Max) tuple specifying the minimum and maximum of crystal sizes to sample.
        :type crystal_size_range: tuple or list of length 2

        :param poissonize: Whether to add Poisson noise to pixel values.
        :type poissonize: bool

        :param number_of_background_photons: Add this number of Poisson distributed photons uniformly over the detector surface (default 0).
        :type number_of_background_photons: int

        :param number_of_diffraction_patterns: Number of diffraction patterns to calculate from each trajectory.
        :type number_of_diffraction_patterns: int, default 1

        :param suppress_fringes: Whether to suppress subsidiary maxima beyond first minimum of the shape transform (default False).
        :type suppress_fringes: bool

        :param beam_parameter_file: Path of the beam parameter file.
        :type beam_parameter_file: str

        :param beam_geometry_file: Path of the beam geometry file.
        :type beam_geometry_file: str

        :param number_of_MPI_processes: Number of MPI processes
        :type number_of_MPI_processes: int, default 1

        :param kwargs: Key-value pairs to pass to the parent class.
        """



        # Check all parameters.
        self.uniform_rotation = uniform_rotation
        self.powder = powder
        self.intensities_file = intensities_file
        self.crystal_size_range = crystal_size_range
        self.poissonize = poissonize
        self.number_of_background_photons = number_of_background_photons
        self.suppress_fringes = suppress_fringes
        self.number_of_MPI_processes=number_of_MPI_processes
        self.beam_parameter_file = beam_parameter_file
        self.beam_geometry_file = beam_geometry_file
        self.number_of_diffraction_patterns = number_of_diffraction_patterns

        super(CrystFELPhotonDiffractorParameters, self).__init__(**kwargs)

    def _setDefaults(self):
        """ Set default for required inherited parameters. """
        self._AbstractCalculatorParameters__cpus_per_task_default = 1

    ### Setters and queries.
    @property
    def powder(self):
        """ Query the 'powder' parameter. """
        return self.__powder
    @powder.setter
    def powder(self, val):
        """ Set the 'powder' parameter to val."""
        self.__powder = checkAndSetInstance( bool, val, False)

    @property
    def intensities_file(self):
        """ Query the 'intensities_file' parameter. """
        return self.__intensities_file
    @intensities_file.setter
    def intensities_file(self, val):
        """ Set the 'intensities_file' parameter to val."""
        self.__intensities_file = checkAndSetInstance( str, val, "")

    @property
    def crystal_size_range(self):
        """ Query the 'crystal_size_range' parameter. """
        return self.__crystal_size_range
    @crystal_size_range.setter
    def crystal_size_range(self, val):
        """ Set the 'crystal_size_range' parameter to val."""
        self.__crystal_size_range = checkAndSetInstance( tuple, val, (,))

    @property
    def poissonize(self):
        """ Query the 'poissonize' parameter. """
        return self.__poissonize
    @poissonize.setter
    def poissonize(self, val):
        """ Set the 'poissonize' parameter to val."""
        self.__poissonize = checkAndSetInstance( bool, val, False)

    @property
    def number_of_background_photons(self):
        """ Query the 'number_of_background_photons' parameter. """
        return self.__number_of_background_photons
    @number_of_background_photons.setter
    def number_of_background_photons(self, val):
        """ Set the 'number_of_background_photons' parameter to val."""
        self.__number_of_background_photons = checkAndSetInstance( int, val, 0)

    @property
    def suppress_fringes(self):
        """ Query the 'suppress_fringes' parameter. """
        return self.__suppress_fringes
    @suppress_fringes.setter
    def suppress_fringes(self, val):
        """ Set the 'suppress_fringes' parameter to val."""
        self.__suppress_fringes = checkAndSetInstance( bool, val, False)

    #@property
    #def xxx(self):
        #""" Query the 'xxx' parameter. """
        #return self.__xxx
    #@xxx.setter
    #def xxx(self, val):
        #""" Set the 'xxx' parameter to val."""
        #self.__xxx = checkAndSetInstance( ttt, val, default)

    @property
    def uniform_rotation(self):
        """ Query for the 'uniform_rotation' parameter. """
        return self.__uniform_rotation
    @uniform_rotation.setter
    def uniform_rotation(self, value):
        """ Set the 'uniform_rotation' parameter to a given value.
        :param value: The value to set 'uniform_rotation' to.
        """
        self.__uniform_rotation = checkAndSetInstance( bool, value, True )

    @property
    def beam_parameter_file(self):
        """ Query for the 'beam_parameter_file' parameter. """
        return self.__beam_parameter_file
    @beam_parameter_file.setter
    def beam_parameter_file(self, value):
        """ Set the 'beam_parameter_file' parameter to a given value.
        :param value: The value to set 'beam_parameter_file' to.
        """
        self.__beam_parameter_file = checkAndSetInstance( str, value, None )

        if self.__beam_parameter_file is not None:
            if not os.path.isfile( self.__beam_parameter_file):
                raise IOError("The beam_parameter_file %s is not a valid file or filename." % (self.__beam_parameter_file) )
        else:
            print ("WARNING: Beam parameter file not set, calculation will most probably fail.")


    @property
    def beam_geometry_file(self):
        """ Query for the 'beam_geometry_file' parameter. """
        return self.__beam_geometry_file
    @beam_geometry_file.setter
    def beam_geometry_file(self, value):
        """ Set the 'beam_geometry_file' parameter to a given value.
        :param value: The value to set 'beam_geometry_file' to.
        """
        self.__beam_geometry_file = checkAndSetInstance( str, value, None )

        if self.__beam_geometry_file is not None:
            if not os.path.isfile( self.__beam_geometry_file):
                raise IOError("The beam_parameter_file %s is not a valid file or filename." % (self.__beam_geometry_file) )
        else:
            print ("WARNING: Geometry file not set, calculation will most probably fail.")


    @property
    def number_of_diffraction_patterns(self):
        """ Query for the 'number_of_diffraction_patterns_file' parameter. """
        return self.__number_of_diffraction_patterns
    @number_of_diffraction_patterns.setter
    def number_of_diffraction_patterns(self, value):
        """ Set the 'number_of_diffraction_patterns' parameter to a given value.
        :param value: The value to set 'number_of_diffraction_patterns' to.
        """
        number_of_diffraction_patterns = checkAndSetInstance( int, value, 1 )

        if number_of_diffraction_patterns > 0:
            self.__number_of_diffraction_patterns = number_of_diffraction_patterns
        else:
            raise ValueError("The parameters 'number_of_diffraction_patterns' must be a positive integer.")
