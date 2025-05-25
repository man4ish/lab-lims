from django.db import models

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class InstrumentType(Base):
    """
    Represents the type of an instrument used in the experiment.
    """
    __tablename__ = 'instrument_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))

    instruments_relation = relationship(
        "Instrument",
        back_populates="instrument_type"
    )


class Instrument(Base):
    """
    Represents an instrument used in the experiment.
    """
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    instrument_type_id = Column(Integer, ForeignKey('instrument_types.id'))

    instrument_type = relationship(
        "InstrumentType",
        back_populates="instruments_relation",
        viewonly=True,
        lazy='joined'
    )


class Pool(Base):
    """
    Represents a pool of samples or data.
    """
    __tablename__ = 'pools'

    id = Column(Integer, primary_key=True)
    label = Column(String(100, collation="utf8_bin"))
    description = Column(String(4096, collation="utf8_bin"))
    date_created = Column(Date)
    active = Column(Boolean)


class SequenceType(Base):
    """
    Represents a type of sequencing data.
    """
    __tablename__ = 'sequence_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45))
    abbrev = Column(String(20))
    active = Column(Boolean)
    description = Column(Text)

    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='sequence_type',
        viewonly=True,
        lazy='joined'
    )
    analysis_outputs = relationship(
        'AnalysisOutput',
        back_populates='sequence_type',
        viewonly=True,
        lazy='joined'
    )


class ReferenceGenome(Base):
    """
    Represents a reference genome used in the analysis.
    """
    __tablename__ = 'reference_genomes'

    id = Column(Integer, primary_key=True)
    label = Column(String(255, collation="utf8_bin"))
    notes = Column(Text(collation="utf8_bin"))
    organism_id = Column(Integer, ForeignKey('organisms.id'))

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
    """
    __tablename__ = 'coordinate_sets'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    source_file = Column(String)
    reference_genome_id = Column(Integer, ForeignKey('reference_genomes.id'))

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
    """
    __tablename__ = 'analysis_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False, unique=True)
    description = Column(String(4096), nullable=True)


class AnalysisOutputType(Base):
    """
    Represents types of analysis outputs.
    """
    __tablename__ = 'analysis_output_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45), nullable=False, unique=True)
    description = Column(Text)

    downstream_file_types = relationship(
        'AnalysisOutputTypeDownstreamFileType',
        back_populates='analysis_output_type'
    )


class AnalysisFileType(Base):
    """
    Represents file types associated with downstream analysis.
    """
    __tablename__ = 'downstream_analysis_file_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45), nullable=False)
    abbrev = Column(String(10), nullable=False)
    variant = Column(Integer, nullable=False, default=0)
    description = Column(String(4096))

    analysis_output_types = relationship(
        'AnalysisOutputTypeDownstreamFileType',
        back_populates='analysis_file_type'
    )


class DownstreamAnalysisFile(Base):
    """
    Represents files associated with downstream analyses.
    """
    __tablename__ = 'downstream_analysis_files'

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

    analysis_file_type = relationship('AnalysisFileType')

    downstream_analysis = relationship(
        'DownstreamAnalysis',
        back_populates='downstream_analysis_files'
    )

    __table_args__ = (
        UniqueConstraint(
            'file_path',
            'downstream_analysis_id'
        ),
    )


class DownstreamAnalysisType(Base):
    """
    Represents types of downstream analyses.
    """
    __tablename__ = 'downstream_analysis_types'

    id = Column(Integer, primary_key=True)
    label = Column(String(45))
    abbrev = Column(String(10))
    description = Column(String(4096))
    active = Column(Boolean)

    downstream_analyses = relationship(
        'DownstreamAnalysis',
        back_populates='downstream_analysis_type'
    )


