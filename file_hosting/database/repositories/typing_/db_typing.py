from typing import TypeAlias


from sqlalchemy.orm import Session


__all__ = ['DbSession']


DbSession: TypeAlias = Session
