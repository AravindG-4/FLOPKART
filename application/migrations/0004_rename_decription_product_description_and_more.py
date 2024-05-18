# Generated by Django 5.0.4 on 2024-05-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_brand_category_product_productimage_seller_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='decription',
            new_name='description',
        ),
        migrations.AddField(
            model_name='brand',
            name='top_subCategories',
            field=models.ManyToManyField(blank=True, related_name='subCats', to='application.subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='colour',
            field=models.CharField(default='Not Mentioned', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], default='M', max_length=3),
        ),
        migrations.AlterField(
            model_name='brand',
            name='top_categories',
            field=models.ManyToManyField(blank=True, related_name='cats', to='application.category'),
        ),
    ]