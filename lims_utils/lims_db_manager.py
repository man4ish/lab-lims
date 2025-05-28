"""
Module: lims_db_manager.py

This module provides functionality for managing interactions with the LIMS (Laboratory Information Management System) database.  
It defines classes and methods to query and manipulate various entities such as:

- SequenceType
- ReferenceGenome
- AnalysisType
- DownstreamAnalysis
- CoordinateSet
- and more.

Note:
    This module is part of the `lims_utils` package.
"""


from typing import List
from sqlalchemy.orm.exc import NoResultFound
from .lims_data_model import (
    Sample,
    SequenceType,
    ReferenceGenome,
    CoordinateSet,
    AnalysisType,
    AnalysisOutput,
    AnalysisOutputType,
    AnalysisFileType,
    DownstreamAnalysisFile,
    DownstreamAnalysis,
    DownstreamAnalysisType
)
from .lims_connector_manager import LimsConnector

class DatabaseManager:
    """
    This class manages database operations for the LIMS system.
    """

    def __init__(self):
        lc = LimsConnector()
        self.engine = lc.initiate_db()
        self.session = lc.get_session()

    def query_all_samples(self, tolerant=False) -> List[Sample]:
        """
        Query all samples.

        Parameters:
            tolerant (bool): If True, returns an empty list if no samples are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[Sample]: List of Sample objects.
        """
        with self.session as session:
            samples = session.query(Sample).all()
            if samples:
                return samples
            if tolerant:
                return []
            raise NoResultFound()

    def query_sample_by_id(self, sample_id: int) -> Sample:
        """
        Query a sample by ID.

        Parameters:
            sample_id (int): ID of the sample.

        Returns:
            Sample: The sample with the specified ID.
        """
        with self.session as session:
            sample = session.query(Sample).filter(Sample.id == sample_id).first()
            if sample:
                return sample
            raise NoResultFound()

    def query_all_sequence_types(self, tolerant=False) -> List[SequenceType]:
        """
        Query all sequence types.

        Parameters:
            tolerant (bool): If True, returns an empty list if no sequence types are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[SequenceType]: List of SequenceType objects.
        """
        with self.session as session:
            sequence_types = session.query(SequenceType).all()
            if sequence_types:
                return sequence_types
            if tolerant:
                return []
            raise NoResultFound()

    def query_sequence_type_by_id(self, sequence_type_id: int) -> SequenceType:
        """
        Query a sequence type by ID.

        Parameters:
            sequence_type_id (int): ID of the sequence type.

        Returns:
            SequenceType: The sequence type with the specified ID.
        """
        with self.session as session:
            sequence_type = (
                session.query(SequenceType)
                .filter(SequenceType.id == sequence_type_id)
                .first()
            )
            if sequence_type:
                return sequence_type
            raise NoResultFound()

    def query_all_reference_genomes(self, tolerant=False) -> List[ReferenceGenome]:
        """
        Query all reference genomes.

        Parameters:
            tolerant (bool): If True, returns an empty list if no reference genomes are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[ReferenceGenome]: List of ReferenceGenome objects.
        """
        with self.session as session:
            reference_genomes = session.query(ReferenceGenome).all()
            if reference_genomes:
                return reference_genomes
            if tolerant:
                return []
            raise NoResultFound()

    def query_reference_genome_by_id(self, reference_genome_id: int) -> ReferenceGenome:
        """
        Query a reference genome by ID.

        Parameters:
            reference_genome_id (int): ID of the reference genome.

        Returns:
            ReferenceGenome: The reference genome with the specified ID.
        """
        with self.session as session:
            reference_genome = (
                session.query(ReferenceGenome)
                .filter(ReferenceGenome.id == reference_genome_id)
                .first()
            )
            if reference_genome:
                return reference_genome
            raise NoResultFound()

    def query_all_analysis_types(self, tolerant=False) -> List[AnalysisType]:
        """
        Query all analysis types.

        Parameters:
            tolerant (bool): If True, returns an empty list if no analysis types are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[AnalysisType]: List of AnalysisType objects.
        """
        with self.session as session:
            analysis_types = session.query(AnalysisType).all()
            if analysis_types:
                return analysis_types
            if tolerant:
                return []
            raise NoResultFound()

    def query_analysis_type_by_id(self, analysis_type_id: int) -> AnalysisType:
        """
        Query an analysis type by ID.

        Parameters:
            analysis_type_id (int): ID of the analysis type.

        Returns:
            AnalysisType: The analysis type with the specified ID.
        """
        with self.session as session:
            analysis_type = (
                session.query(AnalysisType)
                .filter(AnalysisType.id == analysis_type_id)
                .first()
            )
            if analysis_type:
                return analysis_type
            raise NoResultFound()

    def query_all_analysis_output_types(self, tolerant=False) -> List[AnalysisOutputType]:
        """
        Query all analysis output types.

        Parameters:
            tolerant (bool): If True, returns an empty list if no analysis output types are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[AnalysisOutputType]: List of AnalysisOutputType objects.
        """
        with self.session as session:
            analysis_output_types = session.query(AnalysisOutputType).all()
            if analysis_output_types:
                return analysis_output_types
            if tolerant:
                return []
            raise NoResultFound()

    def query_analysis_output_type_by_id(self, analysis_output_type_id: int) -> AnalysisOutputType:
        """
        Query an analysis output type by ID.

        Parameters:
            analysis_output_type_id (int): ID of the analysis output type.

        Returns:
            AnalysisOutputType: The analysis output type with the specified ID.
        """
        with self.session as session:
            analysis_output_type = session.query(AnalysisOutputType).filter(
                AnalysisOutputType.id == analysis_output_type_id).first()
            if analysis_output_type:
                return analysis_output_type
            raise NoResultFound()

    def query_all_analysis_file_types(self, tolerant=False) -> List[AnalysisFileType]:
        """
        Query all analysis file types.

        Parameters:
            tolerant (bool): If True, returns an empty list if no analysis file types are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[AnalysisFileType]: List of AnalysisFileType objects.
        """
        with self.session as session:
            analysis_file_types = session.query(AnalysisFileType).all()
            if analysis_file_types:
                return analysis_file_types
            if tolerant:
                return []
            raise NoResultFound()

    def query_analysis_file_type_by_id(self, analysis_file_type_id: int) -> AnalysisFileType:
        """
        Query an analysis file type by ID.

        Parameters:
            analysis_file_type_id (int): ID of the analysis file type.

        Returns:
            AnalysisFileType: The analysis file type with the specified ID.
        """
        with self.session as session:
            analysis_file_type = session.query(AnalysisFileType).filter(
                AnalysisFileType.id == analysis_file_type_id).first()
            if analysis_file_type:
                return analysis_file_type
            raise NoResultFound()

    def query_all_downstream_analysis_files(self, tolerant=False) -> List[DownstreamAnalysisFile]:
        """
        Query all downstream analysis files.

        Parameters:
            tolerant (bool): If True, returns an empty list if no downstream analysis 
                             files are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[DownstreamAnalysisFile]: List of DownstreamAnalysisFile objects.
        """
        with self.session as session:
            analysis_files = session.query(DownstreamAnalysisFile).all()
            if analysis_files:
                return analysis_files
            if tolerant:
                return []
            raise NoResultFound()

    def query_downstream_analysis_files_by_id(self, file_id: int) -> DownstreamAnalysisFile:
        """
        Query downstream analysis files by ID.

        Parameters:
            file_id (int): ID of the downstream analysis file.

        Returns:
            DownstreamAnalysisFile: The downstream analysis file with the specified ID.
        """
        with self.session as session:
            analysis_files = session.query(DownstreamAnalysisFile).filter(
                DownstreamAnalysisFile.id == file_id).first()
            if analysis_files:
                return analysis_files
            raise NoResultFound()

    def query_downstream_analysis_files_by_path(self, path: str) -> DownstreamAnalysisFile:
        """
        Query downstream analysis files by file path.

        Parameters:
            path (str): File path of the downstream analysis file.

        Returns:
            DownstreamAnalysisFile: The downstream analysis file with the specified file path.
        """
        with self.session as session:
            analysis_files = session.query(DownstreamAnalysisFile).filter(
                DownstreamAnalysisFile.file_path == path).first()
            if analysis_files:
                return analysis_files
            raise NoResultFound()

    def query_all_downstream_analysis(self, tolerant=False) -> List[DownstreamAnalysis]:
        """
        Query all downstream analyses.

        Parameters:
            tolerant (bool): If True, returns an empty list if no downstream analyses are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[DownstreamAnalysis]: List of DownstreamAnalysis objects.
        """
        with self.session as session:
            analyses = session.query(DownstreamAnalysis).all()
            if analyses:
                return analyses
            if tolerant:
                return []
            raise NoResultFound()

    def query_downstream_analysis_by_id(self, analysis_id: int) -> DownstreamAnalysis:
        """
        Query downstream analysis by ID.

        Parameters:
            analysis_id (int): ID of the downstream analysis.

        Returns:
            DownstreamAnalysis: The downstream analysis with the specified ID.
        """
        with self.session as session:
            analyses = session.query(DownstreamAnalysis).filter(
                DownstreamAnalysis.id == analysis_id).first()
            if analyses:
                return analyses
            raise NoResultFound()

    def query_all_coordinate_sets(self, tolerant=False) -> List[CoordinateSet]:
        """
        Query all coordinate sets.

        Parameters:
            tolerant (bool): If True, returns an empty list if no coordinate sets are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[CoordinateSet]: List of CoordinateSet objects.
        """
        with self.session as session:
            coordinate_sets = session.query(CoordinateSet).all()
            if coordinate_sets:
                return coordinate_sets
            if tolerant:
                return []
            raise NoResultFound()

    def query_coordinate_set_by_id(self, coordinate_set_id: int) -> CoordinateSet:
        """
        Query a coordinate set by ID.

        Parameters:
            coordinate_set_id (int): ID of the coordinate set.

        Returns:
            CoordinateSet: The coordinate set with the specified ID.
        """
        with self.session as session:
            coordinate_set = (
                session.query(CoordinateSet)
                .filter(CoordinateSet.id == coordinate_set_id)
                .first()
            )

            if coordinate_set:
                return coordinate_set
            raise NoResultFound()

    def query_all_downstream_analysis_types(self, tolerant=False) -> List[DownstreamAnalysisType]:
        """
        Query all downstream analysis types.

        Parameters:
            tolerant (bool): If True, returns an empty list if no downstream analysis 
                             types are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[DownstreamAnalysisType]: List of DownstreamAnalysisType objects.
        """
        with self.session as session:
            downstream_analysis_types = session.query(DownstreamAnalysisType).all()
            if downstream_analysis_types:
                return downstream_analysis_types
            if tolerant:
                return []
            raise NoResultFound()

    def query_downstream_analysis_type_by_id(
        self,
        downstream_analysis_type_id: int
    ) -> DownstreamAnalysisType:
        """
        Query a downstream analysis type by ID.

        Parameters:
            downstream_analysis_type_id (int): ID of the downstream analysis type.

        Returns:
            DownstreamAnalysisType: The downstream analysis type with the specified ID.
        """
        with self.session as session:
            downstream_analysis_type = session.query(DownstreamAnalysisType).filter(
                DownstreamAnalysisType.id == downstream_analysis_type_id).first()
            if downstream_analysis_type:
                return downstream_analysis_type
            raise NoResultFound()

    def query_all_analysis_outputs(self, tolerant=False) -> List[AnalysisOutput]:
        """
        Query all analysis outputs.

        Parameters:
            tolerant (bool): If True, returns an empty list if no analysis outputs are found.
                             If False, raises NoResultFound exception.

        Returns:
            List[AnalysisOutput]: List of AnalysisOutput objects.
        """
        with self.session as session:
            analysis_outputs = session.query(AnalysisOutput).all()
            if analysis_outputs:
                return analysis_outputs
            if tolerant:
                return []
            raise NoResultFound()

    def query_analysis_output_by_id(self, analysis_output_id: int) -> AnalysisOutput:
        """
        Query an analysis output by ID.

        Parameters:
            analysis_output_id (int): ID of the analysis output.

        Returns:
            AnalysisOutput: The analysis output with the specified ID.
        """
        with self.session as session:
            analysis_output = session.query(AnalysisOutput).filter(
                AnalysisOutput.id == analysis_output_id).first()
            if analysis_output:
                return analysis_output
            raise NoResultFound()