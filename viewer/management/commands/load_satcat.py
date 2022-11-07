from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from viewer.models import ObjectInfo

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from satcat.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if ObjectInfo.objects.exists():
            print('satcat data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading satcat data")

        # Code to load the data into database
        for row in DictReader(open('./satcat.csv')):
            objectinfo = ObjectInfo(object_name=row['OBJECT_NAME'], object_id=row['OBJECT_ID'],
                                    norad_cat_id=row['NORAD_CAT_ID'], object_type=row['OBJECT_TYPE'],
                                    ops_status_code=row['OPS_STATUS_CODE'], owner=row['OWNER'],
                                    launch_date=row['LAUNCH_DATE'], launch_site=row['LAUNCH_SITE'],
                                    decay_date=row['DECAY_DATE'], period=row['PERIOD'], inclination=row['INCLINATION'],
                                    apogee=row['APOGEE'], perigee=row['PERIGEE'], rcs=row['RCS'],
                                    data_status_code=row['DATA_STATUS_CODE'], orbit_center=row['ORBIT_CENTER'],
                                    orbit_type=row['ORBIT_TYPE'])
            objectinfo.save()
