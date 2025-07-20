import datetime
from typing import Optional

from sqlalchemy import BINARY, CHAR, Computed, DateTime, JSON, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Updates(Base):
    __tablename__ = 'updates'

    id: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, server_default=text('(uuid_to_bin(uuid(),1))'))
    payload: Mapped[dict] = mapped_column(JSON, server_default=text('(json_object())'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    id_text: Mapped[Optional[str]] = mapped_column(CHAR(36), Computed('(bin_to_uuid(`id`))', persisted=False))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
