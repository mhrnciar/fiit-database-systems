# Generated by Django 3.1.6 on 2021-03-18 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_insert_or_podanie_issues'),
    ]

    operations = [
        migrations.RunSQL(sql="WITH query AS (SELECT cin, "
                          "corporate_body_name, "
                          "br_section, "
                          "concat_ws(' ', concat_ws(', ', street, postal_code), city) address, "
                          "updated_at, "
                          "row_number() OVER(PARTITION BY cin ORDER BY updated_at DESC) AS row "
                          "FROM ov.znizenie_imania_issues WHERE cin IS NOT NULL) "
                          "INSERT INTO ov.companies "
                          "(cin, name, br_section, address_line, created_at, updated_at, last_update) "
                          "SELECT cin, corporate_body_name, br_section, address, current_timestamp, "
                          "current_timestamp, updated_at FROM query WHERE row = 1 ON CONFLICT DO NOTHING;",
                          reverse_sql='DROP TABLE IF EXISTS ov.companies;')
    ]
