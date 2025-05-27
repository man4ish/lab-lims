from django.test import TestCase
from datetime import date
from core.models import (
    LibraryType, SampleType, SpecimenSource, Barcode, Flowcell, Analyses,
    Run, Lane, Library, LibraryLane, Organism, Gemstone, Project, Sample,
    Protocol, Bardex, InstrumentType, Instrument, Pool, SequenceType,
    ReferenceGenome, CoordinateSet, AnalysisType, AnalysisOutputType,
    AnalysisFileType, DownstreamAnalysisFile, DownstreamAnalysisType,
    DownstreamAnalysis, AnalysisOutputTypeDownstreamFileType, AnalysisOutput
)


class ModelsTestCase(TestCase):

    def setUp(self):
        # Create base objects for foreign keys reused in tests
        self.library_type = LibraryType.objects.create(name="LibType1")
        self.sample_type = SampleType.objects.create(name="SampleType1")
        self.specimen_source = SpecimenSource.objects.create(name="Specimen1")
        self.barcode = Barcode.objects.create()
        self.instrument_type = InstrumentType.objects.create(label="Illumina")
        self.instrument = Instrument.objects.create(label="NovaSeq", instrument_type=self.instrument_type)
        self.pool = Pool.objects.create(label="Pool1")
        self.sequence_type = SequenceType.objects.create(label="SeqType1", abbrev="ST1")
        self.organism = Organism.objects.create(label="Homo sapiens")
        self.gemstone = Gemstone.objects.create(label="Gem1")
        self.project = Project.objects.create(label="Project1", gemstone=self.gemstone)
        self.protocol = Protocol.objects.create(label="Protocol1")
        self.bardex1 = Bardex.objects.create(label="Bardex1", seqtext="ATGC", rc_seqtext="GCAT", abbrev_label="B1")
        self.bardex2 = Bardex.objects.create(label="Bardex2", seqtext="CGTA", rc_seqtext="TACG", abbrev_label="B2")
        self.sample = Sample.objects.create(
            label="Sample1",
            organism=self.organism,
            project=self.project,
            sample_type=self.sample_type,
            specimen_source=self.specimen_source
        )
        self.flowcell = Flowcell.objects.create(label="FC1", barcode=self.barcode)
        self.analysis_type = AnalysisType.objects.create(label="Type1")
        self.analysis_output_type = AnalysisOutputType.objects.create(label="OutputType1")
        self.analysis_file_type = AnalysisFileType.objects.create(label="FileType1", abbrev="FT1")
        self.downstream_analysis_type = DownstreamAnalysisType.objects.create(
            label="DownType1", abbrev="DT1", description="desc", active=True
        )
        self.coordinate_set = CoordinateSet.objects.create(label="CoordSet1", reference_genome=None)
        self.reference_genome = ReferenceGenome.objects.create(label="RefGenome1", organism=self.organism)
        self.downstream_analysis = DownstreamAnalysis.objects.create(
            label="DownAnalysis1",
            downstream_analysis_type=self.downstream_analysis_type,
            sample=self.sample,
            base_dir="/data",
            sequence_type=self.sequence_type,
            coordinate_set=self.coordinate_set,
            reference_genome=self.reference_genome
        )
        self.library = Library.objects.create(
            label="Library1",
            library_type=self.library_type,
            sample=self.sample,
            protocol=self.protocol,
            bardex=self.bardex1,
            second_bardex=self.bardex2,
        )
        self.lane = Lane.objects.create(
            number=1,
            flowcell=self.flowcell,
            pool=self.pool,
            sequence_type=self.sequence_type
        )
    
    def test_str_methods(self):
        self.assertEqual(str(self.library_type), "LibType1")
        self.assertEqual(str(self.barcode), f"Barcode(id={self.barcode.id})")
        self.assertEqual(str(self.flowcell), f"Flowcell(id={self.flowcell.id}, label=FC1)")
        self.assertEqual(str(self.analysis_type), "Type1")
        self.assertEqual(str(self.instrument_type), "Illumina")
        self.assertEqual(str(self.instrument), "NovaSeq")
        self.assertEqual(str(self.pool), "Pool1")
        self.assertEqual(str(self.sequence_type), "SeqType1")
        self.assertEqual(str(self.organism), "Homo sapiens")
        self.assertEqual(str(self.gemstone), "Gem1")
        self.assertEqual(str(self.project), "Project1")
        self.assertEqual(str(self.sample), "Sample1")
        self.assertEqual(str(self.protocol), "Protocol1")
        self.assertEqual(str(self.bardex1), "Bardex1")
        self.assertEqual(str(self.lane), f"Lane 1 (Flowcell: {self.flowcell.id})")
        self.assertEqual(str(self.downstream_analysis), "DownAnalysis1")
    
    def test_library_creation(self):
        lib = self.library
        self.assertEqual(lib.label, "Library1")
        self.assertEqual(lib.library_type, self.library_type)
        self.assertEqual(lib.sample, self.sample)
        self.assertEqual(lib.bardex, self.bardex1)
        self.assertEqual(lib.second_bardex, self.bardex2)
    
    def test_flowcell_relations(self):
        flowcell = self.flowcell
        flowcell.employee_id = 101
        flowcell.is_paired_end = True
        flowcell.save()
        self.assertTrue(flowcell.is_paired_end)
        self.assertEqual(flowcell.employee_id, 101)
        self.assertEqual(flowcell.barcode, self.barcode)
    
    def test_lane_relations(self):
        lane = self.lane
        self.assertEqual(lane.flowcell, self.flowcell)
        self.assertEqual(lane.pool, self.pool)
        self.assertEqual(lane.sequence_type, self.sequence_type)
    
    def test_run_creation(self):
        run = Run.objects.create(label="Run1", flowcell=self.flowcell, instrument=self.instrument)
        self.assertEqual(run.label, "Run1")
        self.assertEqual(run.flowcell, self.flowcell)
        self.assertEqual(run.instrument, self.instrument)
    
    def test_analyses_creation(self):
        analysis = Analyses.objects.create(
            analysis_type=self.analysis_type,
            flowcell=self.flowcell,
            notes="Test analysis",
            software_version="1.0"
        )
        self.assertEqual(analysis.analysis_type, self.analysis_type)
        self.assertEqual(analysis.flowcell, self.flowcell)
        self.assertEqual(analysis.notes, "Test analysis")
    
    def test_downstream_analysis_file_unique_constraint(self):
        daf1 = DownstreamAnalysisFile.objects.create(
            file_path="/path/to/file",
            downstream_analysis_file_type=self.analysis_file_type,
            downstream_analysis=self.downstream_analysis,
            include_freq=5
        )
        with self.assertRaises(Exception):
            # Should fail because unique_together constraint on (file_path, downstream_analysis)
            DownstreamAnalysisFile.objects.create(
                file_path="/path/to/file",
                downstream_analysis_file_type=self.analysis_file_type,
                downstream_analysis=self.downstream_analysis,
                include_freq=10
            )
    
    def test_analysis_output_type_downstream_file_type_unique_constraint(self):
        AnalysisOutputTypeDownstreamFileType.objects.create(
            analysis_output_type=self.analysis_output_type,
            analysis_file_type=self.analysis_file_type
        )
        with self.assertRaises(Exception):
            # Unique constraint violation
            AnalysisOutputTypeDownstreamFileType.objects.create(
                analysis_output_type=self.analysis_output_type,
                analysis_file_type=self.analysis_file_type
            )
