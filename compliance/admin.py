from django.contrib import admin
from .models import Profile, Standard, StandardSection, Compliance, ChecklistItem, Document, Progress, ComplianceSubmission, ComplianceDocument, Remark, Checklist
from .models import ComplianceSubmission, SupportingDocument


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(StandardSection)
class StandardSectionAdmin(admin.ModelAdmin):
    list_display = ('standard', 'section_number', 'title', 'description')

@admin.register(Compliance)
class ComplianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'standard')

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('compliance', 'description', 'completed', 'user')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('compliance', 'title', 'file', 'uploaded_at', 'user')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('compliance', 'user', 'progress')

# @admin.register(ComplianceSubmission)
# class ComplianceSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('business', 'compliance', 'pdf_document', 'submitted_at', 'approved', 'rejected', 'feedback')

@admin.register(ComplianceDocument)
class ComplianceDocumentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'file', 'uploaded_at')

@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ('document', 'text', 'created_at', 'updated_at')

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('business_owner', 'document', 'compliance_rows', 'submitted_at')



class ComplianceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'submitted_at', 'approved', 'rejected')

admin.site.register(ComplianceSubmission, ComplianceSubmissionAdmin)
admin.site.register(SupportingDocument)
