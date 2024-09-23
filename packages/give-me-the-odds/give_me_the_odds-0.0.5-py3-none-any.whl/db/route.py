from sqlalchemy import Column, Integer, String

from db.db import Base


class Route(Base):
    __tablename__ = "routes"
    origin = Column(String(1000), primary_key=True, nullable=False)
    destination = Column(String(1000), primary_key=True, nullable=False)
    travel_time = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Route origin={self.origin} destination={self.destination} travel_time={self.travel_time}"
