# Generated manually
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extra_classes', '0001_initial'),
        ('courses', '0004_alter_course_id_alter_coursecategory_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]
