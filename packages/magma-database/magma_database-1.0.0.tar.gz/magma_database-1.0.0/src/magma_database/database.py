import os
import datetime
import pandas as pd
import shutil

from .config import config
from .resources import volcanoes_df
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List

DATABASE_DRIVER = config['DATABASE_DRIVER']


def database(db_name: str = 'magma.db') -> str:
    """Database location

    Args:
        db_name: database name. Default magma.db

    Returns:
        str: Database location
    """
    database_dir = config['DATABASE_LOCATION']
    if not os.path.isdir(database_dir):
        os.makedirs(database_dir)
    return os.path.join(database_dir, db_name)


db = SqliteDatabase(database=database(), pragmas={
    'foreign_keys': 1,
    'journal_mode': 'wal',
    'cache_size': -32 * 1000
})


def reset() -> bool | None:
    """Reset database.

    Returns:
        True | None
    """
    database_location = database()
    if os.path.exists(database_location):
        backup()

        if not db.is_closed():
            db.close()

        os.remove(database_location)
        db.connect(reuse_if_open=True)
        db.create_tables([Station, Sds, Volcano])
        db.close()
        print(f"⌛ Reset database: {database_location}")
        return True
    return None


def recreate_tables(tables=None) -> None:
    """Drop and create tables."""

    if tables is None:
        tables = [Sds, Station, Volcano]
    backup()
    print("Dropping tables...")
    db.drop_tables(tables)
    print("Creating tables...")
    db.create_tables(tables)


def backup(backup_dir: str = None) -> str | None:
    """Backup database before run

    Args:
        backup_dir: directory to back up

    Returns:
        str: backup file location
    """
    if DATABASE_DRIVER == 'sqlite':
        print("Backing up database...")
        source_database = database()
        source_filename = os.path.basename(source_database)

        if backup_dir is None:
            backup_dir = os.path.dirname(source_database)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{source_filename}-{timestamp}.bak"

        backup_database = os.path.join(backup_dir, backup_filename)
        shutil.copy(source_database, backup_database)
        print(f"Backup database saved to: {backup_database}")
        return backup_database

    print('For now, only sqlite backup is supported.')


class MagmaBaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        database = db

    @classmethod
    def recreate_table(cls, force: bool = False) -> None:
        if (not cls.table_exists()) or (force is True):
            return recreate_tables([cls])
        print(f"Table {cls._meta.table_name} already exists. "
              f"Plase use `recreate_tables(force=True)` to recreate tables.")


class Volcano(MagmaBaseModel):
    code = CharField(unique=True, max_length=3)
    name = CharField(index=True)
    type = CharField(index=True, max_length=1)
    latitude = DecimalField(max_digits=12, decimal_places=8)
    longitude = DecimalField(max_digits=12, decimal_places=8)
    elevation = FloatField(null=True)
    time_zone = CharField(default='Asia/Jakarta')
    regional = CharField(index=True)
    is_submarine = BooleanField(default=False)
    causing_tsunami = BooleanField(default=False)
    smithsonian_number = CharField(null=True)

    class Meta:
        table_name = 'volcanoes'

    @staticmethod
    def fill_database() -> None:
        dict_list = []
        df = volcanoes_df
        db.create_tables([Volcano])

        df = df.drop(columns=[
            'Code Stasiun',
            'Prioritas Pemantauan',
            'Alias',
            'District',
            'Province ID',
            'Province EN',
            'District',
            'Nearest City',
            'Sering Dikunjungi',
            'Pengelola Kawasan Gunung Api',
            'Link Pengelola',
        ])

        df = df.rename(columns={
            'Tipe': 'type',
            'Code': 'code',
            'Smithsonian Number': 'smithsonian_number',
            'Name': 'name',
            'Time Zone': 'time_zone',
            'Regional': 'regional',
            'Latitude (LU)': 'latitude',
            'Longitude (BT)': 'longitude',
            'Elevation': 'elevation',
            'Bawah Laut': 'is_submarine',
            'Pernah Menyebabkan Tsunami': 'causing_tsunami',
        })

        df['smithsonian_number'] = df['smithsonian_number'].apply(lambda x: f'{x:.0f}')
        df['is_submarine'] = df['is_submarine'].apply(lambda x: True if x == 'Ya' else False)
        df['causing_tsunami'] = df['causing_tsunami'].apply(lambda x: True if x == 'Ya' else False)

        for _, row in df.iterrows():
            dictionary = {}
            for column in df.columns:
                dictionary[column] = row[column]
                if column == 'smithsonian_number':
                    dictionary[column] = None if row[column] == 'nan' else row[column]
            dict_list.append(dictionary)

        Volcano.insert_many(dict_list).execute()
        print('Volcano database inserted successfully.')

    @staticmethod
    def to_list(code: str = None) -> List[Dict[str, Any]]:
        if code is None:
            volcanoes = [dict(volcano) for volcano in Volcano.select().dicts()]
            return volcanoes

        volcanoes = Volcano.select().where(Volcano.code == code.upper())
        volcanoes = [dict(volcano) for volcano in volcanoes.dicts()]

        if len(volcanoes) == 0:
            raise EmptyDataError(f"⛔ No data for volcanoes. Check your code parameters.")

        return volcanoes

    @staticmethod
    def to_df(code: str = None) -> pd.DataFrame:
        df = pd.DataFrame(Volcano.to_list(code=code))
        df.set_index('id', inplace=True)
        return df


