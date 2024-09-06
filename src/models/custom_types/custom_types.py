from typing import Annotated

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

int_pk_T = Annotated[int, mapped_column(Integer, primary_key=True)]
