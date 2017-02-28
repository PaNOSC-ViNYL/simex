##########################################################################
#                                                                        #
# Copyright (C) 2016,2017 Carsten Fortmann-Grote                         #
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

""" Test module for the EstherPhotonMatterInteractorParameter class.

    @author : CFG
    @institution : XFEL
    @creation 20160219

"""
import paths
import os
import numpy
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Import the class to test.
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import EstherPhotonMatterInteractorParameters
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetNumberOfLayers
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetAblator
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetAblatorThickness
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetSample
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetSampleThickness
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetWindow
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetWindowThickness
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserWavelength
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserPulse
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserPulseDuration
from SimEx.Parameters.EstherPhotonMatterInteractorParameters import checkAndSetLaserIntensity

class EstherPhotonMatterInteractorParametersTest(unittest.TestCase):
    """
    Test class for the EstherPhotonMatterInteractorParameters class.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

        self.esther_parameters = EstherPhotonMatterInteractorParameters(
                                         number_of_layers=5,
                                         ablator="CH",
                                         ablator_thickness=10.0,
                                         sample="Iron",
                                         sample_thickness=20.0,
                                         window=None,
                                         window_thickness=0.0,
                                         laser_wavelength=800.0,
                                         laser_pulse='flat',
                                         laser_pulse_duration=1.0,
                                         laser_intensity=0.1,
                                                         )

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        esther_parameters = self.esther_parameters
        # Check instance and inheritance.
        self.assertIsInstance( esther_parameters, EstherPhotonMatterInteractorParameters )
        self.assertIsInstance( esther_parameters, AbstractCalculatorParameters )

    def testCheckAndSetNumberOfLayers(self):
        """ Test the check and set method for number of layers. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, "one")
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, "1")
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, [1,2])
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, 10.5)
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, self.esther_parameters)
        self.assertRaises( TypeError, checkAndSetNumberOfLayers, {"1" : "one"})

        # Value raises.
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, 0)
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, 1)
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, 6)
        self.assertRaises( ValueError, checkAndSetNumberOfLayers, -3)

        # Ok.
        self.assertEqual( checkAndSetNumberOfLayers(3), 3)

    def testCheckAndSetAblator(self):
        """ Test the check and set method for the ablator material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetAblator, 1 )
        self.assertRaises( TypeError, checkAndSetAblator, 1.5 )
        self.assertRaises( TypeError, checkAndSetAblator, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetAblator, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetAblator("CH"), "CH" )

    def testCheckAndSetAblatorThickness(self):
        """ Test the check and set method for the ablator thickness. """

        self.assertRaises( TypeError, checkAndSetAblatorThickness, 1 )
        self.assertRaises( TypeError, checkAndSetAblatorThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetAblatorThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetAblator, -10.0 )
        self.assertRaises( ValueError, checkAndSetAblator, 0.0 )

        self.assertEqual( checkAndSetAblatorThickness(10.0), 10.0 )


    def testCheckAndSetSample(self):
        """ Test the check and set method for the sample material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetSample, 1 )
        self.assertRaises( TypeError, checkAndSetSample, 1.5 )
        self.assertRaises( TypeError, checkAndSetSample, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetSample, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetSample("CH"), "CH" )

    def testCheckAndSetSampleThickness(self):
        """ Test the check and set method for the ablator thickness. """

        self.assertRaises( TypeError, checkAndSetSampleThickness, 1 )
        self.assertRaises( TypeError, checkAndSetSampleThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetSampleThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetSample, -10.0 )
        self.assertRaises( ValueError, checkAndSetSample, 0.0 )

        self.assertEqual( checkAndSetSampleThickness(10.0), 10.0 )

    def testCheckAndSetWindow(self):
        """ Test the check and set method for the sample material. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetWindow, 1 )
        self.assertRaises( TypeError, checkAndSetWindow, 1.5 )
        self.assertRaises( TypeError, checkAndSetWindow, ["Aluminum", "CH"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetWindow, "Boron" )

        # Ok.
        self.assertEqual( checkAndSetWindow("LiF"), "LiF" )

    def testCheckAndSetWindowThickness(self):
        """ Test the check and set method for the ablator thickness. """

        self.assertRaises( TypeError, checkAndSetWindowThickness, 1 )
        self.assertRaises( TypeError, checkAndSetWindowThickness, "ten microns" )
        self.assertRaises( TypeError, checkAndSetWindowThickness, [10.0, 10.0] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetWindow, -10.0 )
        self.assertRaises( ValueError, checkAndSetWindow, 0.0 )

        self.assertEqual( checkAndSetWindowThickness(10.0), 10.0 )

    def testCheckAndSetLaserWavelength(self):
        """ Test the check and set method for the laser wavelength. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserWavelength, 1 )
        self.assertRaises( TypeError, checkAndSetLaserWavelength, [100.0, 1024.0] )
        self.assertRaises( TypeError, checkAndSetLaserWavelength, "2 omega" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserWavelength, -1024.0 )

        self.assertEqual( checkAndSetLaserWavelength( 800.0 ) , 800.0 )

    def testCheckAndSetLaserPulse(self):
        """ Test the check and set method for the laser pulse type. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserPulse, 1 )
        self.assertRaises( TypeError, checkAndSetLaserPulse, 1.0 )
        self.assertRaises( TypeError, checkAndSetLaserPulse, ["flat", "ramp"] )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserPulse, "rectangular" )

        self.assertEqual( checkAndSetLaserPulse("flat"), "flat")
        self.assertEqual( checkAndSetLaserPulse("ramp"), "ramp")
        self.assertEqual( checkAndSetLaserPulse("other"), "other")

    def testCheckAndSetLaserPulseDuration(self):
        """ Test the check and set method for the laser pulse duration. """

        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserPulseDuration, 1 )
        self.assertRaises( TypeError, checkAndSetLaserPulseDuration, [10.0, 24.0] )
        self.assertRaises( TypeError, checkAndSetLaserPulseDuration, "2 ns" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserPulseDuration, -10.0 )

        self.assertEqual( checkAndSetLaserPulseDuration( 0.1 ) , 0.1 )


    def testCheckAndSetLaserIntensity(self):
        """ Test the check and set method for the laser intensity. """
        # Type raises.
        self.assertRaises( TypeError, checkAndSetLaserIntensity, 1 )
        self.assertRaises( TypeError, checkAndSetLaserIntensity, [0.1, 0.2] )
        self.assertRaises( TypeError, checkAndSetLaserIntensity, "2 TW/cm2" )

        # Value raises.
        self.assertRaises( ValueError, checkAndSetLaserIntensity, -1.0 )

        self.assertEqual( checkAndSetLaserIntensity( 0.1 ) , 0.1 )


    def testSerialize(self):
        """ Test the serialization of parameters into input deck."""

        # Setup parameters object.
        esther_parameters = self.esther_parameters

        esther_parameters._serialize()

        # Check that the input deck has been generated.
        self.assertTrue( os.path.isdir( esther_parameters._tmp_dir ) )

        self.assertTrue( 'input.dat' in os.listdir( esther_parameters._tmp_dir ) )

if __name__ == '__main__':
    unittest.main()

