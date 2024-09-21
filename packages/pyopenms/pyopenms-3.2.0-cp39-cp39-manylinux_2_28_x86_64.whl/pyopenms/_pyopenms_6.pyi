from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_SpectrumMetaDataLookup_addMissingRTsToPeptideIDs(in_0: List[PeptideIdentification] , filename: Union[bytes, str, String] , stop_on_error: bool ) -> bool:
    """
    Cython signature: bool addMissingRTsToPeptideIDs(libcpp_vector[PeptideIdentification], String filename, bool stop_on_error)
    """
    ...

def __static_SpectrumMetaDataLookup_addMissingSpectrumReferences(in_0: List[PeptideIdentification] , filename: Union[bytes, str, String] , stop_on_error: bool , override_spectra_data: bool , override_spectra_references: bool , proteins: List[ProteinIdentification] ) -> bool:
    """
    Cython signature: bool addMissingSpectrumReferences(libcpp_vector[PeptideIdentification], String filename, bool stop_on_error, bool override_spectra_data, bool override_spectra_references, libcpp_vector[ProteinIdentification] proteins)
    """
    ...

def __static_AASequence_fromString(s: Union[bytes, str, String] ) -> AASequence:
    """
    Cython signature: AASequence fromString(String s)
    """
    ...

def __static_AASequence_fromStringPermissive(s: Union[bytes, str, String] , permissive: bool ) -> AASequence:
    """
    Cython signature: AASequence fromStringPermissive(String s, bool permissive)
    """
    ...

def __static_SpectrumMetaDataLookup_getSpectrumMetaData(spectrum: MSSpectrum , meta: SpectrumMetaData ) -> None:
    """
    Cython signature: void getSpectrumMetaData(MSSpectrum spectrum, SpectrumMetaData & meta)
    """
    ...