class Station(MagmaBaseModel):
    nslc = CharField(index=True, unique=True, max_length=14)
    network = CharField(index=True)
    station = CharField(index=True)
    channel = CharField(index=True)
    location = CharField()

    class Meta:
        table_name = 'stations'

    @staticmethod
    def to_list(nslc: str = None) -> List[Dict[str, Any]]:
        if nslc is None:
            stations = [dict(station) for station in Station.select().dicts()]
            return stations

        stations = Station.select().where(Station.nslc == nslc.upper())
        stations = [dict(station) for station in stations.dicts()]

        if len(stations) == 0:
            raise EmptyDataError(f"⛔ No data for volcanoes. Check your code parameters.")

        return stations

    @staticmethod
    def to_df(nslc: str = None) -> pd.DataFrame:
        df = pd.DataFrame(Station.to_list(nslc))
        df.set_index('id', inplace=True)
        return df


class Sds(MagmaBaseModel):
    nslc = ForeignKeyField(Station, field='nslc', backref='sds')
    date = DateField(index=True)
    start_time = DateTimeField(index=True, null=True)
    end_time = DateTimeField(index=True, null=True)
    completeness = FloatField()
    sampling_rate = FloatField()
    file_location = CharField()
    file_size = BigIntegerField()

    class Meta:
        table_name = 'sds'
        indexes = (
            (('nslc', 'date'), True),
        )

    @staticmethod
    def to_list(nslc: str) -> List[Dict[str, Any]]:
        """Get list of SDS from database

        Returns:
            List[Dict[str, Any]]
        """
        sds_list = []

        sds_dicts = Sds.select().where(Sds.nslc == nslc.upper())
        _sds_list = [dict(sds_dict) for sds_dict in sds_dicts.dicts()]

        if len(_sds_list) == 0:
            raise EmptyDataError(f"⛔ No data for {nslc}. Check your station parameters.")

        for sds in _sds_list:
            _sds = {
                'id': sds['id'],
                'nslc': sds['nslc'],
                'date': str(sds['date']),
                'start_time': str(sds['start_time']),
                'end_time': str(sds['end_time']),
                'completeness': float(sds['completeness']),
                'sampling_rate': float(sds['sampling_rate']),
                'file_location': sds['file_location'],
                'file_size': sds['file_size'],
                'created_at': str(sds['created_at']),
                'updated_at': str(sds['updated_at']),
            }
            sds_list.append(_sds)

        return sds_list

    @staticmethod
    def to_df(nslc: str) -> pd.DataFrame:
        df = pd.DataFrame(Sds.to_list(nslc))
        df.set_index('id', inplace=True)
        return df
