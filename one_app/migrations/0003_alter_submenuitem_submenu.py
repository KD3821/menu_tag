# Generated by Django 4.1.7 on 2023-03-23 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('one_app', '0002_alter_menuitem_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submenuitem',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenuitems', to='one_app.submenu'),
        ),
    ]