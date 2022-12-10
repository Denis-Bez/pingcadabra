from datetime import datetime
from os import path

from sqlalchemy import create_engine, select, update
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  # DATETIME - For sqlite
from sqlalchemy.orm import declarative_base, Session, relationship

parent_dir = path.dirname(path.abspath(__file__))
db_path = path.join(parent_dir, 'bot_database.db')

# engine = create_engine( r'sqlite:///{}'.format(db_path), future=True)
engine = create_engine("postgresql://user:example@85.193.93.171:54321/ping_db")
#engine = create_engine("postgresql://user:example@db:5432/ping_db")
Base = declarative_base()

class Users(Base):
    __tablename__ = "users_table"
    id = Column(Integer, unique=True, primary_key=True)
    users_id = Column(Integer, unique=True, nullable=False)
    status = Column(String, default="Standart")
    first_time = Column(DateTime)
    last_time = Column(DateTime)
    favorite = relationship("Favorites", backref='users', lazy=True)
    
    def __repr__(self):
         return f"users(id={self.id!r}, users_id={self.users_id!r}, last_time={self.last_time!r})"
    
    def add_user(user_id):
        new_user = Users(
            users_id = user_id,
            first_time = datetime.now(),
            last_time = datetime.now()
            )
        with Session(engine) as session:
            session.add_all([new_user])
            session.commit()
    
    def date_update(user_id):
        with Session(engine) as session:
            current_user = session.query(Users).filter(Users.users_id==user_id).first()
            current_user.last_time = datetime.now()
            if current_user.status == "Leave":
                current_user.status = "Standart"
            session.commit()
    
    def check_user_available(user_id):
        with Session(engine) as session:
            if session.query(Users).filter(Users.users_id==user_id).first():
                return True
            return False
    
    def user_leave(user_id):
        with Session(engine) as session:
            current_user = session.query(Users).filter(Users.users_id==user_id).first()
            current_user.status = "Leave" 
            session.commit()
    
    # Return list of favorite user's adresses
    def pull_favorite(user_id):
        favorites_list = []
        with Session(engine) as session:
            user = session.query(Users).filter(Users.users_id==user_id)
            for item in user:
                for favorite in item.favorite:
                    favorites_list.append(favorite.ip)
            return favorites_list


class Favorites(Base):
    __tablename__ = "favorites_table"
    id = Column(Integer, unique=True, primary_key=True)
    ip = Column(String(100), nullable=False, unique=False)
    timer = Column(Integer, nullable=True, unique=False)
    user = Column(Integer, ForeignKey("users_table.id"))


    def __repr__(self):
         return f"favorites(id={self.id!r}, ip={self.ip!r})"
    

    def add_favorite(ip, user_id):
        with Session(engine) as session:     
            current_user = session.query(Users).filter(Users.users_id==user_id).first()
            new_fav = Favorites(ip=ip, user=current_user.id)
            session.add_all([new_fav])
            session.commit()
    

    def delete_favorite(ip, user_id):
        with Session(engine) as session:
            user = session.query(Users).filter(Users.users_id==user_id).first()
            favorite = session.query(Favorites).filter(Favorites.ip==ip, Favorites.user==user.id)
            favorite.delete(synchronize_session=False)
            session.commit()
    

    def add_timer(user_id, timer):
        with Session(engine) as session:
            user = session.query(Users).filter(Users.users_id==user_id)
            for item in user:
                for favorite in item.favorite:
                    favorite.timer = int(timer)
                    session.commit()
    

    def delete_timer(user_id):
        with Session(engine) as session:
            user = session.query(Users).filter(Users.users_id==user_id)
            for item in user:
                for favorite in item.favorite:
                    favorite.timer = None
                    session.commit()


    def get_autocheck_dict():
        all_timers = {'user_id':[], 'timer':[]}
        with Session(engine) as session:
            user = session.query(Users).all()
            for item in user:
                for favorite in item.favorite:
                    if favorite.timer:
                        all_timers['user_id'].append(item.users_id)
                        all_timers['timer'].append(favorite.timer)
                        break
                    else:
                        break
        return all_timers


# --- Creating all tables ---
if __name__ == '__main__':
    Base.metadata.create_all(engine)