class AASeqWithMass:
    """
    Cython implementation of _AASeqWithMass

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AASeqWithMass.html>`_
    """
    
    peptide_mass: float
    
    peptide_seq: AASequence
    
    position: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AASeqWithMass()
        """
        ...
    
    @overload
    def __init__(self, in_0: AASeqWithMass ) -> None:
        """
        Cython signature: void AASeqWithMass(AASeqWithMass &)
        """
        ... 


class AASequence:
    """
    Cython implementation of _AASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AASequence.html>`_

    Representation of a peptide/protein sequence
    This class represents amino acid sequences in OpenMS. An AASequence
    instance primarily contains a sequence of residues.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: AASequence ) -> None:
        """
        Cython signature: void AASequence(AASequence &)
        """
        ...
    
    def __add__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __iadd__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __getitem__(self, in_0: int ) -> Residue:
        """
        Cython signature: Residue operator[](size_t)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def toUnmodifiedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUnmodifiedString()
        Returns the peptide as string without any modifications
        """
        ...
    
    def toUniModString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUniModString()
        Returns the peptide as string with UniMod-style modifications embedded in brackets
        """
        ...
    
    @overload
    def toBracketString(self, ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString()
        Create a TPP compatible string of the modified sequence using bracket notation. Uses integer mass by default
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta)
        Create a TPP compatible string of the modified sequence using bracket notation.
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool , fixed_modifications: List[bytes] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta, libcpp_vector[String] fixed_modifications)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModification(size_t index, const String & modification)
        Sets the modification of the residue at position index. If an empty string is passed replaces the residue with its unmodified version
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: ResidueModification ) -> None:
        """
        Cython signature: void setModification(size_t index, const ResidueModification & modification)
        Sets the modification of AA at index by providing a ResidueModification object. Stricter than just looking for the name and adds the Modification to the DB if not present
        """
        ...
    
    def setModificationByDiffMonoMass(self, index: int , diffMonoMass: float ) -> None:
        """
        Cython signature: void setModificationByDiffMonoMass(size_t index, double diffMonoMass)
        Modifies the residue at index in the sequence and potentially in the ResidueDB
        """
        ...
    
    @overload
    def setNTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNTerminalModification(String modification)
        Sets the N-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setNTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setNTerminalModification(const ResidueModification & mod)
        Sets the N-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setNTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setNTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the N-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    @overload
    def setCTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCTerminalModification(String modification)
        Sets the C-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setCTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setCTerminalModification(const ResidueModification & mod)
        Sets the C-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setCTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setCTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the C-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    def getNTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNTerminalModificationName()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def getNTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getNTerminalModification()
        Returns a copy of the name N-terminal modification object, or None
        """
        ...
    
    def getCTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCTerminalModificationName()
        Returns the name (ID) of the C-terminal modification, or an empty string if none is set
        """
        ...
    
    def getCTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getCTerminalModification()
        Returns a copy of the name C-terminal modification object, or None
        """
        ...
    
    def getResidue(self, index: int ) -> Residue:
        """
        Cython signature: Residue getResidue(size_t index)
        Returns the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Convenience function with ResidueType=Full and charge = 0 by default
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(ResidueType type_, int charge)
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
        Cython signature: double getAverageWeight(ResidueType type_, int charge)
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
        Cython signature: double getMonoWeight(ResidueType type_, int charge)
        """
        ...
    
    @overload
    def getMZ(self, charge: int ) -> float:
        """
        Cython signature: double getMZ(int charge)
        Returns the mass-to-charge ratio of the peptide
        """
        ...
    
    @overload
    def getMZ(self, charge: int , type_: int ) -> float:
        """
        Cython signature: double getMZ(int charge, ResidueType type_)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getPrefix(size_t index)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getSuffix(size_t index)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, index: int , number: int ) -> AASequence:
        """
        Cython signature: AASequence getSubsequence(size_t index, unsigned int number)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def has(self, residue: Residue ) -> bool:
        """
        Cython signature: bool has(Residue residue)
        Returns true if the peptide contains the given residue
        """
        ...
    
    def hasSubsequence(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSubsequence(AASequence peptide)
        Returns true if the peptide contains the given peptide
        """
        ...
    
    def hasPrefix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasPrefix(AASequence peptide)
        Returns true if the peptide has the given prefix
        """
        ...
    
    def hasSuffix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSuffix(AASequence peptide)
        Returns true if the peptide has the given suffix
        """
        ...
    
    def hasNTerminalModification(self) -> bool:
        """
        Cython signature: bool hasNTerminalModification()
        Predicate which is true if the peptide is N-term modified
        """
        ...
    
    def hasCTerminalModification(self) -> bool:
        """
        Cython signature: bool hasCTerminalModification()
        Predicate which is true if the peptide is C-term modified
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        Returns true if any of the residues or termini are modified
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    fromString: __static_AASequence_fromString
    
    fromStringPermissive: __static_AASequence_fromStringPermissive 


class CVMappingRule:
    """
    Cython implementation of _CVMappingRule

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingRule.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingRule()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingRule ) -> None:
        """
        Cython signature: void CVMappingRule(CVMappingRule &)
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String identifier)
        Sets the identifier of the rule
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the identifier of the rule
        """
        ...
    
    def setElementPath(self, element_path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setElementPath(String element_path)
        Sets the path of the DOM element, where this rule is allowed
        """
        ...
    
    def getElementPath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getElementPath()
        Returns the path of the DOM element, where this rule is allowed
        """
        ...
    
    def setRequirementLevel(self, level: int ) -> None:
        """
        Cython signature: void setRequirementLevel(RequirementLevel level)
        Sets the requirement level of this rule
        """
        ...
    
    def getRequirementLevel(self) -> int:
        """
        Cython signature: RequirementLevel getRequirementLevel()
        Returns the requirement level of this rule
        """
        ...
    
    def setCombinationsLogic(self, combinations_logic: int ) -> None:
        """
        Cython signature: void setCombinationsLogic(CombinationsLogic combinations_logic)
        Sets the combination operator of the rule
        """
        ...
    
    def getCombinationsLogic(self) -> int:
        """
        Cython signature: CombinationsLogic getCombinationsLogic()
        Returns the combinations operator of the rule
        """
        ...
    
    def setScopePath(self, path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScopePath(String path)
        Sets the scope path of the rule
        """
        ...
    
    def getScopePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScopePath()
        Returns the scope path of the rule
        """
        ...
    
    def setCVTerms(self, cv_terms: List[CVMappingTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVMappingTerm] cv_terms)
        Sets the terms which are allowed
        """
        ...
    
    def getCVTerms(self) -> List[CVMappingTerm]:
        """
        Cython signature: libcpp_vector[CVMappingTerm] getCVTerms()
        Returns the allowed terms
        """
        ...
    
    def addCVTerm(self, cv_terms: CVMappingTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVMappingTerm cv_terms)
        Adds a term to the allowed terms
        """
        ...
    
    def __richcmp__(self, other: CVMappingRule, op: int) -> Any:
        ...
    CombinationsLogic : __CombinationsLogic
    RequirementLevel : __RequirementLevel 


class CVMappingTerm:
    """
    Cython implementation of _CVMappingTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingTerm ) -> None:
        """
        Cython signature: void CVMappingTerm(CVMappingTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setUseTermName(self, use_term_name: bool ) -> None:
        """
        Cython signature: void setUseTermName(bool use_term_name)
        Sets whether the term name should be used, instead of the accession
        """
        ...
    
    def getUseTermName(self) -> bool:
        """
        Cython signature: bool getUseTermName()
        Returns whether the term name should be used, instead of the accession
        """
        ...
    
    def setUseTerm(self, use_term: bool ) -> None:
        """
        Cython signature: void setUseTerm(bool use_term)
        Sets whether the term itself can be used (or only its children)
        """
        ...
    
    def getUseTerm(self) -> bool:
        """
        Cython signature: bool getUseTerm()
        Returns true if the term can be used, false if only children are allowed
        """
        ...
    
    def setTermName(self, term_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermName(String term_name)
        Sets the name of the term
        """
        ...
    
    def getTermName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermName()
        Returns the name of the term
        """
        ...
    
    def setIsRepeatable(self, is_repeatable: bool ) -> None:
        """
        Cython signature: void setIsRepeatable(bool is_repeatable)
        Sets whether this term can be repeated
        """
        ...
    
    def getIsRepeatable(self) -> bool:
        """
        Cython signature: bool getIsRepeatable()
        Returns true if this term can be repeated, false otherwise
        """
        ...
    
    def setAllowChildren(self, allow_children: bool ) -> None:
        """
        Cython signature: void setAllowChildren(bool allow_children)
        Sets whether children of this term are allowed
        """
        ...
    
    def getAllowChildren(self) -> bool:
        """
        Cython signature: bool getAllowChildren()
        Returns true if the children of this term are allowed to be used
        """
        ...
    
    def setCVIdentifierRef(self, cv_identifier_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_identifier_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def __richcmp__(self, other: CVMappingTerm, op: int) -> Any:
        ... 


class CVTerm:
    """
    Cython implementation of _CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTerm ) -> None:
        """
        Cython signature: void CVTerm(CVTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the term
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the term
        """
        ...
    
    def setCVIdentifierRef(self, cv_id_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_id_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def getValue(self) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue()
        Returns the value of the term
        """
        ...
    
    def setValue(self, value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(DataValue value)
        Sets the value of the term
        """
        ...
    
    def setUnit(self, unit: Unit ) -> None:
        """
        Cython signature: void setUnit(Unit & unit)
        Sets the unit of the term
        """
        ...
    
    def getUnit(self) -> Unit:
        """
        Cython signature: Unit getUnit()
        Returns the unit
        """
        ...
    
    def hasValue(self) -> bool:
        """
        Cython signature: bool hasValue()
        Checks whether the term has a value
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        Checks whether the term has a unit
        """
        ...
    
    def __richcmp__(self, other: CVTerm, op: int) -> Any:
        ... 


class ColumnHeader:
    """
    Cython implementation of _ColumnHeader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ColumnHeader.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    filename: Union[bytes, str, String]
    
    label: Union[bytes, str, String]
    
    size: int
    
    unique_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ColumnHeader()
        """
        ...
    
    @overload
    def __init__(self, in_0: ColumnHeader ) -> None:
        """
        Cython signature: void ColumnHeader(ColumnHeader &)
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
    
    def __richcmp__(self, other: ColumnHeader, op: int) -> Any:
        ... 


class ConsensusIDAlgorithmPEPIons:
    """
    Cython implementation of _ConsensusIDAlgorithmPEPIons

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmPEPIons.html>`_
      -- Inherits from ['ConsensusIDAlgorithmSimilarity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmPEPIons()
        """
        ...
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusIDAlgorithmSimilarity:
    """
    Cython implementation of _ConsensusIDAlgorithmSimilarity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmSimilarity.html>`_
      -- Inherits from ['ConsensusIDAlgorithm']
    """
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusMap:
    """
    Cython implementation of _ConsensusMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ConsensusMap.html>`_
      -- Inherits from ['UniqueIdInterface', 'DocumentIdentifier', 'RangeManagerRtMzInt', 'MetaInfoInterface']

    A container for consensus elements.
    
    A ConsensusMap is a container holding 2-dimensional consensus elements
    (ConsensusFeature) which in turn represent analytes that have been
    quantified across multiple LC-MS/MS experiments. Each analyte in a
    ConsensusFeature is linked to its original LC-MS/MS run, the links are
    maintained by the ConsensusMap class.
    The map is implemented as a vector of elements of type ConsensusFeature.
    
    To be consistent, all maps who are referenced by ConsensusFeature objects
    (through a unique id) need to be registered in this class.
    
    This class supports direct iteration in Python.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConsensusMap()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConsensusMap ) -> None:
        """
        Cython signature: void ConsensusMap(ConsensusMap &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def reserve(self, s: int ) -> None:
        """
        Cython signature: void reserve(size_t s)
        """
        ...
    
    def __getitem__(self, in_0: int ) -> ConsensusFeature:
        """
        Cython signature: ConsensusFeature & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: ConsensusFeature ) -> None:
        """Cython signature: ConsensusFeature & operator[](size_t)"""
        ...
    
    def push_back(self, spec: ConsensusFeature ) -> None:
        """
        Cython signature: void push_back(ConsensusFeature spec)
        """
        ...
    
    def appendRows(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendRows(ConsensusMap)
        Add consensus map entries as new rows
        """
        ...
    
    def appendColumns(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendColumns(ConsensusMap)
        Add consensus map entries as new columns
        """
        ...
    
    @overload
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clears all data and meta data
        """
        ...
    
    @overload
    def clear(self, ) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def updateRanges(self) -> None:
        """
        Cython signature: void updateRanges()
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def setProteinIdentifications(self, in_0: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification])
        Sets the protein identifications
        """
        ...
    
    def getUnassignedPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getUnassignedPeptideIdentifications()
        """
        ...
    
    def setUnassignedPeptideIdentifications(self, in_0: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setUnassignedPeptideIdentifications(libcpp_vector[PeptideIdentification])
        Sets the unassigned peptide identifications
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[DataProcessing] getDataProcessing()
        Returns a const reference to the description of the applied data processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[DataProcessing])
        Sets the description of the applied data processing
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s)
        Sets the file paths to the primary MS run (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , e: MSExperiment ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, MSExperiment & e)
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        Returns the MS run path (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Sorts the peaks according to ascending intensity.
        """
        ...
    
    @overload
    def sortByIntensity(self, ) -> None:
        """
        Cython signature: void sortByIntensity()
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sorts the peaks according to RT position
        """
        ...
    
    def sortByMZ(self) -> None:
        """
        Cython signature: void sortByMZ()
        Sorts the peaks according to m/z position
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Lexicographically sorts the peaks by their position (First RT then m/z)
        """
        ...
    
    @overload
    def sortByQuality(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByQuality(bool reverse)
        Sorts the peaks according to ascending quality.
        """
        ...
    
    @overload
    def sortByQuality(self, ) -> None:
        """
        Cython signature: void sortByQuality()
        """
        ...
    
    def sortBySize(self) -> None:
        """
        Cython signature: void sortBySize()
        Sorts with respect to the size (number of elements)
        """
        ...
    
    def sortByMaps(self) -> None:
        """
        Cython signature: void sortByMaps()
        Sorts with respect to the sets of maps covered by the consensus features (lexicographically)
        """
        ...
    
    def getExperimentType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentType()
        Non-mutable access to the experiment type
        """
        ...
    
    def setExperimentType(self, experiment_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentType(String experiment_type)
        Mutable access to the experiment type
        """
        ...
    
    def sortPeptideIdentificationsByMapIndex(self) -> None:
        """
        Cython signature: void sortPeptideIdentificationsByMapIndex()
        Sorts PeptideIdentifications of consensus features with respect to their map index.
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
    
    def setIdentifier(self, id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id)
        Sets document identifier (e.g. an LSID)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Retrieve document identifier (e.g. an LSID)
        """
        ...
    
    def setLoadedFileType(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFileType(String file_name)
        Sets the file_type according to the type of the file loaded from, preferably done whilst loading
        """
        ...
    
    def getLoadedFileType(self) -> int:
        """
        Cython signature: int getLoadedFileType()
        Returns the file_type (e.g. featureXML, consensusXML, mzData, mzXML, mzML, ...) of the file loaded
        """
        ...
    
    def setLoadedFilePath(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFilePath(String file_name)
        Sets the file_name according to absolute path of the file loaded, preferably done whilst loading
        """
        ...
    
    def getLoadedFilePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLoadedFilePath()
        Returns the file_name which is the absolute path to the file loaded
        """
        ...
    
    def getMinRT(self) -> float:
        """
        Cython signature: double getMinRT()
        Returns the minimum RT
        """
        ...
    
    def getMaxRT(self) -> float:
        """
        Cython signature: double getMaxRT()
        Returns the maximum RT
        """
        ...
    
    def getMinMZ(self) -> float:
        """
        Cython signature: double getMinMZ()
        Returns the minimum m/z
        """
        ...
    
    def getMaxMZ(self) -> float:
        """
        Cython signature: double getMaxMZ()
        Returns the maximum m/z
        """
        ...
    
    def getMinIntensity(self) -> float:
        """
        Cython signature: double getMinIntensity()
        Returns the minimum intensity
        """
        ...
    
    def getMaxIntensity(self) -> float:
        """
        Cython signature: double getMaxIntensity()
        Returns the maximum intensity
        """
        ...
    
    def clearRanges(self) -> None:
        """
        Cython signature: void clearRanges()
        Resets all range dimensions as empty
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
    
    def __richcmp__(self, other: ConsensusMap, op: int) -> Any:
        ...
    
    def __iter__(self) -> ConsensusFeature:
       ... 


class ConsensusXMLFile:
    """
    Cython implementation of _ConsensusXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: ConsensusMap ) -> None:
        """
        Cython signature: void load(String, ConsensusMap &)
        Loads a consensus map from file and calls updateRanges
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: ConsensusMap ) -> None:
        """
        Cython signature: void store(String, ConsensusMap &)
        Stores a consensus map to file
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Mutable access to the options for loading/storing
        """
        ... 


class ConvexHull2D:
    """
    Cython implementation of _ConvexHull2D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConvexHull2D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConvexHull2D()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConvexHull2D ) -> None:
        """
        Cython signature: void ConvexHull2D(ConvexHull2D &)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Removes all points
        """
        ...
    
    def compress(self) -> int:
        """
        Cython signature: size_t compress()
        Allows to reduce the disk/memory footprint of a hull
        """
        ...
    
    def expandToBoundingBox(self) -> None:
        """
        Cython signature: void expandToBoundingBox()
        Expand a convex hull to its bounding box.
        """
        ...
    
    def addPoint(self, point: Union[Sequence[int], Sequence[float]] ) -> bool:
        """
        Cython signature: bool addPoint(DPosition2 point)
        Adds a point to the hull if it is not already contained. Returns if the point was added. This will trigger recomputation of the outer hull points (thus points set with setHullPoints() will be lost)
        """
        ...
    
    def addPoints(self, points: '_np.ndarray[Any, _np.dtype[_np.float32]]' ) -> None:
        """
        Cython signature: void addPoints(libcpp_vector[DPosition2] points)
        Adds points to the hull if it is not already contained. This will trigger recomputation of the outer hull points (thus points set with setHullPoints() will be lost)
        """
        ...
    
    def encloses(self, in_0: Union[Sequence[int], Sequence[float]] ) -> bool:
        """
        Cython signature: bool encloses(DPosition2)
        Returns if the `point` lies in the feature hull
        """
        ...
    
    def getHullPoints(self) -> '_np.ndarray[Any, _np.dtype[_np.float32]]':
        """
        Cython signature: libcpp_vector[DPosition2] getHullPoints()
        Accessor for the outer points
        """
        ...
    
    def setHullPoints(self, in_0: '_np.ndarray[Any, _np.dtype[_np.float32]]' ) -> None:
        """
        Cython signature: void setHullPoints(libcpp_vector[DPosition2])
        Accessor for the outer(!) points (no checking is performed if this is actually a convex hull)
        """
        ...
    
    def getBoundingBox(self) -> DBoundingBox2:
        """
        Cython signature: DBoundingBox2 getBoundingBox()
        Returns the bounding box of the feature hull points
        """
        ...
    
    def __richcmp__(self, other: ConvexHull2D, op: int) -> Any:
        ... 


class CrossLinksDB:
    """
    Cython implementation of _CrossLinksDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CrossLinksDB.html>`_
    """
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        """
        ...
    
    def searchModifications(self, mods: Set[ResidueModification] , mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModifications(libcpp_set[const ResidueModification *] & mods, const String & mod_name, const String & residue, TermSpecificity term_spec)
        """
        ...
    
    @overload
    def getModification(self, index: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(size_t index)
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name)
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name, const String & residue, TermSpecificity term_spec)
        """
        ...
    
    def has(self, modification: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool has(String modification)
        """
        ...
    
    def findModificationIndex(self, mod_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findModificationIndex(const String & mod_name)
        """
        ...
    
    def searchModificationsByDiffMonoMass(self, mods: List[bytes] , mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModificationsByDiffMonoMass(libcpp_vector[String] & mods, double mass, double max_error, const String & residue, TermSpecificity term_spec)
        """
        ...
    
    def getBestModificationByDiffMonoMass(self, mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getBestModificationByDiffMonoMass(double mass, double max_error, const String residue, TermSpecificity term_spec)
        """
        ...
    
    def getAllSearchModifications(self, modifications: List[bytes] ) -> None:
        """
        Cython signature: void getAllSearchModifications(libcpp_vector[String] & modifications)
        """
        ...
    
    def readFromOBOFile(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readFromOBOFile(const String & filename)
        """
        ...
    
    def isInstantiated(self) -> bool:
        """
        Cython signature: bool isInstantiated()
        """
        ... 


class DBoundingBox2:
    """
    Cython implementation of _DBoundingBox2

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DBoundingBox2.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DBoundingBox2()
        """
        ...
    
    @overload
    def __init__(self, in_0: DBoundingBox2 ) -> None:
        """
        Cython signature: void DBoundingBox2(DBoundingBox2 &)
        """
        ...
    
    def minPosition(self) -> Union[Sequence[int], Sequence[float]]:
        """
        Cython signature: DPosition2 minPosition()
        """
        ...
    
    def maxPosition(self) -> Union[Sequence[int], Sequence[float]]:
        """
        Cython signature: DPosition2 maxPosition()
        """
        ... 


class DigestionEnzyme:
    """
    Cython implementation of _DigestionEnzyme

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzyme.html>`_

      Base class for digestion enzymes
    """
    
    @overload
    def __init__(self, in_0: DigestionEnzyme ) -> None:
        """
        Cython signature: void DigestionEnzyme(DigestionEnzyme &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , cleavage_regex: Union[bytes, str, String] , synonyms: Set[bytes] , regex_description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DigestionEnzyme(const String & name, const String & cleavage_regex, libcpp_set[String] & synonyms, String regex_description)
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the enzyme
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the enzyme
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] & synonyms)
        Sets the synonyms
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(const String & synonym)
        Adds a synonym
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the synonyms
        """
        ...
    
    def setRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegEx(const String & cleavage_regex)
        Sets the cleavage regex
        """
        ...
    
    def getRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegEx()
        Returns the cleavage regex
        """
        ...
    
    def setRegExDescription(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegExDescription(const String & value)
        Sets the regex description
        """
        ...
    
    def getRegExDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegExDescription()
        Returns the regex description
        """
        ...
    
    def setValueFromFile(self, key: Union[bytes, str, String] , value: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool setValueFromFile(String key, String value)
        Sets the value of a member variable based on an entry from an input file
        """
        ...
    
    def __richcmp__(self, other: DigestionEnzyme, op: int) -> Any:
        ... 


