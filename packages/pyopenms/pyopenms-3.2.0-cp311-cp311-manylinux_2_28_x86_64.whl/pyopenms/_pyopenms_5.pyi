from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_Deisotoper_deisotopeAndSingleCharge(spectra: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool , min_charge: int , max_charge: int , keep_only_deisotoped: bool , min_isopeaks: int , max_isopeaks: int , make_single_charged: bool , annotate_charge: bool , annotate_iso_peak_count: bool , use_decreasing_model: bool , start_intensity_check: int , add_up_intensity: bool ) -> None:
    """
    Cython signature: void deisotopeAndSingleCharge(MSSpectrum & spectra, double fragment_tolerance, bool fragment_unit_ppm, int min_charge, int max_charge, bool keep_only_deisotoped, unsigned int min_isopeaks, unsigned int max_isopeaks, bool make_single_charged, bool annotate_charge, bool annotate_iso_peak_count, bool use_decreasing_model, unsigned int start_intensity_check, bool add_up_intensity)
    """
    ...

def __static_Deisotoper_deisotopeAndSingleChargeDefault(spectra: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool ) -> None:
    """
    Cython signature: void deisotopeAndSingleChargeDefault(MSSpectrum & spectra, double fragment_tolerance, bool fragment_unit_ppm)
    """
    ...

def __static_Deisotoper_deisotopeWithAveragineModel(spectrum: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool , number_of_final_peaks: int , min_charge: int , max_charge: int , keep_only_deisotoped: bool , min_isopeaks: int , max_isopeaks: int , make_single_charged: bool , annotate_charge: bool , annotate_iso_peak_count: bool , add_up_intensity: bool ) -> None:
    """
    Cython signature: void deisotopeWithAveragineModel(MSSpectrum & spectrum, double fragment_tolerance, bool fragment_unit_ppm, int number_of_final_peaks, int min_charge, int max_charge, bool keep_only_deisotoped, unsigned int min_isopeaks, unsigned int max_isopeaks, bool make_single_charged, bool annotate_charge, bool annotate_iso_peak_count, bool add_up_intensity)
    """
    ...

def __static_NASequence_fromString(s: Union[bytes, str, String] ) -> NASequence:
    """
    Cython signature: NASequence fromString(const String & s)
    """
    ...

def __static_TransformationDescription_getModelTypes(result: List[bytes] ) -> None:
    """
    Cython signature: void getModelTypes(StringList result)
    """
    ...


class AQS_featureConcentration:
    """
    Cython implementation of _AQS_featureConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_featureConcentration.html>`_
    """
    
    feature: Feature
    
    IS_feature: Feature
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_featureConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_featureConcentration ) -> None:
        """
        Cython signature: void AQS_featureConcentration(AQS_featureConcentration &)
        """
        ... 


class AQS_runConcentration:
    """
    Cython implementation of _AQS_runConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_runConcentration.html>`_
    """
    
    sample_name: Union[bytes, str, String]
    
    component_name: Union[bytes, str, String]
    
    IS_component_name: Union[bytes, str, String]
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_runConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_runConcentration ) -> None:
        """
        Cython signature: void AQS_runConcentration(AQS_runConcentration &)
        """
        ... 


class AbsoluteQuantitationStandards:
    """
    Cython implementation of _AbsoluteQuantitationStandards

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandards.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandards ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards(AbsoluteQuantitationStandards &)
        """
        ...
    
    def getComponentFeatureConcentrations(self, run_concentrations: List[AQS_runConcentration] , feature_maps: List[FeatureMap] , component_name: Union[bytes, str, String] , feature_concentrations: List[AQS_featureConcentration] ) -> None:
        """
        Cython signature: void getComponentFeatureConcentrations(libcpp_vector[AQS_runConcentration] & run_concentrations, libcpp_vector[FeatureMap] & feature_maps, const String & component_name, libcpp_vector[AQS_featureConcentration] & feature_concentrations)
        """
        ... 


class AcquisitionInfo:
    """
    Cython implementation of _AcquisitionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AcquisitionInfo.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AcquisitionInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: AcquisitionInfo ) -> None:
        """
        Cython signature: void AcquisitionInfo(AcquisitionInfo &)
        """
        ...
    
    def getMethodOfCombination(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getMethodOfCombination()
        Returns the method of combination
        """
        ...
    
    def setMethodOfCombination(self, method: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setMethodOfCombination(String method)
        Sets the method of combination
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Number a Acquisition objects
        """
        ...
    
    def __getitem__(self, in_0: int ) -> Acquisition:
        """
        Cython signature: Acquisition & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: Acquisition ) -> None:
        """Cython signature: Acquisition & operator[](size_t)"""
        ...
    
    def push_back(self, in_0: Acquisition ) -> None:
        """
        Cython signature: void push_back(Acquisition)
        Append a Acquisition object
        """
        ...
    
    def resize(self, n: int ) -> None:
        """
        Cython signature: void resize(size_t n)
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
    
    def __richcmp__(self, other: AcquisitionInfo, op: int) -> Any:
        ... 


class AnnotationStatistics:
    """
    Cython implementation of _AnnotationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AnnotationStatistics.html>`_
    """
    
    states: List[int]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AnnotationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: AnnotationStatistics ) -> None:
        """
        Cython signature: void AnnotationStatistics(AnnotationStatistics &)
        """
        ...
    
    def __richcmp__(self, other: AnnotationStatistics, op: int) -> Any:
        ... 


class Attachment:
    """
    Cython implementation of _Attachment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::QcMLFile_1_1Attachment.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    binary: Union[bytes, str, String]
    
    qualityRef: Union[bytes, str, String]
    
    colTypes: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Attachment()
        """
        ...
    
    @overload
    def __init__(self, in_0: Attachment ) -> None:
        """
        Cython signature: void Attachment(Attachment &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def toCSVString(self, separator: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toCSVString(String separator)
        """
        ...
    
    def __richcmp__(self, other: Attachment, op: int) -> Any:
        ... 


class CVMappingFile:
    """
    Cython implementation of _CVMappingFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void CVMappingFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , cv_mappings: CVMappings , strip_namespaces: bool ) -> None:
        """
        Cython signature: void load(const String & filename, CVMappings & cv_mappings, bool strip_namespaces)
        Loads CvMappings from the given file
        """
        ... 


class CVTermList:
    """
    Cython implementation of _CVTermList

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTermList.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTermList()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTermList ) -> None:
        """
        Cython signature: void CVTermList(CVTermList &)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        Sets the CV terms
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        Replaces the specified CV term
        """
        ...
    
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        Returns the accession string of the term
        """
        ...
    
    def addCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVTerm & term)
        Adds a CV term
        """
        ...
    
    def hasCVTerm(self, accession: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVTerm(String accession)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
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
    
    def __richcmp__(self, other: CVTermList, op: int) -> Any:
        ... 


class ChromatogramPeak:
    """
    Cython implementation of _ChromatogramPeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ChromatogramPeak_1_1ChromatogramPeak.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramPeak()
        A 1-dimensional raw data point or peak for chromatograms
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramPeak ) -> None:
        """
        Cython signature: void ChromatogramPeak(ChromatogramPeak &)
        """
        ...
    
    @overload
    def __init__(self, retention_time: DPosition1 , intensity: float ) -> None:
        """
        Cython signature: void ChromatogramPeak(DPosition1 retention_time, double intensity)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: double getIntensity()
        Returns the intensity
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(double)
        Sets the intensity
        """
        ...
    
    def getPosition(self) -> DPosition1:
        """
        Cython signature: DPosition1 getPosition()
        """
        ...
    
    def setPosition(self, in_0: DPosition1 ) -> None:
        """
        Cython signature: void setPosition(DPosition1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the retention time
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Sets retention time
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        Alias for getRT()
        """
        ...
    
    def setPos(self, in_0: float ) -> None:
        """
        Cython signature: void setPos(double)
        Alias for setRT()
        """
        ...
    
    def __richcmp__(self, other: ChromatogramPeak, op: int) -> Any:
        ... 


class CrossLinkSpectrumMatch:
    """
    Cython implementation of _CrossLinkSpectrumMatch

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1CrossLinkSpectrumMatch.html>`_
    """
    
    cross_link: ProteinProteinCrossLink
    
    scan_index_light: int
    
    scan_index_heavy: int
    
    score: float
    
    rank: int
    
    xquest_score: float
    
    pre_score: float
    
    percTIC: float
    
    wTIC: float
    
    wTICold: float
    
    int_sum: float
    
    intsum_alpha: float
    
    intsum_beta: float
    
    total_current: float
    
    precursor_error_ppm: float
    
    match_odds: float
    
    match_odds_alpha: float
    
    match_odds_beta: float
    
    log_occupancy: float
    
    log_occupancy_alpha: float
    
    log_occupancy_beta: float
    
    xcorrx_max: float
    
    xcorrc_max: float
    
    matched_linear_alpha: int
    
    matched_linear_beta: int
    
    matched_xlink_alpha: int
    
    matched_xlink_beta: int
    
    num_iso_peaks_mean: float
    
    num_iso_peaks_mean_linear_alpha: float
    
    num_iso_peaks_mean_linear_beta: float
    
    num_iso_peaks_mean_xlinks_alpha: float
    
    num_iso_peaks_mean_xlinks_beta: float
    
    ppm_error_abs_sum_linear_alpha: float
    
    ppm_error_abs_sum_linear_beta: float
    
    ppm_error_abs_sum_xlinks_alpha: float
    
    ppm_error_abs_sum_xlinks_beta: float
    
    ppm_error_abs_sum_linear: float
    
    ppm_error_abs_sum_xlinks: float
    
    ppm_error_abs_sum_alpha: float
    
    ppm_error_abs_sum_beta: float
    
    ppm_error_abs_sum: float
    
    precursor_correction: int
    
    precursor_total_intensity: float
    
    precursor_target_intensity: float
    
    precursor_signal_proportion: float
    
    precursor_target_peak_count: int
    
    precursor_residual_peak_count: int
    
    frag_annotations: List[PeptideHit_PeakAnnotation]
    
    peptide_id_index: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CrossLinkSpectrumMatch()
        """
        ...
    
    @overload
    def __init__(self, in_0: CrossLinkSpectrumMatch ) -> None:
        """
        Cython signature: void CrossLinkSpectrumMatch(CrossLinkSpectrumMatch &)
        """
        ... 


class Deisotoper:
    """
    Cython implementation of _Deisotoper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Deisotoper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Deisotoper()
        """
        ...
    
    @overload
    def __init__(self, in_0: Deisotoper ) -> None:
        """
        Cython signature: void Deisotoper(Deisotoper &)
        """
        ...
    
    deisotopeAndSingleCharge: __static_Deisotoper_deisotopeAndSingleCharge
    
    deisotopeAndSingleChargeDefault: __static_Deisotoper_deisotopeAndSingleChargeDefault
    
    deisotopeWithAveragineModel: __static_Deisotoper_deisotopeWithAveragineModel 


