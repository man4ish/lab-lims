from django.db import models

class LibraryType(models.Model):
    name = models.CharField(max_length=100)

class SampleType(models.Model):
    name = models.CharField(max_length=100)

class SpecimenSource(models.Model):
    name = models.CharField(max_length=100)

class Barcode(models.Model):
    # Equivalent to SQLAlchemy Integer PK
    # Django automatically adds an id primary key field if not specified, but I added explicitly for clarity
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Barcode(id={self.id})"


class Flowcell(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)
    employee_id = models.IntegerField(null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    clustering_station_id = models.IntegerField(null=True, blank=True)
    old_comments = models.CharField(max_length=2048, null=True, blank=True)
    is_paired_end = models.BooleanField(null=True, blank=True)
    failed = models.BooleanField(null=True, blank=True)
    barcode = models.ForeignKey(Barcode, on_delete=models.SET_NULL, null=True, blank=True, related_name='flowcells')
    active = models.BooleanField(null=True, blank=True)

    # Related fields are auto-created in Django, but you can specify reverse relation names if needed.
    # Here 'runs', 'lanes', and 'analyses' would be reverse relations from related models.

    def __str__(self):
        return f"Flowcell(id={self.id}, label={self.label})"


class Analyses(models.Model):
    id = models.AutoField(primary_key=True)
    analysis_type = models.ForeignKey('AnalysisType', on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses')
    flowcell = models.ForeignKey(Flowcell, on_delete=models.CASCADE, related_name='analyses')
    date_performed = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=2048, null=True, blank=True)
    software_version = models.CharField(max_length=128, null=True, blank=True)
    contaminant_filtered = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Analyses(id={self.id}, flowcell_id={self.flowcell_id})"


class Run(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)
    date_started = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)
    cycles = models.IntegerField(null=True, blank=True)
    instrument = models.ForeignKey('Instrument', on_delete=models.SET_NULL, null=True, blank=True, related_name='runs')
    flowcell = models.ForeignKey(Flowcell, on_delete=models.CASCADE, related_name='runs')
    employee_id = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=2048, null=True, blank=True)
    cycle1_attachment_id = models.IntegerField(null=True, blank=True)
    read2_cycle1_attachment_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Run(id={self.id}, label={self.label})"
    
class Lane(models.Model):
    number = models.IntegerField()
    is_control = models.BooleanField(null=True, blank=True)
    is_titer = models.BooleanField(null=True, blank=True)
    flowcell = models.ForeignKey('Flowcell', on_delete=models.CASCADE, related_name='lanes')
    pool = models.ForeignKey('Pool', on_delete=models.CASCADE, related_name='lanes')
    failed = models.BooleanField(null=True, blank=True)
    sequence_type = models.ForeignKey('SequenceType', on_delete=models.CASCADE)

    def __str__(self):
        return f"Lane {self.number} (Flowcell: {self.flowcell_id})"


class Library(models.Model):
    label = models.CharField(max_length=100)
    library_type = models.ForeignKey('LibraryType', on_delete=models.CASCADE)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='libraries')
    employee_id = models.IntegerField(null=True, blank=True)
    protocol = models.ForeignKey('Protocol', on_delete=models.CASCADE)
    date_created = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=4096, null=True, blank=True)
    insert_size = models.IntegerField(null=True, blank=True)
    client_provided = models.BooleanField(null=True, blank=True)
    bardex = models.ForeignKey('Bardex', on_delete=models.CASCADE, related_name='library_index_1')
    second_bardex = models.ForeignKey('Bardex', on_delete=models.CASCADE, related_name='library_index_2', null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.label


class LibraryLane(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name='library_lanes')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='library_lanes')
    units = models.CharField(max_length=10)
    concentration = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"LibraryLane {self.id} - Lane {self.lane_id} / Library {self.library_id}"


