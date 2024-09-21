from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_DateTime_now() -> DateTime:
    """
    Cython signature: DateTime now()
    """
    ...

def __static_IMTypes_toDriftTimeUnit(dtu_string: bytes ) -> int:
    """
    Cython signature: DriftTimeUnit toDriftTimeUnit(const libcpp_string & dtu_string)
    """
    ...

def __static_IMTypes_toIMFormat(IM_format: bytes ) -> int:
    """
    Cython signature: IMFormat toIMFormat(const libcpp_string & IM_format)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const DriftTimeUnit value)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const IMFormat value)
    """
    ...


class AbsoluteQuantitationStandardsFile:
    """
    Cython implementation of _AbsoluteQuantitationStandardsFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandardsFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandardsFile ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile(AbsoluteQuantitationStandardsFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , run_concentrations: List[AQS_runConcentration] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[AQS_runConcentration] & run_concentrations)
        """
        ... 


class BiGaussModel:
    """
    Cython implementation of _BiGaussModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BiGaussModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BiGaussModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: BiGaussModel ) -> None:
        """
        Cython signature: void BiGaussModel(BiGaussModel &)
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        """
        ... 


class CVReference:
    """
    Cython implementation of _CVReference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVReference.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVReference()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVReference ) -> None:
        """
        Cython signature: void CVReference(CVReference &)
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the CV reference
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the CV reference
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(const String & identifier)
        Sets the CV identifier which is referenced
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the CV identifier which is referenced
        """
        ...
    
    def __richcmp__(self, other: CVReference, op: int) -> Any:
        ... 


class ChannelInfo:
    """
    Cython implementation of _ChannelInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChannelInfo.html>`_
    """
    
    description: bytes
    
    name: int
    
    id: int
    
    center: float
    
    active: bool 


class ClusterProxyKD:
    """
    Cython implementation of _ClusterProxyKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ClusterProxyKD.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ClusterProxyKD()
        """
        ...
    
    @overload
    def __init__(self, in_0: ClusterProxyKD ) -> None:
        """
        Cython signature: void ClusterProxyKD(ClusterProxyKD &)
        """
        ...
    
    @overload
    def __init__(self, size: int , avg_distance: float , center_index: int ) -> None:
        """
        Cython signature: void ClusterProxyKD(size_t size, double avg_distance, size_t center_index)
        """
        ...
    
    def getSize(self) -> int:
        """
        Cython signature: size_t getSize()
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        """
        ...
    
    def getAvgDistance(self) -> float:
        """
        Cython signature: double getAvgDistance()
        """
        ...
    
    def getCenterIndex(self) -> int:
        """
        Cython signature: size_t getCenterIndex()
        """
        ...
    
    def __richcmp__(self, other: ClusterProxyKD, op: int) -> Any:
        ... 