class EmgModel:
    """
    Cython implementation of _EmgModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgModel.html>`_
      -- Inherits from ['InterpolationModel']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgModel()
        Exponentially modified gaussian distribution model for elution profiles
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgModel ) -> None:
        """
        Cython signature: void EmgModel(EmgModel &)
        """
        ...
    
    def getIntensity(self, coord: float ) -> float:
        """
        Cython signature: double getIntensity(double coord)
        Access model predicted intensity at position 'pos'
        """
        ...
    
    def getScalingFactor(self) -> float:
        """
        Cython signature: double getScalingFactor()
        Returns the interpolation class
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        Sets the offset of the model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns the "center" of the model, particular definition (depends on the derived model)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        Sets sample/supporting points of interpolation wrt params
        """
        ...
    
    def setInterpolationStep(self, interpolation_step: float ) -> None:
        """
        Cython signature: void setInterpolationStep(double interpolation_step)
        Sets the interpolation step for the linear interpolation of the model
        """
        ...
    
    def setScalingFactor(self, scaling: float ) -> None:
        """
        Cython signature: void setScalingFactor(double scaling)
        Sets the scaling factor of the model
        """
        ...
    
    def getInterpolation(self) -> LinearInterpolation:
        """
        Cython signature: LinearInterpolation getInterpolation()
        Returns the interpolation class
        """
        ... 


class FeatureFinderAlgorithmPicked:
    """
    Cython implementation of _FeatureFinderAlgorithmPicked

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderAlgorithmPicked.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderAlgorithmPicked()
        """
        ...
    
    def run(self, input_map: MSExperiment , output: FeatureMap , param: Param , seeds: FeatureMap ) -> None:
        """
        Cython signature: void run(MSExperiment & input_map, FeatureMap & output, Param & param, FeatureMap & seeds)
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


