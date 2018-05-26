#%%
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean
FINGERPRINTS_TABLENAME = "fingerprints"
SONGS_TABLENAME = "songs"
FIELD_SONG_ID = 'song_id'
FIELD_FINGERPRINTED = 'fingerprinted'
FIELD_FILE_SHA1 = 'file_sha1'
FIELD_SONGNAME = 'song_name'
#%%
engine = create_engine(
    'postgresql://postgres:0@localhost:5432/metamusic', echo=True)
Base = declarative_base(engine)

metadata = Base.metadata
print(Base)
#%%


class songs(Base):
    __tablename__ = SONGS_TABLENAME
    FIELD_SONG_ID = Column(FIELD_SONG_ID, Integer,
                           primary_key=True, unique=True, nullable=False)
    FIELD_SONGNAME = Column(FIELD_SONGNAME, String(250), nullable=False)
    FIELD_FINGERPRINTED = Column(FIELD_FINGERPRINTED, Boolean, default=0)
    FIELD_FILE_SHA1 = Column(FIELD_FILE_SHA1, LargeBinary, nullable=False)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


metadata.create_all(engine)
