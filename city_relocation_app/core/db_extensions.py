from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# database object
db = SQLAlchemy()

# login manager
login_manager = LoginManager()

# password hashing
bcrypt = Bcrypt()


# login configuration
login_manager.login_view = "auth.signin"
login_manager.login_message = "Please login to continue"


# user loader for session handling
@login_manager.user_loader
def load_user(user_id):
    from core.domain.user_entity import User
    return User.query.get(int(user_id))