class DigestionEnzymeRNA:
    """
    Cython implementation of _DigestionEnzymeRNA

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzymeRNA.html>`_
      -- Inherits from ['DigestionEnzyme']

    Representation of a digestion enzyme for RNA (RNase)
    
    The cutting sites of these enzymes are defined using two different mechanisms:
    First, a single regular expression that is applied to strings of unmodified RNA sequence and defines cutting sites via zero-length matches (using lookahead/lookbehind assertions).
    This is the same mechanism that is used for proteases (see ProteaseDigestion).
    However, due to the complex notation involved, this approach is not practical for modification-aware digestion.
    Thus, the second mechanism uses two regular expressions ("cuts after"/"cuts before"), which are applied to the short codes (e.g. "m6A") of sequential ribonucleotides.
    If both expressions match, then there is a cutting site between the two ribonucleotides.
    
    There is support for terminal (5'/3') modifications that may be generated on fragments as a result of RNase cleavage.
    A typical example is 3'-phosphate, resulting from cleavage of the phosphate backbone.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DigestionEnzymeRNA()
        """
        ...
    
    @overload
    def __init__(self, in_0: DigestionEnzymeRNA ) -> None:
        """
        Cython signature: void DigestionEnzymeRNA(DigestionEnzymeRNA &)
        """
        ...
    
    def setCutsAfterRegEx(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCutsAfterRegEx(String value)
        Sets the "cuts after ..." regular expression
        """
        ...
    
    def getCutsAfterRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCutsAfterRegEx()
        Returns the "cuts after ..." regular expression
        """
        ...
    
    def setCutsBeforeRegEx(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCutsBeforeRegEx(String value)
        Sets the "cuts before ..." regular expression
        """
        ...
    
    def getCutsBeforeRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCutsBeforeRegEx()
        Returns the "cuts before ..." regular expression
        """
        ...
    
    def setThreePrimeGain(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setThreePrimeGain(String value)
        Sets the 3' gain
        """
        ...
    
    def setFivePrimeGain(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFivePrimeGain(String value)
        Sets the 5' gain
        """
        ...
    
    def getThreePrimeGain(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getThreePrimeGain()
        Returns the 3' gain
        """
        ...
    
    def getFivePrimeGain(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFivePrimeGain()
        Returns the 5' gain
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the enzyme
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the enzyme
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] & synonyms)
        Sets the synonyms
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(const String & synonym)
        Adds a synonym
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the synonyms
        """
        ...
    
    def setRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegEx(const String & cleavage_regex)
        Sets the cleavage regex
        """
        ...
    
    def getRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegEx()
        Returns the cleavage regex
        """
        ...
    
    def setRegExDescription(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegExDescription(const String & value)
        Sets the regex description
        """
        ...
    
    def getRegExDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegExDescription()
        Returns the regex description
        """
        ...
    
    def setValueFromFile(self, key: Union[bytes, str, String] , value: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool setValueFromFile(String key, String value)
        Sets the value of a member variable based on an entry from an input file
        """
        ...
    
    def __richcmp__(self, other: DigestionEnzymeRNA, op: int) -> Any:
        ... 


class EmpiricalFormula:
    """
    Cython implementation of _EmpiricalFormula

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmpiricalFormula.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmpiricalFormula()
        Representation of an empirical formula
        """
        ...
    
    @overload
    def __init__(self, in_0: EmpiricalFormula ) -> None:
        """
        Cython signature: void EmpiricalFormula(EmpiricalFormula &)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void EmpiricalFormula(String)
        EmpiricalFormula Constructor from string
        """
        ...
    
    @overload
    def __init__(self, number: int , element: Element , charge: int ) -> None:
        """
        Cython signature: void EmpiricalFormula(ptrdiff_t number, Element * element, ptrdiff_t charge)
        EmpiricalFormula Constructor with element pointer and number
        """
        ...
    
    def getMonoWeight(self) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the formula (includes proton charges)
        """
        ...
    
    def getAverageWeight(self) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the formula (includes proton charges)
        """
        ...
    
    def estimateFromWeightAndComp(self, average_weight: float , C: float , H: float , N: float , O: float , S: float , P: float ) -> bool:
        """
        Cython signature: bool estimateFromWeightAndComp(double average_weight, double C, double H, double N, double O, double S, double P)
        Fills this EmpiricalFormula with an approximate elemental composition for a given average weight and approximate elemental stoichiometry
        """
        ...
    
    def estimateFromWeightAndCompAndS(self, average_weight: float , S: int , C: float , H: float , N: float , O: float , P: float ) -> bool:
        """
        Cython signature: bool estimateFromWeightAndCompAndS(double average_weight, unsigned int S, double C, double H, double N, double O, double P)
        Fills this EmpiricalFormula with an approximate elemental composition for a given average weight, exact number of sulfurs, and approximate elemental stoichiometry
        """
        ...
    
    @overload
    def getIsotopeDistribution(self, in_0: CoarseIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution(CoarseIsotopePatternGenerator)
        Computes the isotope distribution of an empirical formula using the CoarseIsotopePatternGenerator or the FineIsotopePatternGenerator method
        """
        ...
    
    @overload
    def getIsotopeDistribution(self, in_0: FineIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution(FineIsotopePatternGenerator)
        """
        ...
    
    def getConditionalFragmentIsotopeDist(self, precursor: EmpiricalFormula , precursor_isotopes: Set[int] , method: CoarseIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getConditionalFragmentIsotopeDist(EmpiricalFormula & precursor, libcpp_set[unsigned int] & precursor_isotopes, CoarseIsotopePatternGenerator method)
        """
        ...
    
    def getNumberOfAtoms(self) -> int:
        """
        Cython signature: size_t getNumberOfAtoms()
        Returns the total number of atoms
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: ptrdiff_t getCharge()
        Returns the total charge
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(ptrdiff_t charge)
        Sets the charge
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the formula as a string (charges are not included)
        """
        ...
    
    def getElementalComposition(self) -> Dict[bytes, int]:
        """
        Cython signature: libcpp_map[libcpp_string,int] getElementalComposition()
        Get elemental composition as a hash {'Symbol' -> NrAtoms}
        """
        ...
    
    def isEmpty(self) -> bool:
        """
        Cython signature: bool isEmpty()
        Returns true if the formula does not contain a element
        """
        ...
    
    def isCharged(self) -> bool:
        """
        Cython signature: bool isCharged()
        Returns true if charge is not equal to zero
        """
        ...
    
    def hasElement(self, element: Element ) -> bool:
        """
        Cython signature: bool hasElement(Element * element)
        Returns true if the formula contains the element
        """
        ...
    
    def contains(self, ef: EmpiricalFormula ) -> bool:
        """
        Cython signature: bool contains(EmpiricalFormula ef)
        Returns true if all elements from `ef` ( empirical formula ) are LESS abundant (negative allowed) than the corresponding elements of this EmpiricalFormula
        """
        ...
    
    def __add__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __sub__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __iadd__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __isub__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def calculateTheoreticalIsotopesNumber(self) -> float:
        """
        Cython signature: double calculateTheoreticalIsotopesNumber()
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the formula as a string (charges are not included)
        """
        ...
    
    def __richcmp__(self, other: EmpiricalFormula, op: int) -> Any:
        ... 


class FalseDiscoveryRate:
    """
    Cython implementation of _FalseDiscoveryRate

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FalseDiscoveryRate.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FalseDiscoveryRate()
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[PeptideIdentification] , reverse_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & forward_ids, libcpp_vector[PeptideIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & id)
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[ProteinIdentification] , reverse_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & forward_ids, libcpp_vector[ProteinIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & id)
        """
        ...
    
    def applyEstimated(self, ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void applyEstimated(libcpp_vector[ProteinIdentification] & ids)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: List[ProteinIdentification] , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(libcpp_vector[ProteinIdentification] & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: ProteinIdentification , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(ProteinIdentification & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyBasic(self, run_info: List[ProteinIdentification] , ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[ProteinIdentification] & run_info, libcpp_vector[PeptideIdentification] & ids)
        """
        ...
    
    @overload
    def applyBasic(self, ids: List[PeptideIdentification] , higher_score_better: bool , charge: int , identifier: Union[bytes, str, String] , only_best_per_pep: bool ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[PeptideIdentification] & ids, bool higher_score_better, int charge, String identifier, bool only_best_per_pep)
        """
        ...
    
    @overload
    def applyBasic(self, cmap: ConsensusMap , use_unassigned_peptides: bool ) -> None:
        """
        Cython signature: void applyBasic(ConsensusMap & cmap, bool use_unassigned_peptides)
        """
        ...
    
    @overload
    def applyBasic(self, id: ProteinIdentification , groups_too: bool ) -> None:
        """
        Cython signature: void applyBasic(ProteinIdentification & id, bool groups_too)
        """
        ...
    
    def applyPickedProteinFDR(self, id: ProteinIdentification , decoy_string: String , decoy_prefix: bool , groups_too: bool ) -> None:
        """
        Cython signature: void applyPickedProteinFDR(ProteinIdentification & id, String & decoy_string, bool decoy_prefix, bool groups_too)
        """
        ...
    
    @overload
    def rocN(self, ids: List[PeptideIdentification] , fp_cutoff: int ) -> float:
        """
        Cython signature: double rocN(libcpp_vector[PeptideIdentification] & ids, size_t fp_cutoff)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, bool include_unassigned_peptides)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , identifier: Union[bytes, str, String] , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, const String & identifier, bool include_unassigned_peptides)
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


class FeatureDeconvolution:
    """
    Cython implementation of _FeatureDeconvolution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureDeconvolution.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureDeconvolution()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureDeconvolution ) -> None:
        """
        Cython signature: void FeatureDeconvolution(FeatureDeconvolution &)
        """
        ...
    
    def compute(self, input: FeatureMap , output: FeatureMap , cmap1: ConsensusMap , cmap2: ConsensusMap ) -> None:
        """
        Cython signature: void compute(FeatureMap & input, FeatureMap & output, ConsensusMap & cmap1, ConsensusMap & cmap2)
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
    CHARGEMODE_FD : __CHARGEMODE_FD 


class FeatureDistance:
    """
    Cython implementation of _FeatureDistance

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureDistance.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, max_intensity: float , force_constraints: bool ) -> None:
        """
        Cython signature: void FeatureDistance(double max_intensity, bool force_constraints)
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureDistance ) -> None:
        """
        Cython signature: void FeatureDistance(FeatureDistance &)
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


class IDDecoyProbability:
    """
    Cython implementation of _IDDecoyProbability

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDDecoyProbability.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDDecoyProbability()
        IDDecoyProbability calculates probabilities using decoy approach
        """
        ...
    
    @overload
    def __init__(self, in_0: IDDecoyProbability ) -> None:
        """
        Cython signature: void IDDecoyProbability(IDDecoyProbability)
        """
        ...
    
    @overload
    def apply(self, prob_ids: List[PeptideIdentification] , fwd_ids: List[PeptideIdentification] , rev_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & prob_ids, libcpp_vector[PeptideIdentification] & fwd_ids, libcpp_vector[PeptideIdentification] & rev_ids)
        Converts the forward and reverse identification into probabilities
        
        
        :param prob_ids: Output of the algorithm which includes identifications with probability based scores
        :param fwd_ids: Input parameter which represents the identifications of the forward search
        :param rev_ids: Input parameter which represents the identifications of the reversed search
        """
        ...
    
    @overload
    def apply(self, ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids)
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


class IDRipper:
    """
    Cython implementation of _IDRipper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IDRipper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IDRipper()
        Ripping protein/peptide identification according their file origin
        """
        ...
    
    def rip(self, rfis: List[RipFileIdentifier] , rfcs: List[RipFileContent] , proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , full_split: bool , split_ident_runs: bool ) -> None:
        """
        Cython signature: void rip(libcpp_vector[RipFileIdentifier] & rfis, libcpp_vector[RipFileContent] & rfcs, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, bool full_split, bool split_ident_runs)
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


class IdentificationRuns:
    """
    Cython implementation of _IdentificationRuns

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IdentificationRuns.html>`_
    """
    
    def __init__(self, prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void IdentificationRuns(libcpp_vector[ProteinIdentification] & prot_ids)
        """
        ... 


class IndexedMzMLDecoder:
    """
    Cython implementation of _IndexedMzMLDecoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLDecoder.html>`_

    A class to analyze indexedmzML files and extract the offsets of individual tags
    
    Specifically, this class allows one to extract the offsets of the <indexList>
    tag and of all <spectrum> and <chromatogram> tag using the indices found at
    the end of the indexedmzML XML structure
    
    While findIndexListOffset tries extracts the offset of the indexList tag from
    the last 1024 bytes of the file, this offset allows the function parseOffsets
    to extract all elements contained in the <indexList> tag and thus get access
    to all spectra and chromatogram offsets
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IndexedMzMLDecoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: IndexedMzMLDecoder ) -> None:
        """
        Cython signature: void IndexedMzMLDecoder(IndexedMzMLDecoder &)
        """
        ...
    
    def findIndexListOffset(self, in_: Union[bytes, str, String] , buffersize: int ) -> streampos:
        """
        Cython signature: streampos findIndexListOffset(String in_, int buffersize)
        Tries to extract the indexList offset from an indexedmzML\n
        
        This function reads by default the last few (1024) bytes of the given
        input file and tries to read the content of the <indexListOffset> tag
        The idea is that somewhere in the last parts of the file specified by the
        input string, the string <indexListOffset>xxx</indexListOffset> occurs
        This function returns the xxx part converted to an integer\n
        
        Since this function cannot determine where it will start reading
        the XML, no regular XML parser can be used for this. Therefore it uses
        regex to do its job. It matches the <indexListOffset> part and any
        numerical characters that follow
        
        
        :param in: Filename of the input indexedmzML file
        :param buffersize: How many bytes of the input file should be searched for the tag
        :return: A positive integer containing the content of the indexListOffset tag, returns -1 in case of failure no tag was found (you can re-try with a larger buffersize but most likely its not an indexed mzML). Using -1 is what the reference docu recommends: http://en.cppreference.com/w/cpp/io/streamoff
        :raises:
          Exception: FileNotFound is thrown if file cannot be found
        :raises:
          Exception: ParseError if offset cannot be parsed
        """
        ... 


class IndexedMzMLFileLoader:
    """
    Cython implementation of _IndexedMzMLFileLoader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLFileLoader.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IndexedMzMLFileLoader()
        A class to load an indexedmzML file
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> bool:
        """
        Cython signature: bool load(String, OnDiscMSExperiment &)
        Load a file\n
        
        Tries to parse the file, success needs to be checked with the return value
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> None:
        """
        Cython signature: void store(String, OnDiscMSExperiment &)
        Store a file from an on-disc data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void store(String, MSExperiment &)
        Store a file from an in-memory data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
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
        Returns the options for loading/storing
        """
        ... 


class IonSource:
    """
    Cython implementation of _IonSource

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonSource.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IonSource()
        Description of an ion source (part of a MS Instrument)
        """
        ...
    
    @overload
    def __init__(self, in_0: IonSource ) -> None:
        """
        Cython signature: void IonSource(IonSource &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the ionization mode
        """
        ...
    
    def setPolarity(self, polarity: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity polarity)
        Sets the ionization mode
        """
        ...
    
    def getInletType(self) -> int:
        """
        Cython signature: InletType getInletType()
        Returns the inlet type
        """
        ...
    
    def setInletType(self, inlet_type: int ) -> None:
        """
        Cython signature: void setInletType(InletType inlet_type)
        Sets the inlet type
        """
        ...
    
    def getIonizationMethod(self) -> int:
        """
        Cython signature: IonizationMethod getIonizationMethod()
        Returns the ionization method
        """
        ...
    
    def setIonizationMethod(self, ionization_type: int ) -> None:
        """
        Cython signature: void setIonizationMethod(IonizationMethod ionization_type)
        Sets the ionization method
        """
        ...
    
    def getOrder(self) -> int:
        """
        Cython signature: int getOrder()
        Returns the position of this part in the whole Instrument
        
        Order can be ignored, as long the instrument has this default setup:
          - one ion source
          - one or many mass analyzers
          - one ion detector
        
        For more complex instruments, the order should be defined.
        """
        ...
    
    def setOrder(self, order: int ) -> None:
        """
        Cython signature: void setOrder(int order)
        Sets the order
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
    
    def __richcmp__(self, other: IonSource, op: int) -> Any:
        ...
    InletType : __InletType
    IonizationMethod : __IonizationMethod
    Polarity : __Polarity 


class IsobaricChannelInformation:
    """
    Cython implementation of _IsobaricChannelInformation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IsobaricQuantitationMethod_1_1IsobaricChannelInformation.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: int
    
    description: Union[bytes, str, String]
    
    center: float
    
    affected_channels: List[int]
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , id_: int , description: Union[bytes, str, String] , center: float , affected_channels: List[int] ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(String name, int id_, String description, double center, libcpp_vector[int] affected_channels)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricChannelInformation ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(IsobaricChannelInformation &)
        """
        ... 


class IsotopeFitter1D:
    """
    Cython implementation of _IsotopeFitter1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeFitter1D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeFitter1D()
        Isotope distribution fitter (1-dim.) approximated using linear interpolation
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeFitter1D ) -> None:
        """
        Cython signature: void IsotopeFitter1D(IsotopeFitter1D &)
        """
        ... 


class KroenikFile:
    """
    Cython implementation of _KroenikFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KroenikFile.html>`_

    File adapter for Kroenik (HardKloer sibling) files
    
    The first line is the header and contains the column names:
    File,  First Scan,  Last Scan,  Num of Scans,  Charge,  Monoisotopic Mass,  Base Isotope Peak,  Best Intensity,  Summed Intensity,  First RTime,  Last RTime,  Best RTime,  Best Correlation,  Modifications
    
    Every subsequent line is a feature
    
    All properties in the file are converted to Feature properties, whereas "First Scan", "Last Scan", "Num of Scans" and "Modifications" are stored as
    metavalues with the following names "FirstScan", "LastScan", "NumOfScans" and "AveragineModifications"
    
    The width in m/z of the overall convex hull of each feature is set to 3 Th in lack of a value provided by the Kroenik file
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void KroenikFile()
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(String filename, MSSpectrum & spectrum)
        Stores a MSExperiment into a Kroenik file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void load(String filename, FeatureMap & feature_map)
        Loads a Kroenik file into a featureXML
        
        The content of the file is stored in `features`
        
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class MRMTransitionGroupPicker:
    """
    Cython implementation of _MRMTransitionGroupPicker

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroupPicker.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMTransitionGroupPicker ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker(MRMTransitionGroupPicker &)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: LightMRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(LightMRMTransitionGroupCP transition_group)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: MRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(MRMTransitionGroupCP transition_group)
        """
        ...
    
    def createMRMFeature(self, transition_group: LightMRMTransitionGroupCP , picked_chroms: List[MSChromatogram] , smoothed_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> MRMFeature:
        """
        Cython signature: MRMFeature createMRMFeature(LightMRMTransitionGroupCP transition_group, libcpp_vector[MSChromatogram] & picked_chroms, libcpp_vector[MSChromatogram] & smoothed_chroms, const int chr_idx, const int peak_idx)
        """
        ...
    
    def remove_overlapping_features(self, picked_chroms: List[MSChromatogram] , best_left: float , best_right: float ) -> None:
        """
        Cython signature: void remove_overlapping_features(libcpp_vector[MSChromatogram] & picked_chroms, double best_left, double best_right)
        """
        ...
    
    def findLargestPeak(self, picked_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> None:
        """
        Cython signature: void findLargestPeak(libcpp_vector[MSChromatogram] & picked_chroms, int & chr_idx, int & peak_idx)
        """
        ...
    
    def findWidestPeakIndices(self, picked_chroms: List[MSChromatogram] , chrom_idx: int , point_idx: int ) -> None:
        """
        Cython signature: void findWidestPeakIndices(libcpp_vector[MSChromatogram] & picked_chroms, int & chrom_idx, int & point_idx)
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


class MSDataCachedConsumer:
    """
    Cython implementation of _MSDataCachedConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataCachedConsumer.html>`_

    Transforming and cached writing consumer of MS data
    
    Is able to transform a spectrum on the fly while it is read using a
    function pointer that can be set on the object. The spectra is then
    cached to disk using the functions provided in CachedMzMLHandler.
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , clear: bool ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename, bool clear)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        
        May delete data from spectrum (if clearData is set)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
        
        May delete data from chromatogram (if clearData is set)
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


class MSDataSqlConsumer:
    """
    Cython implementation of _MSDataSqlConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataSqlConsumer.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int , buffer_size: int , full_meta: bool , lossy_compression: bool , linear_mass_acc: float ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(String filename, uint64_t run_id, int buffer_size, bool full_meta, bool lossy_compression, double linear_mass_acc)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataSqlConsumer ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(MSDataSqlConsumer &)
        """
        ...
    
    def flush(self) -> None:
        """
        Cython signature: void flush()
        Flushes the data for good
        
        After calling this function, no more data is held in the buffer but the
        class is still able to receive new data
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ... 


class MapAlignmentAlgorithmIdentification:
    """
    Cython implementation of _MapAlignmentAlgorithmIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmIdentification.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmIdentification()
        """
        ...
    
    @overload
    def align(self, in_0: List[MSExperiment] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[MSExperiment] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def align(self, in_0: List[FeatureMap] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[FeatureMap] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def align(self, in_0: List[ConsensusMap] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[ConsensusMap] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def setReference(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setReference(MSExperiment &)
        """
        ...
    
    @overload
    def setReference(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void setReference(FeatureMap &)
        """
        ...
    
    @overload
    def setReference(self, in_0: ConsensusMap ) -> None:
        """
        Cython signature: void setReference(ConsensusMap &)
        """
        ...
    
    @overload
    def setReference(self, in_0: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setReference(libcpp_vector[PeptideIdentification] &)
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


class MetaboliteFeatureDeconvolution:
    """
    Cython implementation of _MetaboliteFeatureDeconvolution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboliteFeatureDeconvolution.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboliteFeatureDeconvolution()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboliteFeatureDeconvolution ) -> None:
        """
        Cython signature: void MetaboliteFeatureDeconvolution(MetaboliteFeatureDeconvolution &)
        """
        ...
    
    def compute(self, fm_in: FeatureMap , fm_out: FeatureMap , cons_map: ConsensusMap , cons_map_p: ConsensusMap ) -> None:
        """
        Cython signature: void compute(FeatureMap & fm_in, FeatureMap & fm_out, ConsensusMap & cons_map, ConsensusMap & cons_map_p)
        Compute a zero-charge feature map from a set of charged features
        
        Find putative ChargePairs, then score them and hand over to ILP
        
        
        :param fm_in: Input feature-map
        :param fm_out: Output feature-map (sorted by position and augmented with user params)
        :param cons_map: Output of grouped features belonging to a charge group
        :param cons_map_p: Output of paired features connected by an edge
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
    CHARGEMODE_MFD : __CHARGEMODE_MFD 


class ModificationDefinitionsSet:
    """
    Cython implementation of _ModificationDefinitionsSet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationDefinitionsSet.html>`_

    Representation of a set of modification definitions
    
    This class enhances the modification definitions as defined in the
    class ModificationDefinition into a set of definitions. This is also
    e.g. used as input parameters in search engines.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(ModificationDefinitionsSet &)
        """
        ...
    
    @overload
    def __init__(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(StringList fixed_modifications, StringList variable_modifications)
        """
        ...
    
    def setMaxModifications(self, max_mod: int ) -> None:
        """
        Cython signature: void setMaxModifications(size_t max_mod)
        Sets the maximal number of modifications allowed per peptide
        """
        ...
    
    def getMaxModifications(self) -> int:
        """
        Cython signature: size_t getMaxModifications()
        Return the maximal number of modifications allowed per peptide
        """
        ...
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        Returns the number of modifications stored in this set
        """
        ...
    
    def getNumberOfFixedModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfFixedModifications()
        Returns the number of fixed modifications stored in this set
        """
        ...
    
    def getNumberOfVariableModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfVariableModifications()
        Returns the number of variable modifications stored in this set
        """
        ...
    
    def addModification(self, mod_def: ModificationDefinition ) -> None:
        """
        Cython signature: void addModification(ModificationDefinition & mod_def)
        Adds a modification definition to the set
        """
        ...
    
    @overload
    def setModifications(self, mod_defs: Set[ModificationDefinition] ) -> None:
        """
        Cython signature: void setModifications(libcpp_set[ModificationDefinition] & mod_defs)
        Sets the modification definitions
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: Union[bytes, str, String] , variable_modifications: String ) -> None:
        """
        Cython signature: void setModifications(const String & fixed_modifications, String & variable_modifications)
        Set the modification definitions from a string
        
        The strings should contain a comma separated list of modifications. The names
        can be PSI-MOD identifier or any other unique name supported by PSI-MOD. TermSpec
        definitions and other specific definitions are given by the modifications themselves.
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void setModifications(StringList & fixed_modifications, StringList & variable_modifications)
        Same as above, but using StringList instead of comma separated strings
        """
        ...
    
    def getModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getModifications()
        Returns the stored modification definitions
        """
        ...
    
    def getFixedModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getFixedModifications()
        Returns the stored fixed modification definitions
        """
        ...
    
    def getVariableModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getVariableModifications()
        Returns the stored variable modification definitions
        """
        ...
    
    @overload
    def getModificationNames(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void getModificationNames(StringList & fixed_modifications, StringList & variable_modifications)
        Populates the output lists with the modification names (use e.g. for
        """
        ...
    
    @overload
    def getModificationNames(self, ) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getModificationNames()
        Returns only the names of the modifications stored in the set
        """
        ...
    
    def getFixedModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getFixedModificationNames()
        Returns only the names of the fixed modifications
        """
        ...
    
    def getVariableModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getVariableModificationNames()
        Returns only the names of the variable modifications
        """
        ...
    
    def isCompatible(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool isCompatible(AASequence & peptide)
        Returns true if the peptide is compatible with the definitions, e.g. does not contain other modifications
        """
        ...
    
    def inferFromPeptides(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void inferFromPeptides(libcpp_vector[PeptideIdentification] & peptides)
        Infers the sets of defined modifications from the modifications present on peptide identifications
        """
        ... 


class MorpheusScore:
    """
    Cython implementation of _MorpheusScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore ) -> None:
        """
        Cython signature: void MorpheusScore(MorpheusScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> MorpheusScore_Result:
        """
        Cython signature: MorpheusScore_Result compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, const MSSpectrum & exp_spectrum, const MSSpectrum & theo_spectrum)
        Returns Morpheus Score
        """
        ... 


class MorpheusScore_Result:
    """
    Cython implementation of _MorpheusScore_Result

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore_Result.html>`_
    """
    
    matches: int
    
    n_peaks: int
    
    score: float
    
    MIC: float
    
    TIC: float
    
    err: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore_Result()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore_Result ) -> None:
        """
        Cython signature: void MorpheusScore_Result(MorpheusScore_Result &)
        """
        ... 


class MultiplexDeltaMassesGenerator:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: MultiplexDeltaMassesGenerator ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(MultiplexDeltaMassesGenerator &)
        """
        ...
    
    @overload
    def __init__(self, labels: Union[bytes, str, String] , missed_cleavages: int , label_mass_shift: Dict[Union[bytes, str, String], float] ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(String labels, int missed_cleavages, libcpp_map[String,double] label_mass_shift)
        """
        ...
    
    def generateKnockoutDeltaMasses(self) -> None:
        """
        Cython signature: void generateKnockoutDeltaMasses()
        """
        ...
    
    def getDeltaMassesList(self) -> List[MultiplexDeltaMasses]:
        """
        Cython signature: libcpp_vector[MultiplexDeltaMasses] getDeltaMassesList()
        """
        ...
    
    def getLabelShort(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelShort(String label)
        """
        ...
    
    def getLabelLong(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelLong(String label)
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


class MultiplexDeltaMassesGenerator_Label:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator_Label

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator_Label.html>`_
    """
    
    short_name: Union[bytes, str, String]
    
    long_name: Union[bytes, str, String]
    
    description: Union[bytes, str, String]
    
    delta_mass: float
    
    def __init__(self, sn: Union[bytes, str, String] , ln: Union[bytes, str, String] , d: Union[bytes, str, String] , dm: float ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator_Label(String sn, String ln, String d, double dm)
        """
        ... 


class MzTabFile:
    """
    Cython implementation of _MzTabFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabFile ) -> None:
        """
        Cython signature: void MzTabFile(MzTabFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void store(String filename, MzTab & mz_tab)
        Stores MzTab file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void load(String filename, MzTab & mz_tab)
        Loads MzTab file
        """
        ... 


class PScore:
    """
    Cython implementation of _PScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: PScore ) -> None:
        """
        Cython signature: void PScore(PScore &)
        """
        ...
    
    def calculateIntensityRankInMZWindow(self, mz: List[float] , intensities: List[float] , mz_window: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] calculateIntensityRankInMZWindow(libcpp_vector[double] & mz, libcpp_vector[double] & intensities, double mz_window)
        Calculate local (windowed) peak ranks
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        The result can be used to efficiently filter spectra for top 1..n peaks in mass windows
        
        
        :param mz: The m/z positions of the peaks
        :param intensities: The intensities of the peaks
        :param mz_window: The window in Thomson centered at each peak
        """
        ...
    
    def calculateRankMap(self, peak_map: MSExperiment , mz_window: float ) -> List[List[int]]:
        """
        Cython signature: libcpp_vector[libcpp_vector[size_t]] calculateRankMap(MSExperiment & peak_map, double mz_window)
        Precalculated, windowed peak ranks for a whole experiment
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        
        
        :param peak_map: Fragment spectra used for rank calculation. Typically a peak map after removal of all MS1 spectra
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    def calculatePeakLevelSpectra(self, spec: MSSpectrum , ranks: List[int] , min_level: int , max_level: int ) -> Dict[int, MSSpectrum]:
        """
        Cython signature: libcpp_map[size_t,MSSpectrum] calculatePeakLevelSpectra(MSSpectrum & spec, libcpp_vector[size_t] & ranks, size_t min_level, size_t max_level)
        Calculates spectra for peak level between min_level to max_level and stores them in the map
        
        A spectrum of peak level n retains the (n+1) top intensity peaks in a sliding mz_window centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectra: List[MSSpectrum] , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, libcpp_vector[MSSpectrum] & theo_spectra, double mz_window)
        Computes the PScore for a vector of theoretical spectra
        
        Similar to Andromeda, a vector of theoretical spectra can be provided that e.g. contain loss spectra or higher charge spectra depending on the sequence.
        The best score obtained by scoring all those theoretical spectra against the experimental ones is returned
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank).
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectrum: MSSpectrum , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, MSSpectrum & theo_spectrum, double mz_window)
        Computes the PScore for a single theoretical spectrum
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank)
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ... 


class ParamValue:
    """
    Cython implementation of _ParamValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParamValue.html>`_

    Class to hold strings, numeric values, vectors of strings and vectors of numeric values using the stl types
    
    - To choose one of these types, just use the appropriate constructor
    - Automatic conversion is supported and throws Exceptions in case of invalid conversions
    - An empty object is created with the default constructor
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamValue ) -> None:
        """
        Cython signature: void ParamValue(ParamValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void ParamValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str] ) -> None:
        """
        Cython signature: void ParamValue(const libcpp_utf8_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void ParamValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void ParamValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[libcpp_utf8_string])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[int])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[double])
        """
        ...
    
    def toStringVector(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] toStringVector()
        Explicitly convert ParamValue to string vector
        """
        ...
    
    def toDoubleVector(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleVector()
        Explicitly convert ParamValue to DoubleList
        """
        ...
    
    def toIntVector(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntVector()
        Explicitly convert ParamValue to IntList
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        Converts the strings 'true' and 'false' to a bool
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: ValueType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        Test if the value is empty
        """
        ... 


class PeakIndex:
    """
    Cython implementation of _PeakIndex

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakIndex.html>`_

    Index of a peak or feature
    
    This struct can be used to store both peak or feature indices
    """
    
    peak: int
    
    spectrum: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakIndex()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakIndex ) -> None:
        """
        Cython signature: void PeakIndex(PeakIndex &)
        """
        ...
    
    @overload
    def __init__(self, peak: int ) -> None:
        """
        Cython signature: void PeakIndex(size_t peak)
        """
        ...
    
    @overload
    def __init__(self, spectrum: int , peak: int ) -> None:
        """
        Cython signature: void PeakIndex(size_t spectrum, size_t peak)
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        Returns if the current peak ref is valid
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Invalidates the current index
        """
        ...
    
    def getFeature(self, map_: FeatureMap ) -> Feature:
        """
        Cython signature: Feature getFeature(FeatureMap & map_)
        Returns the feature (or consensus feature) corresponding to this index
        
        This method is intended for arrays of features e.g. FeatureMap
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def getPeak(self, map_: MSExperiment ) -> Peak1D:
        """
        Cython signature: Peak1D getPeak(MSExperiment & map_)
        Returns a peak corresponding to this index
        
        This method is intended for arrays of DSpectra e.g. MSExperiment
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def getSpectrum(self, map_: MSExperiment ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getSpectrum(MSExperiment & map_)
        Returns a spectrum corresponding to this index
        
        This method is intended for arrays of DSpectra e.g. MSExperiment
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def __richcmp__(self, other: PeakIndex, op: int) -> Any:
        ... 


class PepXMLFileMascot:
    """
    Cython implementation of _PepXMLFileMascot

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PepXMLFileMascot.html>`_

    Used to load Mascot PepXML files
    
    A schema for this format can be found at http://www.matrixscience.com/xmlns/schema/pepXML_v18/pepXML_v18.xsd
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void PepXMLFileMascot()
        """
        ... 


class Product:
    """
    Cython implementation of _Product

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Product.html>`_

    This class describes the product isolation window for special scan types, such as MRM
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Product()
        """
        ...
    
    @overload
    def __init__(self, in_0: Product ) -> None:
        """
        Cython signature: void Product(Product &)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the target m/z
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Sets the target m/z
        """
        ...
    
    def getIsolationWindowLowerOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowLowerOffset()
        Returns the lower offset from the target m/z
        """
        ...
    
    def setIsolationWindowLowerOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowLowerOffset(double bound)
        Sets the lower offset from the target m/z
        """
        ...
    
    def getIsolationWindowUpperOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowUpperOffset()
        Returns the upper offset from the target m/z
        """
        ...
    
    def setIsolationWindowUpperOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowUpperOffset(double bound)
        Sets the upper offset from the target m/z
        """
        ...
    
    def __richcmp__(self, other: Product, op: int) -> Any:
        ... 


class ProteinInference:
    """
    Cython implementation of _ProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinInference.html>`_

    [experimental class] given a peptide quantitation, infer corresponding protein quantities
    
    Infers protein ratios from peptide ratios (currently using unique peptides only).
    Use the IDMapper class to add protein and peptide information to a
    quantitative ConsensusMap prior to this step
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinInference ) -> None:
        """
        Cython signature: void ProteinInference(ProteinInference &)
        """
        ...
    
    def infer(self, consensus_map: ConsensusMap , reference_map: int ) -> None:
        """
        Cython signature: void infer(ConsensusMap & consensus_map, unsigned int reference_map)
        Given a peptide quantitation, infer corresponding protein quantities
        
        Infers protein ratios from peptide ratios (currently using unique peptides only).
        Use the IDMapper class to add protein and peptide information to a
        quantitative ConsensusMap prior to this step
        
        
        :param consensus_map: Peptide quantitation with ProteinIdentifications attached, where protein quantitation will be attached
        :param reference_map: Index of (iTRAQ) reference channel within the consensus map
        """
        ... 


class ProteinProteinCrossLink:
    """
    Cython implementation of _ProteinProteinCrossLink

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1ProteinProteinCrossLink.html>`_
    """
    
    alpha: AASequence
    
    beta: AASequence
    
    cross_link_position: List[int, int]
    
    cross_linker_mass: float
    
    cross_linker_name: Union[bytes, str, String]
    
    term_spec_alpha: int
    
    term_spec_beta: int
    
    precursor_correction: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinProteinCrossLink()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinProteinCrossLink ) -> None:
        """
        Cython signature: void ProteinProteinCrossLink(ProteinProteinCrossLink &)
        """
        ...
    
    def getType(self) -> int:
        """
        Cython signature: ProteinProteinCrossLinkType getType()
        """
        ...
    
    def __richcmp__(self, other: ProteinProteinCrossLink, op: int) -> Any:
        ... 


class RankScaler:
    """
    Cython implementation of _RankScaler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RankScaler.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void RankScaler()
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
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


class RipFileContent:
    """
    Cython implementation of _RipFileContent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileContent.html>`_
    """
    
    def __init__(self, prot_idents: List[ProteinIdentification] , pep_idents: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void RipFileContent(libcpp_vector[ProteinIdentification] & prot_idents, libcpp_vector[PeptideIdentification] & pep_idents)
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        """
        ... 


class RipFileIdentifier:
    """
    Cython implementation of _RipFileIdentifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileIdentifier.html>`_
    """
    
    def __init__(self, id_runs: IdentificationRuns , pep_id: PeptideIdentification , file_origin_map: Dict[Union[bytes, str, String], int] , origin_annotation_fmt: int , split_ident_runs: bool ) -> None:
        """
        Cython signature: void RipFileIdentifier(IdentificationRuns & id_runs, PeptideIdentification & pep_id, libcpp_map[String,unsigned int] & file_origin_map, OriginAnnotationFormat origin_annotation_fmt, bool split_ident_runs)
        """
        ...
    
    def getIdentRunIdx(self) -> int:
        """
        Cython signature: unsigned int getIdentRunIdx()
        """
        ...
    
    def getFileOriginIdx(self) -> int:
        """
        Cython signature: unsigned int getFileOriginIdx()
        """
        ...
    
    def getOriginFullname(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOriginFullname()
        """
        ...
    
    def getOutputBasename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputBasename()
        """
        ... 


class SignalToNoiseEstimatorMedian:
    """
    Cython implementation of _SignalToNoiseEstimatorMedian[_MSSpectrum]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMedian[_MSSpectrum].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedian()
        """
        ...
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMedian ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedian(SignalToNoiseEstimatorMedian &)
        """
        ...
    
    def init(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void init(MSSpectrum & spectrum)
        """
        ...
    
    def getSignalToNoise(self, index: int ) -> float:
        """
        Cython signature: double getSignalToNoise(size_t index)
        """
        ...
    
    def getSparseWindowPercent(self) -> float:
        """
        Cython signature: double getSparseWindowPercent()
        """
        ...
    
    def getHistogramRightmostPercent(self) -> float:
        """
        Cython signature: double getHistogramRightmostPercent()
        """
        ...
    IntensityThresholdCalculation : __IntensityThresholdCalculation 


class SimpleSearchEngineAlgorithm:
    """
    Cython implementation of _SimpleSearchEngineAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleSearchEngineAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleSearchEngineAlgorithm ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm(SimpleSearchEngineAlgorithm &)
        """
        ...
    
    def search(self, in_mzML: Union[bytes, str, String] , in_db: Union[bytes, str, String] , prot_ids: List[ProteinIdentification] , pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void search(const String & in_mzML, const String & in_db, libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & pep_ids)
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


class SiriusMSFile:
    """
    Cython implementation of _SiriusMSFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile ) -> None:
        """
        Cython signature: void SiriusMSFile(SiriusMSFile &)
        """
        ... 


class SiriusMSFile_AccessionInfo:
    """
    Cython implementation of _SiriusMSFile_AccessionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_AccessionInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_AccessionInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo(SiriusMSFile_AccessionInfo &)
        """
        ... 


class SiriusMSFile_CompoundInfo:
    """
    Cython implementation of _SiriusMSFile_CompoundInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_CompoundInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_CompoundInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo(SiriusMSFile_CompoundInfo &)
        """
        ... 


class SpectrumMetaData:
    """
    Cython implementation of _SpectrumMetaData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumMetaData.html>`_
    """
    
    rt: float
    
    precursor_rt: float
    
    precursor_mz: float
    
    precursor_charge: int
    
    ms_level: int
    
    scan_number: int
    
    native_id: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumMetaData()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumMetaData ) -> None:
        """
        Cython signature: void SpectrumMetaData(SpectrumMetaData &)
        """
        ... 


class SpectrumMetaDataLookup:
    """
    Cython implementation of _SpectrumMetaDataLookup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumMetaDataLookup.html>`_
      -- Inherits from ['SpectrumLookup']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void SpectrumMetaDataLookup()
        """
        ...
    
    @overload
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] , get_precursor_rt: bool ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp, bool get_precursor_rt)
        Read spectra and store their meta data
        
        :param SpectrumContainer: Spectrum container class, must support `size` and `operator[]`
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>")
        :param get_precursor_rt: Assign precursor retention times? (This relies on all precursor spectra being present and in the right order.)
        """
        ...
    
    @overload
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp)
        Read and index spectra for later look-up
        
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>". For example, "scan=(?<SCAN>\\d+)").
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, index: int , meta: SpectrumMetaData ) -> None:
        """
        Cython signature: void getSpectrumMetaData(size_t index, SpectrumMetaData & meta)
        Look up meta data of a spectrum
        
        :param index: Index of the spectrum
        :param meta: Meta data output
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, spectrum_ref: Union[bytes, str, String] , meta: SpectrumMetaData ) -> None:
        """
        Cython signature: void getSpectrumMetaData(String spectrum_ref, SpectrumMetaData & meta)
        Extract meta data from a spectrum
        
        :param spectrum: Spectrum input
        :param meta: Meta data output
        :param scan_regexp: Regular expression for extracting scan number from spectrum native ID
        :param precursor_rts: RTs of potential precursor spectra of different MS levels
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, spectrum_ref: Union[bytes, str, String] , meta: SpectrumMetaData , flags: bytes ) -> None:
        """
        Cython signature: void getSpectrumMetaData(String spectrum_ref, SpectrumMetaData & meta, unsigned char flags)
        Extract meta data via a spectrum reference
        
        :param spectrum_ref: Spectrum reference to parse
        :param metadata: Meta data output
        :param flags: What meta data to extract
        """
        ...
    
    def setSpectraDataRef(self, spectra_data: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSpectraDataRef(const String & spectra_data)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if any spectra were set
        """
        ...
    
    def findByRT(self, rt: float ) -> int:
        """
        Cython signature: size_t findByRT(double rt)
        Look up spectrum by retention time (RT)
        
        :param rt: Retention time to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByNativeID(self, native_id: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByNativeID(String native_id)
        Look up spectrum by native ID
        
        :param native_id: Native ID to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByIndex(self, index: int , count_from_one: bool ) -> int:
        """
        Cython signature: size_t findByIndex(size_t index, bool count_from_one)
        Look up spectrum by index (position in the vector of spectra)
        
        :param index: Index to look up
        :param count_from_one: Do indexes start counting at one (default zero)?
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByScanNumber(self, scan_number: int ) -> int:
        """
        Cython signature: size_t findByScanNumber(size_t scan_number)
        Look up spectrum by scan number (extracted from the native ID)
        
        :param scan_number: Scan number to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByReference(self, spectrum_ref: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByReference(String spectrum_ref)
        Look up spectrum by reference
        
        :param spectrum_ref: Spectrum reference to parse
        :returns: Index of the spectrum that matched
        """
        ...
    
    def addReferenceFormat(self, regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addReferenceFormat(String regexp)
        Register a possible format for a spectrum reference
        
        :param regexp: Regular expression defining the format
        """
        ...
    
    def extractScanNumber(self, native_id: Union[bytes, str, String] , native_id_type_accession: Union[bytes, str, String] ) -> int:
        """
        Cython signature: int extractScanNumber(const String & native_id, const String & native_id_type_accession)
        """
        ...
    
    addMissingRTsToPeptideIDs: __static_SpectrumMetaDataLookup_addMissingRTsToPeptideIDs
    
    addMissingSpectrumReferences: __static_SpectrumMetaDataLookup_addMissingSpectrumReferences
    
    getSpectrumMetaData: __static_SpectrumMetaDataLookup_getSpectrumMetaData 


class SwathMap:
    """
    Cython implementation of _SwathMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1SwathMap.html>`_
    """
    
    lower: float
    
    upper: float
    
    center: float
    
    ms1: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SwathMap()
        Data structure to hold one SWATH map with information about upper / lower isolation window and whether the map is MS1 or MS2
        """
        ...
    
    @overload
    def __init__(self, in_0: SwathMap ) -> None:
        """
        Cython signature: void SwathMap(SwathMap &)
        """
        ...
    
    @overload
    def __init__(self, mz_start: float , mz_end: float , mz_center: float , is_ms1: bool ) -> None:
        """
        Cython signature: void SwathMap(double mz_start, double mz_end, double mz_center, bool is_ms1)
        """
        ... 


class TMTEighteenPlexQuantitationMethod:
    """
    Cython implementation of _TMTEighteenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTEighteenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTEighteenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod(TMTEighteenPlexQuantitationMethod &)
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


class TMTElevenPlexQuantitationMethod:
    """
    Cython implementation of _TMTElevenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTElevenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTElevenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTElevenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTElevenPlexQuantitationMethod(TMTElevenPlexQuantitationMethod &)
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


class TMTSixteenPlexQuantitationMethod:
    """
    Cython implementation of _TMTSixteenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTSixteenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTSixteenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTSixteenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTSixteenPlexQuantitationMethod(TMTSixteenPlexQuantitationMethod &)
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


class TM_DataPoint:
    """
    Cython implementation of _TM_DataPoint

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TM_DataPoint.html>`_
    """
    
    first: float
    
    second: float
    
    note: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TM_DataPoint()
        """
        ...
    
    @overload
    def __init__(self, in_0: float , in_1: float ) -> None:
        """
        Cython signature: void TM_DataPoint(double, double)
        """
        ...
    
    @overload
    def __init__(self, in_0: float , in_1: float , in_2: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void TM_DataPoint(double, double, const String &)
        """
        ...
    
    def __richcmp__(self, other: TM_DataPoint, op: int) -> Any:
        ... 


class Unit:
    """
    Cython implementation of _Unit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Unit.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    cv_ref: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Unit()
        """
        ...
    
    @overload
    def __init__(self, in_0: Unit ) -> None:
        """
        Cython signature: void Unit(Unit)
        """
        ...
    
    @overload
    def __init__(self, p_accession: Union[bytes, str, String] , p_name: Union[bytes, str, String] , p_cv_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void Unit(const String & p_accession, const String & p_name, const String & p_cv_ref)
        """
        ...
    
    def __richcmp__(self, other: Unit, op: int) -> Any:
        ... 


class WindowMower:
    """
    Cython implementation of _WindowMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1WindowMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void WindowMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: WindowMower ) -> None:
        """
        Cython signature: void WindowMower(WindowMower &)
        """
        ...
    
    def filterPeakSpectrumForTopNInSlidingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInSlidingWindow(MSSpectrum & spectrum)
        Sliding window version (slower)
        """
        ...
    
    def filterPeakSpectrumForTopNInJumpingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInJumpingWindow(MSSpectrum & spectrum)
        Jumping window version (faster)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
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


class XTandemInfile:
    """
    Cython implementation of _XTandemInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XTandemInfile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void XTandemInfile()
        """
        ...
    
    def setFragmentMassTolerance(self, tolerance: float ) -> None:
        """
        Cython signature: void setFragmentMassTolerance(double tolerance)
        """
        ...
    
    def getFragmentMassTolerance(self) -> float:
        """
        Cython signature: double getFragmentMassTolerance()
        """
        ...
    
    def setPrecursorMassTolerancePlus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerancePlus(double tol)
        """
        ...
    
    def getPrecursorMassTolerancePlus(self) -> float:
        """
        Cython signature: double getPrecursorMassTolerancePlus()
        """
        ...
    
    def setPrecursorMassToleranceMinus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassToleranceMinus(double tol)
        """
        ...
    
    def getPrecursorMassToleranceMinus(self) -> float:
        """
        Cython signature: double getPrecursorMassToleranceMinus()
        """
        ...
    
    def setPrecursorErrorType(self, mono_isotopic: int ) -> None:
        """
        Cython signature: void setPrecursorErrorType(MassType mono_isotopic)
        """
        ...
    
    def getPrecursorErrorType(self) -> int:
        """
        Cython signature: MassType getPrecursorErrorType()
        """
        ...
    
    def setFragmentMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setFragmentMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getFragmentMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getFragmentMassErrorUnit()
        """
        ...
    
    def setPrecursorMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setPrecursorMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getPrecursorMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getPrecursorMassErrorUnit()
        """
        ...
    
    def setNumberOfThreads(self, threads: int ) -> None:
        """
        Cython signature: void setNumberOfThreads(unsigned int threads)
        """
        ...
    
    def getNumberOfThreads(self) -> int:
        """
        Cython signature: unsigned int getNumberOfThreads()
        """
        ...
    
    def setModifications(self, mods: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModifications(ModificationDefinitionsSet & mods)
        """
        ...
    
    def getModifications(self) -> ModificationDefinitionsSet:
        """
        Cython signature: ModificationDefinitionsSet getModifications()
        """
        ...
    
    def setOutputFilename(self, output: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputFilename(const String & output)
        """
        ...
    
    def getOutputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputFilename()
        """
        ...
    
    def setInputFilename(self, input_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInputFilename(const String & input_file)
        """
        ...
    
    def getInputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInputFilename()
        """
        ...
    
    def setTaxonomyFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomyFilename(const String & filename)
        """
        ...
    
    def getTaxonomyFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomyFilename()
        """
        ...
    
    def setDefaultParametersFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDefaultParametersFilename(const String & filename)
        """
        ...
    
    def getDefaultParametersFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDefaultParametersFilename()
        """
        ...
    
    def setTaxon(self, taxon: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxon(const String & taxon)
        """
        ...
    
    def getTaxon(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxon()
        """
        ...
    
    def setMaxPrecursorCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxPrecursorCharge(int max_charge)
        """
        ...
    
    def getMaxPrecursorCharge(self) -> int:
        """
        Cython signature: int getMaxPrecursorCharge()
        """
        ...
    
    def setNumberOfMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setNumberOfMissedCleavages(unsigned int missed_cleavages)
        """
        ...
    
    def getNumberOfMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getNumberOfMissedCleavages()
        """
        ...
    
    def setOutputResults(self, result: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputResults(String result)
        """
        ...
    
    def getOutputResults(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputResults()
        """
        ...
    
    def setMaxValidEValue(self, value: float ) -> None:
        """
        Cython signature: void setMaxValidEValue(double value)
        """
        ...
    
    def getMaxValidEValue(self) -> float:
        """
        Cython signature: double getMaxValidEValue()
        """
        ...
    
    def setSemiCleavage(self, semi_cleavage: bool ) -> None:
        """
        Cython signature: void setSemiCleavage(bool semi_cleavage)
        """
        ...
    
    def setAllowIsotopeError(self, allow_isotope_error: bool ) -> None:
        """
        Cython signature: void setAllowIsotopeError(bool allow_isotope_error)
        """
        ...
    
    def write(self, filename: Union[bytes, str, String] , ignore_member_parameters: bool , force_default_mods: bool ) -> None:
        """
        Cython signature: void write(String filename, bool ignore_member_parameters, bool force_default_mods)
        """
        ...
    
    def setCleavageSite(self, cleavage_site: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavageSite(String cleavage_site)
        """
        ...
    
    def getCleavageSite(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavageSite()
        """
        ...
    ErrorUnit : __ErrorUnit
    MassType : __MassType 


class __CHARGEMODE_FD:
    None
    QFROMFEATURE : int
    QHEURISTIC : int
    QALL : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __CHARGEMODE_MFD:
    None
    QFROMFEATURE : int
    QHEURISTIC : int
    QALL : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __CombinationsLogic:
    None
    OR : int
    AND : int
    XOR : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ErrorUnit:
    None
    DALTONS : int
    PPM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __InletType:
    None
    INLETNULL : int
    DIRECT : int
    BATCH : int
    CHROMATOGRAPHY : int
    PARTICLEBEAM : int
    MEMBRANESEPARATOR : int
    OPENSPLIT : int
    JETSEPARATOR : int
    SEPTUM : int
    RESERVOIR : int
    MOVINGBELT : int
    MOVINGWIRE : int
    FLOWINJECTIONANALYSIS : int
    ELECTROSPRAYINLET : int
    THERMOSPRAYINLET : int
    INFUSION : int
    CONTINUOUSFLOWFASTATOMBOMBARDMENT : int
    INDUCTIVELYCOUPLEDPLASMA : int
    MEMBRANE : int
    NANOSPRAY : int
    SIZE_OF_INLETTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IntensityThresholdCalculation:
    None
    MANUAL : int
    AUTOMAXBYSTDEV : int
    AUTOMAXBYPERCENT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IonizationMethod:
    None
    IONMETHODNULL : int
    ESI : int
    EI : int
    CI : int
    FAB : int
    TSP : int
    LD : int
    FD : int
    FI : int
    PD : int
    SI : int
    TI : int
    API : int
    ISI : int
    CID : int
    CAD : int
    HN : int
    APCI : int
    APPI : int
    ICP : int
    NESI : int
    MESI : int
    SELDI : int
    SEND : int
    FIB : int
    MALDI : int
    MPI : int
    DI : int
    FA : int
    FII : int
    GD_MS : int
    NICI : int
    NRMS : int
    PI : int
    PYMS : int
    REMPI : int
    AI : int
    ASI : int
    AD : int
    AUI : int
    CEI : int
    CHEMI : int
    DISSI : int
    LSI : int
    PEI : int
    SOI : int
    SPI : int
    SUI : int
    VI : int
    AP_MALDI : int
    SILI : int
    SALDI : int
    SIZE_OF_IONIZATIONMETHOD : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __MassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class OriginAnnotationFormat:
    None
    FILE_ORIGIN : int
    MAP_INDEX : int
    ID_MERGE_INDEX : int
    UNKNOWN_OAF : int
    SIZE_OF_ORIGIN_ANNOTATION_FORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Polarity:
    None
    POLNULL : int
    POSITIVE : int
    NEGATIVE : int
    SIZE_OF_POLARITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __RequirementLevel:
    None
    MUST : int
    SHOULD : int
    MAY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ValueType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