class ContactPerson:
    """
    Cython implementation of _ContactPerson

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ContactPerson.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ContactPerson()
        """
        ...
    
    @overload
    def __init__(self, in_0: ContactPerson ) -> None:
        """
        Cython signature: void ContactPerson(ContactPerson &)
        """
        ...
    
    def getFirstName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFirstName()
        Returns the first name of the person
        """
        ...
    
    def setFirstName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFirstName(String name)
        Sets the first name of the person
        """
        ...
    
    def getLastName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLastName()
        Returns the last name of the person
        """
        ...
    
    def setLastName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLastName(String name)
        Sets the last name of the person
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the full name of the person (gets split into first and last name internally)
        """
        ...
    
    def getInstitution(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstitution()
        Returns the affiliation
        """
        ...
    
    def setInstitution(self, institution: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstitution(String institution)
        Sets the affiliation
        """
        ...
    
    def getEmail(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEmail()
        Returns the email address
        """
        ...
    
    def setEmail(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEmail(String email)
        Sets the email address
        """
        ...
    
    def getURL(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getURL()
        Returns the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def setURL(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setURL(String email)
        Sets the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def getAddress(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAddress()
        Returns the address
        """
        ...
    
    def setAddress(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAddress(String email)
        Sets the address
        """
        ...
    
    def getContactInfo(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getContactInfo()
        Returns miscellaneous info about the contact person
        """
        ...
    
    def setContactInfo(self, contact_info: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setContactInfo(String contact_info)
        Sets miscellaneous info about the contact person
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ContactPerson, op: int) -> Any:
        ... 


class Date:
    """
    Cython implementation of _Date

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Date.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Date()
        """
        ...
    
    @overload
    def __init__(self, in_0: Date ) -> None:
        """
        Cython signature: void Date(Date &)
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(const String & date)
        """
        ...
    
    def today(self) -> Date:
        """
        Cython signature: Date today()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ... 


class DateTime:
    """
    Cython implementation of _DateTime

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DateTime.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DateTime()
        """
        ...
    
    @overload
    def __init__(self, in_0: DateTime ) -> None:
        """
        Cython signature: void DateTime(DateTime &)
        """
        ...
    
    def setDate(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDate(String date)
        """
        ...
    
    def setTime(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTime(String date)
        """
        ...
    
    def getDate(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDate()
        """
        ...
    
    def getTime(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTime()
        """
        ...
    
    def now(self) -> DateTime:
        """
        Cython signature: DateTime now()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(String date)
        """
        ...
    
    now: __static_DateTime_now 


class DecoyGenerator:
    """
    Cython implementation of _DecoyGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DecoyGenerator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DecoyGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: DecoyGenerator ) -> None:
        """
        Cython signature: void DecoyGenerator(DecoyGenerator &)
        """
        ...
    
    def setSeed(self, in_0: int ) -> None:
        """
        Cython signature: void setSeed(uint64_t)
        """
        ...
    
    def reverseProtein(self, protein: AASequence ) -> AASequence:
        """
        Cython signature: AASequence reverseProtein(const AASequence & protein)
        Reverses the protein sequence
        """
        ...
    
    def reversePeptides(self, protein: AASequence , protease: Union[bytes, str, String] ) -> AASequence:
        """
        Cython signature: AASequence reversePeptides(const AASequence & protein, const String & protease)
        Reverses the protein's peptide sequences between enzymatic cutting positions
        """
        ...
    
    def shufflePeptides(self, aas: AASequence , protease: Union[bytes, str, String] , max_attempts: int ) -> AASequence:
        """
        Cython signature: AASequence shufflePeptides(const AASequence & aas, const String & protease, const int max_attempts)
        Shuffle the protein's peptide sequences between enzymatic cutting positions, each peptide is shuffled @param max_attempts times to minimize sequence identity
        """
        ... 


class EmgGradientDescent:
    """
    Cython implementation of _EmgGradientDescent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgGradientDescent.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgGradientDescent()
        Compute the area, background and shape metrics of a peak
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgGradientDescent ) -> None:
        """
        Cython signature: void EmgGradientDescent(EmgGradientDescent &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSChromatogram , output_peak: MSChromatogram ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSChromatogram & input_peak, MSChromatogram & output_peak)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSSpectrum , output_peak: MSSpectrum ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSSpectrum & input_peak, MSSpectrum & output_peak)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSChromatogram , output_peak: MSChromatogram , left_pos: float , right_pos: float ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSChromatogram & input_peak, MSChromatogram & output_peak, double left_pos, double right_pos)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSSpectrum , output_peak: MSSpectrum , left_pos: float , right_pos: float ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSSpectrum & input_peak, MSSpectrum & output_peak, double left_pos, double right_pos)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FIAMSScheduler:
    """
    Cython implementation of _FIAMSScheduler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FIAMSScheduler.html>`_

      ADD PYTHON DOCUMENTATION HERE
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FIAMSScheduler()
        Scheduler for FIA-MS data batches. Works with FIAMSDataProcessor
        """
        ...
    
    @overload
    def __init__(self, in_0: FIAMSScheduler ) -> None:
        """
        Cython signature: void FIAMSScheduler(FIAMSScheduler &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , base_dir: Union[bytes, str, String] , load_cached_: bool ) -> None:
        """
        Cython signature: void FIAMSScheduler(String filename, String base_dir, bool load_cached_)
        """
        ...
    
    def run(self) -> None:
        """
        Cython signature: void run()
        Run the FIA-MS data analysis for the batch defined in the @filename_
        """
        ...
    
    def getBaseDir(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseDir()
        Returns the base directory for the relevant paths from the csv file
        """
        ... 


class FeatureGroupingAlgorithm:
    """
    Cython implementation of _FeatureGroupingAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithmQT:
    """
    Cython implementation of _FeatureGroupingAlgorithmQT

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmQT.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmQT()
        """
        ...
    
    @overload
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    @overload
    def group(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[ConsensusMap] & maps, ConsensusMap & out)
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithmUnlabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmUnlabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmUnlabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmUnlabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def addToGroup(self, map_id: int , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void addToGroup(int map_id, FeatureMap feature_map)
        """
        ...
    
    def setReference(self, map_id: int , map: FeatureMap ) -> None:
        """
        Cython signature: void setReference(int map_id, FeatureMap map)
        """
        ...
    
    def getResultMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getResultMap()
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureHandle:
    """
    Cython implementation of _FeatureHandle

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureHandle.html>`_
      -- Inherits from ['Peak2D', 'UniqueIdInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureHandle()
        Representation of a Peak2D, RichPeak2D or Feature
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureHandle ) -> None:
        """
        Cython signature: void FeatureHandle(FeatureHandle &)
        """
        ...
    
    @overload
    def __init__(self, map_index: int , point: Peak2D , element_index: int ) -> None:
        """
        Cython signature: void FeatureHandle(uint64_t map_index, Peak2D & point, uint64_t element_index)
        """
        ...
    
    def getMapIndex(self) -> int:
        """
        Cython signature: uint64_t getMapIndex()
        Returns the map index
        """
        ...
    
    def setMapIndex(self, i: int ) -> None:
        """
        Cython signature: void setMapIndex(uint64_t i)
        Sets the map index
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(int charge)
        Sets the charge
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge
        """
        ...
    
    def setWidth(self, width: float ) -> None:
        """
        Cython signature: void setWidth(float width)
        Sets the width (FWHM)
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        Returns the width (FWHM)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
        Returns the data point intensity (height)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        Returns the data point intensity (height)
        """
        ...
    
    def getUniqueId(self) -> int:
        """
        Cython signature: size_t getUniqueId()
        Returns the unique id
        """
        ...
    
    def clearUniqueId(self) -> int:
        """
        Cython signature: size_t clearUniqueId()
        Clear the unique id. The new unique id will be invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def hasValidUniqueId(self) -> int:
        """
        Cython signature: size_t hasValidUniqueId()
        Returns whether the unique id is valid. Returns 1 if the unique id is valid, 0 otherwise
        """
        ...
    
    def hasInvalidUniqueId(self) -> int:
        """
        Cython signature: size_t hasInvalidUniqueId()
        Returns whether the unique id is invalid. Returns 1 if the unique id is invalid, 0 otherwise
        """
        ...
    
    def setUniqueId(self, rhs: int ) -> None:
        """
        Cython signature: void setUniqueId(uint64_t rhs)
        Assigns a new, valid unique id. Always returns 1
        """
        ...
    
    def ensureUniqueId(self) -> int:
        """
        Cython signature: size_t ensureUniqueId()
        Assigns a valid unique id, but only if the present one is invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def isValid(self, unique_id: int ) -> bool:
        """
        Cython signature: bool isValid(uint64_t unique_id)
        Returns true if the unique_id is valid, false otherwise
        """
        ...
    
    def __richcmp__(self, other: FeatureHandle, op: int) -> Any:
        ... 


class Fitter1D:
    """
    Cython implementation of _Fitter1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Fitter1D.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Fitter1D()
        Abstract base class for all 1D-dimensional model fitter
        """
        ...
    
    @overload
    def __init__(self, in_0: Fitter1D ) -> None:
        """
        Cython signature: void Fitter1D(Fitter1D &)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class GNPSMetaValueFile:
    """
    Cython implementation of _GNPSMetaValueFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GNPSMetaValueFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GNPSMetaValueFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: GNPSMetaValueFile ) -> None:
        """
        Cython signature: void GNPSMetaValueFile(GNPSMetaValueFile &)
        """
        ...
    
    def store(self, consensus_map: ConsensusMap , output_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const ConsensusMap & consensus_map, const String & output_file)
        Write meta value table (tsv file) from a list of mzML files. Required for GNPS FBMN.
        
        This will produce the minimal required meta values and can be extended manually.
        
        :param consensus_map: Input ConsensusMap from which the input mzML files will be determined.
        :param output_file: Output file path for the meta value table.
        """
        ... 


class GaussTraceFitter:
    """
    Cython implementation of _GaussTraceFitter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GaussTraceFitter.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GaussTraceFitter()
        Fitter for RT profiles using a Gaussian background model
        """
        ...
    
    @overload
    def __init__(self, in_0: GaussTraceFitter ) -> None:
        """
        Cython signature: void GaussTraceFitter(GaussTraceFitter &)
        """
        ...
    
    def fit(self, traces: MassTraces ) -> None:
        """
        Cython signature: void fit(MassTraces & traces)
        Override important methods
        """
        ...
    
    def getLowerRTBound(self) -> float:
        """
        Cython signature: double getLowerRTBound()
        Returns the lower RT bound
        """
        ...
    
    def getUpperRTBound(self) -> float:
        """
        Cython signature: double getUpperRTBound()
        Returns the upper RT bound
        """
        ...
    
    def getHeight(self) -> float:
        """
        Cython signature: double getHeight()
        Returns height of the fitted gaussian model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns center of the fitted gaussian model
        """
        ...
    
    def getFWHM(self) -> float:
        """
        Cython signature: double getFWHM()
        Returns FWHM of the fitted gaussian model
        """
        ...
    
    def getSigma(self) -> float:
        """
        Cython signature: double getSigma()
        Returns Sigma of the fitted gaussian model
        """
        ...
    
    def checkMaximalRTSpan(self, max_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMaximalRTSpan(double max_rt_span)
        """
        ...
    
    def checkMinimalRTSpan(self, rt_bounds: List[float, float] , min_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMinimalRTSpan(libcpp_pair[double,double] & rt_bounds, double min_rt_span)
        """
        ...
    
    def computeTheoretical(self, trace: MassTrace , k: int ) -> float:
        """
        Cython signature: double computeTheoretical(MassTrace & trace, size_t k)
        """
        ...
    
    def getArea(self) -> float:
        """
        Cython signature: double getArea()
        Returns area of the fitted gaussian model
        """
        ...
    
    def getGnuplotFormula(self, trace: MassTrace , function_name: bytes , baseline: float , rt_shift: float ) -> Union[bytes, str, String]:
        """
        Cython signature: String getGnuplotFormula(MassTrace & trace, char function_name, double baseline, double rt_shift)
        """
        ...
    
    def getValue(self, rt: float ) -> float:
        """
        Cython signature: double getValue(double rt)
        Returns value of the fitted gaussian model
        """
        ... 


class GridBasedCluster:
    """
    Cython implementation of _GridBasedCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GridBasedCluster.html>`_
    """
    
    @overload
    def __init__(self, centre: Union[Sequence[int], Sequence[float]] , bounding_box: DBoundingBox2 , point_indices: List[int] , property_A: int , properties_B: List[int] ) -> None:
        """
        Cython signature: void GridBasedCluster(DPosition2 centre, DBoundingBox2 bounding_box, libcpp_vector[int] point_indices, int property_A, libcpp_vector[int] properties_B)
        """
        ...
    
    @overload
    def __init__(self, centre: Union[Sequence[int], Sequence[float]] , bounding_box: DBoundingBox2 , point_indices: List[int] ) -> None:
        """
        Cython signature: void GridBasedCluster(DPosition2 centre, DBoundingBox2 bounding_box, libcpp_vector[int] point_indices)
        """
        ...
    
    @overload
    def __init__(self, in_0: GridBasedCluster ) -> None:
        """
        Cython signature: void GridBasedCluster(GridBasedCluster &)
        """
        ...
    
    def getCentre(self) -> Union[Sequence[int], Sequence[float]]:
        """
        Cython signature: DPosition2 getCentre()
        Returns cluster centre
        """
        ...
    
    def getBoundingBox(self) -> DBoundingBox2:
        """
        Cython signature: DBoundingBox2 getBoundingBox()
        Returns bounding box
        """
        ...
    
    def getPoints(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getPoints()
        Returns indices of points in cluster
        """
        ...
    
    def getPropertyA(self) -> int:
        """
        Cython signature: int getPropertyA()
        Returns property A
        """
        ...
    
    def getPropertiesB(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getPropertiesB()
        Returns properties B of all points
        """
        ... 


class ILPDCWrapper:
    """
    Cython implementation of _ILPDCWrapper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ILPDCWrapper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ILPDCWrapper()
        """
        ...
    
    @overload
    def __init__(self, in_0: ILPDCWrapper ) -> None:
        """
        Cython signature: void ILPDCWrapper(ILPDCWrapper &)
        """
        ...
    
    def compute(self, fm: FeatureMap , pairs: List[ChargePair] , verbose_level: int ) -> float:
        """
        Cython signature: double compute(FeatureMap fm, libcpp_vector[ChargePair] & pairs, size_t verbose_level)
        Compute optimal solution and return value of objective function. If the input feature map is empty, a warning is issued and -1 is returned
        """
        ... 


class IMTypes:
    """
    Cython implementation of _IMTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IMTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMTypes()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMTypes ) -> None:
        """
        Cython signature: void IMTypes(IMTypes &)
        """
        ...
    
    @overload
    def determineIMFormat(self, exp: MSExperiment ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSExperiment & exp)
        """
        ...
    
    @overload
    def determineIMFormat(self, spec: MSSpectrum ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSSpectrum & spec)
        """
        ...
    
    toDriftTimeUnit: __static_IMTypes_toDriftTimeUnit
    
    toIMFormat: __static_IMTypes_toIMFormat
    
    toString: __static_IMTypes_toString
    
    toString: __static_IMTypes_toString 


class IndexedMzMLHandler:
    """
    Cython implementation of _IndexedMzMLHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLHandler.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IndexedMzMLHandler()
        """
        ...
    
    @overload
    def __init__(self, in_0: IndexedMzMLHandler ) -> None:
        """
        Cython signature: void IndexedMzMLHandler(IndexedMzMLHandler &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void IndexedMzMLHandler(String filename)
        """
        ...
    
    def openFile(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void openFile(String filename)
        """
        ...
    
    def getParsingSuccess(self) -> bool:
        """
        Cython signature: bool getParsingSuccess()
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> _Interfaces_Spectrum:
        """
        Cython signature: shared_ptr[_Interfaces_Spectrum] getSpectrumById(int id_)
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> _Interfaces_Chromatogram:
        """
        Cython signature: shared_ptr[_Interfaces_Chromatogram] getChromatogramById(int id_)
        """
        ...
    
    def getMSSpectrumById(self, id_: int ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getMSSpectrumById(int id_)
        """
        ...
    
    def getMSSpectrumByNativeId(self, id_: bytes , spec: MSSpectrum ) -> None:
        """
        Cython signature: void getMSSpectrumByNativeId(libcpp_string id_, MSSpectrum & spec)
        """
        ...
    
    def getMSChromatogramById(self, id_: int ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getMSChromatogramById(int id_)
        """
        ...
    
    def getMSChromatogramByNativeId(self, id_: bytes , chrom: MSChromatogram ) -> None:
        """
        Cython signature: void getMSChromatogramByNativeId(libcpp_string id_, MSChromatogram & chrom)
        """
        ...
    
    def setSkipXMLChecks(self, skip: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool skip)
        """
        ... 


class IsobaricChannelExtractor:
    """
    Cython implementation of _IsobaricChannelExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricChannelExtractor.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, in_0: IsobaricChannelExtractor ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(IsobaricChannelExtractor &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def extractChannels(self, ms_exp_data: MSExperiment , consensus_map: ConsensusMap ) -> None:
        """
        Cython signature: void extractChannels(MSExperiment & ms_exp_data, ConsensusMap & consensus_map)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IsotopeLabelingMDVs:
    """
    Cython implementation of _IsotopeLabelingMDVs

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeLabelingMDVs.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeLabelingMDVs()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeLabelingMDVs ) -> None:
        """
        Cython signature: void IsotopeLabelingMDVs(IsotopeLabelingMDVs &)
        """
        ...
    
    def isotopicCorrection(self, normalized_feature: Feature , corrected_feature: Feature , correction_matrix: MatrixDouble , correction_matrix_agent: int ) -> None:
        """
        Cython signature: void isotopicCorrection(const Feature & normalized_feature, Feature & corrected_feature, MatrixDouble & correction_matrix, const DerivatizationAgent & correction_matrix_agent)
        This function performs an isotopic correction to account for unlabeled abundances coming from
        the derivatization agent (e.g., tBDMS) using correction matrix method and is calculated as follows:
        
        
        :param normalized_feature: Feature with normalized values for each component and unlabeled chemical formula for each component group
        :param correction_matrix: Square matrix holding correction factors derived either experimentally or theoretically which describe how spectral peaks of naturally abundant 13C contribute to spectral peaks that overlap (or convolve) the spectral peaks of the corrected MDV of the derivatization agent
        :param correction_matrix_agent: Name of the derivatization agent, the internally stored correction matrix if the name of the agent is supplied, only "TBDMS" is supported for now
        :return: corrected_feature: Feature with corrected values for each component
        """
        ...
    
    def isotopicCorrections(self, normalized_featureMap: FeatureMap , corrected_featureMap: FeatureMap , correction_matrix: MatrixDouble , correction_matrix_agent: int ) -> None:
        """
        Cython signature: void isotopicCorrections(const FeatureMap & normalized_featureMap, FeatureMap & corrected_featureMap, MatrixDouble & correction_matrix, const DerivatizationAgent & correction_matrix_agent)
        This function performs an isotopic correction to account for unlabeled abundances coming from
        the derivatization agent (e.g., tBDMS) using correction matrix method and is calculated as follows:
        
        
        :param normalized_featuremap: FeatureMap with normalized values for each component and unlabeled chemical formula for each component group
        :param correction_matrix: Square matrix holding correction factors derived either experimentally or theoretically which describe how spectral peaks of naturally abundant 13C contribute to spectral peaks that overlap (or convolve) the spectral peaks of the corrected MDV of the derivatization agent
        :param correction_matrix_agent: Name of the derivatization agent, the internally stored correction matrix if the name of the agent is supplied, only "TBDMS" is supported for now
        :return corrected_featuremap: FeatureMap with corrected values for each component
        """
        ...
    
    def calculateIsotopicPurity(self, normalized_feature: Feature , experiment_data: List[float] , isotopic_purity_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateIsotopicPurity(const Feature & normalized_feature, const libcpp_vector[double] & experiment_data, const String & isotopic_purity_name)
        This function calculates the isotopic purity of the MDV using the following formula:
        isotopic purity of tracer (atom % 13C) = n / [n + (M + n-1)/(M + n)],
        where n in M+n is represented as the index of the result
        The formula is extracted from "High-resolution 13C metabolic flux analysis",
        Long et al, doi:10.1038/s41596-019-0204-0
        
        
        :param normalized_feature: Feature with normalized values for each component and the number of heavy labeled e.g., carbons. Out is a Feature with the calculated isotopic purity for the component group
        :param experiment_data: Vector of experiment data in percent
        :param isotopic_purity_name: Name of the isotopic purity tracer to be saved as a meta value
        """
        ...
    
    def calculateMDVAccuracy(self, normalized_feature: Feature , feature_name: Union[bytes, str, String] , fragment_isotopomer_theoretical_formula: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDVAccuracy(const Feature & normalized_feature, const String & feature_name, const String & fragment_isotopomer_theoretical_formula)
        This function calculates the accuracy of the MDV as compared to the theoretical MDV (only for 12C quality control experiments)
        using average deviation to the mean. The result is mapped to the meta value "average_accuracy" in the updated feature
        
        
        :param normalized_feature: Feature with normalized values for each component and the chemical formula of the component group. Out is a Feature with the component group accuracy and accuracy for the error for each component
        :param fragment_isotopomer_measured: Measured scan values
        :param fragment_isotopomer_theoretical_formula: Empirical formula from which the theoretical values will be generated
        """
        ...
    
    def calculateMDVAccuracies(self, normalized_featureMap: FeatureMap , feature_name: Union[bytes, str, String] , fragment_isotopomer_theoretical_formulas: Dict[Union[bytes, str], Union[bytes, str]] ) -> None:
        """
        Cython signature: void calculateMDVAccuracies(const FeatureMap & normalized_featureMap, const String & feature_name, const libcpp_map[libcpp_utf8_string,libcpp_utf8_string] & fragment_isotopomer_theoretical_formulas)
        This function calculates the accuracy of the MDV as compared to the theoretical MDV (only for 12C quality control experiments)
        using average deviation to the mean
        
        
        param normalized_featuremap: FeatureMap with normalized values for each component and the chemical formula of the component group. Out is a FeatureMap with the component group accuracy and accuracy for the error for each component
        param fragment_isotopomer_measured: Measured scan values
        param fragment_isotopomer_theoretical_formula: A map of ProteinName/peptideRef to Empirical formula from which the theoretical values will be generated
        """
        ...
    
    def calculateMDV(self, measured_feature: Feature , normalized_feature: Feature , mass_intensity_type: int , feature_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDV(const Feature & measured_feature, Feature & normalized_feature, const MassIntensityType & mass_intensity_type, const String & feature_name)
        """
        ...
    
    def calculateMDVs(self, measured_featureMap: FeatureMap , normalized_featureMap: FeatureMap , mass_intensity_type: int , feature_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDVs(const FeatureMap & measured_featureMap, FeatureMap & normalized_featureMap, const MassIntensityType & mass_intensity_type, const String & feature_name)
        """
        ... 


class ItraqConstants:
    """
    Cython implementation of _ItraqConstants

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqConstants.html>`_

    Some constants used throughout iTRAQ classes
    
    Constants for iTRAQ experiments and a ChannelInfo structure to store information about a single channel
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqConstants()
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqConstants ) -> None:
        """
        Cython signature: void ItraqConstants(ItraqConstants &)
        """
        ...
    
    def getIsotopeMatrixAsStringList(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> List[bytes]:
        """
        Cython signature: StringList getIsotopeMatrixAsStringList(int itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert isotope correction matrix to stringlist\n
        
        Each line is converted into a string of the format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        Useful for creating parameters or debug output
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def updateIsotopeMatrixFromStringList(self, itraq_type: int , channels: List[bytes] , isotope_corrections: List[MatrixDouble] ) -> None:
        """
        Cython signature: void updateIsotopeMatrixFromStringList(int itraq_type, StringList & channels, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert strings to isotope correction matrix rows\n
        
        Each string of format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        is parsed and the corresponding channel(row) in the matrix is updated
        Not all channels need to be present, missing channels will be left untouched
        Useful to update the matrix with user isotope correction values
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param channels: New channel isotope values as strings
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def translateIsotopeMatrix(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> MatrixDouble:
        """
        Cython signature: MatrixDouble translateIsotopeMatrix(int & itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        """
        ... 


class ItraqEightPlexQuantitationMethod:
    """
    Cython implementation of _ItraqEightPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqEightPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod()
        iTRAQ 8 plex quantitation to be used with the IsobaricQuantitation
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod(ItraqEightPlexQuantitationMethod &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getChannelInformation(self) -> List[IsobaricChannelInformation]:
        """
        Cython signature: libcpp_vector[IsobaricChannelInformation] getChannelInformation()
        """
        ...
    
    def getNumberOfChannels(self) -> int:
        """
        Cython signature: size_t getNumberOfChannels()
        """
        ...
    
    def getIsotopeCorrectionMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getIsotopeCorrectionMatrix()
        """
        ...
    
    def getReferenceChannel(self) -> int:
        """
        Cython signature: size_t getReferenceChannel()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class KDTreeFeatureNode:
    """
    Cython implementation of _KDTreeFeatureNode

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KDTreeFeatureNode.html>`_
    """
    
    @overload
    def __init__(self, in_0: KDTreeFeatureNode ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureNode &)
        """
        ...
    
    @overload
    def __init__(self, data: KDTreeFeatureMaps , idx: int ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureMaps * data, size_t idx)
        """
        ...
    
    def __getitem__(self, i: int ) -> float:
        """
        Cython signature: double operator[](size_t i)
        """
        ...
    
    def getIndex(self) -> int:
        """
        Cython signature: size_t getIndex()
        Returns index of corresponding feature in data_
        """
        ... 


class LinearResampler:
    """
    Cython implementation of _LinearResampler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LinearResampler.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LinearResampler()
        """
        ...
    
    @overload
    def __init__(self, in_0: LinearResampler ) -> None:
        """
        Cython signature: void LinearResampler(LinearResampler &)
        """
        ...
    
    def raster(self, input: MSSpectrum ) -> None:
        """
        Cython signature: void raster(MSSpectrum & input)
        Applies the resampling algorithm to an MSSpectrum
        """
        ...
    
    def rasterExperiment(self, input: MSExperiment ) -> None:
        """
        Cython signature: void rasterExperiment(MSExperiment & input)
        Resamples the data in an MSExperiment
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class LowessSmoothing:
    """
    Cython implementation of _LowessSmoothing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LowessSmoothing.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void LowessSmoothing()
        """
        ...
    
    def smoothData(self, x: List[float] , y: List[float] , y_smoothed: List[float] ) -> None:
        """
        Cython signature: void smoothData(libcpp_vector[double] x, libcpp_vector[double] y, libcpp_vector[double] & y_smoothed)
        Smoothing method that receives x and y coordinates (e.g., RT and intensities) and computes smoothed intensities
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MRMAssay:
    """
    Cython implementation of _MRMAssay

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMAssay.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMAssay()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMAssay ) -> None:
        """
        Cython signature: void MRMAssay(MRMAssay &)
        """
        ...
    
    def reannotateTransitions(self, exp: TargetedExperiment , precursor_mz_threshold: float , product_mz_threshold: float , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , round_decPow: int ) -> None:
        """
        Cython signature: void reannotateTransitions(TargetedExperiment & exp, double precursor_mz_threshold, double product_mz_threshold, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, int round_decPow)
        Annotates and filters transitions in a TargetedExperiment
        
        
        :param exp: The input, unfiltered transitions
        :param precursor_mz_threshold: The precursor m/z threshold in Th for annotation
        :param product_mz_threshold: The product m/z threshold in Th for annotation
        :param fragment_types: The fragment types to consider for annotation
        :param fragment_charges: The fragment charges to consider for annotation
        :param enable_specific_losses: Whether specific neutral losses should be considered
        :param enable_unspecific_losses: Whether unspecific neutral losses (H2O1, H3N1, C1H2N2, C1H2N1O1) should be considered
        :param round_decPow: Round product m/z values to decimal power (default: -4)
        """
        ...
    
    def restrictTransitions(self, exp: TargetedExperiment , lower_mz_limit: float , upper_mz_limit: float , swathes: List[List[float, float]] ) -> None:
        """
        Cython signature: void restrictTransitions(TargetedExperiment & exp, double lower_mz_limit, double upper_mz_limit, libcpp_vector[libcpp_pair[double,double]] swathes)
        Restrict and filter transitions in a TargetedExperiment
        
        
        :param exp: The input, unfiltered transitions
        :param lower_mz_limit: The lower product m/z limit in Th
        :param upper_mz_limit: The upper product m/z limit in Th
        :param swathes: The swath window settings (to exclude fragment ions falling into the precursor isolation window)
        """
        ...
    
    def detectingTransitions(self, exp: TargetedExperiment , min_transitions: int , max_transitions: int ) -> None:
        """
        Cython signature: void detectingTransitions(TargetedExperiment & exp, int min_transitions, int max_transitions)
        Select detecting fragment ions
        
        
        :param exp: The input, unfiltered transitions
        :param min_transitions: The minimum number of transitions required per assay
        :param max_transitions: The maximum number of transitions required per assay
        """
        ...
    
    def filterMinMaxTransitionsCompound(self, exp: TargetedExperiment , min_transitions: int , max_transitions: int ) -> None:
        """
        Cython signature: void filterMinMaxTransitionsCompound(TargetedExperiment & exp, int min_transitions, int max_transitions)
        Filters target and decoy transitions by intensity, only keeping the top N transitions
        
        
        :param exp: The transition list which will be filtered
        :param min_transitions: The minimum number of transitions required per assay (targets only)
        :param max_transitions: The maximum number of transitions allowed per assay
        """
        ...
    
    def filterUnreferencedDecoysCompound(self, exp: TargetedExperiment ) -> None:
        """
        Cython signature: void filterUnreferencedDecoysCompound(TargetedExperiment & exp)
        Filters decoy transitions, which do not have respective target transition
        based on the transitionID.
        
        References between targets and decoys will be constructed based on the transitionsID
        and the "_decoy_" string. For example:
        
        target: 84_CompoundName_[M+H]+_88_22
        decoy: 84_CompoundName_decoy_[M+H]+_88_22
        
        
        :param exp: The transition list which will be filtered
        """
        ...
    
    def uisTransitions(self, exp: TargetedExperiment , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , enable_ms2_precursors: bool , mz_threshold: float , swathes: List[List[float, float]] , round_decPow: int , max_num_alternative_localizations: int , shuffle_seed: int ) -> None:
        """
        Cython signature: void uisTransitions(TargetedExperiment & exp, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, bool enable_ms2_precursors, double mz_threshold, libcpp_vector[libcpp_pair[double,double]] swathes, int round_decPow, size_t max_num_alternative_localizations, int shuffle_seed)
        Annotate UIS / site-specific transitions
        
        Performs the following actions:
        
        - Step 1: For each peptide, compute all theoretical alternative peptidoforms; see transitions generateTargetInSilicoMap_()
        - Step 2: Generate target identification transitions; see generateTargetAssays_()
        
        - Step 3a: Generate decoy sequences that share peptidoform properties with targets; see generateDecoySequences_()
        - Step 3b: Generate decoy in silico peptide map containing theoretical transition; see generateDecoyInSilicoMap_()
        - Step 4: Generate decoy identification transitions; see generateDecoyAssays_()
        
        The IPF algorithm uses the concept of "identification transitions" that
        are used to discriminate different peptidoforms, these are generated in
        this function.  In brief, the algorithm takes the existing set of
        peptides and transitions and then appends these "identification
        transitions" for targets and decoys. The novel transitions are set to be
        non-detecting and non-quantifying and are annotated with the set of
        peptidoforms to which they map.
        
        
        :param exp: The input, unfiltered transitions
        :param fragment_types: The fragment types to consider for annotation
        :param fragment_charges: The fragment charges to consider for annotation
        :param enable_specific_losses: Whether specific neutral losses should be considered
        :param enable_unspecific_losses: Whether unspecific neutral losses (H2O1, H3N1, C1H2N2, C1H2N1O1) should be considered
        :param enable_ms2_precursors: Whether MS2 precursors should be considered
        :param mz_threshold: The product m/z threshold in Th for annotation
        :param swathes: The swath window settings (to exclude fragment ions falling
        :param round_decPow: Round product m/z values to decimal power (default: -4)
        :param max_num_alternative_localizations: Maximum number of allowed peptide sequence permutations
        :param shuffle_seed: Set seed for shuffle (-1: select seed based on time)
        :param disable_decoy_transitions: Whether to disable generation of decoy UIS transitions
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MRMMapping:
    """
    Cython implementation of _MRMMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMMapping.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMMapping()
        """
        ...
    
    def mapExperiment(self, input_chromatograms: MSExperiment , targeted_exp: TargetedExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void mapExperiment(MSExperiment input_chromatograms, TargetedExperiment targeted_exp, MSExperiment & output)
        Maps input chromatograms to assays in a targeted experiment
        
        The output chromatograms are an annotated copy of the input chromatograms
        with native id, precursor information and peptide sequence (if available)
        annotated in the chromatogram files
        
        The algorithm tries to match a given set of chromatograms and targeted
        assays. It iterates through all the chromatograms retrieves one or more
        matching targeted assay for the chromatogram. By default, the algorithm
        assumes that a 1:1 mapping exists. If a chromatogram cannot be mapped
        (does not have a corresponding assay) the algorithm issues a warning, the
        user can specify that the program should abort in such a case (see
        error_on_unmapped)
        
        :note If multiple mapping is enabled (see map_multiple_assays parameter)
        then each mapped assay will get its own chromatogram that contains the
        same raw data but different meta-annotation. This *can* be useful if the
        same transition is used to monitor multiple analytes but may also
        indicate a problem with too wide mapping tolerances
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MascotInfile:
    """
    Cython implementation of _MascotInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotInfile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotInfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotInfile ) -> None:
        """
        Cython signature: void MascotInfile(MascotInfile &)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , spec: MSSpectrum , mz: float , retention_time: float , search_title: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename, MSSpectrum & spec, double mz, double retention_time, String search_title)
        Stores the peak list in a MascotInfile that can be used as input for MASCOT shell execution
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , experiment: MSExperiment , search_title: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & experiment, String search_title)
        Stores the experiment data in a MascotInfile that can be used as input for MASCOT shell execution
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & exp)
        Loads a Mascot Generic File into a PeakMap
        
        
        :param filename: File name which the map should be read from
        :param exp: The map which is filled with the data from the given file
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        """
        ...
    
    def getBoundary(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBoundary()
        Returns the boundary used for the MIME format
        """
        ...
    
    def setBoundary(self, boundary: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBoundary(const String & boundary)
        Sets the boundary used for the MIME format.By default a 22 character random string is used
        """
        ...
    
    def getDB(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDB()
        Returns the DB to use
        """
        ...
    
    def setDB(self, db: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDB(const String & db)
        Sets the DB (default MSDB). See mascot path /config/mascot.dat in "Databases" section for possible settings
        """
        ...
    
    def getSearchType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchType()
        Returns the search type
        """
        ...
    
    def setSearchType(self, search_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchType(const String & search_type)
        Sets the search type (default MIS). So far only MIS is supported!Valid types are "MIS" (MS/MS Ion Search), "PMF" (Peptide Mass Fingerprint) , "SQ" (Sequence Query)
        """
        ...
    
    def getHits(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getHits()
        Returns the number of hits to report back
        """
        ...
    
    def setHits(self, hits: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setHits(const String & hits)
        Sets the number of hits to report back (default 20)
        """
        ...
    
    def getCleavage(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavage()
        Returns the enzyme used for cleavage
        """
        ...
    
    def setCleavage(self, cleavage: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavage(const String & cleavage)
        Sets the enzyme used for cleavage (default Trypsin). See mascot path /config/enzymes for possible settings
        """
        ...
    
    def getMassType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getMassType()
        Returns the used mass type ("Monoisotopic" or "Average")
        """
        ...
    
    def setMassType(self, mass_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setMassType(const String & mass_type)
        Sets the used mass type "Monoisotopic" or "Average" (default Monoisotopic)
        """
        ...
    
    def getModifications(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getModifications()
        Returns a vector containing the fixed modifications (default none)
        """
        ...
    
    def setModifications(self, mods: List[bytes] ) -> None:
        """
        Cython signature: void setModifications(libcpp_vector[String] & mods)
        Sets the fixed modifications (default none). See mascot path /config/mod_file for possible settings
        """
        ...
    
    def getVariableModifications(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getVariableModifications()
        Returns a vector containing the variable modifications (default none)
        """
        ...
    
    def setVariableModifications(self, mods: List[bytes] ) -> None:
        """
        Cython signature: void setVariableModifications(libcpp_vector[String] & mods)
        Sets the fixed modifications (default none). See mascot path /config/mod_file for possible settings
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        Returns the instrument type
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(const String & instrument)
        Sets the instrument type (Default Default). Possible instruments are ESI-QUAD-TOF, MALDI-TOF-PSD, ESI-TRAP, ESI-QUAD, ESI-FTICR, MALDI-TOF-TOF, ESI-4SECTOR, FTMS-ECD, MALDI-QUAD-TOF, MALDI-QIT-TOF
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getMissedCleavages()
        Returns the number of allowed missed cleavages
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(unsigned int missed_cleavages)
        Sets the number of allowed missed cleavages (default 1)
        """
        ...
    
    def getPrecursorMassTolerance(self) -> float:
        """
        Cython signature: float getPrecursorMassTolerance()
        Returns the precursor mass tolerance
        """
        ...
    
    def setPrecursorMassTolerance(self, precursor_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerance(float precursor_mass_tolerance)
        Sets the precursor mass tolerance in Da (default 2.0)
        """
        ...
    
    def getPeakMassTolerance(self) -> float:
        """
        Cython signature: float getPeakMassTolerance()
        Returns the peak mass tolerance in Da
        """
        ...
    
    def setPeakMassTolerance(self, ion_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPeakMassTolerance(float ion_mass_tolerance)
        Sets the peak mass tolerance in Da (default 1.0)
        """
        ...
    
    def getTaxonomy(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomy()
        Returns the taxonomy
        """
        ...
    
    def setTaxonomy(self, taxonomy: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomy(const String & taxonomy)
        Sets the taxonomy (default All entries). See mascot path /config/taxonomy for possible settings
        """
        ...
    
    def getFormVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormVersion()
        Returns the Mascot form version
        """
        ...
    
    def setFormVersion(self, form_version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFormVersion(const String & form_version)
        Sets the Mascot form version (default 1.01)
        """
        ...
    
    def getCharges(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCharges()
        Returns the charges
        """
        ...
    
    def setCharges(self, charges: List[int] ) -> None:
        """
        Cython signature: void setCharges(libcpp_vector[int] & charges)
        Sets the charges (default 1+, 2+ and 3+)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MassTraceDetection:
    """
    Cython implementation of _MassTraceDetection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassTraceDetection.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTraceDetection()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTraceDetection ) -> None:
        """
        Cython signature: void MassTraceDetection(MassTraceDetection &)
        """
        ...
    
    def run(self, input_map: MSExperiment , traces: List[Kernel_MassTrace] , max_traces: int ) -> None:
        """
        Cython signature: void run(MSExperiment & input_map, libcpp_vector[Kernel_MassTrace] & traces, size_t max_traces)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MetaInfoDescription:
    """
    Cython implementation of _MetaInfoDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoDescription.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoDescription ) -> None:
        """
        Cython signature: void MetaInfoDescription(MetaInfoDescription &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the peak annotations
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the peak annotations
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns a reference to the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: MetaInfoDescription, op: int) -> Any:
        ... 


class MetaInfoRegistry:
    """
    Cython implementation of _MetaInfoRegistry

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoRegistry.html>`_

    Registry which assigns unique integer indices to strings
    
    When registering a new name an index >= 1024 is assigned.
    Indices from 1 to 1023 are reserved for fast access and will never change:
    1 - isotopic_range
    2 - cluster_id
    3 - label
    4 - icon
    5 - color
    6 - RT
    7 - MZ
    8 - predicted_RT
    9 - predicted_RT_p_value
    10 - spectrum_reference
    11 - ID
    12 - low_quality
    13 - charge
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoRegistry()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoRegistry ) -> None:
        """
        Cython signature: void MetaInfoRegistry(MetaInfoRegistry &)
        """
        ...
    
    def registerName(self, name: Union[bytes, str, String] , description: Union[bytes, str, String] , unit: Union[bytes, str, String] ) -> int:
        """
        Cython signature: unsigned int registerName(const String & name, const String & description, const String & unit)
        Registers a string, stores its description and unit, and returns the corresponding index. If the string is already registered, it returns the index of the string
        """
        ...
    
    @overload
    def setDescription(self, index: int , description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(unsigned int index, const String & description)
        Sets the description (String), corresponding to an index
        """
        ...
    
    @overload
    def setDescription(self, name: Union[bytes, str, String] , description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(const String & name, const String & description)
        Sets the description (String), corresponding to a name
        """
        ...
    
    @overload
    def setUnit(self, index: int , unit: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnit(unsigned int index, const String & unit)
        Sets the unit (String), corresponding to an index
        """
        ...
    
    @overload
    def setUnit(self, name: Union[bytes, str, String] , unit: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnit(const String & name, const String & unit)
        Sets the unit (String), corresponding to a name
        """
        ...
    
    def getIndex(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: unsigned int getIndex(const String & name)
        Returns the integer index corresponding to a string. If the string is not registered, returns UInt(-1) (= UINT_MAX)
        """
        ...
    
    def getName(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getName(unsigned int index)
        Returns the corresponding name to an index
        """
        ...
    
    @overload
    def getDescription(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription(unsigned int index)
        Returns the description of an index
        """
        ...
    
    @overload
    def getDescription(self, name: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription(const String & name)
        Returns the description of a name
        """
        ...
    
    @overload
    def getUnit(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getUnit(unsigned int index)
        Returns the unit of an index
        """
        ...
    
    @overload
    def getUnit(self, name: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getUnit(const String & name)
        Returns the unit of a name
        """
        ... 


class MultiplexIsotopicPeakPattern:
    """
    Cython implementation of _MultiplexIsotopicPeakPattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexIsotopicPeakPattern.html>`_
    """
    
    @overload
    def __init__(self, c: int , ppp: int , ms: MultiplexDeltaMasses , msi: int ) -> None:
        """
        Cython signature: void MultiplexIsotopicPeakPattern(int c, int ppp, MultiplexDeltaMasses ms, int msi)
        """
        ...
    
    @overload
    def __init__(self, in_0: MultiplexIsotopicPeakPattern ) -> None:
        """
        Cython signature: void MultiplexIsotopicPeakPattern(MultiplexIsotopicPeakPattern &)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns charge
        """
        ...
    
    def getPeaksPerPeptide(self) -> int:
        """
        Cython signature: int getPeaksPerPeptide()
        Returns peaks per peptide
        """
        ...
    
    def getMassShifts(self) -> MultiplexDeltaMasses:
        """
        Cython signature: MultiplexDeltaMasses getMassShifts()
        Returns mass shifts
        """
        ...
    
    def getMassShiftIndex(self) -> int:
        """
        Cython signature: int getMassShiftIndex()
        Returns mass shift index
        """
        ...
    
    def getMassShiftCount(self) -> int:
        """
        Cython signature: unsigned int getMassShiftCount()
        Returns number of mass shifts i.e. the number of peptides in the multiplet
        """
        ...
    
    def getMassShiftAt(self, i: int ) -> float:
        """
        Cython signature: double getMassShiftAt(int i)
        Returns mass shift at position i
        """
        ...
    
    def getMZShiftAt(self, i: int ) -> float:
        """
        Cython signature: double getMZShiftAt(int i)
        Returns m/z shift at position i
        """
        ...
    
    def getMZShiftCount(self) -> int:
        """
        Cython signature: unsigned int getMZShiftCount()
        Returns number of m/z shifts
        """
        ... 


class MzMLSpectrumDecoder:
    """
    Cython implementation of _MzMLSpectrumDecoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLSpectrumDecoder.html>`_

    A class to decode input strings that contain an mzML chromatogram or spectrum tag
    
    It uses xercesc to parse a string containing either a exactly one mzML
    spectrum or chromatogram (from <chromatogram> to </chromatogram> or
    <spectrum> to </spectrum> tag). It returns the data contained in the
    binaryDataArray for Intensity / mass-to-charge or Intensity / time
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSpectrumDecoder ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder(MzMLSpectrumDecoder &)
        """
        ...
    
    def domParseChromatogram(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Chromatogram ) -> None:
        """
        Cython signature: void domParseChromatogram(String in_, shared_ptr[_Interfaces_Chromatogram] & cptr)
        Extract data from a string which contains a full mzML chromatogram
        
        Extracts data from the input string which is expected to contain exactly
        one <chromatogram> tag (from <chromatogram> to </chromatogram>). This
        function will extract the contained binaryDataArray and provide the
        result as Chromatogram
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting chromatogram
        """
        ...
    
    def domParseSpectrum(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Spectrum ) -> None:
        """
        Cython signature: void domParseSpectrum(String in_, shared_ptr[_Interfaces_Spectrum] & cptr)
        Extract data from a string which contains a full mzML spectrum
        
        Extracts data from the input string which is expected to contain exactly
        one <spectrum> tag (from <spectrum> to </spectrum>). This function will
        extract the contained binaryDataArray and provide the result as Spectrum
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting spectrum
        """
        ...
    
    def setSkipXMLChecks(self, only: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool only)
        Whether to skip some XML checks (e.g. removing whitespace inside base64 arrays) and be fast instead
        """
        ... 


class MzTabM:
    """
    Cython implementation of _MzTabM

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabM.html>`_

    Data model of MzTabM files
    
    Please see the official MzTabM specification at https://github.com/HUPO-PSI/mzTab/tree/master/specification_document-releases/2_0-Metabolomics-Release
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabM()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabM ) -> None:
        """
        Cython signature: void MzTabM(MzTabM &)
        """
        ...
    
    def exportFeatureMapToMzTabM(self, feature_map: FeatureMap ) -> MzTabM:
        """
        Cython signature: MzTabM exportFeatureMapToMzTabM(FeatureMap feature_map)
        Export FeatureMap with Identifications to MzTabM
        """
        ... 


class MzXMLFile:
    """
    Cython implementation of _MzXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzXMLFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzXMLFile ) -> None:
        """
        Cython signature: void MzXMLFile(MzXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, MSExperiment & exp)
        Loads a MSExperiment from a MzXML file
        
        
        :param exp: MSExperiment
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & exp)
        Stores a MSExperiment in a MzXML file
        
        
        :param exp: MSExperiment
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class NonNegativeLeastSquaresSolver:
    """
    Cython implementation of _NonNegativeLeastSquaresSolver

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NonNegativeLeastSquaresSolver.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver()
        """
        ...
    
    @overload
    def __init__(self, in_0: NonNegativeLeastSquaresSolver ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver(NonNegativeLeastSquaresSolver &)
        """
        ...
    
    def solve(self, A: MatrixDouble , b: MatrixDouble , x: MatrixDouble ) -> int:
        """
        Cython signature: int solve(MatrixDouble & A, MatrixDouble & b, MatrixDouble & x)
        """
        ...
    RETURN_STATUS : __RETURN_STATUS 


class OPXLDataStructs:
    """
    Cython implementation of _OPXLDataStructs

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OPXLDataStructs.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OPXLDataStructs()
        """
        ...
    
    @overload
    def __init__(self, in_0: OPXLDataStructs ) -> None:
        """
        Cython signature: void OPXLDataStructs(OPXLDataStructs &)
        """
        ...
    PeptidePosition : __PeptidePosition
    ProteinProteinCrossLinkType : __ProteinProteinCrossLinkType 


class Peak1D:
    """
    Cython implementation of _Peak1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Peak1D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Peak1D()
        """
        ...
    
    @overload
    def __init__(self, in_0: Peak1D ) -> None:
        """
        Cython signature: void Peak1D(Peak1D &)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        """
        ...
    
    def setPos(self, pos: float ) -> None:
        """
        Cython signature: void setPos(double pos)
        """
        ...
    
    def __richcmp__(self, other: Peak1D, op: int) -> Any:
        ... 


class PeakPickerIterative:
    """
    Cython implementation of _PeakPickerIterative

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakPickerIterative.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakPickerIterative()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakPickerIterative ) -> None:
        """
        Cython signature: void PeakPickerIterative(PeakPickerIterative &)
        """
        ...
    
    def pick(self, input: MSSpectrum , output: MSSpectrum ) -> None:
        """
        Cython signature: void pick(MSSpectrum & input, MSSpectrum & output)
        This will pick one single spectrum. The PeakPickerHiRes is used to
        generate seeds, these seeds are then used to re-center the mass and
        compute peak width and integrated intensity of the peak
        
        Finally, other peaks that would fall within the primary peak are
        discarded
        
        The output are the remaining peaks
        """
        ...
    
    def pickExperiment(self, input: MSExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void pickExperiment(MSExperiment & input, MSExperiment & output)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class PercolatorFeatureSetHelper:
    """
    Cython implementation of _PercolatorFeatureSetHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorFeatureSetHelper.html>`_

    Percolator feature set and integration helper
    
    This class contains functions to handle (compute, aggregate, integrate)
    Percolator features. This includes the calculation or extraction of
    Percolator features depending on the search engine(s) for later use with
    PercolatorAdapter. It also includes handling the reintegration of the
    percolator result into the set of Identifications
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorFeatureSetHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorFeatureSetHelper ) -> None:
        """
        Cython signature: void PercolatorFeatureSetHelper(PercolatorFeatureSetHelper &)
        """
        ...
    
    def concatMULTISEPeptideIds(self, all_peptide_ids: List[PeptideIdentification] , new_peptide_ids: List[PeptideIdentification] , search_engine: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void concatMULTISEPeptideIds(libcpp_vector[PeptideIdentification] & all_peptide_ids, libcpp_vector[PeptideIdentification] & new_peptide_ids, String search_engine)
        Appends a vector of PeptideIdentification to another and prepares Percolator features in MetaInfo (With the respective key "CONCAT:" + search_engine)
        
        
        :param all_peptide_ids: PeptideIdentification vector to append to
        :param new_peptide_ids: PeptideIdentification vector to be appended
        :param search_engine: Search engine to depend on for feature creation
        """
        ...
    
    def mergeMULTISEPeptideIds(self, all_peptide_ids: List[PeptideIdentification] , new_peptide_ids: List[PeptideIdentification] , search_engine: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void mergeMULTISEPeptideIds(libcpp_vector[PeptideIdentification] & all_peptide_ids, libcpp_vector[PeptideIdentification] & new_peptide_ids, String search_engine)
        Merges a vector of PeptideIdentification into another and prepares the merged MetaInfo and scores for collection in addMULTISEFeatures for feature registration
        
        
        :param all_peptide_idsL: PeptideIdentification vector to be merged into
        :param new_peptide_idsL: PeptideIdentification vector to merge
        :param search_engineL: Search engine to create features from their scores
        """
        ...
    
    def mergeMULTISEProteinIds(self, all_protein_ids: List[ProteinIdentification] , new_protein_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void mergeMULTISEProteinIds(libcpp_vector[ProteinIdentification] & all_protein_ids, libcpp_vector[ProteinIdentification] & new_protein_ids)
        Concatenates SearchParameter of multiple search engine runs and merges PeptideEvidences, collects used search engines in MetaInfo for collection in addMULTISEFeatures for feature registration
        
        
        :param all_protein_ids: ProteinIdentification vector to be merged into
        :param new_protein_ids: ProteinIdentification vector to merge
        """
        ...
    
    def addMSGFFeatures(self, peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] ) -> None:
        """
        Cython signature: void addMSGFFeatures(libcpp_vector[PeptideIdentification] & peptide_ids, StringList & feature_set)
        Creates and adds MSGF+ specific Percolator features and registers them in feature_set. MSGF+ should be run with the addFeatures flag enabled
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param feature_set: Register of added features
        """
        ...
    
    def addXTANDEMFeatures(self, peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] ) -> None:
        """
        Cython signature: void addXTANDEMFeatures(libcpp_vector[PeptideIdentification] & peptide_ids, StringList & feature_set)
        Creates and adds X!Tandem specific Percolator features and registers them in feature_set
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param feature_set: Register of added features
        """
        ...
    
    def addCOMETFeatures(self, peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] ) -> None:
        """
        Cython signature: void addCOMETFeatures(libcpp_vector[PeptideIdentification] & peptide_ids, StringList & feature_set)
        Creates and adds Comet specific Percolator features and registers them in feature_set
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param feature_set: Register of added features
        """
        ...
    
    def addMASCOTFeatures(self, peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] ) -> None:
        """
        Cython signature: void addMASCOTFeatures(libcpp_vector[PeptideIdentification] & peptide_ids, StringList & feature_set)
        Creates and adds Mascot specific Percolator features and registers them in feature_set
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param feature_set: Register of added features
        """
        ...
    
    def addMULTISEFeatures(self, peptide_ids: List[PeptideIdentification] , search_engines_used: List[bytes] , feature_set: List[bytes] , complete_only: bool , limits_imputation: bool ) -> None:
        """
        Cython signature: void addMULTISEFeatures(libcpp_vector[PeptideIdentification] & peptide_ids, StringList & search_engines_used, StringList & feature_set, bool complete_only, bool limits_imputation)
        Adds multiple search engine specific Percolator features and registers them in feature_set
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param search_engines_used: The list of search engines to be considered
        :param feature_set: Register of added features
        :param complete_only: Will only add features for PeptideIdentifications where all given search engines identified something
        :param limits_imputation: Uses C++ numeric limits as imputed values instead of min/max of that feature
        """
        ...
    
    def addCONCATSEFeatures(self, peptide_id_list: List[PeptideIdentification] , search_engines_used: List[bytes] , feature_set: List[bytes] ) -> None:
        """
        Cython signature: void addCONCATSEFeatures(libcpp_vector[PeptideIdentification] & peptide_id_list, StringList & search_engines_used, StringList & feature_set)
        Adds multiple search engine specific Percolator features and registers them in feature_set
        
        This struct can be used to store both peak or feature indices
        
        
        :param peptide_ids: PeptideIdentification vector to create Percolator features in
        :param search_engines_used: The list of search engines to be considered
        :param feature_set: Register of added features
        """
        ...
    
    def checkExtraFeatures(self, psms: List[PeptideHit] , extra_features: List[bytes] ) -> None:
        """
        Cython signature: void checkExtraFeatures(libcpp_vector[PeptideHit] & psms, StringList & extra_features)
        Checks and removes requested extra Percolator features that are actually unavailable (to compute)
        
        
        :param psms: The vector of PeptideHit to be checked
        :param extra_features: The list of requested extra features
        """
        ... 


class ProgressLogger:
    """
    Cython implementation of _ProgressLogger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProgressLogger.html>`_

    Base class for all classes that want to report their progress
    
    Per default the progress log is disabled. Use setLogType to enable it
    
    Use startProgress, setProgress and endProgress for the actual logging
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProgressLogger()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProgressLogger ) -> None:
        """
        Cython signature: void ProgressLogger(ProgressLogger &)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class ProtXMLFile:
    """
    Cython implementation of _ProtXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProtXMLFile.html>`_

    Used to load (storing not supported, yet) ProtXML files
    
    This class is used to load (storing not supported, yet) documents that implement
    the schema of ProtXML files
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ProtXMLFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_ids: ProteinIdentification , peptide_ids: PeptideIdentification ) -> None:
        """
        Cython signature: void load(String filename, ProteinIdentification & protein_ids, PeptideIdentification & peptide_ids)
        Loads the identifications of an ProtXML file without identifier
        
        The information is read in and the information is stored in the
        corresponding variables
        
        :raises:
          Exception: FileNotFound is thrown if the file could not be found
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , protein_ids: ProteinIdentification , peptide_ids: PeptideIdentification , document_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(String filename, ProteinIdentification & protein_ids, PeptideIdentification & peptide_ids, String document_id)
        """
        ... 


class ProteaseDB:
    """
    Cython implementation of _ProteaseDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteaseDB.html>`_
    """
    
    def getEnzyme(self, name: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzyme(const String & name)
        """
        ...
    
    def getEnzymeByRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzymeByRegEx(const String & cleavage_regex)
        """
        ...
    
    def getAllNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllNames(libcpp_vector[String] & all_names)
        """
        ...
    
    def getAllXTandemNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllXTandemNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for XTandem
        """
        ...
    
    def getAllOMSSANames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllOMSSANames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for OMSSA
        """
        ...
    
    def getAllCometNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllCometNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for Comet
        """
        ...
    
    def getAllMSGFNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllMSGFNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for MSGFPlus
        """
        ...
    
    def hasEnzyme(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasEnzyme(const String & name)
        """
        ...
    
    def hasRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasRegEx(const String & cleavage_regex)
        """
        ... 


class SequestOutfile:
    """
    Cython implementation of _SequestOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SequestOutfile.html>`_

    Representation of a Sequest output file
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SequestOutfile()
        Representation of a Sequest output file
        """
        ...
    
    @overload
    def __init__(self, in_0: SequestOutfile ) -> None:
        """
        Cython signature: void SequestOutfile(SequestOutfile &)
        """
        ...
    
    def load(self, result_filename: Union[bytes, str, String] , peptide_identifications: List[PeptideIdentification] , protein_identification: ProteinIdentification , p_value_threshold: float , pvalues: List[float] , database: Union[bytes, str, String] , ignore_proteins_per_peptide: bool ) -> None:
        """
        Cython signature: void load(const String & result_filename, libcpp_vector[PeptideIdentification] & peptide_identifications, ProteinIdentification & protein_identification, double p_value_threshold, libcpp_vector[double] & pvalues, const String & database, bool ignore_proteins_per_peptide)
        Loads data from a Sequest outfile
        
        :param result_filename: The file to be loaded
        :param peptide_identifications: The identifications
        :param protein_identification: The protein identifications
        :param p_value_threshold: The significance level (for the peptide hit scores)
        :param pvalues: A list with the pvalues of the peptides (pvalues computed with peptide prophet)
        :param database: The database used for the search
        :param ignore_proteins_per_peptide: This is a hack to deal with files that use a suffix like "+1" in column "Reference", but do not actually list extra protein references in subsequent lines
        """
        ...
    
    def getColumns(self, line: Union[bytes, str, String] , substrings: List[bytes] , number_of_columns: int , reference_column: int ) -> bool:
        """
        Cython signature: bool getColumns(const String & line, libcpp_vector[String] & substrings, size_t number_of_columns, size_t reference_column)
        Retrieves columns from a Sequest outfile line
        """
        ...
    
    def getACAndACType(self, line: Union[bytes, str, String] , accession: String , accession_type: String ) -> None:
        """
        Cython signature: void getACAndACType(String line, String & accession, String & accession_type)
        Retrieves the accession type and accession number from a protein description line
        """
        ...
    
    def __richcmp__(self, other: SequestOutfile, op: int) -> Any:
        ... 


class SiriusExportAlgorithm:
    """
    Cython implementation of _SiriusExportAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusExportAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusExportAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusExportAlgorithm ) -> None:
        """
        Cython signature: void SiriusExportAlgorithm(SiriusExportAlgorithm &)
        """
        ...
    
    def isFeatureOnly(self) -> bool:
        """
        Cython signature: bool isFeatureOnly()
        """
        ...
    
    def getFilterByNumMassTraces(self) -> int:
        """
        Cython signature: unsigned int getFilterByNumMassTraces()
        """
        ...
    
    def getPrecursorMzTolerance(self) -> float:
        """
        Cython signature: double getPrecursorMzTolerance()
        """
        ...
    
    def getPrecursorRtTolerance(self) -> float:
        """
        Cython signature: double getPrecursorRtTolerance()
        """
        ...
    
    def precursorMzToleranceUnitIsPPM(self) -> bool:
        """
        Cython signature: bool precursorMzToleranceUnitIsPPM()
        """
        ...
    
    def isNoMasstraceInfoIsotopePattern(self) -> bool:
        """
        Cython signature: bool isNoMasstraceInfoIsotopePattern()
        """
        ...
    
    def getIsotopePatternIterations(self) -> int:
        """
        Cython signature: int getIsotopePatternIterations()
        """
        ...
    
    def preprocessing(self, featureXML_path: Union[bytes, str, String] , spectra: MSExperiment , feature_mapping_info: FeatureMapping_FeatureMappingInfo , feature_ms2_indices: FeatureMapping_FeatureToMs2Indices ) -> None:
        """
        Cython signature: void preprocessing(const String & featureXML_path, MSExperiment & spectra, FeatureMapping_FeatureMappingInfo & feature_mapping_info, FeatureMapping_FeatureToMs2Indices & feature_ms2_indices)
        Preprocessing needed for SIRIUS
        
        Filter number of masstraces and perform feature mapping
        
        :param featureXML_path: Path to featureXML
        :param spectra: Input of MSExperiment with spectra information
        :param feature_mapping_info: Emtpy - stores FeatureMaps and KDTreeMaps internally
        :param feature_ms2_indices: Empty FeatureToMs2Indices
        """
        ...
    
    def logFeatureSpectraNumber(self, featureXML_path: Union[bytes, str, String] , feature_ms2_indices: FeatureMapping_FeatureToMs2Indices , spectra: MSExperiment ) -> None:
        """
        Cython signature: void logFeatureSpectraNumber(const String & featureXML_path, FeatureMapping_FeatureToMs2Indices & feature_ms2_indices, MSExperiment & spectra)
        Logs number of features and spectra used
        
        Prints the number of features and spectra used (OPENMS_LOG_INFO)
        
        :param featureXML_path: Path to featureXML
        :param feature_ms2_indices: FeatureToMs2Indices with feature mapping
        :param spectra: Input of MSExperiment with spectra information
        """
        ...
    
    def run(self, mzML_files: List[bytes] , featureXML_files: List[bytes] , out_ms: Union[bytes, str, String] , out_compoundinfo: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void run(const StringList & mzML_files, const StringList & featureXML_files, const String & out_ms, const String & out_compoundinfo)
        Runs SiriusExport with mzML and featureXML (optional) files as input.
        
        Generates a SIRIUS .ms file and compound info table (optional).
        
        :param mzML_files: List with paths to mzML files
        :param featureXML_files: List with paths to featureXML files
        :param out_ms: Output file name for SIRIUS .ms file
        :param out_compoundinfo: Output file name for tsv file with compound info
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class SpectrumAlignment:
    """
    Cython implementation of _SpectrumAlignment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAlignment.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAlignment()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAlignment ) -> None:
        """
        Cython signature: void SpectrumAlignment(SpectrumAlignment &)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class SplineInterpolatedPeaks:
    """
    Cython implementation of _SplineInterpolatedPeaks

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineInterpolatedPeaks.html>`_
    """
    
    @overload
    def __init__(self, mz: List[float] , intensity: List[float] ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(libcpp_vector[double] mz, libcpp_vector[double] intensity)
        """
        ...
    
    @overload
    def __init__(self, raw_spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSSpectrum raw_spectrum)
        """
        ...
    
    @overload
    def __init__(self, raw_chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSChromatogram raw_chromatogram)
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineInterpolatedPeaks ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(SplineInterpolatedPeaks &)
        """
        ...
    
    def getPosMin(self) -> float:
        """
        Cython signature: double getPosMin()
        """
        ...
    
    def getPosMax(self) -> float:
        """
        Cython signature: double getPosMax()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def getNavigator(self, scaling: float ) -> SplineSpectrum_Navigator:
        """
        Cython signature: SplineSpectrum_Navigator getNavigator(double scaling)
        """
        ... 


class SplineSpectrum_Navigator:
    """
    Cython implementation of _SplineSpectrum_Navigator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineSpectrum_Navigator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator()
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineSpectrum_Navigator ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(SplineSpectrum_Navigator)
        """
        ...
    
    @overload
    def __init__(self, packages: List[SplinePackage] , posMax: float , scaling: float ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(libcpp_vector[SplinePackage] * packages, double posMax, double scaling)
        """
        ...
    
    def eval(self, pos: float ) -> float:
        """
        Cython signature: double eval(double pos)
        """
        ...
    
    def getNextPos(self, pos: float ) -> float:
        """
        Cython signature: double getNextPos(double pos)
        """
        ... 


class SwathMapMassCorrection:
    """
    Cython implementation of _SwathMapMassCorrection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SwathMapMassCorrection.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SwathMapMassCorrection()
        """
        ...
    
    @overload
    def __init__(self, in_0: SwathMapMassCorrection ) -> None:
        """
        Cython signature: void SwathMapMassCorrection(SwathMapMassCorrection)
        """
        ... 


class Tagging:
    """
    Cython implementation of _Tagging

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Tagging.html>`_

    Meta information about tagging of a sample e.g. ICAT labeling
    
    Holds information about the mass difference between light and heavy tag
    All other relevant information is provided by Modification
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Tagging()
        """
        ...
    
    @overload
    def __init__(self, in_0: Tagging ) -> None:
        """
        Cython signature: void Tagging(Tagging &)
        """
        ...
    
    def getMassShift(self) -> float:
        """
        Cython signature: double getMassShift()
        Returns the mass difference between light and heavy variant (default is 0.0)
        """
        ...
    
    def setMassShift(self, mass_shift: float ) -> None:
        """
        Cython signature: void setMassShift(double mass_shift)
        Sets the mass difference between light and heavy variant
        """
        ...
    
    def getVariant(self) -> int:
        """
        Cython signature: IsotopeVariant getVariant()
        Returns the isotope variant of the tag (default is LIGHT)
        """
        ...
    
    def setVariant(self, variant: int ) -> None:
        """
        Cython signature: void setVariant(IsotopeVariant variant)
        Sets the isotope variant of the tag
        """
        ... 


class TargetedExperiment:
    """
    Cython implementation of _TargetedExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TargetedExperiment.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TargetedExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: TargetedExperiment ) -> None:
        """
        Cython signature: void TargetedExperiment(TargetedExperiment &)
        """
        ...
    
    def __add__(self: TargetedExperiment, other: TargetedExperiment) -> TargetedExperiment:
        ...
    
    def __iadd__(self: TargetedExperiment, other: TargetedExperiment) -> TargetedExperiment:
        ...
    
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        """
        ...
    
    def sortTransitionsByProductMZ(self) -> None:
        """
        Cython signature: void sortTransitionsByProductMZ()
        """
        ...
    
    def setCVs(self, cvs: List[CV] ) -> None:
        """
        Cython signature: void setCVs(libcpp_vector[CV] cvs)
        """
        ...
    
    def getCVs(self) -> List[CV]:
        """
        Cython signature: libcpp_vector[CV] getCVs()
        """
        ...
    
    def addCV(self, cv: CV ) -> None:
        """
        Cython signature: void addCV(CV cv)
        """
        ...
    
    def setContacts(self, contacts: List[Contact] ) -> None:
        """
        Cython signature: void setContacts(libcpp_vector[Contact] contacts)
        """
        ...
    
    def getContacts(self) -> List[Contact]:
        """
        Cython signature: libcpp_vector[Contact] getContacts()
        """
        ...
    
    def addContact(self, contact: Contact ) -> None:
        """
        Cython signature: void addContact(Contact contact)
        """
        ...
    
    def setPublications(self, publications: List[Publication] ) -> None:
        """
        Cython signature: void setPublications(libcpp_vector[Publication] publications)
        """
        ...
    
    def getPublications(self) -> List[Publication]:
        """
        Cython signature: libcpp_vector[Publication] getPublications()
        """
        ...
    
    def addPublication(self, publication: Publication ) -> None:
        """
        Cython signature: void addPublication(Publication publication)
        """
        ...
    
    def setTargetCVTerms(self, cv_terms: CVTermList ) -> None:
        """
        Cython signature: void setTargetCVTerms(CVTermList cv_terms)
        """
        ...
    
    def getTargetCVTerms(self) -> CVTermList:
        """
        Cython signature: CVTermList getTargetCVTerms()
        """
        ...
    
    def addTargetCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addTargetCVTerm(CVTerm cv_term)
        """
        ...
    
    def setTargetMetaValue(self, name: Union[bytes, str, String] , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setTargetMetaValue(String name, DataValue value)
        """
        ...
    
    def setInstruments(self, instruments: List[TargetedExperiment_Instrument] ) -> None:
        """
        Cython signature: void setInstruments(libcpp_vector[TargetedExperiment_Instrument] instruments)
        """
        ...
    
    def getInstruments(self) -> List[TargetedExperiment_Instrument]:
        """
        Cython signature: libcpp_vector[TargetedExperiment_Instrument] getInstruments()
        """
        ...
    
    def addInstrument(self, instrument: TargetedExperiment_Instrument ) -> None:
        """
        Cython signature: void addInstrument(TargetedExperiment_Instrument instrument)
        """
        ...
    
    def setSoftware(self, software: List[Software] ) -> None:
        """
        Cython signature: void setSoftware(libcpp_vector[Software] software)
        """
        ...
    
    def getSoftware(self) -> List[Software]:
        """
        Cython signature: libcpp_vector[Software] getSoftware()
        """
        ...
    
    def addSoftware(self, software: Software ) -> None:
        """
        Cython signature: void addSoftware(Software software)
        """
        ...
    
    def setProteins(self, proteins: List[Protein] ) -> None:
        """
        Cython signature: void setProteins(libcpp_vector[Protein] proteins)
        """
        ...
    
    def getProteins(self) -> List[Protein]:
        """
        Cython signature: libcpp_vector[Protein] getProteins()
        """
        ...
    
    def getProteinByRef(self, ref: Union[bytes, str, String] ) -> Protein:
        """
        Cython signature: Protein getProteinByRef(String ref)
        """
        ...
    
    def hasProtein(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasProtein(String ref)
        """
        ...
    
    def addProtein(self, protein: Protein ) -> None:
        """
        Cython signature: void addProtein(Protein protein)
        """
        ...
    
    def setCompounds(self, rhs: List[Compound] ) -> None:
        """
        Cython signature: void setCompounds(libcpp_vector[Compound] rhs)
        """
        ...
    
    def getCompounds(self) -> List[Compound]:
        """
        Cython signature: libcpp_vector[Compound] getCompounds()
        """
        ...
    
    def addCompound(self, rhs: Compound ) -> None:
        """
        Cython signature: void addCompound(Compound rhs)
        """
        ...
    
    def hasCompound(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCompound(String ref)
        """
        ...
    
    def getCompoundByRef(self, ref: Union[bytes, str, String] ) -> Compound:
        """
        Cython signature: Compound getCompoundByRef(String ref)
        """
        ...
    
    def setPeptides(self, rhs: List[Peptide] ) -> None:
        """
        Cython signature: void setPeptides(libcpp_vector[Peptide] rhs)
        """
        ...
    
    def getPeptides(self) -> List[Peptide]:
        """
        Cython signature: libcpp_vector[Peptide] getPeptides()
        """
        ...
    
    def hasPeptide(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasPeptide(String ref)
        """
        ...
    
    def getPeptideByRef(self, ref: Union[bytes, str, String] ) -> Peptide:
        """
        Cython signature: Peptide getPeptideByRef(String ref)
        """
        ...
    
    def addPeptide(self, rhs: Peptide ) -> None:
        """
        Cython signature: void addPeptide(Peptide rhs)
        """
        ...
    
    def setTransitions(self, transitions: List[ReactionMonitoringTransition] ) -> None:
        """
        Cython signature: void setTransitions(libcpp_vector[ReactionMonitoringTransition] transitions)
        """
        ...
    
    def getTransitions(self) -> List[ReactionMonitoringTransition]:
        """
        Cython signature: libcpp_vector[ReactionMonitoringTransition] getTransitions()
        """
        ...
    
    def addTransition(self, transition: ReactionMonitoringTransition ) -> None:
        """
        Cython signature: void addTransition(ReactionMonitoringTransition transition)
        """
        ...
    
    def setIncludeTargets(self, targets: List[IncludeExcludeTarget] ) -> None:
        """
        Cython signature: void setIncludeTargets(libcpp_vector[IncludeExcludeTarget] targets)
        """
        ...
    
    def getIncludeTargets(self) -> List[IncludeExcludeTarget]:
        """
        Cython signature: libcpp_vector[IncludeExcludeTarget] getIncludeTargets()
        """
        ...
    
    def addIncludeTarget(self, target: IncludeExcludeTarget ) -> None:
        """
        Cython signature: void addIncludeTarget(IncludeExcludeTarget target)
        """
        ...
    
    def setExcludeTargets(self, targets: List[IncludeExcludeTarget] ) -> None:
        """
        Cython signature: void setExcludeTargets(libcpp_vector[IncludeExcludeTarget] targets)
        """
        ...
    
    def getExcludeTargets(self) -> List[IncludeExcludeTarget]:
        """
        Cython signature: libcpp_vector[IncludeExcludeTarget] getExcludeTargets()
        """
        ...
    
    def addExcludeTarget(self, target: IncludeExcludeTarget ) -> None:
        """
        Cython signature: void addExcludeTarget(IncludeExcludeTarget target)
        """
        ...
    
    def setSourceFiles(self, source_files: List[SourceFile] ) -> None:
        """
        Cython signature: void setSourceFiles(libcpp_vector[SourceFile] source_files)
        """
        ...
    
    def getSourceFiles(self) -> List[SourceFile]:
        """
        Cython signature: libcpp_vector[SourceFile] getSourceFiles()
        """
        ...
    
    def addSourceFile(self, source_file: SourceFile ) -> None:
        """
        Cython signature: void addSourceFile(SourceFile source_file)
        """
        ...
    
    def containsInvalidReferences(self) -> bool:
        """
        Cython signature: bool containsInvalidReferences()
        """
        ...
    
    def __richcmp__(self, other: TargetedExperiment, op: int) -> Any:
        ... 


class TransformationXMLFile:
    """
    Cython implementation of _TransformationXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void TransformationXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription , fit_model: bool ) -> None:
        """
        Cython signature: void load(String, TransformationDescription &, bool fit_model)
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void store(String, TransformationDescription)
        """
        ... 


class UnimodXMLFile:
    """
    Cython implementation of _UnimodXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1UnimodXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void UnimodXMLFile()
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class XQuestResultXMLFile:
    """
    Cython implementation of _XQuestResultXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XQuestResultXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XQuestResultXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: XQuestResultXMLFile ) -> None:
        """
        Cython signature: void XQuestResultXMLFile(XQuestResultXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , pep_ids: List[PeptideIdentification] , prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[PeptideIdentification] & pep_ids, libcpp_vector[ProteinIdentification] & prot_ids)
        Load the content of the xquest.xml file into the provided data structures
        
        :param filename: Filename of the file which is to be loaded
        :param pep_ids: Where the spectra with identifications of the input file will be loaded to
        :param prot_ids: Where the protein identification of the input file will be loaded to
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , poid: List[ProteinIdentification] , peid: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(const String & filename, libcpp_vector[ProteinIdentification] & poid, libcpp_vector[PeptideIdentification] & peid)
        Stores the identifications in a xQuest XML file
        """
        ...
    
    def getNumberOfHits(self) -> int:
        """
        Cython signature: int getNumberOfHits()
        Returns the total number of hits in the file
        """
        ...
    
    def getMinScore(self) -> float:
        """
        Cython signature: double getMinScore()
        Returns minimum score among the hits in the file
        """
        ...
    
    def getMaxScore(self) -> float:
        """
        Cython signature: double getMaxScore()
        Returns maximum score among the hits in the file
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , preprocessed_pair_spectra: OPXL_PreprocessedPairSpectra , spectrum_pairs: List[List[int, int]] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, OPXL_PreprocessedPairSpectra preprocessed_pair_spectra, libcpp_vector[libcpp_pair[size_t,size_t]] spectrum_pairs, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing matching peaks between heavy and light spectra after comparing and filtering
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param preprocessed_pair_spectra: The preprocessed spectra after comparing and filtering
        :param spectrum_pairs: Indices of spectrum pairs in the input map
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap. The indices in spectrum_pairs correspond to spectra in this map
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing spectra for visualization. This version of the function is meant to be used for label-free linkers
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class __DerivatizationAgent:
    None
    NOT_SELECTED : int
    TBDMS : int
    SIZE_OF_DERIVATIZATIONAGENT : int

    def getMapping(self) -> Dict[int, str]:
       ...
    DerivatizationAgent : __DerivatizationAgent 


class DriftTimeUnit:
    None
    NONE : int
    MILLISECOND : int
    VSSC : int
    FAIMS_COMPENSATION_VOLTAGE : int
    SIZE_OF_DRIFTTIMEUNIT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IMFormat:
    None
    NONE : int
    CONCATENATED : int
    MULTIPLE_SPECTRA : int
    MIXED : int
    SIZE_OF_IMFORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ITRAQ_TYPES:
    None
    FOURPLEX : int
    EIGHTPLEX : int
    TMT_SIXPLEX : int
    SIZE_OF_ITRAQ_TYPES : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IsotopeVariant:
    None
    LIGHT : int
    HEAVY : int
    SIZE_OF_ISOTOPEVARIANT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class LogType:
    None
    CMD : int
    GUI : int
    NONE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __MassIntensityType:
    None
    NORM_MAX : int
    NORM_SUM : int
    SIZE_OF_MASSINTENSITYTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ...
    MassIntensityType : __MassIntensityType 


class __PeptidePosition:
    None
    INTERNAL : int
    C_TERM : int
    N_TERM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ProteinProteinCrossLinkType:
    None
    CROSS : int
    MONO : int
    LOOP : int
    NUMBER_OF_CROSS_LINK_TYPES : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __RETURN_STATUS:
    None
    SOLVED : int
    ITERATION_EXCEEDED : int

    def getMapping(self) -> Dict[int, str]:
       ... 

