from django.contrib import admin
from .models import Organism, Project, SampleType, SpecimenSource, Sample

admin.site.register(Organism)
admin.site.register(Project)
admin.site.register(SampleType)
admin.site.register(SpecimenSource)
admin.site.register(Sample)
