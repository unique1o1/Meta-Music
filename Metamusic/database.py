# %%
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, ForeignKey
from contextlib import contextmanager
import json
import sys
from itertools import zip_longest
import binascii
FINGERPRINTS_TABLENAME = "fingerprints"
SONGS_TABLENAME = "songs"
FIELD_SONG_ID = 'song_id'
FIELD_FINGERPRINTED = 'fingerprinted'
FIELD_FILE_SHA1 = 'file_sha1'
FIELD_SONGNAME = 'song_name'
FINGERPRINTS_TABLENAME = 'fingerprints'
FIELD_OFFSET = 'offset'
FIELD_HASH = 'hash'
# %%


try:
    with open('./Metamusic/config', 'r') as f:
        config = json.load(f)
except IOError as err:
    print("Cannot open configuration: {} Exiting".format(str(err)))
    sys.exit(1)
engine = create_engine(
    'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(**config))
Base = declarative_base(engine)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
metadata.create_all(engine)
# %%


@contextmanager
def session_withcommit():
    try:
        session = Session()
        yield session
    except Exception as e:
        raise e
    finally:
        session.commit()


def commit(func):
    '''Used as a decorator for automatically making session commits'''
    def wrap(**kwarg):
        with session_withcommit() as session:
            a = func(**kwarg)
            session.add(a)
        return session.query(songs).order_by(
            songs.song_id.desc()).first().song_id
    return wrap


class songs(Base):
    __tablename__ = SONGS_TABLENAME
    song_id = Column(FIELD_SONG_ID, Integer,
                     primary_key=True, unique=True, nullable=False)
    song_name = Column(FIELD_SONGNAME, String(250), nullable=False)
    fingerprinted = Column(FIELD_FINGERPRINTED, Boolean, default=0)
    file_sha1 = Column(FIELD_FILE_SHA1, LargeBinary, nullable=False)
# %%


class fingerprints(Base):
    __tablename__ = 'fingerprints'
    hash_id = Column('hash_id', Integer,
                     primary_key=True, unique=True, nullable=False)
    hash = Column(FIELD_HASH, LargeBinary, unique=True,
                  nullable=False, index=True)
    song_id = Column(FIELD_SONG_ID, Integer, ForeignKey(
        'songs.song_id'), unique=True, nullable=False)
    offset = Column(FIELD_OFFSET, Integer, unique=True, nullable=False)

    # #%%
    # metadata.create_all(engine)

    # %%


def get_songs():
    """
    Return songs that have the fingerprinted flag set TRUE (1).
    """
    with session_withcommit() as session:
        val = session.query(songs).all()
        for row in val:
            yield row


def set_fingerprinted_flag(id):
    with session_withcommit() as session:

        session.query(songs).filter_by(
            song_id=id).first().fingerprinted = True


def delete_unfingerprinted_songs():
    with session_withcommit() as session:
        session.query(songs).filter_by(fingerprinted=False).delete()
# %%


@commit
def insert_song(file_hash, song_name):

    # print(binascii.unhexlify(hashes_sha1[num]))
    return songs(song_name=song_name, file_sha1=binascii.unhexlify(file_hash))


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * 2
    # return (filter(None, values) for values
    #         in zip_longest(fillvalue=fillvalue, *args))


def insert_hashes(sid, hashes):

    values = []
    for hash, offset in hashes:
        values.append((hash, sid, offset))
    grouper(values, 1000)

    # for split_values in grouper(values, 1000):
    #         cur.executemany(self.INSERT_FINGERPRINT, split_values)
