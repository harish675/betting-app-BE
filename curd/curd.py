
from sqlalchemy.exc import SQLAlchemyError
import logging
class DBOperation:  
    
    def __init__(self):
       pass   

    def create(self, data, session):
        try:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data
        except SQLAlchemyError as e:
            session.rollback()
            return None
           
        finally:
            session.close()

    def read(self, table, query,session):
        # Implement the logic to read records from the database
         result = session.query(table).filter(query).all()
         return result
    
    def read_one(self, table, query, session):
    # Use .first() to return the first matching record or None
        result = session.query(table).filter(query).first()
        return result
    
    # def update(self, table, query, data):
    #     # Implement the logic to update records in the database
    #     pass

    # def delete(self, table, query):
    #     # Implement the logic to delete records from the database
    #     pass