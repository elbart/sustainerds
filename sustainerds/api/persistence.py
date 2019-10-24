import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

from sustainerds.api.core.persistence import BaseModel


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(cls=BaseModel, metadata=metadata)

assert "+0000" == time.strftime("%z"), (
    "This application is required to run in UTC timezone. Please update your environment, "
    "e.g. run `TZ=UTC bin/starter`."
)
