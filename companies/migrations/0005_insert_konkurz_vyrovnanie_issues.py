# Generated by Django 3.1.6 on 2021-03-18 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_insert_likvidator_issues'),
    ]

    operations = [
        migrations.RunSQL(sql="INSERT INTO ov.companies_companies (cin, name, address_line, created_at, "
                          "updated_at, last_update) SELECT DISTINCT ON (cin) "
                          "cin, "
                          "corporate_body_name, "
                          "concat_ws(' ', concat_ws(', ', street, postal_code), city), "
                          "created_at, "
                          "updated_at, "
                          "max(updated_at) "
                          "OVER(PARTITION BY cin ORDER BY updated_at DESC) "
                          "FROM ov.konkurz_vyrovnanie_issues WHERE cin IS NOT NULL ON CONFLICT (cin) DO NOTHING;",
                          reverse_sql='DROP TABLE IF EXISTS ov.companies_companies;')
    ]
