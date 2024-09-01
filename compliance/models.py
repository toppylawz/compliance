from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Uploader(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

class ComplianceDocument(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compliance_documents')
    file = models.FileField(upload_to='compliance_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ComplianceEntry(models.Model):
    document = models.ForeignKey(ComplianceDocument, on_delete=models.CASCADE)
    requirement_section_category = models.CharField(max_length=255)
    assessment = models.TextField()
    in_compliance = models.BooleanField(default=False)
    not_compliance = models.BooleanField(default=False)
    compliance_remarks = models.TextField(blank=True, null=True)
    business_remarks = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.requirement_section_category

class Profile(models.Model):
    USER_ROLES = (
        ('staff', 'Staff'),
        ('business', 'Business'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='business')

    def __str__(self):
        return f'{self.user.username} - {self.role}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Standard(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class StandardSection(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.standard.name} - {self.section_number}"

class Compliance(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ChecklistItem(models.Model):
    compliance = models.ForeignKey(Compliance, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class Document(models.Model):
    compliance = models.ForeignKey(Compliance, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Progress(models.Model):
    compliance = models.ForeignKey(Compliance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Progress percentage
    status_message = models.CharField(max_length=255, default="Has not started reviewing")

    def __str__(self):
        return f'{self.user.username} - {self.compliance.name} - {self.progress}%'

class ComplianceSubmission(models.Model):
    business = models.ForeignKey(User, on_delete=models.CASCADE)
    compliance = models.ForeignKey(ComplianceDocument, on_delete=models.CASCADE)
    pdf_document = models.FileField(upload_to='submissions/', blank=True, null=True)  # Make it optional
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    resubmitted = models.BooleanField(default=False)

    @property
    def status_message(self):
        if self.approved:
            return "Approved"
        elif self.rejected:
            return "Rejected"
        elif self.feedback:
            return "Feedback Received"
        elif self.resubmitted:
            return "Resubmitted"
        else:
            return "Not Reviewed"

    def __str__(self):
        return f'Submission {self.id} by {self.business.username}'

class SupportingDocument(models.Model):
    compliance_submission = models.ForeignKey(ComplianceSubmission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='supporting_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Remark(models.Model):
    document = models.ForeignKey(ComplianceDocument, on_delete=models.CASCADE, related_name='remarks')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Remark for {self.document.file.name}'

class Checklist(models.Model):
    business_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklists')
    document = models.ForeignKey(ComplianceDocument, on_delete=models.CASCADE, related_name='checklists')
    compliance_rows = models.JSONField()  # Storing the checklist data as JSON
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.business_owner.username} - {self.document.file.name}'
