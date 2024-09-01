# Generated by Django 5.0.6 on 2024-08-01 04:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compliance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('compliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliance')),
            ],
        ),
        migrations.CreateModel(
            name='ComplianceDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='compliance_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compliance_documents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compliance_rows', models.JSONField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('business_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='compliance.compliancedocument')),
            ],
        ),
        migrations.CreateModel(
            name='ComplianceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement_section_category', models.CharField(max_length=255)),
                ('assessment', models.TextField()),
                ('in_compliance', models.BooleanField(default=False)),
                ('not_compliance', models.BooleanField(default=False)),
                ('compliance_remarks', models.TextField(blank=True, null=True)),
                ('business_remarks', models.TextField(blank=True, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliancedocument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComplianceSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_document', models.FileField(blank=True, null=True, upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('resubmitted', models.BooleanField(default=False)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('compliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliancedocument')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('compliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('staff', 'Staff'), ('business', 'Business')], default='business', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
                ('status_message', models.CharField(default='Has not started reviewing', max_length=255)),
                ('compliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remarks', to='compliance.compliancedocument')),
            ],
        ),
        migrations.AddField(
            model_name='compliance',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.standard'),
        ),
        migrations.CreateModel(
            name='StandardSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.standard')),
            ],
        ),
        migrations.CreateModel(
            name='SupportingDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='supporting_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('compliance_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.compliancesubmission')),
            ],
        ),
        migrations.CreateModel(
            name='Uploader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