class FeatureFinderIdentificationAlgorithm:
    """
    Cython implementation of _FeatureFinderIdentificationAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderIdentificationAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']

    Algorithm class for FeatureFinderIdentification
    
    External IDs (peptides_ext, proteins_ext) may be empty,
    in which case no machine learning or FDR estimation will be performed.
    Optional seeds from e.g. untargeted FeatureFinders can be added with
    seeds.
    Results will be written to features .
    Caution: peptide IDs will be shrunk to best hit, FFid metavalues added
    and potential seed IDs added.
    
    Usage:
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderIdentificationAlgorithm()
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap , seeds: FeatureMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features, FeatureMap & seeds)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        :param seeds: Optional seeds for feature detection from e.g. untargeted FeatureFinders
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap , seeds: FeatureMap , spectra_file: String ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features, FeatureMap & seeds, String & spectra_file)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        :param seeds: Optional seeds for feature detection from e.g. untargeted FeatureFinders
        :param spectra_file: Path will be stored in features in case the MSExperiment has no proper primaryMSRunPath
        """
        ...
    
    def runOnCandidates(self, features: FeatureMap ) -> None:
        """
        Cython signature: void runOnCandidates(FeatureMap & features)
        Run feature detection on identified features (e.g. loaded from an IdXML file)
        """
        ...
    
    def setMSData(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setMSData(const MSExperiment &)
        Sets ms data
        """
        ...
    
    def getMSData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getMSData()
        Returns ms data as MSExperiment
        """
        ...
    
    def getChromatograms(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getChromatograms()
        Returns chromatogram data as MSExperiment
        """
        ...
    
    def getLibrary(self) -> TargetedExperiment:
        """
        Cython signature: TargetedExperiment getLibrary()
        Returns constructed assay library
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


class FeatureGroupingAlgorithmLabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmLabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmLabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmLabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
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


class GNPSQuantificationFile:
    """
    Cython implementation of _GNPSQuantificationFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GNPSQuantificationFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GNPSQuantificationFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: GNPSQuantificationFile ) -> None:
        """
        Cython signature: void GNPSQuantificationFile(GNPSQuantificationFile &)
        """
        ...
    
    def store(self, consensus_map: ConsensusMap , output_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const ConsensusMap & consensus_map, const String & output_file)
        Write feature quantification table (txt file) from a ConsensusMap. Required for GNPS FBMN.
        
        The table contains map information on the featureXML files from which the ConsensusMap was generated as well as
        a row for every consensus feature with information on rt, mz, intensity, width and quality. The same information is
        added for each original feature in the consensus feature.
        
        :param consensus_map: Input ConsensusMap annotated with IonIdentityMolecularNetworking.annotateConsensusMap.
        :param output_file: Output file path for the feature quantification table.
        """
        ... 


class Instrument:
    """
    Cython implementation of _Instrument

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Instrument.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Instrument()
        Description of a MS instrument
        """
        ...
    
    @overload
    def __init__(self, in_0: Instrument ) -> None:
        """
        Cython signature: void Instrument(Instrument &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the instrument
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the instrument
        """
        ...
    
    def getVendor(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVendor()
        Returns the instrument vendor
        """
        ...
    
    def setVendor(self, vendor: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setVendor(String vendor)
        Sets the instrument vendor
        """
        ...
    
    def getModel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModel()
        Returns the instrument model
        """
        ...
    
    def setModel(self, model: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModel(String model)
        Sets the instrument model
        """
        ...
    
    def getCustomizations(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCustomizations()
        Returns a description of customizations
        """
        ...
    
    def setCustomizations(self, customizations: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCustomizations(String customizations)
        Sets the a description of customizations
        """
        ...
    
    def getIonSources(self) -> List[IonSource]:
        """
        Cython signature: libcpp_vector[IonSource] getIonSources()
        Returns the ion source list
        """
        ...
    
    def setIonSources(self, ion_sources: List[IonSource] ) -> None:
        """
        Cython signature: void setIonSources(libcpp_vector[IonSource] ion_sources)
        Sets the ion source list
        """
        ...
    
    def getMassAnalyzers(self) -> List[MassAnalyzer]:
        """
        Cython signature: libcpp_vector[MassAnalyzer] getMassAnalyzers()
        Returns the mass analyzer list
        """
        ...
    
    def setMassAnalyzers(self, mass_analyzers: List[MassAnalyzer] ) -> None:
        """
        Cython signature: void setMassAnalyzers(libcpp_vector[MassAnalyzer] mass_analyzers)
        Sets the mass analyzer list
        """
        ...
    
    def getIonDetectors(self) -> List[IonDetector]:
        """
        Cython signature: libcpp_vector[IonDetector] getIonDetectors()
        Returns the ion detector list
        """
        ...
    
    def setIonDetectors(self, ion_detectors: List[IonDetector] ) -> None:
        """
        Cython signature: void setIonDetectors(libcpp_vector[IonDetector] ion_detectors)
        Sets the ion detector list
        """
        ...
    
    def getSoftware(self) -> Software:
        """
        Cython signature: Software getSoftware()
        Returns the instrument software
        """
        ...
    
    def setSoftware(self, software: Software ) -> None:
        """
        Cython signature: void setSoftware(Software software)
        Sets the instrument software
        """
        ...
    
    def getIonOptics(self) -> int:
        """
        Cython signature: IonOpticsType getIonOptics()
        Returns the ion optics type
        """
        ...
    
    def setIonOptics(self, ion_optics: int ) -> None:
        """
        Cython signature: void setIonOptics(IonOpticsType ion_optics)
        Sets the ion optics type
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
    
    def __richcmp__(self, other: Instrument, op: int) -> Any:
        ... 


class IsobaricIsotopeCorrector:
    """
    Cython implementation of _IsobaricIsotopeCorrector

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricIsotopeCorrector.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricIsotopeCorrector ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector(IsobaricIsotopeCorrector &)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqEightPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqFourPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTSixPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTTenPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTTenPlexQuantitationMethod * quant_method)
        """
        ... 


class IsobaricNormalizer:
    """
    Cython implementation of _IsobaricNormalizer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricNormalizer.html>`_
    """
    
    @overload
    def __init__(self, in_0: IsobaricNormalizer ) -> None:
        """
        Cython signature: void IsobaricNormalizer(IsobaricNormalizer &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricNormalizer(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricNormalizer(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricNormalizer(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricNormalizer(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def normalize(self, consensus_map: ConsensusMap ) -> None:
        """
        Cython signature: void normalize(ConsensusMap & consensus_map)
        """
        ... 


class ItraqFourPlexQuantitationMethod:
    """
    Cython implementation of _ItraqFourPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqFourPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqFourPlexQuantitationMethod()
        iTRAQ 4 plex quantitation to be used with the IsobaricQuantitation
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void ItraqFourPlexQuantitationMethod(ItraqFourPlexQuantitationMethod &)
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


class LightCompound:
    """
    Cython implementation of _LightCompound

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightCompound.html>`_
    """
    
    rt: float
    
    drift_time: float
    
    charge: int
    
    sequence: bytes
    
    protein_refs: List[bytes]
    
    peptide_group_label: bytes
    
    id: bytes
    
    sum_formula: bytes
    
    compound_name: bytes
    
    modifications: List[LightModification]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightCompound()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightCompound ) -> None:
        """
        Cython signature: void LightCompound(LightCompound &)
        """
        ...
    
    def setDriftTime(self, d: float ) -> None:
        """
        Cython signature: void setDriftTime(double d)
        """
        ...
    
    def getDriftTime(self) -> float:
        """
        Cython signature: double getDriftTime()
        """
        ...
    
    def getChargeState(self) -> int:
        """
        Cython signature: int getChargeState()
        """
        ...
    
    def isPeptide(self) -> bool:
        """
        Cython signature: bool isPeptide()
        """
        ...
    
    def setChargeState(self, ch: int ) -> None:
        """
        Cython signature: void setChargeState(int ch)
        """
        ... 


class LightModification:
    """
    Cython implementation of _LightModification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightModification.html>`_
    """
    
    location: int
    
    unimod_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightModification()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightModification ) -> None:
        """
        Cython signature: void LightModification(LightModification &)
        """
        ... 


class LightProtein:
    """
    Cython implementation of _LightProtein

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightProtein.html>`_
    """
    
    id: bytes
    
    sequence: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightProtein()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightProtein ) -> None:
        """
        Cython signature: void LightProtein(LightProtein &)
        """
        ... 


class LightTargetedExperiment:
    """
    Cython implementation of _LightTargetedExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTargetedExperiment.html>`_
    """
    
    transitions: List[LightTransition]
    
    compounds: List[LightCompound]
    
    proteins: List[LightProtein]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTargetedExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTargetedExperiment ) -> None:
        """
        Cython signature: void LightTargetedExperiment(LightTargetedExperiment &)
        """
        ...
    
    def getTransitions(self) -> List[LightTransition]:
        """
        Cython signature: libcpp_vector[LightTransition] getTransitions()
        """
        ...
    
    def getCompounds(self) -> List[LightCompound]:
        """
        Cython signature: libcpp_vector[LightCompound] getCompounds()
        """
        ...
    
    def getProteins(self) -> List[LightProtein]:
        """
        Cython signature: libcpp_vector[LightProtein] getProteins()
        """
        ...
    
    def getCompoundByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getCompoundByRef(libcpp_string & ref)
        """
        ...
    
    def getPeptideByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getPeptideByRef(libcpp_string & ref)
        """
        ... 


class LightTransition:
    """
    Cython implementation of _LightTransition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTransition.html>`_
    """
    
    transition_name: bytes
    
    peptide_ref: bytes
    
    library_intensity: float
    
    product_mz: float
    
    precursor_mz: float
    
    fragment_charge: int
    
    decoy: bool
    
    detecting_transition: bool
    
    quantifying_transition: bool
    
    identifying_transition: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTransition()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTransition ) -> None:
        """
        Cython signature: void LightTransition(LightTransition &)
        """
        ...
    
    def getProductChargeState(self) -> int:
        """
        Cython signature: int getProductChargeState()
        """
        ...
    
    def isProductChargeStateSet(self) -> bool:
        """
        Cython signature: bool isProductChargeStateSet()
        """
        ...
    
    def getNativeID(self) -> bytes:
        """
        Cython signature: libcpp_string getNativeID()
        """
        ...
    
    def getPeptideRef(self) -> bytes:
        """
        Cython signature: libcpp_string getPeptideRef()
        """
        ...
    
    def getLibraryIntensity(self) -> float:
        """
        Cython signature: double getLibraryIntensity()
        """
        ...
    
    def setLibraryIntensity(self, l: float ) -> None:
        """
        Cython signature: void setLibraryIntensity(double l)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        """
        ...
    
    def getCompoundRef(self) -> bytes:
        """
        Cython signature: libcpp_string getCompoundRef()
        """
        ...
    
    def setDetectingTransition(self, d: bool ) -> None:
        """
        Cython signature: void setDetectingTransition(bool d)
        """
        ...
    
    def isDetectingTransition(self) -> bool:
        """
        Cython signature: bool isDetectingTransition()
        """
        ...
    
    def setQuantifyingTransition(self, q: bool ) -> None:
        """
        Cython signature: void setQuantifyingTransition(bool q)
        """
        ...
    
    def isQuantifyingTransition(self) -> bool:
        """
        Cython signature: bool isQuantifyingTransition()
        """
        ...
    
    def setIdentifyingTransition(self, i: bool ) -> None:
        """
        Cython signature: void setIdentifyingTransition(bool i)
        """
        ...
    
    def isIdentifyingTransition(self) -> bool:
        """
        Cython signature: bool isIdentifyingTransition()
        """
        ... 


class LogConfigHandler:
    """
    Cython implementation of _LogConfigHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LogConfigHandler.html>`_
    """
    
    def parse(self, setting: List[bytes] ) -> Param:
        """
        Cython signature: Param parse(const StringList & setting)
        Translates the given list of parameter settings into a LogStream configuration
        
        Translates the given list of parameter settings into a LogStream configuration.
        Usually this list stems from a command line call.
        
        Each element in the stringlist should follow this naming convention
        
        <LOG_NAME> <ACTION> <PARAMETER>
        
        with
        - LOG_NAME: DEBUG,INFO,WARNING,ERROR,FATAL_ERROR
        - ACTION: add,remove,clear
        - PARAMETER: for 'add'/'remove' it is the stream name (cout, cerr or a filename), 'clear' does not require any further parameter
        
        Example:
        `DEBUG add debug.log`
        
        This function will **not** apply to settings to the log handlers. Use configure() for that.
        
        :param setting: StringList containing the configuration options
        :raises ParseError: In case of an invalid configuration.
        :return: Param object containing all settings, that can be applied using the LogConfigHandler.configure() method
        """
        ...
    
    def configure(self, param: Param ) -> None:
        """
        Cython signature: void configure(const Param & param)
        Applies the given parameters (@p param) to the current configuration
        
        <LOG_NAME> <ACTION> <PARAMETER> <STREAMTYPE>
        
        LOG_NAME: DEBUG, INFO, WARNING, ERROR, FATAL_ERROR
        ACTION: add, remove, clear
        PARAMETER: for 'add'/'remove' it is the stream name ('cout', 'cerr' or a filename), 'clear' does not require any further parameter
        STREAMTYPE: FILE, STRING (for a StringStream, which you can grab by this name using getStream() )
        
        You cannot specify a file named "cout" or "cerr" even if you specify streamtype 'FILE' - the handler will mistake this for the
        internal streams, but you can use "./cout" to print to a file named cout.
        
        A classical configuration would contain a list of settings e.g.
        
        `DEBUG add debug.log FILE`
        `INFO remove cout FILE` (FILE will be ignored)
        `INFO add string_stream1 STRING`
        
        :raises ElementNotFound: If the LogStream (first argument) does not exist.
        :raises FileNotWritable: If a file (or stream) should be opened as log file (or stream) that is not accessible.
        :raises IllegalArgument: If a stream should be registered, that was already registered with a different type.
        """
        ...
    
    def setLogLevel(self, log_level: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLogLevel(const String & log_level)
        Sets a minimum log_level by removing all streams from loggers lower than that level.
        Valid levels are from low to high: "DEBUG", "INFO", "WARNING", "ERROR", "FATAL_ERROR"
        """
        ... 


class MRMScoring:
    """
    Cython implementation of _MRMScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1MRMScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMScoring()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMScoring ) -> None:
        """
        Cython signature: void MRMScoring(MRMScoring &)
        """
        ...
    
    def calcXcorrCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrCoelutionScore()
        Calculate the cross-correlation coelution score. The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrCoelutionWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrCoelutionWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation coelution score
        
        The score is a distance where zero indicates perfect coelution. The
        score is weighted by the transition intensities, non-perfect coelution
        in low-intensity transitions should thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastCoelutionScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastCoelutionScore()
        Calculate the separate cross-correlation contrast score
        """
        ...
    
    def calcXcorrPrecursorContrastCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastCoelutionScore()
        Calculate the precursor cross-correlation contrast score against the transitions
        
        The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrShapeScore()
        Calculate the cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation.
        """
        ...
    
    def calcXcorrShapeWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrShapeWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation. The score is weighted by the transition
        intensities, non-perfect coelution in low-intensity transitions should
        thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastShapeScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastShapeScore()
        Calculate the separate cross-correlation contrast shape score
        """
        ...
    
    def calcXcorrPrecursorContrastShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastShapeScore()
        Calculate the precursor cross-correlation shape score against the transitions
        """
        ...
    
    def calcRTScore(self, peptide: LightCompound , normalized_experimental_rt: float ) -> float:
        """
        Cython signature: double calcRTScore(LightCompound & peptide, double normalized_experimental_rt)
        """
        ...
    
    def calcMIScore(self) -> float:
        """
        Cython signature: double calcMIScore()
        """
        ...
    
    def calcMIWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcMIWeightedScore(const libcpp_vector[double] & normalized_library_intensity)
        """
        ...
    
    def calcMIPrecursorScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorScore()
        """
        ...
    
    def calcMIPrecursorContrastScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorContrastScore()
        """
        ...
    
    def calcMIPrecursorCombinedScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorCombinedScore()
        """
        ...
    
    def calcSeparateMIContrastScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateMIContrastScore()
        """
        ...
    
    def getMIMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getMIMatrix()
        """
        ... 


class MSDataStoringConsumer:
    """
    Cython implementation of _MSDataStoringConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataStoringConsumer.html>`_

    Consumer class that simply stores the data
    
    This class is able to keep spectra and chromatograms passed to it in memory
    and the data can be accessed through getData()
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSDataStoringConsumer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataStoringConsumer ) -> None:
        """
        Cython signature: void MSDataStoringConsumer(MSDataStoringConsumer &)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Sets experimental settings
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Sets expected size
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, in_0: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram &)
        """
        ...
    
    def getData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getData()
        """
        ... 


class MSPGenericFile:
    """
    Cython implementation of _MSPGenericFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSPGenericFile.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSPGenericFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSPGenericFile ) -> None:
        """
        Cython signature: void MSPGenericFile(MSPGenericFile &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void MSPGenericFile(const String & filename, MSExperiment & library)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & library)
        Load the file's data and metadata, and save it into an `MSExperiment`
        
        
        :param filename: Path to the MSP input file
        :param library: The variable into which the extracted information will be saved
        :raises:
          Exception: FileNotFound If the file could not be found
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, const MSExperiment & library)
        Save data and metadata into a file
        
        
        :param filename: Path to the MSP input file
        :param library: The variable from which extracted information will be saved
        :raises:
          Exception: FileNotWritable If the file is not writable
        """
        ...
    
    def getDefaultParameters(self, params: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param & params)
        Returns the class' default parameters
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


class MapAlignmentEvaluationAlgorithmRecall:
    """
    Cython implementation of _MapAlignmentEvaluationAlgorithmRecall

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentEvaluationAlgorithmRecall.html>`_
      -- Inherits from ['MapAlignmentEvaluationAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentEvaluationAlgorithmRecall()
        """
        ... 


class MapAlignmentTransformer:
    """
    Cython implementation of _MapAlignmentTransformer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentTransformer.html>`_

    This class collects functions for applying retention time transformations to data structures
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MapAlignmentTransformer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MapAlignmentTransformer ) -> None:
        """
        Cython signature: void MapAlignmentTransformer(MapAlignmentTransformer &)
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: MSExperiment , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(MSExperiment &, TransformationDescription &, bool)
        Applies the given transformation to a peak map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: FeatureMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(FeatureMap &, TransformationDescription &, bool)
        Applies the given transformation to a feature map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: ConsensusMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(ConsensusMap &, TransformationDescription &, bool)
        Applies the given transformation to a consensus map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: List[PeptideIdentification] , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(libcpp_vector[PeptideIdentification] &, TransformationDescription &, bool)
        Applies the given transformation to peptide identifications
        """
        ... 


class MascotXMLFile:
    """
    Cython implementation of _MascotXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotXMLFile ) -> None:
        """
        Cython signature: void MascotXMLFile(MascotXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , rt_mapping: SpectrumMetaDataLookup ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, SpectrumMetaDataLookup & rt_mapping)
        Loads data from a Mascot XML file
        
        
        :param filename: The file to be loaded
        :param protein_identification: Protein identifications belonging to the whole experiment
        :param id_data: The identifications with m/z and RT
        :param lookup: Helper object for looking up spectrum meta data
        :raises:
          Exception: FileNotFound is thrown if the file does not exists
        :raises:
          Exception: ParseError is thrown if the file does not suit to the standard
        """
        ...
    
    def initializeLookup(self, lookup: SpectrumMetaDataLookup , experiment: MSExperiment , scan_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void initializeLookup(SpectrumMetaDataLookup & lookup, MSExperiment & experiment, const String & scan_regex)
        Initializes a helper object for looking up spectrum meta data (RT, m/z)
        
        
        :param lookup: Helper object to initialize
        :param experiment: Experiment containing the spectra
        :param scan_regex: Optional regular expression for extracting information from references to spectra
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class MassExplainer:
    """
    Cython implementation of _MassExplainer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassExplainer.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassExplainer()
        Computes empirical formulas for given mass differences using a set of allowed elements
        """
        ...
    
    @overload
    def __init__(self, in_0: MassExplainer ) -> None:
        """
        Cython signature: void MassExplainer(MassExplainer &)
        """
        ...
    
    @overload
    def __init__(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void MassExplainer(libcpp_vector[Adduct] adduct_base)
        """
        ...
    
    @overload
    def __init__(self, q_min: int , q_max: int , max_span: int , thresh_logp: float ) -> None:
        """
        Cython signature: void MassExplainer(int q_min, int q_max, int max_span, double thresh_logp)
        """
        ...
    
    def setAdductBase(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void setAdductBase(libcpp_vector[Adduct] adduct_base)
        Sets the set of possible adducts
        """
        ...
    
    def getAdductBase(self) -> List[Adduct]:
        """
        Cython signature: libcpp_vector[Adduct] getAdductBase()
        Returns the set of adducts
        """
        ...
    
    def getCompomerById(self, id: int ) -> Compomer:
        """
        Cython signature: Compomer getCompomerById(size_t id)
        Returns a compomer by its Id (useful after a query() )
        """
        ...
    
    def compute(self) -> None:
        """
        Cython signature: void compute()
        Fill map with possible mass-differences along with their explanation
        """
        ... 


class Modification:
    """
    Cython implementation of _Modification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Modification.html>`_
      -- Inherits from ['SampleTreatment']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Modification()
        """
        ...
    
    @overload
    def __init__(self, in_0: Modification ) -> None:
        """
        Cython signature: void Modification(Modification &)
        """
        ...
    
    def getReagentName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getReagentName()
        Returns the name of the reagent that was used (default "")
        """
        ...
    
    def setReagentName(self, reagent_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setReagentName(const String & reagent_name)
        Sets the name of the reagent that was used
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Returns the mass change (default 0.0)
        """
        ...
    
    def setMass(self, mass: float ) -> None:
        """
        Cython signature: void setMass(double mass)
        Sets the mass change
        """
        ...
    
    def getSpecificityType(self) -> int:
        """
        Cython signature: Modification_SpecificityType getSpecificityType()
        Returns the specificity of the reagent (default AA)
        """
        ...
    
    def setSpecificityType(self, specificity_type: int ) -> None:
        """
        Cython signature: void setSpecificityType(Modification_SpecificityType & specificity_type)
        Sets the specificity of the reagent
        """
        ...
    
    def getAffectedAminoAcids(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAffectedAminoAcids()
        Returns a string containing the one letter code of the amino acids that are affected by the reagent (default "")
        """
        ...
    
    def setAffectedAminoAcids(self, affected_amino_acids: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAffectedAminoAcids(const String & affected_amino_acids)
        Returns a string containing the one letter code of the amino acids that are affected by the reagent. Do not separate them by space, tab or comma!
        """
        ...
    
    def getType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getType()
        Returns the treatment type
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the description of the sample treatment
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(const String & comment)
        Sets the description of the sample treatment
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
    
    def __richcmp__(self, other: Modification, op: int) -> Any:
        ...
    Modification_SpecificityType : __Modification_SpecificityType 


class MzMLSqliteHandler:
    """
    Cython implementation of _MzMLSqliteHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1MzMLSqliteHandler.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(String filename, uint64_t run_id)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(MzMLSqliteHandler &)
        """
        ...
    
    def readExperiment(self, exp: MSExperiment , meta_only: bool ) -> None:
        """
        Cython signature: void readExperiment(MSExperiment & exp, bool meta_only)
        Read an experiment into an MSExperiment structure
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def readSpectra(self, exp: List[MSSpectrum] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readSpectra(libcpp_vector[MSSpectrum] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of spectra (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def readChromatograms(self, exp: List[MSChromatogram] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readChromatograms(libcpp_vector[MSChromatogram] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of chromatograms (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns number of spectra in the file, reutrns the number of spectra
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms in the file
        """
        ...
    
    def setConfig(self, write_full_meta: bool , use_lossy_compression: bool , linear_abs_mass_acc: float ) -> None:
        """
        Cython signature: void setConfig(bool write_full_meta, bool use_lossy_compression, double linear_abs_mass_acc)
        Sets file configuration
        
        
        :param write_full_meta: Whether to write a complete mzML meta data structure into the RUN_EXTRA field (allows complete recovery of the input file)
        :param use_lossy_compression: Whether to use lossy compression (ms numpress)
        :param linear_abs_mass_acc: Accepted loss in mass accuracy (absolute m/z, in Th)
        """
        ...
    
    def getSpectraIndicesbyRT(self, RT: float , deltaRT: float , indices: List[int] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraIndicesbyRT(double RT, double deltaRT, libcpp_vector[int] indices)
        Returns spectral indices around a specific retention time
        
        :param RT: The retention time
        :param deltaRT: Tolerance window around RT (if less or equal than zero, only the first spectrum *after* RT is returned)
        :param indices: Spectra to consider (if empty, all spectra are considered)
        :return: The indices of the spectra within RT +/- deltaRT
        """
        ...
    
    def writeExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void writeExperiment(MSExperiment exp)
        Write an MSExperiment to disk
        """
        ...
    
    def createTables(self) -> None:
        """
        Cython signature: void createTables()
        Create data tables for a new file
        """
        ...
    
    def writeSpectra(self, spectra: List[MSSpectrum] ) -> None:
        """
        Cython signature: void writeSpectra(libcpp_vector[MSSpectrum] spectra)
        Writes a set of spectra to disk
        """
        ...
    
    def writeChromatograms(self, chroms: List[MSChromatogram] ) -> None:
        """
        Cython signature: void writeChromatograms(libcpp_vector[MSChromatogram] chroms)
        Writes a set of chromatograms to disk
        """
        ...
    
    def writeRunLevelInformation(self, exp: MSExperiment , write_full_meta: bool ) -> None:
        """
        Cython signature: void writeRunLevelInformation(MSExperiment exp, bool write_full_meta)
        Write the run-level information for an experiment into tables
        
        This is a low level function, do not call this function unless you know what you are doing
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def getRunID(self) -> int:
        """
        Cython signature: uint64_t getRunID()
        Extract the `RUN` ID from the sqMass file
        """
        ... 


class MzTabMFile:
    """
    Cython implementation of _MzTabMFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabMFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabMFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabMFile ) -> None:
        """
        Cython signature: void MzTabMFile(MzTabMFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , mztab_m: MzTabM ) -> None:
        """
        Cython signature: void store(String filename, MzTabM & mztab_m)
        Store MzTabM file
        """
        ... 


class NASequence:
    """
    Cython implementation of _NASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NASequence.html>`_

    Representation of an RNA sequence
    This class represents nucleic acid sequences in OpenMS. An NASequence
    instance primarily contains a sequence of ribonucleotides.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: NASequence ) -> None:
        """
        Cython signature: void NASequence(NASequence &)
        """
        ...
    
    def getSequence(self) -> List[Ribonucleotide]:
        """
        Cython signature: libcpp_vector[const Ribonucleotide *] getSequence()
        """
        ...
    
    def __getitem__(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * operator[](size_t index)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def setSequence(self, seq: List[Ribonucleotide] ) -> None:
        """
        Cython signature: void setSequence(const libcpp_vector[const Ribonucleotide *] & seq)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def setFivePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setFivePrimeMod(const Ribonucleotide * modification)
        Sets the 5' modification
        """
        ...
    
    def getFivePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getFivePrimeMod()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def setThreePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setThreePrimeMod(const Ribonucleotide * modification)
        Sets the 3' modification
        """
        ...
    
    def getThreePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getThreePrimeMod()
        """
        ...
    
    def get(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * get(size_t index)
        Returns the residue at position index
        """
        ...
    
    def set(self, index: int , r: Ribonucleotide ) -> None:
        """
        Cython signature: void set(size_t index, const Ribonucleotide * r)
        Sets the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the formula of the peptide
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getAverageWeight(self, ) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the peptide
        """
        ...
    
    @overload
    def getAverageWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getAverageWeight(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getMonoWeight(self, ) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the peptide
        """
        ...
    
    @overload
    def getMonoWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getMonoWeight(NASFragmentType type_, int charge)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getPrefix(size_t length)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getSuffix(size_t length)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, start: int , length: int ) -> NASequence:
        """
        Cython signature: NASequence getSubsequence(size_t start, size_t length)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def __richcmp__(self, other: NASequence, op: int) -> Any:
        ...
    NASFragmentType : __NASFragmentType
    
    fromString: __static_NASequence_fromString 


class NLargest:
    """
    Cython implementation of _NLargest

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NLargest.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NLargest()
        """
        ...
    
    @overload
    def __init__(self, in_0: NLargest ) -> None:
        """
        Cython signature: void NLargest(NLargest &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        Keep only n-largest peaks in each spectrum of a peak map
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


class NoopMSDataWritingConsumer:
    """
    Cython implementation of _NoopMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NoopMSDataWritingConsumer.html>`_

    Consumer class that perform no operation
    
    This is sometimes necessary to fulfill the requirement of passing an
    valid MSDataWritingConsumer object or pointer but no operation is
    required
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void NoopMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ...
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        """
        ... 


class Normalizer:
    """
    Cython implementation of _Normalizer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Normalizer.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Normalizer()
        """
        ...
    
    @overload
    def __init__(self, in_0: Normalizer ) -> None:
        """
        Cython signature: void Normalizer(Normalizer)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        Normalizes the spectrum
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        Normalizes the peak spectrum
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        Normalizes the peak map
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


class OMSSACSVFile:
    """
    Cython implementation of _OMSSACSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSACSVFile.html>`_

    File adapter for OMSSACSV files
    
    The files contain the results of the OMSSA algorithm in a comma separated manner. This file adapter is able to
    load the data from such a file into the structures of OpenMS
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OMSSACSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: OMSSACSVFile ) -> None:
        """
        Cython signature: void OMSSACSVFile(OMSSACSVFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data)
        Loads a OMSSA file
        
        The content of the file is stored in `features`
        
        
        :param filename: The name of the file to read from
        :param protein_identification: The protein ProteinIdentification data
        :param id_data: The peptide ids of the file
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class OpenSwathOSWWriter:
    """
    Cython implementation of _OpenSwathOSWWriter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathOSWWriter.html>`_
    """
    
    @overload
    def __init__(self, output_filename: Union[bytes, str, String] , run_id: int , input_filename: Union[bytes, str, String] , uis_scores: bool ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(String output_filename, uint64_t run_id, String input_filename, bool uis_scores)
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathOSWWriter ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(OpenSwathOSWWriter &)
        """
        ...
    
    def isActive(self) -> bool:
        """
        Cython signature: bool isActive()
        """
        ...
    
    def writeHeader(self) -> None:
        """
        Cython signature: void writeHeader()
        Initializes file by generating SQLite tables
        """
        ...
    
    def prepareLine(self, compound: LightCompound , tr: LightTransition , output: FeatureMap , id_: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String prepareLine(LightCompound & compound, LightTransition * tr, FeatureMap & output, String id_)
        Prepare a single line (feature) for output
        
        The result can be flushed to disk using writeLines (either line by line or after collecting several lines)
        
        
        :param pep: The compound (peptide/metabolite) used for extraction
        :param transition: The transition used for extraction
        :param output: The feature map containing all features (each feature will generate one entry in the output)
        :param id: The transition group identifier (peptide/metabolite id)
        :return: A String to be written using writeLines
        """
        ...
    
    def writeLines(self, to_osw_output: List[bytes] ) -> None:
        """
        Cython signature: void writeLines(libcpp_vector[String] to_osw_output)
        Write data to disk
        
        Takes a set of pre-prepared data statements from prepareLine and flushes them to disk
        
        
        :param to_osw_output: Statements generated by prepareLine
        """
        ... 


class PI_PeakArea:
    """
    Cython implementation of _PI_PeakArea

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakArea.html>`_
    """
    
    area: float
    
    height: float
    
    apex_pos: float
    
    hull_points: '_np.ndarray[Any, _np.dtype[_np.float32]]'
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakArea()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakArea ) -> None:
        """
        Cython signature: void PI_PeakArea(PI_PeakArea &)
        """
        ... 


class PI_PeakBackground:
    """
    Cython implementation of _PI_PeakBackground

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakBackground.html>`_
    """
    
    area: float
    
    height: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakBackground()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakBackground ) -> None:
        """
        Cython signature: void PI_PeakBackground(PI_PeakBackground &)
        """
        ... 


class PI_PeakShapeMetrics:
    """
    Cython implementation of _PI_PeakShapeMetrics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakShapeMetrics.html>`_
    """
    
    width_at_5: float
    
    width_at_10: float
    
    width_at_50: float
    
    start_position_at_5: float
    
    start_position_at_10: float
    
    start_position_at_50: float
    
    end_position_at_5: float
    
    end_position_at_10: float
    
    end_position_at_50: float
    
    total_width: float
    
    tailing_factor: float
    
    asymmetry_factor: float
    
    slope_of_baseline: float
    
    baseline_delta_2_height: float
    
    points_across_baseline: int
    
    points_across_half_height: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakShapeMetrics()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakShapeMetrics ) -> None:
        """
        Cython signature: void PI_PeakShapeMetrics(PI_PeakShapeMetrics &)
        """
        ... 


class PeakFileOptions:
    """
    Cython implementation of _PeakFileOptions

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakFileOptions.html>`_

    Options for loading files containing peak data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakFileOptions()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void PeakFileOptions(PeakFileOptions &)
        """
        ...
    
    def setMetadataOnly(self, in_0: bool ) -> None:
        """
        Cython signature: void setMetadataOnly(bool)
        Sets whether or not to load only meta data
        """
        ...
    
    def getMetadataOnly(self) -> bool:
        """
        Cython signature: bool getMetadataOnly()
        Returns whether or not to load only meta data
        """
        ...
    
    def setWriteSupplementalData(self, in_0: bool ) -> None:
        """
        Cython signature: void setWriteSupplementalData(bool)
        Sets whether or not to write supplemental peak data in MzData files
        """
        ...
    
    def getWriteSupplementalData(self) -> bool:
        """
        Cython signature: bool getWriteSupplementalData()
        Returns whether or not to write supplemental peak data in MzData files
        """
        ...
    
    def setMSLevels(self, levels: List[int] ) -> None:
        """
        Cython signature: void setMSLevels(libcpp_vector[int] levels)
        Sets the desired MS levels for peaks to load
        """
        ...
    
    def addMSLevel(self, level: int ) -> None:
        """
        Cython signature: void addMSLevel(int level)
        Adds a desired MS level for peaks to load
        """
        ...
    
    def clearMSLevels(self) -> None:
        """
        Cython signature: void clearMSLevels()
        Clears the MS levels
        """
        ...
    
    def hasMSLevels(self) -> bool:
        """
        Cython signature: bool hasMSLevels()
        Returns true, if MS levels have been set
        """
        ...
    
    def containsMSLevel(self, level: int ) -> bool:
        """
        Cython signature: bool containsMSLevel(int level)
        Returns true, if MS level `level` has been set
        """
        ...
    
    def getMSLevels(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getMSLevels()
        Returns the set MS levels
        """
        ...
    
    def setCompression(self, in_0: bool ) -> None:
        """
        Cython signature: void setCompression(bool)
        Sets if data should be compressed when writing
        """
        ...
    
    def getCompression(self) -> bool:
        """
        Cython signature: bool getCompression()
        Returns true, if data should be compressed when writing
        """
        ...
    
    def setMz32Bit(self, mz_32_bit: bool ) -> None:
        """
        Cython signature: void setMz32Bit(bool mz_32_bit)
        Sets if mz-data and rt-data should be stored with 32bit or 64bit precision
        """
        ...
    
    def getMz32Bit(self) -> bool:
        """
        Cython signature: bool getMz32Bit()
        Returns true, if mz-data and rt-data should be stored with 32bit precision
        """
        ...
    
    def setIntensity32Bit(self, int_32_bit: bool ) -> None:
        """
        Cython signature: void setIntensity32Bit(bool int_32_bit)
        Sets if intensity data should be stored with 32bit or 64bit precision
        """
        ...
    
    def getIntensity32Bit(self) -> bool:
        """
        Cython signature: bool getIntensity32Bit()
        Returns true, if intensity data should be stored with 32bit precision
        """
        ...
    
    def setRTRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setRTRange(DRange1 & range_)
        Restricts the range of RT values for peaks to load
        """
        ...
    
    def hasRTRange(self) -> bool:
        """
        Cython signature: bool hasRTRange()
        Returns true if an RT range has been set
        """
        ...
    
    def getRTRange(self) -> DRange1:
        """
        Cython signature: DRange1 getRTRange()
        Returns the RT range
        """
        ...
    
    def setMZRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setMZRange(DRange1 & range_)
        Restricts the range of MZ values for peaks to load
        """
        ...
    
    def hasMZRange(self) -> bool:
        """
        Cython signature: bool hasMZRange()
        Returns true if an MZ range has been set
        """
        ...
    
    def getMZRange(self) -> DRange1:
        """
        Cython signature: DRange1 getMZRange()
        Returns the MZ range
        """
        ...
    
    def setIntensityRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setIntensityRange(DRange1 & range_)
        Restricts the range of intensity values for peaks to load
        """
        ...
    
    def hasIntensityRange(self) -> bool:
        """
        Cython signature: bool hasIntensityRange()
        Returns true if an intensity range has been set
        """
        ...
    
    def getIntensityRange(self) -> DRange1:
        """
        Cython signature: DRange1 getIntensityRange()
        Returns the intensity range
        """
        ...
    
    def getMaxDataPoolSize(self) -> int:
        """
        Cython signature: size_t getMaxDataPoolSize()
        Returns maximal size of the data pool
        """
        ...
    
    def setMaxDataPoolSize(self, s: int ) -> None:
        """
        Cython signature: void setMaxDataPoolSize(size_t s)
        Sets maximal size of the data pool
        """
        ...
    
    def setSortSpectraByMZ(self, doSort: bool ) -> None:
        """
        Cython signature: void setSortSpectraByMZ(bool doSort)
        Sets whether or not to sort peaks in spectra
        """
        ...
    
    def getSortSpectraByMZ(self) -> bool:
        """
        Cython signature: bool getSortSpectraByMZ()
        Returns whether or not peaks in spectra should be sorted
        """
        ...
    
    def setSortChromatogramsByRT(self, doSort: bool ) -> None:
        """
        Cython signature: void setSortChromatogramsByRT(bool doSort)
        Sets whether or not to sort peaks in chromatograms
        """
        ...
    
    def getSortChromatogramsByRT(self) -> bool:
        """
        Cython signature: bool getSortChromatogramsByRT()
        Returns whether or not peaks in chromatograms should be sorted
        """
        ...
    
    def hasFilters(self) -> bool:
        """
        Cython signature: bool hasFilters()
        """
        ...
    
    def setFillData(self, only: bool ) -> None:
        """
        Cython signature: void setFillData(bool only)
        Sets whether to fill the actual data into the container (spectrum/chromatogram)
        """
        ...
    
    def getFillData(self) -> bool:
        """
        Cython signature: bool getFillData()
        Returns whether to fill the actual data into the container (spectrum/chromatogram)
        """
        ...
    
    def setSkipXMLChecks(self, only: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool only)
        Sets whether to skip some XML checks and be fast instead
        """
        ...
    
    def getSkipXMLChecks(self) -> bool:
        """
        Cython signature: bool getSkipXMLChecks()
        Returns whether to skip some XML checks and be fast instead
        """
        ...
    
    def getWriteIndex(self) -> bool:
        """
        Cython signature: bool getWriteIndex()
        Returns whether to write an index at the end of the file (e.g. indexedmzML file format)
        """
        ...
    
    def setWriteIndex(self, write_index: bool ) -> None:
        """
        Cython signature: void setWriteIndex(bool write_index)
        Returns whether to write an index at the end of the file (e.g. indexedmzML file format)
        """
        ...
    
    def getNumpressConfigurationMassTime(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationMassTime()
        Sets numpress configuration options for m/z or rt dimension
        """
        ...
    
    def setNumpressConfigurationMassTime(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationMassTime(NumpressConfig config)
        Returns numpress configuration options for m/z or rt dimension
        """
        ...
    
    def getNumpressConfigurationIntensity(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationIntensity()
        Sets numpress configuration options for intensity dimension
        """
        ...
    
    def setNumpressConfigurationIntensity(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationIntensity(NumpressConfig config)
        Returns numpress configuration options for intensity dimension
        """
        ...
    
    def getNumpressConfigurationFloatDataArray(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationFloatDataArray()
        Sets numpress configuration options for float data arrays
        """
        ...
    
    def setNumpressConfigurationFloatDataArray(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationFloatDataArray(NumpressConfig config)
        Returns numpress configuration options for float data arrays
        """
        ...
    
    def setForceMQCompatability(self, forceMQ: bool ) -> None:
        """
        Cython signature: void setForceMQCompatability(bool forceMQ)
        [mzXML only!]Returns Whether to write a scan-index and meta data to indicate a Thermo FTMS/ITMS instrument (required to have parameter control in MQ)
        """
        ...
    
    def getForceMQCompatability(self) -> bool:
        """
        Cython signature: bool getForceMQCompatability()
        [mzXML only!]Returns Whether to write a scan-index and meta data to indicate a Thermo FTMS/ITMS instrument (required to have parameter control in MQ)
        """
        ...
    
    def setForceTPPCompatability(self, forceTPP: bool ) -> None:
        """
        Cython signature: void setForceTPPCompatability(bool forceTPP)
        [ mzML only!]Returns Whether to skip writing the \<isolationWindow\> tag so that TPP finds the correct precursor m/z
        """
        ...
    
    def getForceTPPCompatability(self) -> bool:
        """
        Cython signature: bool getForceTPPCompatability()
        [mzML only!]Returns Whether to skip writing the \<isolationWindow\> tag so that TPP finds the correct precursor m/z
        """
        ... 


class PeakIntegrator:
    """
    Cython implementation of _PeakIntegrator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakIntegrator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakIntegrator()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakIntegrator ) -> None:
        """
        Cython signature: void PeakIntegrator(PeakIntegrator &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param)
        """
        ...
    
    @overload
    def integratePeak(self, chromatogram: MSChromatogram , left: float , right: float ) -> PI_PeakArea:
        """
        Cython signature: PI_PeakArea integratePeak(MSChromatogram & chromatogram, double left, double right)
        """
        ...
    
    @overload
    def integratePeak(self, spectrum: MSSpectrum , left: float , right: float ) -> PI_PeakArea:
        """
        Cython signature: PI_PeakArea integratePeak(MSSpectrum & spectrum, double left, double right)
        """
        ...
    
    @overload
    def estimateBackground(self, chromatogram: MSChromatogram , left: float , right: float , peak_apex_pos: float ) -> PI_PeakBackground:
        """
        Cython signature: PI_PeakBackground estimateBackground(MSChromatogram & chromatogram, double left, double right, double peak_apex_pos)
        """
        ...
    
    @overload
    def estimateBackground(self, spectrum: MSSpectrum , left: float , right: float , peak_apex_pos: float ) -> PI_PeakBackground:
        """
        Cython signature: PI_PeakBackground estimateBackground(MSSpectrum & spectrum, double left, double right, double peak_apex_pos)
        """
        ...
    
    @overload
    def calculatePeakShapeMetrics(self, chromatogram: MSChromatogram , left: float , right: float , peak_height: float , peak_apex_pos: float ) -> PI_PeakShapeMetrics:
        """
        Cython signature: PI_PeakShapeMetrics calculatePeakShapeMetrics(MSChromatogram & chromatogram, double left, double right, double peak_height, double peak_apex_pos)
        """
        ...
    
    @overload
    def calculatePeakShapeMetrics(self, spectrum: MSSpectrum , left: float , right: float , peak_height: float , peak_apex_pos: float ) -> PI_PeakShapeMetrics:
        """
        Cython signature: PI_PeakShapeMetrics calculatePeakShapeMetrics(MSSpectrum & spectrum, double left, double right, double peak_height, double peak_apex_pos)
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


class PepXMLFile:
    """
    Cython implementation of _PepXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PepXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void PepXMLFile()
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , experiment_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String experiment_name)
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , experiment_name: Union[bytes, str, String] , lookup: SpectrumMetaDataLookup ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String experiment_name, SpectrumMetaDataLookup lookup)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , mz_file: Union[bytes, str, String] , mz_name: Union[bytes, str, String] , peptideprophet_analyzed: bool , rt_tolerance: float ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String mz_file, String mz_name, bool peptideprophet_analyzed, double rt_tolerance)
        """
        ...
    
    def keepNativeSpectrumName(self, keep: bool ) -> None:
        """
        Cython signature: void keepNativeSpectrumName(bool keep)
        """
        ...
    
    def setParseUnknownScores(self, parse_unknown_scores: bool ) -> None:
        """
        Cython signature: void setParseUnknownScores(bool parse_unknown_scores)
        """
        ... 


class PeptideIdentification:
    """
    Cython implementation of _PeptideIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideIdentification ) -> None:
        """
        Cython signature: void PeptideIdentification(PeptideIdentification &)
        """
        ...
    
    def getHits(self) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getHits()
        Returns the peptide hits as const
        """
        ...
    
    def insertHit(self, in_0: PeptideHit ) -> None:
        """
        Cython signature: void insertHit(PeptideHit)
        Appends a peptide hit
        """
        ...
    
    def setHits(self, in_0: List[PeptideHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[PeptideHit])
        Sets the peptide hits
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the peptide significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Setting of the peptide significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        """
        ...
    
    def setScoreType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String)
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        """
        ...
    
    def setHigherScoreBetter(self, in_0: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String)
        """
        ...
    
    def hasMZ(self) -> bool:
        """
        Cython signature: bool hasMZ()
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
    
    def hasRT(self) -> bool:
        """
        Cython signature: bool hasRT()
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        """
        ...
    
    def getBaseName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseName()
        """
        ...
    
    def setBaseName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBaseName(String)
        """
        ...
    
    def getExperimentLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentLabel()
        """
        ...
    
    def setExperimentLabel(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentLabel(String)
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        """
        ...
    
    def sortByRank(self) -> None:
        """
        Cython signature: void sortByRank()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def getReferencingHits(self, in_0: List[PeptideHit] , in_1: Set[bytes] ) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getReferencingHits(libcpp_vector[PeptideHit], libcpp_set[String] &)
        Returns all peptide hits which reference to a given protein accession (i.e. filter by protein accession)
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
    
    def __richcmp__(self, other: PeptideIdentification, op: int) -> Any:
        ... 


class PlainMSDataWritingConsumer:
    """
    Cython implementation of _PlainMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PlainMSDataWritingConsumer.html>`_
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void PlainMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Set experimental settings for the whole file
        
        
        :param exp: Experimental settings to be used for this file (from this and the first spectrum/chromatogram, the class will deduce most of the header of the mzML file)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Set expected size of spectra and chromatograms to be written
        
        These numbers will be written in the spectrumList and chromatogramList
        tag in the mzML file. Therefore, these will contain wrong numbers if
        the expected size is not set correctly
        
        
        :param expectedSpectra: Number of spectra expected
        :param expectedChromatograms: Number of chromatograms expected
        """
        ...
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        Optionally add a data processing method to each chromatogram and spectrum
        
        The provided DataProcessing object will be added to each chromatogram
        and spectrum written to to the mzML file
        
        
        :param d: The DataProcessing object to be added
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        Returns the number of spectra written
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        Returns the number of chromatograms written
        """
        ...
    
    def setOptions(self, opt: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions opt)
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ... 


class PrecursorPurity:
    """
    Cython implementation of _PrecursorPurity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PrecursorPurity.html>`_

    Precursor purity or noise estimation
    
    This class computes metrics for precursor isolation window purity (or noise)
    The function extracts the peaks from an isolation window targeted for fragmentation
    and determines which peaks are isotopes of the target and which come from other sources
    The intensities of the assumed target peaks are summed up as the target intensity
    Using this information it calculates an intensity ratio for the relative intensity of the target
    compared to other sources
    These metrics are combined over the previous and the next MS1 spectrum
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PrecursorPurity()
        """
        ...
    
    @overload
    def __init__(self, in_0: PrecursorPurity ) -> None:
        """
        Cython signature: void PrecursorPurity(PrecursorPurity &)
        """
        ...
    
    def computePrecursorPurity(self, ms1: MSSpectrum , pre: Precursor , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool ) -> PurityScores:
        """
        Cython signature: PurityScores computePrecursorPurity(MSSpectrum ms1, Precursor pre, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm)
        Compute precursor purity metrics for one MS2 precursor
        
        Note: This function is implemented in a general way and can also be used for e.g. MS3 precursor isolation windows in MS2 spectra
        Spectra annotated with charge 0 will be treated as charge 1.
        
        
        :param ms1: The Spectrum containing the isolation window
        :param pre: The precursor containing the definition the isolation window
        :param precursor_mass_tolerance: The precursor tolerance. Is used for determining the targeted peak and deisotoping
        :param precursor_mass_tolerance_unit_ppm: The unit of the precursor tolerance
        """
        ... 


class PurityScores:
    """
    Cython implementation of _PurityScores

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PurityScores.html>`_
    """
    
    total_intensity: float
    
    target_intensity: float
    
    signal_proportion: float
    
    target_peak_count: int
    
    interfering_peak_count: int
    
    interfering_peaks: MSSpectrum
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PurityScores()
        """
        ...
    
    @overload
    def __init__(self, in_0: PurityScores ) -> None:
        """
        Cython signature: void PurityScores(PurityScores &)
        """
        ... 


class QTCluster:
    """
    Cython implementation of _QTCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTCluster.html>`_
    """
    
    def __init__(self, in_0: QTCluster ) -> None:
        """
        Cython signature: void QTCluster(QTCluster &)
        """
        ...
    
    def getCenterRT(self) -> float:
        """
        Cython signature: double getCenterRT()
        Returns the RT value of the cluster
        """
        ...
    
    def getCenterMZ(self) -> float:
        """
        Cython signature: double getCenterMZ()
        Returns the m/z value of the cluster center
        """
        ...
    
    def getXCoord(self) -> int:
        """
        Cython signature: int getXCoord()
        Returns the x coordinate in the grid
        """
        ...
    
    def getYCoord(self) -> int:
        """
        Cython signature: int getYCoord()
        Returns the y coordinate in the grid
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the size of the cluster (number of elements, incl. center)
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: double getQuality()
        Returns the cluster quality and recomputes if necessary
        """
        ...
    
    def getAnnotations(self) -> Set[AASequence]:
        """
        Cython signature: libcpp_set[AASequence] getAnnotations()
        Returns the set of peptide sequences annotated to the cluster center
        """
        ...
    
    def setInvalid(self) -> None:
        """
        Cython signature: void setInvalid()
        Sets current cluster as invalid (also frees some memory)
        """
        ...
    
    def isInvalid(self) -> bool:
        """
        Cython signature: bool isInvalid()
        Whether current cluster is invalid
        """
        ...
    
    def initializeCluster(self) -> None:
        """
        Cython signature: void initializeCluster()
        Has to be called before adding elements (calling
        """
        ...
    
    def finalizeCluster(self) -> None:
        """
        Cython signature: void finalizeCluster()
        Has to be called after adding elements (after calling
        """
        ...
    
    def __richcmp__(self, other: QTCluster, op: int) -> Any:
        ... 


class ReactionMonitoringTransition:
    """
    Cython implementation of _ReactionMonitoringTransition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ReactionMonitoringTransition.html>`_
      -- Inherits from ['CVTermList']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ReactionMonitoringTransition()
        """
        ...
    
    @overload
    def __init__(self, in_0: ReactionMonitoringTransition ) -> None:
        """
        Cython signature: void ReactionMonitoringTransition(ReactionMonitoringTransition &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getNativeID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeID()
        """
        ...
    
    def getPeptideRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPeptideRef()
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        """
        ...
    
    def setNativeID(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeID(String name)
        """
        ...
    
    def setPeptideRef(self, peptide_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPeptideRef(String peptide_ref)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def setProductMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setProductMZ(double)
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        Returns the precursor mz (Q1 value)
        """
        ...
    
    def setPrecursorMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setPrecursorMZ(double)
        Sets the precursor mz (Q1 value)
        """
        ...
    
    def getDecoyTransitionType(self) -> int:
        """
        Cython signature: DecoyTransitionType getDecoyTransitionType()
        Returns the type of transition (target or decoy)
        """
        ...
    
    def setCompoundRef(self, compound_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCompoundRef(const String & compound_ref)
        """
        ...
    
    def getCompoundRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCompoundRef()
        """
        ...
    
    def hasPrecursorCVTerms(self) -> bool:
        """
        Cython signature: bool hasPrecursorCVTerms()
        Returns true if precursor CV Terms exist (means it is safe to call getPrecursorCVTermList)
        """
        ...
    
    def setPrecursorCVTermList(self, list_: CVTermList ) -> None:
        """
        Cython signature: void setPrecursorCVTermList(CVTermList & list_)
        Sets a list of precursor CV Terms
        """
        ...
    
    def addPrecursorCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addPrecursorCVTerm(CVTerm & cv_term)
        Adds precursor CV Term
        """
        ...
    
    def getPrecursorCVTermList(self) -> CVTermList:
        """
        Cython signature: CVTermList getPrecursorCVTermList()
        Obtains the list of CV Terms for the precursor
        """
        ...
    
    def addProductCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addProductCVTerm(CVTerm & cv_term)
        """
        ...
    
    def getIntermediateProducts(self) -> List[TraMLProduct]:
        """
        Cython signature: libcpp_vector[TraMLProduct] getIntermediateProducts()
        """
        ...
    
    def addIntermediateProduct(self, product: TraMLProduct ) -> None:
        """
        Cython signature: void addIntermediateProduct(TraMLProduct product)
        """
        ...
    
    def setIntermediateProducts(self, products: List[TraMLProduct] ) -> None:
        """
        Cython signature: void setIntermediateProducts(libcpp_vector[TraMLProduct] & products)
        """
        ...
    
    def setProduct(self, product: TraMLProduct ) -> None:
        """
        Cython signature: void setProduct(TraMLProduct product)
        """
        ...
    
    def getProduct(self) -> TraMLProduct:
        """
        Cython signature: TraMLProduct getProduct()
        """
        ...
    
    def setRetentionTime(self, rt: RetentionTime ) -> None:
        """
        Cython signature: void setRetentionTime(RetentionTime rt)
        """
        ...
    
    def getRetentionTime(self) -> RetentionTime:
        """
        Cython signature: RetentionTime getRetentionTime()
        """
        ...
    
    def setPrediction(self, prediction: Prediction ) -> None:
        """
        Cython signature: void setPrediction(Prediction & prediction)
        Sets prediction
        """
        ...
    
    def addPredictionTerm(self, prediction: CVTerm ) -> None:
        """
        Cython signature: void addPredictionTerm(CVTerm & prediction)
        Adds prediction term
        """
        ...
    
    def hasPrediction(self) -> bool:
        """
        Cython signature: bool hasPrediction()
        Returns true if a Prediction object exists (means it is safe to call getPrediction)
        """
        ...
    
    def getPrediction(self) -> Prediction:
        """
        Cython signature: Prediction getPrediction()
        Obtains the Prediction object
        """
        ...
    
    def setDecoyTransitionType(self, d: int ) -> None:
        """
        Cython signature: void setDecoyTransitionType(DecoyTransitionType & d)
        Sets the type of transition (target or decoy)
        """
        ...
    
    def getLibraryIntensity(self) -> float:
        """
        Cython signature: double getLibraryIntensity()
        Returns the library intensity (ion count or normalized ion count from a spectral library)
        """
        ...
    
    def setLibraryIntensity(self, intensity: float ) -> None:
        """
        Cython signature: void setLibraryIntensity(double intensity)
        Sets the library intensity (ion count or normalized ion count from a spectral library)
        """
        ...
    
    def getProductChargeState(self) -> int:
        """
        Cython signature: int getProductChargeState()
        Returns the charge state of the product
        """
        ...
    
    def isProductChargeStateSet(self) -> bool:
        """
        Cython signature: bool isProductChargeStateSet()
        Returns true if charge state of product is already set
        """
        ...
    
    def isDetectingTransition(self) -> bool:
        """
        Cython signature: bool isDetectingTransition()
        """
        ...
    
    def setDetectingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setDetectingTransition(bool val)
        """
        ...
    
    def isIdentifyingTransition(self) -> bool:
        """
        Cython signature: bool isIdentifyingTransition()
        """
        ...
    
    def setIdentifyingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setIdentifyingTransition(bool val)
        """
        ...
    
    def isQuantifyingTransition(self) -> bool:
        """
        Cython signature: bool isQuantifyingTransition()
        """
        ...
    
    def setQuantifyingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setQuantifyingTransition(bool val)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        Sets the CV terms
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        Replaces the specified CV term
        """
        ...
    
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        Returns the accession string of the term
        """
        ...
    
    def addCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVTerm & term)
        Adds a CV term
        """
        ...
    
    def hasCVTerm(self, accession: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVTerm(String accession)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
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
    
    def __richcmp__(self, other: ReactionMonitoringTransition, op: int) -> Any:
        ... 


class RichPeak2D:
    """
    Cython implementation of _RichPeak2D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RichPeak2D.html>`_
      -- Inherits from ['Peak2D', 'UniqueIdInterface', 'MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RichPeak2D()
        A 2-dimensional raw data point or peak with meta information
        """
        ...
    
    @overload
    def __init__(self, in_0: RichPeak2D ) -> None:
        """
        Cython signature: void RichPeak2D(RichPeak2D &)
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
    
    def __richcmp__(self, other: RichPeak2D, op: int) -> Any:
        ... 


class SimplePeak:
    """
    Cython implementation of _SimplePeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimplePeak.html>`_
    """
    
    mz: float
    
    charge: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimplePeak()
        A simple struct to represent peaks with mz and charge and sort them easily
        """
        ...
    
    @overload
    def __init__(self, mz: float , charge: int ) -> None:
        """
        Cython signature: void SimplePeak(double mz, int charge)
        """
        ...
    
    @overload
    def __init__(self, in_0: SimplePeak ) -> None:
        """
        Cython signature: void SimplePeak(SimplePeak &)
        """
        ... 


class SimpleTSGXLMS:
    """
    Cython implementation of _SimpleTSGXLMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleTSGXLMS.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleTSGXLMS()
        Generates theoretical spectra for cross-linked peptides
        
        The spectra this class generates are vectors of SimplePeaks
        This class generates the same peak types as TheoreticalSpectrumGeneratorXLMS
        and the interface is very similar, but it is simpler and faster
        SimplePeak only contains an mz value and a charge. No intensity values
        or String annotations or other additional DataArrays are generated
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleTSGXLMS ) -> None:
        """
        Cython signature: void SimpleTSGXLMS(SimpleTSGXLMS &)
        """
        ...
    
    def getLinearIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , charge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getLinearIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, int charge, size_t link_pos_2)
        Generates fragment ions not containing the cross-linker for one peptide
        
        B-ions are generated from the beginning of the peptide up to the first linked position,
        y-ions are generated from the second linked position up the end of the peptide
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param charge: The maximal charge of the ions
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , precursor_mass: float , mincharge: int , maxcharge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, double precursor_mass, int mincharge, int maxcharge, size_t link_pos_2)
        Generates fragment ions containing the cross-linker for one peptide
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        Since in the case of a cross-link a whole second peptide is attached to the other side of the cross-link,
        a precursor mass for the two peptides and the linker is needed
        In the case of a loop link the precursor mass is the mass of the only peptide and the linker
        Although this function is more general, currently it is mainly used for loop-links and mono-links,
        because residues in the second, unknown peptide cannot be considered for possible neutral losses
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
        :param mincharge: The minimal charge of the ions
        :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , crosslink: ProteinProteinCrossLink , frag_alpha: bool , mincharge: int , maxcharge: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, ProteinProteinCrossLink crosslink, bool frag_alpha, int mincharge, int maxcharge)
        Generates fragment ions containing the cross-linker for a pair of peptides
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        This function generates neutral loss ions by considering both linked peptides
        Only one of the peptides, decided by @frag_alpha, is fragmented
        This simplifies the function, but it has to be called twice to get all fragments of a peptide pair
        The generated ion types and other additional settings are determined by the tool parameters
        This function is not suitable to generate fragments for mono-links or loop-links
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param crosslink: ProteinProteinCrossLink to be fragmented
        :param link_pos: The position of the cross-linker on the given peptide
        :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
        :param frag_alpha: True, if the fragmented peptide is the Alpha peptide
        :param mincharge: The minimal charge of the ions
        :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
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


class SpectrumAccessOpenMS:
    """
    Cython implementation of _SpectrumAccessOpenMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMS.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS(SpectrumAccessOpenMS &)
        """
        ...
    
    @overload
    def __init__(self, ms_experiment: MSExperiment ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS(shared_ptr[MSExperiment] & ms_experiment)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class SpectrumAccessOpenMSInMemory:
    """
    Cython implementation of _SpectrumAccessOpenMSInMemory

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMSInMemory.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMS &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMSCached &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSInMemory ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMSInMemory &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessQuadMZTransforming ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessQuadMZTransforming &)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class String:
    """
    Cython implementation of _String

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1String.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void String()
        """
        ...
    
    def __richcmp__(self, other: String, op: int) -> Any:
        ... 


class StringView:
    """
    Cython implementation of _StringView

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StringView.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void StringView()
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void StringView(const libcpp_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: StringView ) -> None:
        """
        Cython signature: void StringView(StringView &)
        """
        ...
    
    def substr(self, start: int , end: int ) -> StringView:
        """
        Cython signature: StringView substr(size_t start, size_t end)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def getString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getString()
        """
        ...
    
    def __richcmp__(self, other: StringView, op: int) -> Any:
        ... 


class TSE_Match:
    """
    Cython implementation of _TSE_Match

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TSE_Match.html>`_
    """
    
    spectrum: MSSpectrum
    
    score: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TSE_Match()
        """
        ...
    
    @overload
    def __init__(self, in_0: TSE_Match ) -> None:
        """
        Cython signature: void TSE_Match(TSE_Match &)
        """
        ...
    
    @overload
    def __init__(self, spectrum: MSSpectrum , score: float ) -> None:
        """
        Cython signature: void TSE_Match(MSSpectrum & spectrum, double score)
        """
        ... 


class TargetedSpectraExtractor:
    """
    Cython implementation of _TargetedSpectraExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TargetedSpectraExtractor.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TargetedSpectraExtractor()
        """
        ...
    
    @overload
    def __init__(self, in_0: TargetedSpectraExtractor ) -> None:
        """
        Cython signature: void TargetedSpectraExtractor(TargetedSpectraExtractor &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: TargetedExperiment , in_2: List[MSSpectrum] , in_3: FeatureMap ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, TargetedExperiment &, libcpp_vector[MSSpectrum] &, FeatureMap &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: TargetedExperiment , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, TargetedExperiment &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: FeatureMap , in_2: FeatureMap , in_3: List[MSSpectrum] ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, FeatureMap &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    def searchSpectrum(self, in_0: FeatureMap , in_1: FeatureMap , in_2: bool ) -> None:
        """
        Cython signature: void searchSpectrum(FeatureMap &, FeatureMap &, bool)
        """
        ...
    
    def pickSpectrum(self, in_0: MSSpectrum , in_1: MSSpectrum ) -> None:
        """
        Cython signature: void pickSpectrum(MSSpectrum &, MSSpectrum &)
        """
        ...
    
    @overload
    def scoreSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] , in_2: FeatureMap , in_3: List[MSSpectrum] ) -> None:
        """
        Cython signature: void scoreSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def scoreSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void scoreSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def selectSpectra(self, in_0: List[MSSpectrum] , in_1: FeatureMap , in_2: List[MSSpectrum] , in_3: FeatureMap ) -> None:
        """
        Cython signature: void selectSpectra(libcpp_vector[MSSpectrum] &, FeatureMap &, libcpp_vector[MSSpectrum] &, FeatureMap &)
        """
        ...
    
    @overload
    def selectSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] ) -> None:
        """
        Cython signature: void selectSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: TargetedExperiment , in_2: List[MSSpectrum] , in_3: FeatureMap , in_4: bool ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, TargetedExperiment &, libcpp_vector[MSSpectrum] &, FeatureMap &, bool)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: TargetedExperiment , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, TargetedExperiment &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: FeatureMap , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    def constructTransitionsList(self, in_0: FeatureMap , in_1: FeatureMap , in_2: TargetedExperiment ) -> None:
        """
        Cython signature: void constructTransitionsList(FeatureMap &, FeatureMap &, TargetedExperiment &)
        """
        ...
    
    def storeSpectraMSP(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void storeSpectraMSP(const String &, MSExperiment &)
        """
        ...
    
    def mergeFeatures(self, in_0: FeatureMap , in_1: FeatureMap ) -> None:
        """
        Cython signature: void mergeFeatures(FeatureMap &, FeatureMap &)
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


class TraMLFile:
    """
    Cython implementation of _TraMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TraMLFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TraMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TraMLFile ) -> None:
        """
        Cython signature: void TraMLFile(TraMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void load(String filename, TargetedExperiment & id)
        Loads a map from a TraML file
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void store(String filename, TargetedExperiment & id)
        Stores a map in a TraML file
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(String filename, StringList & errors, StringList & warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        """
        ... 


class TransformationDescription:
    """
    Cython implementation of _TransformationDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationDescription.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationDescription ) -> None:
        """
        Cython signature: void TransformationDescription(TransformationDescription &)
        """
        ...
    
    def getDataPoints(self) -> List[TM_DataPoint]:
        """
        Cython signature: libcpp_vector[TM_DataPoint] getDataPoints()
        Returns the data points
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[TM_DataPoint] & data)
        Sets the data points. Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[List[float, float]] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[libcpp_pair[double,double]] & data)
        Sets the data points (backwards-compatible overload). Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    def apply(self, in_0: float ) -> float:
        """
        Cython signature: double apply(double)
        Applies the transformation to `value`
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] , params: Param ) -> None:
        """
        Cython signature: void fitModel(String model_type, Param params)
        Fits a model to the data
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void fitModel(String model_type)
        Fits a model to the data
        """
        ...
    
    def getModelType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModelType()
        Gets the type of the fitted model
        """
        ...
    
    def getModelParameters(self) -> Param:
        """
        Cython signature: Param getModelParameters()
        Returns the model parameters
        """
        ...
    
    def invert(self) -> None:
        """
        Cython signature: void invert()
        Computes an (approximate) inverse of the transformation
        """
        ...
    
    def getDeviations(self, diffs: List[float] , do_apply: bool , do_sort: bool ) -> None:
        """
        Cython signature: void getDeviations(libcpp_vector[double] & diffs, bool do_apply, bool do_sort)
        Get the deviations between the data pairs
        
        :param diffs: Output
        :param do_apply: Get deviations after applying the model?
        :param do_sort: Sort `diffs` before returning?
        """
        ...
    
    def getStatistics(self) -> TransformationStatistics:
        """
        Cython signature: TransformationStatistics getStatistics()
        """
        ...
    
    getModelTypes: __static_TransformationDescription_getModelTypes 


class TransformationStatistics:
    """
    Cython implementation of _TransformationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationStatistics.html>`_
    """
    
    xmin: float
    
    xmax: float
    
    ymin: float
    
    ymax: float
    
    percentiles_before: Dict[int, float]
    
    percentiles_after: Dict[int, float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationStatistics ) -> None:
        """
        Cython signature: void TransformationStatistics(TransformationStatistics &)
        """
        ... 


class XMLFile:
    """
    Cython implementation of _XMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1XMLFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: XMLFile ) -> None:
        """
        Cython signature: void XMLFile(XMLFile &)
        """
        ...
    
    @overload
    def __init__(self, schema_location: Union[bytes, str, String] , version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void XMLFile(const String & schema_location, const String & version)
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class XQuestScores:
    """
    Cython implementation of _XQuestScores

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XQuestScores.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XQuestScores()
        """
        ...
    
    @overload
    def __init__(self, in_0: XQuestScores ) -> None:
        """
        Cython signature: void XQuestScores(XQuestScores &)
        """
        ...
    
    @overload
    def preScore(self, matched_alpha: int , ions_alpha: int , matched_beta: int , ions_beta: int ) -> float:
        """
        Cython signature: float preScore(size_t matched_alpha, size_t ions_alpha, size_t matched_beta, size_t ions_beta)
        Compute a simple and fast to compute pre-score for a cross-link spectrum match
        
        :param matched_alpha: Number of experimental peaks matched to theoretical linear ions from the alpha peptide
        :param ions_alpha: Number of theoretical ions from the alpha peptide
        :param matched_beta: Number of experimental peaks matched to theoretical linear ions from the beta peptide
        :param ions_beta: Number of theoretical ions from the beta peptide
        """
        ...
    
    @overload
    def preScore(self, matched_alpha: int , ions_alpha: int ) -> float:
        """
        Cython signature: float preScore(size_t matched_alpha, size_t ions_alpha)
        Compute a simple and fast to compute pre-score for a mono-link spectrum match
        
        :param matched_alpha: Number of experimental peaks matched to theoretical linear ions from the alpha peptide
        :param ions_alpha: Number of theoretical ions from the alpha peptide
        """
        ...
    
    def matchOddsScore(self, theoretical_spec: MSSpectrum , fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , is_xlink_spectrum: bool , n_charges: int ) -> float:
        """
        Cython signature: double matchOddsScore(MSSpectrum & theoretical_spec, double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, bool is_xlink_spectrum, size_t n_charges)
        Compute the match-odds score, a score based on the probability of getting the given number of matched peaks by chance
        
        :param theoretical_spec: Theoretical spectrum, sorted by position
        :param matched_size: Alignment between the theoretical and the experimental spectra
        :param fragment_mass_tolerance: Fragment mass tolerance of the alignment
        :param fragment_mass_tolerance_unit_ppm: Fragment mass tolerance unit of the alignment, true = ppm, false = Da
        :param is_xlink_spectrum: Type of cross-link, true = cross-link, false = mono-link
        :param n_charges: Number of considered charges in the theoretical spectrum
        """
        ...
    
    def logOccupancyProb(self, theoretical_spec: MSSpectrum , matched_size: int , fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool ) -> float:
        """
        Cython signature: double logOccupancyProb(MSSpectrum theoretical_spec, size_t matched_size, double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm)
        Compute the logOccupancyProb score, similar to the match_odds, a score based on the probability of getting the given number of matched peaks by chance
        
        :param theoretical_spec: Theoretical spectrum, sorted by position
        :param matched_size: Number of matched peaks between experimental and theoretical spectra
        :param fragment_mass_tolerance: The tolerance of the alignment
        :param fragment_mass_tolerance_unit: The tolerance unit of the alignment, true = ppm, false = Da
        """
        ...
    
    def weightedTICScoreXQuest(self, alpha_size: int , beta_size: int , intsum_alpha: float , intsum_beta: float , total_current: float , type_is_cross_link: bool ) -> float:
        """
        Cython signature: double weightedTICScoreXQuest(size_t alpha_size, size_t beta_size, double intsum_alpha, double intsum_beta, double total_current, bool type_is_cross_link)
        """
        ...
    
    def weightedTICScore(self, alpha_size: int , beta_size: int , intsum_alpha: float , intsum_beta: float , total_current: float , type_is_cross_link: bool ) -> float:
        """
        Cython signature: double weightedTICScore(size_t alpha_size, size_t beta_size, double intsum_alpha, double intsum_beta, double total_current, bool type_is_cross_link)
        """
        ...
    
    def matchedCurrentChain(self, matched_spec_common: List[List[int, int]] , matched_spec_xlinks: List[List[int, int]] , spectrum_common_peaks: MSSpectrum , spectrum_xlink_peaks: MSSpectrum ) -> float:
        """
        Cython signature: double matchedCurrentChain(libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks, MSSpectrum & spectrum_common_peaks, MSSpectrum & spectrum_xlink_peaks)
        """
        ...
    
    def totalMatchedCurrent(self, matched_spec_common_alpha: List[List[int, int]] , matched_spec_common_beta: List[List[int, int]] , matched_spec_xlinks_alpha: List[List[int, int]] , matched_spec_xlinks_beta: List[List[int, int]] , spectrum_common_peaks: MSSpectrum , spectrum_xlink_peaks: MSSpectrum ) -> float:
        """
        Cython signature: double totalMatchedCurrent(libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common_beta, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_beta, MSSpectrum & spectrum_common_peaks, MSSpectrum & spectrum_xlink_peaks)
        """
        ...
    
    def xCorrelation(self, spec1: MSSpectrum , spec2: MSSpectrum , maxshift: int , tolerance: float ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] xCorrelation(MSSpectrum & spec1, MSSpectrum & spec2, int maxshift, double tolerance)
        """
        ...
    
    def xCorrelationPrescore(self, spec1: MSSpectrum , spec2: MSSpectrum , tolerance: float ) -> float:
        """
        Cython signature: double xCorrelationPrescore(MSSpectrum & spec1, MSSpectrum & spec2, double tolerance)
        """
        ... 


class DecoyTransitionType:
    None
    UNKNOWN : int
    TARGET : int
    DECOY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IonOpticsType:
    None
    UNKNOWN : int
    MAGNETIC_DEFLECTION : int
    DELAYED_EXTRACTION : int
    COLLISION_QUADRUPOLE : int
    SELECTED_ION_FLOW_TUBE : int
    TIME_LAG_FOCUSING : int
    REFLECTRON : int
    EINZEL_LENS : int
    FIRST_STABILITY_REGION : int
    FRINGING_FIELD : int
    KINETIC_ENERGY_ANALYZER : int
    STATIC_FIELD : int
    SIZE_OF_IONOPTICSTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Modification_SpecificityType:
    None
    AA : int
    AA_AT_CTERM : int
    AA_AT_NTERM : int
    CTERM : int
    NTERM : int
    SIZE_OF_SPECIFICITYTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __NASFragmentType:
    None
    Full : int
    Internal : int
    FivePrime : int
    ThreePrime : int
    AIon : int
    BIon : int
    CIon : int
    XIon : int
    YIon : int
    ZIon : int
    Precursor : int
    BIonMinusH20 : int
    YIonMinusH20 : int
    BIonMinusNH3 : int
    YIonMinusNH3 : int
    NonIdentified : int
    Unannotated : int
    WIon : int
    AminusB : int
    DIon : int
    SizeOfNASFragmentType : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class QuotingMethod:
    None
    NONE : int
    ESCAPE : int
    DOUBLE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

