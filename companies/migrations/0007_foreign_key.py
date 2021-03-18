# Generated by Django 3.1.6 on 2021-03-18 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_insert_konkurz_restrukturalizacia_actors'),
    ]

    operations = [
        migrations.RunSQL(sql='ALTER TABLE ov.or_podanie_issues ADD CONSTRAINT fk_companies FOREIGN KEY (cin) '
                          'REFERENCES ov.companies_companies ON UPDATE CASCADE ON DELETE CASCADE;',
                          reverse_sql='ALTER TABLE ov.or_podanie_issues DROP CONSTRAINT IF EXISTS fk_companies;'),

        migrations.RunSQL(sql='ALTER TABLE ov.znizenie_imania_issues ADD CONSTRAINT fk_companies FOREIGN KEY (cin) '
                          'REFERENCES ov.companies_companies ON UPDATE CASCADE ON DELETE CASCADE;',
                          reverse_sql='ALTER TABLE ov.znizenie_imania_issues DROP CONSTRAINT IF EXISTS fk_companies;'),

        migrations.RunSQL(sql='ALTER TABLE ov.likvidator_issues ADD CONSTRAINT fk_companies FOREIGN KEY (cin) '
                          'REFERENCES ov.companies_companies ON UPDATE CASCADE ON DELETE CASCADE;',
                          reverse_sql='ALTER TABLE ov.likvidator_issues DROP CONSTRAINT IF EXISTS fk_companies;'),

        migrations.RunSQL(sql='ALTER TABLE ov.konkurz_vyrovnanie_issues ADD CONSTRAINT fk_companies FOREIGN KEY (cin) '
                          'REFERENCES ov.companies_companies ON UPDATE CASCADE ON DELETE CASCADE;',
                          reverse_sql='ALTER TABLE ov.konkurz_vyrovnanie_issues DROP CONSTRAINT '
                                      'IF EXISTS fk_companies;'),

        migrations.RunSQL(sql='ALTER TABLE ov.konkurz_restrukturalizacia_actors ADD CONSTRAINT fk_companies '
                          'FOREIGN KEY (cin) REFERENCES ov.companies_companies ON UPDATE CASCADE ON DELETE CASCADE;',
                          reverse_sql='ALTER TABLE ov.konkurz_restrukturalizacia_actors DROP CONSTRAINT '
                                      'IF EXISTS fk_companies;')
    ]
