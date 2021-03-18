# Generated by Django 3.1.6 on 2021-03-18 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_insert_konkurz_vyrovnanie_issues'),
    ]

    operations = [
        migrations.RunSQL("INSERT INTO ov.companies_companies (cin, name, address_line, created_at, "
                          "updated_at, last_update) SELECT DISTINCT ON (cin) "
                          "cin, "
                          "corporate_body_name, "
                          "concat_ws(' ', concat_ws(', ', street, postal_code), city), "
                          "created_at, "
                          "updated_at, "
                          "max(updated_at) "
                          "OVER(PARTITION BY cin ORDER BY updated_at DESC) "
                          "FROM ov.konkurz_restrukturalizacia_actors WHERE cin IS NOT NULL ON CONFLICT (cin) DO NOTHING;")
    ]