class DownstreamAnalysis(Base):
    """
    Represents downstream analyses.
    """
    __tablename__ = 'downstream_analyses'

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

    downstream_analysis_files = relationship(
        'DownstreamAnalysisFile',
        back_populates='downstream_analysis'
    )
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
    """
    __tablename__ = 'analysis_output_type_downstream_analysis_file_types'

    id = Column(Integer, primary_key=True)
    analysis_output_type_id = Column(Integer, ForeignKey('analysis_output_types.id'))
    downstream_analysis_file_type_id = Column(
        Integer,
        ForeignKey('downstream_analysis_file_types.id')
    )

    analysis_output_type = relationship(
        'AnalysisOutputType',
        back_populates='downstream_file_types'
    )
    analysis_file_type = relationship(
        'AnalysisFileType',
        back_populates='analysis_output_types'
    )

    __table_args__ = (
        UniqueConstraint(
            'analysis_output_type_id',
            'downstream_analysis_file_type_id'
        ),
    )


class AnalysisOutput(Base):
    """
    Represents analysis outputs.
    """
    __tablename__ = 'analysis_outputs'

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'))
    sequence_type_id = Column(Integer, ForeignKey('sequence_types.id'))
    analysis_output_type_id = Column(Integer, ForeignKey('analysis_output_types.id'))
    downstream_analysis_id = Column(Integer, ForeignKey('downstream_analyses.id'))
    is_primary = Column(Boolean, default=False)

    sample = relationship('Sample', viewonly=True, lazy='joined')
    sequence_type = relationship('SequenceType', back_populates='analysis_outputs')
    analysis_output_type = relationship('AnalysisOutputType')
    analysis = relationship('DownstreamAnalysis', back_populates='outputs')


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Organism(Base):
    """
    Represents an organism (species).
    """
    __tablename__ = 'organisms'

    id = Column(Integer, primary_key=True)
    genus = Column(String(100, collation="utf8_bin"), nullable=False)
    species = Column(String(100, collation="utf8_bin"), nullable=False)
    common_name = Column(String(100, collation="utf8_bin"))

    reference_genomes = relationship('ReferenceGenome', back_populates='organism')


class Sample(Base):
    """
    Represents a biological sample.
    """
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True)
    label = Column(String(255, collation="utf8_bin"), nullable=False, unique=True)
    description = Column(String(4096, collation="utf8_bin"))
    date_collected = Column(Date)
    organism_id = Column(Integer, ForeignKey('organisms.id'))
    pool_id = Column(Integer, ForeignKey('pools.id'))
    active = Column(Boolean, default=True)

    organism = relationship('Organism', back_populates='samples')
    pool = relationship('Pool')
    downstream_analyses = relationship('DownstreamAnalysis', back_populates='sample')


# Update Organism.samples relationship now that Sample is defined
Organism.samples = relationship('Sample', back_populates='organism')


class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(150, collation="utf8_bin"), unique=True, nullable=False)
    email = Column(String(255, collation="utf8_bin"), unique=True, nullable=False)
    full_name = Column(String(255, collation="utf8_bin"))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Project(Base):
    """
    Represents a project grouping samples or analyses.
    """
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, collation="utf8_bin"), unique=True, nullable=False)
    description = Column(Text(collation="utf8_bin"))
    date_created = Column(DateTime)
    active = Column(Boolean, default=True)

    samples = relationship('Sample', secondary='project_samples', back_populates='projects')


class ProjectSample(Base):
    """
    Association table for many-to-many relationship between Project and Sample.
    """
    __tablename__ = 'project_samples'

    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'), primary_key=True)


# Add projects relationship to Sample
Sample.projects = relationship('Project', secondary='project_samples', back_populates='samples')


class Experiment(Base):
    """
    Represents an experiment in which samples are analyzed.
    """
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    label = Column(String(255, collation="utf8_bin"), unique=True, nullable=False)
    description = Column(Text(collation="utf8_bin"))
    date_performed = Column(Date)
    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    pool_id = Column(Integer, ForeignKey('pools.id'))

    instrument = relationship('Instrument')
    pool = relationship('Pool')
    samples = relationship('Sample', secondary='experiment_samples', back_populates='experiments')


class ExperimentSample(Base):
    """
    Association table for many-to-many relationship between Experiment and Sample.
    """
    __tablename__ = 'experiment_samples'

    experiment_id = Column(Integer, ForeignKey('experiments.id'), primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'), primary_key=True)


# Add experiments relationship to Sample
Sample.experiments = relationship('Experiment', secondary='experiment_samples', back_populates='samples')



