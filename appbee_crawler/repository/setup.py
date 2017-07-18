from sqlalchemy import String, Column, Integer, create_engine, Numeric, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Setup():
    def getEngine(self):
        engine = create_engine('sqlite:///./sample.db', echo=True)
        Base.metadata.create_all(engine)
        return engine

class Category(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return "<Category(id='%s', title='%s'>" % (self.id, self.title)

class App(Base):
    __tablename__ = 'apps'

    package_name = Column(String, primary_key=True)
    app_name = Column(String)
    app_price = Column(Integer)
    category_id = Column(String)
    contents_rating = Column(String)
    description = Column(String)
    developer = Column(String)
    star = Column(Numeric(2, 1))
    installs_min = Column(BigInteger)
    installs_max = Column(BigInteger)
    review_count = Column(Integer)
    updated_date = Column(String)
    inapp_price_min = Column(Integer)
    inapp_price_max = Column(Integer)

    def __repr__(self):
        return "<App(package_name = '%s',app_name = '%s' ,app_price = '%s' ,category_id = '%s' ,contents_rating = '%s',description = '%s',developer = '%s',star = '%s',installsMin = '%s',installsMax = '%s',review_count = '%s', updated_date = '%s')>" \
               % (self.package_name, self.app_name, self.app_price, self.category_id, self.contents_rating, self.description, self.developer, self.star, self.installs_min, self.installs_max, self.review_count, self.updated_date_date)
