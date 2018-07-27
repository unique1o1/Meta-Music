# %%
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from multiprocessing import Pool, cpu_count, TimeoutError
from sqlalchemy import Column, Integer, String, Binary, Boolean, ForeignKey
from contextlib import contextmanager
import json
import sys
import time
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
    file_sha1 = Column(FIELD_FILE_SHA1, Binary(length=40), nullable=False)
# %%


class fingerprints(Base):
    __tablename__ = 'fingerprints'
    hash_id = Column('hash_id', Integer,
                     primary_key=True, unique=True, nullable=False)
    hash = Column(FIELD_HASH, Binary(length=20),
                  nullable=False, index=True)
    song_id = Column(FIELD_SONG_ID, Integer, ForeignKey(
        'songs.song_id'), nullable=False)
    offset = Column(FIELD_OFFSET, Integer, nullable=False)

    # #%%
    # metadata.create_all(engine)

    # %%


def get_song_by_id(sid):
    session = Session()
    return session.query(songs).filter(songs.song_id == sid).one_or_none()


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


def get_num_fingerprints():
    with session_withcommit() as session:
        print(session.query(fingerprints).count())


def get_num_of_songs():
    with session_withcommit() as session:
        print(session.query(songs).count())


def get_num_fingerprints_by_id(sid):
    with session_withcommit() as session:
        print(session.query(fingerprints).filter_by(song_id=sid).count())


@commit
def insert_song(file_hash, song_name):

    # print(binascii.unhexlify(hashes_sha1[num]))
    return songs(song_name=song_name, file_sha1=binascii.unhexlify(file_hash))


def insert_hashes(sid, hashes):
    with session_withcommit() as session:
        for hash, offset in set(hashes):
            session.add(fingerprints(
                hash=binascii.unhexlify(hash),
                song_id=sid,
                offset=int(offset)
            ))


def return_matches(hashes):

        # Create a dictionary of hash => offset pairs for later lookups
    mapper = {}
    values = []
    for hash, offset in hashes:
        mapper[hash] = offset
        values.append(binascii.unhexlify(hash))

    # Get an iterable of all the hashes we need
    session = Session()
    for fingerprint in session.query(fingerprints).filter(
            fingerprints.hash.in_(values)):
        hash = binascii.hexlify(fingerprint.hash).decode('utf-8')
        yield (fingerprint.song_id, fingerprint.offset - mapper[hash])

    # pool = Pool(cpu_count())
    # iterator = pool.imap(return_Matches_Pool, session.query(fingerprints).filter(
    #     fingerprints.hash.in_(values)))
    # while True:
    #     try:
    #         song_id, offset, hash = iterator.next()
    #         yield (song_id, offset-mapper[hash])
    #     except TimeoutError:
    #         continue
    #     except StopIteration:
    #         break


# def return_Matches_Pool(fingerprint):
#     return (fingerprint.song_id, fingerprint.offset,
#             binascii.hexlify(fingerprint.hash).decode('utf-8'))
