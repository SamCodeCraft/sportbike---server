from sqlalchemy_serializer import SeralizerMixin
from models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


# Validators
def validate_email(email):
    # Email validation logic
    if not validate.Email()(email):
        raise ValidationError('Invalid email address.')

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bike(db.Model):
    __tablename__ = 'bike'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'description': self.description,
            'image': self.image,
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Authentication Schema
class UserSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))

# Authentication Routes
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # In a real application, you would create and return JWT tokens here.
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/logout', methods=['POST'])
def logout():
    # Since JWT is not used, there's no token to invalidate. This endpoint is just a placeholder.
    return jsonify({'message': 'Logout successful'}), 200