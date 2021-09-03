# -*- coding: utf-8 -*-

from sqlmodel import create_engine

# init engine
engine = create_engine(
    url="sqlite:///data/scitizen.db", connect_args={"check_same_thread": False}
)
