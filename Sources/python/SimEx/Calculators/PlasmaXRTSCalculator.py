""":module PlasmaXRTSCalculator: Module that holds the PlasmaXRTSCalculator class."""
##########################################################################
#                                                                        #
# Copyright (C) 2016-2018 Carsten Fortmann-Grote                         #
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

import h5py
import os
import re
import numpy
import subprocess

from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

class PlasmaXRTSCalculator(AbstractPhotonDiffractor):
    """
    :class PlasmaXRTSCalculator: Represents a plasma x-ray Thomson scattering calculation.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters for the PlasmaXRTSCalculator.
        :type parameters: PlasmaXRTSCalculatorParameters

        :param input_path: Path to the input data for this calculator.
        :type input_path: str

        :param output_path: Where to write output data generated by this calculator.
        :type output_path: str, default 'xrts.h5'

        """

        # Check parameters.
        parameters = checkAndSetParameters( parameters )

        # Set default output.
        if output_path is None:
            output_path = 'xrts_out.h5'

        # Init base class.
        super( PlasmaXRTSCalculator, self).__init__(parameters, input_path, output_path)

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

        # Overwrite provided_data.
        self.__expected_data = ['/data/snp_<7 digit index>/ff',
                                '/data/snp_<7 digit index>/halfQ',
                                '/data/snp_<7 digit index>/Nph',
                                '/data/snp_<7 digit index>/r',
                                '/data/snp_<7 digit index>/T',
                                '/data/snp_<7 digit index>/Z',
                                '/data/snp_<7 digit index>/xyz',
                                '/data/snp_<7 digit index>/Sq_halfQ',
                                '/data/snp_<7 digit index>/Sq_bound',
                                '/data/snp_<7 digit index>/Sq_free',
                                '/history/parent/detail',
                                '/history/parent/parent',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/version']

        self.__provided_data = [
                                '/data/',
                                '/data/dynamic'
                                '/data/dynamic/energy_shifts',
                                '/data/dynamic/Skw_free',
                                '/data/dynamic/Skw_bound',
                                '/data/dynamic/collision_frequency',
                                '/data/static'
                                '/data/static/Sk_bound',
                                '/data/static/Sk_ion',
                                '/data/static/Sk_elastic',
                                '/data/static/Sk_core_inelastic',
                                '/data/static/Sk_free_inelastic',
                                '/data/static/Sk_total',
                                '/data/static/fk',
                                '/data/static/qk',
                                '/data/static/ionization_potential_delta'
                                '/data/static/LFC',
                                '/history/parent/detail',
                                '/history/parent/parent',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/info/units/energy'
                                '/info/units/structure_factor'
                                '/params/beam/photonEnergy',
                                '/params/beam/spectrum',
                                '/params/info',
                                ]

        self._input_data = {}

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine xrts."""

        # Serialize the parameters (generate the input deck).
        self.parameters._serialize()

        # Write the spectrum if required.
        if self.parameters.source_spectrum == 'PROP':
            self._serializeSourceSpectrum()

        #pwd = os.getcwd()

        # Setup command sequence and issue the system call.
        # Make sure to cd to correct directory where input deck is located.
        command_sequence = ['xrs']

        process = subprocess.Popen( command_sequence, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.parameters._tmp_dir )

        # Catch stdout and stderr, wait until process terminates.
        out, err = process.communicate(input=None)

        # Error handling.
        if not err == b'':
            print (err)
            raise RuntimeError
        # Check if data was produced.
        path_to_data = os.path.join( self.parameters._tmp_dir, 'xrts_out.txt' )
        if not os.path.isfile( path_to_data ):
            raise IOError

        # Store output internally.
        self.__run_log = out.decode('utf-8')

        # Write to tmp_dir.
        with open( os.path.join( self.parameters._tmp_dir ,'xrts.log'), 'w') as log_file_handle:
                log_file_handle.write(out.decode('utf-8'))

        # Store data internally.
        self.__run_data = numpy.loadtxt( path_to_data )

        # Static data.
        self.__static_data = _parseStaticData( self.__run_log )

        # Cd back to where we came from.
        #os.chdir( pwd )

    @property
    def data(self):
        """ Query for the field data. """
        return self.__run_data

    @property
    def static_data(self):
        """ Query for the static data. """
        return self.__static_data


    def _readH5(self):
        """
        Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        # Import wpg only here if needed.
        import wpg
        from wpg.srwlib import srwl
        # Construct the wave.
        wavefront = wpg.Wavefront()
        wavefront.load_hdf5(self.input_path)

        ### Switch to frequency domain and get spectrum
        srwl.SetRepresElecField(wavefront._srwl_wf, 'f')

        # Get mesh
        mesh = wavefront.params.Mesh
        dx = (mesh.xMax - mesh.xMin) / (mesh.nx - 1)
        dy = (mesh.yMax - mesh.yMin) / (mesh.ny - 1)

        # Get intensity and sum over x,y coordinates.
        int0 = wavefront.get_intensity().sum(axis=(0,1))
        int0 = int0 * (dx * dy * 1.e6)  # scale to proper unit sqrt(W/mm^2)

        dSlice = 0
        if mesh.nSlices > 1:
            dSlice = (mesh.sliceMax - mesh.sliceMin) / (mesh.nSlices - 1)

        energies = numpy.arange(mesh.nSlices) * dSlice + mesh.sliceMin
        radiated_energy_per_photon_energy = int0

        # Get mean of spectrum
        spectrum_mean = numpy.sum(energies*radiated_energy_per_photon_energy)/numpy.sum(radiated_energy_per_photon_energy)

        self._input_data = {}
        photon_energy = wavefront.params.photonEnergy
        if self.parameters.photon_energy != photon_energy:
            print("WARNING: Parameter 'photon_energy' (%4.3e eV) not equal to source photon energy (%4.3e eV). Will proceed with source photon energy." % (self.parameters.photon_energy, photon_energy))
        if abs(spectrum_mean - photon_energy) > 1.0 :
            print("WARNING: Given photon energy (%4.3e eV) deviates from spectral mean (%4.3e) by > 1 eV. Will proceed with spectral mean." % (photon_energy, spectrum_mean))
            photon_energy = spectrum_mean

        # Finally store the photon energy on the class.
        self.parameters.photon_energy = photon_energy

        source_data = numpy.vstack((energies-photon_energy, radiated_energy_per_photon_energy)).transpose()
        self._input_data['source_spectrum'] = source_data

    def saveH5(self):
        """
        Method to save the data to a file.
        """

        # Setup h5 data groups and sets.
        with h5py.File( self.output_path, 'w' ) as h5:
            # Data
            h5.create_group("/data/dynamic")
            h5.create_group("/data/static")

            # History
            h5.create_group("/history/parent")

            # Info
            h5.create_group("/info/units/")

            # Parameters
            h5.create_group("/params/beam")


            # Create data datasets.
            # Dynamic data.
            energies  = self.__run_data[:,0]
            Skw_free  = self.__run_data[:,1]
            Skw_bound = self.__run_data[:,2]
            Skw_total = self.__run_data[:,3]

            ### TODO
            #collfreq  = self.__run_data[:,4]

            energy_shifts = h5.create_dataset("data/dynamic/energy_shifts", data=energies)
            energy_shifts.attrs['unit'] = 'eV'

            Skw_free = h5.create_dataset("data/dynamic/Skw_free", data=Skw_free)
            Skw_free.attrs['unit'] =  'eV**-1'

            Skw_bound = h5.create_dataset("data/dynamic/Skw_bound", data=Skw_bound)
            Skw_bound.attrs['unit'] =  'eV**-1'

            Skw_total = h5.create_dataset("data/dynamic/Skw_total", data=Skw_total)
            Skw_total.attrs['unit'] = 'eV**-1'

            # Save to h5 file.
            for key, value in list(self.__static_data.items()):
                h5.create_dataset("/data/static/%s" % (key), data=value)

            # Attach a unit to the ionization potential lowering.
            h5['/data/static/']['ipl'].attrs['unit'] = 'eV'


                                    #'/history/parent/detail',
                                    #'/history/parent/parent',
                                    #'/info/package_version',
                                    #'/info/contact',
                                    #'/info/data_description',
                                    #'/info/method_description',
                                    #'/params/beam/photonEnergy',
                                    #'/params/beam/spectrum',
                                    #'/params/info',
            ####
            # Close the file.
            ####
            h5.close()
            # Never write after this line in this function.

    def _serializeSourceSpectrum(self):
        """ Write the source spectrum to a file on disk. """

        source_spectrum_data = self._input_data['source_spectrum']
        source_spectrum_path = os.path.join( self.parameters._tmp_dir, 'source_spectrum.txt')

        try:
            numpy.savetxt( source_spectrum_path, source_spectrum_data, delimiter='\t' )
        except:
            print("Source spectrum could not be saved. Please check temporary directory %s exists. Backtrace follows.")
            raise

def _parseStaticData(data_string):
        """ """
        """
        Function to parse the run log and extract static data (form factors etc.)

        :params data_string: The string to parse.
        :type data_string: str

        :return: A dictionary with static data.
        :rtype: dict

        """
        # Setup return dictionary.
        static_dict = {}

        # Extract static data from
        pattern_after_equal = '\\s\\d+\\.\\d+e[\+,\-]\\d+'
        static_dict['k']           = extractDate('k\(w=0\)\\s+\[m\^-1\]\\s+='+pattern_after_equal, data_string)
        static_dict['fk']           = extractDate('f\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['qk']           = extractDate('q\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['Sk_ion']       = extractDate('S_ii\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['Sk_free']      = extractDate('S_ee\^0\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['Sk_core']      = extractDate('Core_inelastic\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['Wk']           = extractDate('Elastic\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['Sk_total']     = extractDate('S_total\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['ipl']          = extractDate('IP depression \[eV\]\\s+='+pattern_after_equal, data_string)
        static_dict['lfc']          = extractDate('G\(k\)\\s+='+pattern_after_equal, data_string)
        static_dict['debye_waller'] = extractDate('Debye-Waller\\s+='+pattern_after_equal, data_string)

        return static_dict

def extractDate(pattern_string, text):
    """ Workhorse function to get a pattern from text using a regular expression.
    :param pattern_string: The regex pattern to find.
    :type pattern_string: str (argument to re.compile)

    :param text: The string from which to extract the date.
    :type text: str

    :return The date.
    :rtype: float

    """

    # Find the line.
    pattern = re.compile(pattern_string)
    line = pattern.findall(text)

    # Extract value (behind the '=' symbol).
    pattern = re.compile("=\\s")
    return  float( pattern.split( line[0] )[-1] )
#
# Check and set functions
#

def checkAndSetParameters( parameters ):
    """
    Utility to check if the parameters dictionary is ok .

    :param parameters: The parameters to check.
    :type parameters: AbstractCalculatorParameters
    """

    if not isinstance( parameters, AbstractCalculatorParameters ):
        raise RuntimeError( "The 'parameters' argument must be of the type AbstractCalculatorParameters.")
    return parameters
