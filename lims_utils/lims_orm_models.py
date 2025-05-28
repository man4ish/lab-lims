"""
Module: lims_orm_models.py

This module defines the `DatabaseManager` class, which provides an interface for interacting 
with a Laboratory Information Management System (LIMS) database using SQLAlchemy ORM.

The class includes methods to query and retrieve various domain-specific entities such as:
- SequenceType
- ReferenceGenome
- AnalysisType
- DownstreamAnalysis
- CoordinateSet
and others relevant to the LIMS data model.

Note:
    This module is part of the `lims_utils` package.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    UniqueConstraint,
    DateTime,
    Date,
    Boolean,
    ForeignKey,
    DECIMAL,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()

class Barcode(Base):
    """
    Represents a barcode entity in the database.

    Attributes:
    - id (int): Primary key for the barcode table.
    """
    __tablename__ = 'core_core_barcodes'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"<Barcode(id={self.id})>"


class Flowcell(Base):
    """
    Represents a flowcell entity in the database.

    Attributes:
    - id (int): Primary key for the flowcells table.
    - label (str): Label of the flowcell.
    - employee_id (int): ID of the employee associated with the flowcell.
    - date_created (Date): Date when the flowcell was created.
    - clustering_station_id (int): ID of the clustering station associated with the flowcell.
    - old_comments (str): Previous comments associated with the flowcell.
    - is_paired_end (bool): Boolean indicating if the flowcell is paired-end.
    - failed (bool): Boolean indicating if the flowcell is marked as failed.
    - barcode_id (int): Foreign key to the 'barcodes' table.
    - active (bool): Boolean indicating if the flowcell is active.
    """
    __tablename__ = 'core_core_flowcells'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    employee_id = Column(Integer)
    date_created = Column(Date)
    clustering_station_id = Column(Integer)
    old_comments = Column(String(2048, collation="utf8_bin"))
    is_paired_end = Column(Boolean)
    failed = Column(Boolean)
    barcode_id = Column(Integer, ForeignKey('barcodes.id'))
    active = Column(Boolean)

    # Define relationships
    runs = relationship('Run', back_populates='flowcell', viewonly=True, lazy='joined')
    lanes = relationship('Lane', back_populates='flowcell', viewonly=True, lazy='joined')
    analyses = relationship('Analyses', back_populates='flowcell', lazy='dynamic')


class Analyses(Base):
    """
    Represents an analysis entity in the database.

    Attributes:
    - id (int): Primary key for the analyses table.
    - analysis_type_id (int): Foreign key to the 'analysis_types' table.
    - flowcell_id (int): Foreign key to the 'flowcells' table.
    - date_performed (Date): Date when the analysis was performed.
    - notes (str): Additional notes associated with the analysis.
    - software_version (str): Version of the software used for the analysis.
    - contaminant_filtered (bool): Boolean indicating if contaminants were filtered 
      during the analysis.
    """
    __tablename__ = 'core_core_analyses'

    id = Column(Integer, primary_key=True)
    analysis_type_id = Column(Integer, ForeignKey('analysis_types.id'))
    flowcell_id = Column(Integer, ForeignKey('flowcells.id'))
    date_performed = Column(Date)
    notes = Column(String(2048, collation="utf8_bin"))
    software_version = Column(String(128, collation="utf8_bin"))
    contaminant_filtered = Column(Boolean)

    # Define relationships
    #analysis_type = relationship('AnalysisTypes')
    flowcell = relationship('Flowcell', back_populates='analyses')


class Run(Base):
    """
    Represents a run entity in the database.

    Attributes:
    - id (int): Primary key for the runs table.
    - label (str): Label of the run.
    - date_started (Date): Date when the run was started.
    - date_completed (Date): Date when the run was completed.
    - cycles (int): Number of cycles for the run.
    - instrument_id (int): Foreign key to the 'instruments' table.
    - flowcell_id (int): Foreign key to the 'flowcells' table.
    - employee_id (int): ID of the employee associated with the run.
    - notes (str): Additional notes associated with the run.
    - cycle1_attachment_id (int): ID of the cycle1 attachment.
    - read2_cycle1_attachment_id (int): ID of the read2 cycle1 attachment.
    """
    __tablename__ = 'core_core_runs'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    date_started = Column(Date)
    date_completed = Column(Date)
    cycles = Column(Integer)
    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    flowcell_id = Column(Integer, ForeignKey('flowcells.id'))
    employee_id = Column(Integer)
    notes = Column(String(2048, collation="utf8_bin"))
    cycle1_attachment_id = Column(Integer)
    read2_cycle1_attachment_id = Column(Integer)

    # Define relationships
    instrument = relationship('Instrument', backref='runs', viewonly=True, lazy='joined')
    flowcell = relationship('Flowcell', back_populates='runs', viewonly=True, lazy='joined')


class Lane(Base):
    """
    Represents a lane entity in the database.

    Attributes:
    - id (int): Primary key for the lanes table.
    - number (int): Lane number.
    - is_control (bool): Boolean indicating if the lane is a control.
    - is_titer (bool): Boolean indicating if the lane is a titer.
    - flowcell_id (int): Foreign key to the 'flowcells' table.
    - pool_id (int): Foreign key to the 'pools' table.
    - failed (bool): Boolean indicating if the lane is marked as failed.
    - sequence_type_id (int): Foreign key to the 'sequence_types' table.
    """
    __tablename__ = 'core_core_lanes'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    is_control = Column(Boolean)
    is_titer = Column(Boolean)
    flowcell_id = Column(Integer, ForeignKey('flowcells.id'))
    pool_id = Column(Integer, ForeignKey('pools.id'))
    failed = Column(Boolean)
    sequence_type_id = Column(Integer, ForeignKey('sequence_types.id'))

    # Define relationships
    flowcell_id = Column(Integer, ForeignKey('flowcells.id'))
    flowcell = relationship('Flowcell', back_populates='lanes', viewonly=True, lazy='joined')
    library_lanes = relationship('LibraryLane', back_populates='lane', viewonly=True, lazy='joined')
    pool = relationship('Pool', backref="lanes", viewonly=True, lazy="joined")


class LibraryLane(Base):
    """
    Represents a library lane entity in the database.

    Attributes:
    - id (int): Primary key for the library_lanes table.
    - lane_id (int): Foreign key to the 'lanes' table.
    - library_id (int): Foreign key to the 'libraries' table.
    - units (str): Units associated with the library lane.
    - concentration (Decimal): Concentration of the library lane.
    """
    __tablename__ = 'core_core_library_lanes'

    id = Column(Integer, primary_key=True)
    lane_id = Column(Integer, ForeignKey('lanes.id'))
    library_id = Column(Integer, ForeignKey('libraries.id'))
    units = Column(String(10, collation="utf8_bin"))
    concentration = Column(DECIMAL(10, 2))

    # Define a foreign key relationship between 'library_lanes' and 'lanes'
    lane = relationship('Lane', back_populates='library_lanes', viewonly=True, lazy='joined')
    library = relationship('Library', back_populates='library_lanes', viewonly=True, lazy='joined')

class Library(Base):
    """
    Represents a library entity in the database.

    Attributes:
    - id (int): Primary key for the libraries table.
    - label (str): Label of the library.
    - library_type_id (int): Foreign key to the 'library_types' table.
    - sample_id (int): Foreign key to the 'samples' table.
    - employee_id (int): ID of the employee associated with the library.
    - protocol_id (int): Foreign key to the 'protocols' table.
    - date_created (Date): Date when the library was created.
    - description (str): Description of the library.
    - insert_size (int): Insert size of the library.
    - client_provided (bool): Boolean indicating if the library was provided by the client.
    - bardex_id (int): Foreign key to the 'bardexes' table.
    - second_bardex_id (int): Second bardex ID.
    - active (bool): Boolean indicating if the library is active.
    """
    __tablename__ = 'core_core_libraries'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    library_type_id = Column(Integer, ForeignKey('library_types.id'))
    sample_id = Column(Integer, ForeignKey('samples.id'))
    employee_id = Column(Integer)
    protocol_id = Column(Integer, ForeignKey('protocols.id'))
    date_created = Column(Date)
    description = Column(String(4096, collation="utf8_bin"))
    insert_size = Column(Integer)
    client_provided = Column(Boolean)
    bardex_id = Column(Integer, ForeignKey('bardexes.id'))
    second_bardex_id = Column(Integer)
    active = Column(Boolean)

    # Foreign Key Constraints
    __table_args__ = (
        ForeignKeyConstraint(['bardex_id'], ['bardexes.id']),
        ForeignKeyConstraint(['second_bardex_id'], ['bardexes.id']),
    )

    # Define Relationships
    sample = relationship('Sample', back_populates='libraries', viewonly=True, lazy='joined')
    index_1 = relationship("Bardex", foreign_keys=[bardex_id], viewonly=True, lazy='joined')
    index_2 = relationship("Bardex", foreign_keys=[second_bardex_id], viewonly=True, lazy='joined')
    library_lanes = relationship(
        'LibraryLane',
        back_populates='library',
        viewonly=True,
        lazy='joined'
    )


class Organism(Base):
    """
    Represents an organism entity in the database.

    Attributes:
    - id (int): Primary key for the organisms table.
    - label (str): Label of the organism.
    """
    __tablename__ = 'core_core_organisms'

    id = Column(Integer, primary_key=True)
    label = Column(String)


class Sample(Base):
    """
    Represents a sample entity in the database.

    Attributes:
    - id (int): Primary key for the samples table.
    - label (str): Label of the sample.
    - organism_id (int): Foreign key to the 'organisms' table.
    - project_id (int): Foreign key to the 'projects' table.
    - description (str): Description of the sample.
    - sample_type_id (int): Foreign key to the 'sample_types' table.
    - specimen_source_id (int): Foreign key to the 'specimen_sources' table.
    """
    __tablename__ = 'core_core_samples'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))

    organism_id = Column(Integer, ForeignKey('organisms.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    description = Column(String(4096, collation="utf8_bin"))
    sample_type_id = Column(Integer, ForeignKey('sample_types.id'))
    specimen_source_id = Column(Integer, ForeignKey('specimen_sources.id'))

    # Define relationships
    project = relationship('Project', backref="samples", viewonly=True, lazy='joined')
    libraries = relationship(
        'Library',
        back_populates='sample',
        viewonly=True,
        lazy='joined'
    )
    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='sample',
        viewonly=True,
        lazy='joined'
    )
    analysis_outputs = relationship(
        'AnalysisOutput',
        back_populates='sample',
        viewonly=True,
        lazy='joined'
    )


class Project(Base):
    """
    Represents a project entity in the database.

    Attributes:
    - id (int): Primary key for the projects table.
    - label (str): Label of the project.
    - gemstone_id (int): Foreign key to the 'gemstones' table.
    - ftp_url (str): FTP URL associated with the project.
    - ftp_user (str): FTP username for the project.
    - website_url (str): Website URL associated with the project.
    - website_user (str): Website username for the project.
    - website_password (str): Website password for the project.
    - old_comments (str): Old comments related to the project.
    - is_current (bool): Boolean indicating if the project is current.
    - active (bool): Boolean indicating if the project is active.
    """
    __tablename__ = 'core_core_projects'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    gemstone_id = Column(Integer, ForeignKey('gemstones.id'))
    ftp_url = Column(String(50, collation="utf8_bin"))
    ftp_user = Column(String(10, collation="utf8_bin"))
    website_url = Column(String(50, collation="utf8_bin"))
    website_user = Column(String(12, collation="utf8_bin"))
    website_password = Column(String(10, collation="utf8_bin"))
    old_comments = Column(String(4096, collation="utf8_bin"))
    is_current = Column(Boolean)
    active = Column(Boolean)

    # Relationship to Gemstone
    gemstone = relationship(
        'Gemstone',
        back_populates='project',
        viewonly=True,
        lazy='joined'
    )


class Gemstone(Base):
    """
    Represents a gemstone entity in the database.

    Attributes:
    - id (int): Primary key for the gemstones table.
    - label (str): Label of the gemstone.
    """
    __tablename__ = 'core_core_gemstones'

    id = Column(Integer, primary_key=True)
    label = Column(String(20, collation="utf8_bin"))

    # Relationships
    project = relationship(
        'Project',
        back_populates='gemstone',
        viewonly=True,
        lazy='joined'
    )


class ProtocolHasBardex(Base):
    """
    Represents the relationship between Protocol and Bardex entities in the database.

    Attributes:
    - protocol_id (int): Foreign key to the 'protocols' table.
    - bardex_id (int): Foreign key to the 'bardexes' table.
    """
    __tablename__ = 'core_core_protocol_has_bardexes'

    protocol_id = Column(Integer, ForeignKey('protocols.id'), primary_key=True)
    bardex_id = Column(Integer, ForeignKey('bardexes.id'), primary_key=True)

    # Define relationships
    protocol = relationship(
        'Protocol',
        back_populates='protocol_has_bardexes'
    )
    bardex = relationship('Bardex', back_populates='protocol_has_bardexes')


class Bardex(Base):
    """
    Represents a bardex entity in the database.

    Attributes:
    - id (int): Primary key for the bardexes table.
    - label (str): Label of the bardex.
    - seqtext (str): Sequence text associated with the bardex.
    - note (str): Note related to the bardex.
    - rc_seqtext (str): Reverse complement sequence text associated with the bardex.
    - abbrev_label (str): Abbreviated label of the bardex.
    """
    __tablename__ = 'core_core_bardexes'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    seqtext = Column(String(100, collation="utf8_bin"))
    note = Column(String(255, collation="utf8_bin"))
    rc_seqtext = Column(String(100, collation="utf8_bin"))
    abbrev_label = Column(String(100, collation="utf8_bin"))

    # Define relationships
    first_libraries = relationship(
        "Library",
        back_populates="index_1",
        foreign_keys="[Library.bardex_id]"
    )
    second_libraries = relationship(
        "Library",
        back_populates="index_2",
        foreign_keys="[Library.second_bardex_id]"
    )
    protocol_has_bardexes = relationship('ProtocolHasBardex', back_populates='bardex')


class Protocol(Base):
    """
    Represents a protocol entity in the database.

    Attributes:
    - id (int): Primary key for the protocols table.
    - label (str): Label of the protocol.
    - description (str): Description of the protocol.
    - is_current (int): Integer indicating if the protocol is current.
    - adapter_length (int): Adapter length associated with the protocol.
    """
    __tablename__ = 'core_core_protocols'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(100, collation="utf8mb3_bin"), nullable=False)
    description = Column(String(2048, collation="utf8mb3_bin"))
    is_current = Column(Integer, nullable=False, default=1)
    adapter_length = Column(Integer)

    # Relationship definition
    protocol_has_bardexes = relationship('ProtocolHasBardex', back_populates='protocol')


class InstrumentType(Base):
    """
    Represents the type of an instrument used in the experiment.

    Attributes:
    - id (int): The primary key identifier for the instrument type.
    - label (str): The label/name of the instrument type.
    - instruments_relation (Relationship): Relationship to the 'Instrument' class,
      specifying the instruments associated with this type.
    """
    __tablename__ = 'core_core_instrument_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))

    # Define a relationship
    instruments_relation = relationship("Instrument", back_populates="instrument_type")


class Instrument(Base):
    """
    Represents an instrument used in the experiment.

    Attributes:
    - id (int): The primary key identifier for the instrument.
    - label (str): The label/name of the instrument.
    - instrument_type_id (int): Foreign key linking to the 'InstrumentType' class.
    - instrument_type (Relationship): Relationship to the 'InstrumentType' class,
      specifying the type of this instrument.
    """
    __tablename__ = 'core_core_instruments'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    instrument_type_id = Column(Integer, ForeignKey('instrument_types.id'))

    # Define relationship
    instrument_type = relationship(
        "InstrumentType",
        back_populates="instruments_relation",
        viewonly=True, lazy='joined'
    )


class Pool(Base):
    """
    Represents a pool of samples or data.

    Attributes:
    - id (int): The primary key identifier for the pool.
    - label (str): The label/name of the pool.
    - description (str): Description or additional information about the pool.
    - date_created (Date): The date when the pool was created.
    - active (bool): Indicates if the pool is active or not.
    """
    __tablename__ = 'core_core_pools'
    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    description = Column(String(4096, collation="utf8_bin"))
    date_created = Column(Date)
    active = Column(Boolean)


class SequenceType(Base):
    """
    Represents a type of sequencing data.

    Attributes:
    - id (int): The primary key identifier for the sequence type.
    - label (str): The label/name of the sequence type.
    - abbrev (str): The abbreviated label for the sequence type.
    - active (bool): Indicates if the sequence type is active or not.
    - description (str): Description or additional information about the sequence type.
    """
    __tablename__ = 'core_core_sequence_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45))
    abbrev = Column(String(20))
    active = Column(Boolean)
    description = Column(Text)

    # Define a relationship
    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='sequence_type',
        viewonly=True, lazy='joined'
    )
    analysis_outputs = relationship(
        'AnalysisOutput',
        back_populates='sequence_type',
        viewonly=True, lazy='joined'
    )


class ReferenceGenome(Base):
    """
    Represents a reference genome used in the analysis.

    Attributes:
    - id (int): The primary key identifier for the reference genome.
    - label (str): The label/name of the reference genome.
    - notes (str): Additional notes or information about the reference genome.
    - organism_id (int): Foreign key linking to the 'Organism' class.
    - organism (Relationship): Relationship to the 'Organism' class.
    """
    __tablename__ = 'core_core_reference_genomes'

    id = Column(Integer, primary_key=True)
    label = Column(String(255, collation="utf8_bin"))
    notes = Column(Text(collation="utf8_bin"))
    organism_id = Column(Integer, ForeignKey('organisms.id'))

    # Define relationships
    organism = relationship('Organism', viewonly=True, lazy='joined')
    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='reference_genome',
        viewonly=True,
        lazy='joined'
    )

class CoordinateSet(Base):
    """
    Represents a coordinate set used in the analysis.

    Attributes:
    - id (int): The primary key identifier for the coordinate set.
    - label (str): The label/name of the coordinate set.
    - source_file (str): Path or source file associated with the coordinate set.
    - reference_genome_id (int): Foreign key linking to the 'ReferenceGenome' class.
    - reference_genome (Relationship): Relationship to the 'ReferenceGenome' class.
    """
    __tablename__ = 'core_core_coordinate_sets'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    source_file = Column(String)
    reference_genome_id = Column(Integer, ForeignKey('reference_genomes.id'))

    # Define a relationship
    reference_genome = relationship('ReferenceGenome')
    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='coordinate_set',
        viewonly=True,
        lazy='joined'
    )

class AnalysisType(Base):
    """
    Represents types of analysis that can be performed.

    Attributes:
    - id (int): Primary key identifier for the analysis type.
    - label (str): Name or label of the analysis type.
    - description (str): Description of the analysis type.
    """
    __tablename__ = 'core_core_analysis_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False, unique=True)
    description = Column(String(4096), nullable=True)


class AnalysisOutputType(Base):
    """
    Represents types of analysis outputs.

    Attributes:
    - id (int): Primary key identifier for the analysis output type.
    - label (str): Name or label of the analysis output type.
    - description (str): Description of the analysis output type.
    """
    __tablename__ = 'core_core_analysis_output_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45), nullable=False, unique=True)
    description = Column(Text)

    # Relationship to analysis_output_type_downstream_analysis_file_types table
    downstream_file_types = relationship(
        'AnalysisOutputTypeDownstreamFileType',
        back_populates='analysis_output_type'
    )


class AnalysisFileType(Base):
    """
    Represents file types associated with downstream analysis.

    Attributes:
    - id (int): Primary key identifier for the analysis file type.
    - label (str): Name or label of the analysis file type.
    - abbrev (str): Abbreviation of the analysis file type.
    - variant (int): Variant identifier for the analysis file type.
    - description (str): Description of the analysis file type.
    """
    __tablename__ = 'core_core_downstream_analysis_file_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45), nullable=False)
    abbrev = Column(String(10), nullable=False)
    variant = Column(Integer, nullable=False, default=0)
    description = Column(String(4096))

    # Relationship to analysis_output_type_downstream_analysis_file_types table
    analysis_output_types = relationship(
        'AnalysisOutputTypeDownstreamFileType',
        back_populates='analysis_file_type'
    )


class DownstreamAnalysisFile(Base):
    """
    Represents files associated with downstream analyses.

    Attributes:
    - id (int): Primary key identifier for the downstream analysis file.
    - file_path (str): Path of the downstream analysis file.
    - downstream_analysis_file_type_id (int): Foreign key linking to analysis file type.
    - downstream_analysis_id (int): Foreign key linking to downstream analysis.
    - include_freq (int): Frequency of the file inclusion.
    - description (str): Description of the downstream analysis file.
    """
    __tablename__ = 'core_core_downstream_analysis_files'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(750), nullable=False)
    downstream_analysis_file_type_id = Column(
        Integer,
        ForeignKey('downstream_analysis_file_types.id')
    )
    downstream_analysis_id = Column(
        Integer,
        ForeignKey('downstream_analyses.id')
    )
    include_freq = Column(Integer, nullable=False, default=0)
    description = Column(String(2048))

    # Relationships
    analysis_file_type = relationship('AnalysisFileType')

    downstream_analysis = relationship(
        'DownstreamAnalysis',
        back_populates='downstream_analysis_files'
    )

    # Unique constraint on the combination of file_path
    # and downstream_analysis_id
    __table_args__ = (UniqueConstraint
        (
            'file_path',
            'downstream_analysis_id')
        ,)


class DownstreamAnalysisType(Base):
    """
    Represents types of downstream analyses.

    Attributes:
    - id (int): Primary key identifier for the downstream analysis type.
    - label (str): Name or label of the downstream analysis type.
    - abbrev (str): Abbreviation of the downstream analysis type.
    - description (str): Description of the downstream analysis type.
    - active (bool): Indicates if the downstream analysis type is active.
    """
    __tablename__ = 'core_core_downstream_analysis_types'
    id = Column(Integer, primary_key=True)
    label = Column(String(45))
    abbrev = Column(String(10))
    description = Column(String(4096))
    active = Column(Boolean)

    # Relationships
    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='downstream_analysis_type'
    )


class DownstreamAnalysis(Base):
    """
    Represents downstream analyses.

    Attributes:
    - id (int): Primary key identifier for the downstream analysis.
    - label (str): Name or label of the downstream analysis.
    - analysis_date (DateTime): Date of the analysis.
    - downstream_analysis_type_id (int): Foreign key linking to downstream analysis type.
    - sample_id (int): Foreign key linking to samples.
    - base_dir (str): Base directory for the analysis.
    - description (str): Description of the downstream analysis.
    - sequence_type_id (int): Foreign key linking to sequence types.
    - coordinate_set_id (int): Foreign key linking to coordinate sets.
    - reference_genome_id (int): Foreign key linking to reference genomes.
    """
    __tablename__ = 'core_core_downstream_analyses'

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    analysis_date = Column(DateTime)
    downstream_analysis_type_id = Column(
        Integer,
        ForeignKey('downstream_analysis_types.id'),
        nullable=False
    )
    sample_id = Column(Integer, ForeignKey('samples.id'))
    base_dir = Column(String(1024))
    description = Column(String(4096))
    sequence_type_id = Column(Integer, ForeignKey('sequence_types.id'))
    coordinate_set_id = Column(Integer, ForeignKey('coordinate_sets.id'))
    reference_genome_id = Column(Integer, ForeignKey('reference_genomes.id'))

    # Relationships
    downstream_analysis_files = relationship(
        'DownstreamAnalysisFile',
        back_populates='downstream_analysis'
    )
    '''
    files = relationship(
        'DownstreamAnalysisFile',
        back_populates='downstream_analysis',
        cascade='all, delete-orphan',
        primaryjoin='DownstreamAnalysis.id == DownstreamAnalysisFile.downstream_analysis_id',
        single_parent=True,
        foreign_keys=[
            "DownstreamAnalysisFile.downstream_analysis_id", 
            "DownstreamAnalysisFile.downstream_analysis_file_type_id"
        ],
        remote_side='DownstreamAnalysisFile.downstream_analysis_id',
        overlaps="downstream_analysis_files"  # Add this line to address the warning
    )
    '''
    outputs = relationship(
        'AnalysisOutput',
        back_populates='analysis',
        cascade='all, delete-orphan',
        foreign_keys='AnalysisOutput.downstream_analysis_id',
        primaryjoin='DownstreamAnalysis.id == AnalysisOutput.downstream_analysis_id'
    )

    downstream_analysis_type = relationship(
        'DownstreamAnalysisType',
        back_populates='downstream_analyses'
    )
    sample = relationship('Sample', back_populates='downstream_analyses')
    sequence_type = relationship('SequenceType', back_populates='downstream_analyses')
    coordinate_set = relationship('CoordinateSet', back_populates='downstream_analyses')
    reference_genome = relationship('ReferenceGenome', back_populates='downstream_analyses')


class AnalysisOutputTypeDownstreamFileType(Base):
    """
    Represents the relationship between analysis output types and downstream analysis file types.

    Attributes:
    - id (int): Primary key identifier for the relationship.
    - analysis_output_type_id (int): Foreign key linking to analysis output types.
    - downstream_analysis_file_type_id (int): Foreign key linking to downstream analysis file types.
    """
    __tablename__ = 'core_core_analysis_output_type_downstream_analysis_file_types'

    id = Column(Integer, primary_key=True)
    analysis_output_type_id = Column(Integer, ForeignKey('analysis_output_types.id'))
    downstream_analysis_file_type_id = Column(
        Integer,
        ForeignKey('downstream_analysis_file_types.id')
    )

    # Relationships
    analysis_output_type = relationship(
        'AnalysisOutputType',
        back_populates='downstream_file_types'
    )
    analysis_file_type = relationship(
        'AnalysisFileType',
        back_populates='analysis_output_types'
    )

    # Unique constraint on the combination of analysis_output_type_id and
    # downstream_analysis_file_type_id
    __table_args__ = (
        UniqueConstraint(
            'analysis_output_type_id',
            'downstream_analysis_file_type_id'
        )
    ,)


class AnalysisOutput(Base):
    """
    Represents analysis outputs.

    Attributes:
    - id (int): Primary key identifier for the analysis output.
    - sample_id (int): Foreign key linking to samples.
    - sequence_type_id (int): Foreign key linking to sequence types
    - analysis_output_type_id (int): Foreign key linking to analysis output types.
    - downstream_analysis_id (int): Foreign key linking to downstream analyses.
    - is_primary (bool): Indicates if the analysis output is primary.
    """
    __tablename__ = 'core_analysis_outputs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey('samples.id'), nullable=False)
    sequence_type_id = Column(
        Integer,
        ForeignKey('sequence_types.id'),
        nullable=False
    )
    analysis_output_type_id = Column(
        Integer,
        ForeignKey('analysis_output_types.id'),
        nullable=False
    )
    downstream_analysis_id = Column(
        Integer,
        ForeignKey('downstream_analyses.id'),
        nullable=False
    )
    is_primary = Column(Boolean, nullable=False, default=False)

    #Relationships
    sample = relationship('Sample', back_populates='analysis_outputs')
    sequence_type = relationship('SequenceType', back_populates='analysis_outputs')
    analysis = relationship('DownstreamAnalysis', back_populates='outputs')
    analysis_output_type = relationship('AnalysisOutputType')