class Organism(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label    
    
class Gemstone(models.Model):
    label = models.CharField(max_length=20)

    def __str__(self):
        return self.label


class Project(models.Model):
    label = models.CharField(max_length=100)
    gemstone = models.ForeignKey(Gemstone, on_delete=models.CASCADE, related_name='projects')
    ftp_url = models.CharField(max_length=50, null=True, blank=True)
    ftp_user = models.CharField(max_length=10, null=True, blank=True)
    website_url = models.CharField(max_length=50, null=True, blank=True)
    website_user = models.CharField(max_length=12, null=True, blank=True)
    website_password = models.CharField(max_length=10, null=True, blank=True)
    old_comments = models.TextField(max_length=4096, null=True, blank=True)
    is_current = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.label


class Sample(models.Model):
    label = models.CharField(max_length=100)
    organism = models.ForeignKey('Organism', on_delete=models.CASCADE, related_name='samples')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='samples')
    description = models.TextField(max_length=4096, null=True, blank=True)
    sample_type = models.ForeignKey('SampleType', on_delete=models.CASCADE)
    specimen_source = models.ForeignKey('SpecimenSource', on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class Protocol(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField(max_length=2048, null=True, blank=True)
    is_current = models.IntegerField(default=1)
    adapter_length = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.label

class Bardex(models.Model):
    label = models.CharField(max_length=100)
    seqtext = models.CharField(max_length=100)
    note = models.CharField(max_length=255, null=True, blank=True)
    rc_seqtext = models.CharField(max_length=100)
    abbrev_label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class ProtocolHasBardex(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='protocol_has_bardexes')
    bardex = models.ForeignKey(Bardex, on_delete=models.CASCADE, related_name='protocol_has_bardexes')

    class Meta:
        unique_together = (('protocol', 'bardex'),)

    def __str__(self):
        return f"Protocol {self.protocol_id} - Bardex {self.bardex_id}"    
    






class InstrumentType(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Instrument(models.Model):
    label = models.CharField(max_length=100)
    instrument_type = models.ForeignKey(
        InstrumentType,
        on_delete=models.CASCADE,
        related_name='instruments'
    )

    def __str__(self):
        return self.label
    

class Pool(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=4096, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.label


class SequenceType(models.Model):
    label = models.CharField(max_length=45)
    abbrev = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label


class ReferenceGenome(models.Model):
    label = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    organism = models.ForeignKey(
        'Organism',
        on_delete=models.PROTECT,
        related_name='reference_genomes',
        null=True, blank=True
    )

    def __str__(self):
        return self.label


class CoordinateSet(models.Model):
    label = models.CharField(max_length=255)
    source_file = models.CharField(max_length=255, null=True, blank=True)
    reference_genome = models.ForeignKey(
        ReferenceGenome,
        on_delete=models.PROTECT,
        related_name='coordinate_sets',
        null=True, blank=True
    )

    def __str__(self):
        return self.label
    
class AnalysisType(models.Model):
    label = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return self.label


class AnalysisOutputType(models.Model):
    label = models.CharField(max_length=45, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label


class AnalysisFileType(models.Model):
    label = models.CharField(max_length=45)
    abbrev = models.CharField(max_length=10)
    variant = models.IntegerField(default=0)
    description = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return self.label


class DownstreamAnalysisFile(models.Model):
    file_path = models.CharField(max_length=750)
    downstream_analysis_file_type = models.ForeignKey(
        AnalysisFileType,
        on_delete=models.PROTECT,
        related_name='downstream_analysis_files'
    )
    downstream_analysis = models.ForeignKey(
        'DownstreamAnalysis',  # Assuming 'DownstreamAnalysis' model exists
        on_delete=models.CASCADE,
        related_name='downstream_analysis_files'
    )
    include_freq = models.IntegerField(default=0)
    description = models.CharField(max_length=2048, null=True, blank=True)

    class Meta:
        unique_together = ('file_path', 'downstream_analysis')

    def __str__(self):
        return f"{self.file_path} ({self.downstream_analysis})"

class DownstreamAnalysisType(models.Model):
    label = models.CharField(max_length=45)
    abbrev = models.CharField(max_length=10)
    description = models.CharField(max_length=4096)
    active = models.BooleanField()

    def __str__(self):
        return self.label


class DownstreamAnalysis(models.Model):
    label = models.CharField(max_length=50)
    analysis_date = models.DateTimeField(null=True, blank=True)

    downstream_analysis_type = models.ForeignKey(
        DownstreamAnalysisType,
        on_delete=models.PROTECT,
        related_name='downstream_analyses'
    )
    sample = models.ForeignKey(
        'Sample',  # Make sure Sample model exists
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='downstream_analyses'
    )
    base_dir = models.CharField(max_length=1024, null=True, blank=True)
    description = models.CharField(max_length=4096, null=True, blank=True)

    sequence_type = models.ForeignKey(
        'SequenceType',  # Make sure SequenceType model exists
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='downstream_analyses'
    )
    coordinate_set = models.ForeignKey(
        'CoordinateSet',  # Make sure CoordinateSet model exists
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='downstream_analyses'
    )
    reference_genome = models.ForeignKey(
        'ReferenceGenome',  # Make sure ReferenceGenome model exists
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='downstream_analyses'
    )

    def __str__(self):
        return self.label

class AnalysisOutputTypeDownstreamFileType(models.Model):
    analysis_output_type = models.ForeignKey(
        AnalysisOutputType,
        on_delete=models.CASCADE,
        related_name='downstream_file_types'
    )
    analysis_file_type = models.ForeignKey(
        AnalysisFileType,
        on_delete=models.CASCADE,
        related_name='analysis_output_types'
    )

    class Meta:
        unique_together = ('analysis_output_type', 'analysis_file_type')


class AnalysisOutput(models.Model):
    sample = models.ForeignKey(
        'Sample',  # Ensure Sample model exists
        on_delete=models.CASCADE,
        related_name='analysis_outputs'
    )
    sequence_type = models.ForeignKey(
        'SequenceType',  # Ensure SequenceType model exists
        on_delete=models.CASCADE,
        related_name='analysis_outputs'
    )
    analysis_output_type = models.ForeignKey(
        AnalysisOutputType,
        on_delete=models.CASCADE
    )
    analysis = models.ForeignKey(
        'DownstreamAnalysis',  # Ensure DownstreamAnalysis model exists
        on_delete=models.CASCADE,
        related_name='outputs'
    )
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Output {self.id} (Primary: {self.is_primary})"