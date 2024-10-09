from models import db, User, Bike, Login
from config import Ressource, request, jsonify, auth, app, bycrypt, api, session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registering main routes
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Sportbike World!"})

    @app.route('/engines')
    def engines():
        return jsonify({"message": "Engines Page"})

    @app.route('/parts-accessories')
    def parts_accessories():
        return jsonify({"message": "Parts & Accessories Page"})

    @app.route('/motorcycle-clothing')
    def motorcycle_clothing():
        return jsonify({"message": "Motorcycle Clothing Page"})

    @app.route('/helmets')
    def helmets():
        return jsonify({"message": "Helmets Page"})

    @app.route('/outlets')
    def outlets():
        return jsonify({"message": "Outlets Page"})

    @app.route('/store')
    def store():
        return jsonify({"message": "Store Page"})

    @app.route('/rental')
    def rental():
        return jsonify({"message": "Rental Page"})

    @app.route('/workplace')
    def workplace():
        return jsonify({"message": "Workplace Page"})

    @app.route('/news')
    def news():
        return jsonify({"message": "News Page"})

    @app.route('/contact-us')
    def contact_us():
        return jsonify({"message": "Contact Us Page"})

    # Registering bike routes
    @app.route('/api/bikes', methods=['GET'])
    def get_bikes():
        bikes = Bike.query.all()
        return jsonify([bike.to_dict() for bike in bikes])

    @app.route('/api/bikes/<int:id>', methods=['GET'])
    def get_bike(id):
        bike = Bike.query.get_or_404(id)
        return jsonify(bike.to_dict())

    @app.route('/api/bikes', methods=['POST'])
    def create_bike():
        data = request.get_json()
        if not all(key in data for key in ['make', 'model', 'year', 'price', 'image', 'description']):
            return jsonify({"error": "Missing data"}), 400
        bike = Bike(**data)
        db.session.add(bike)
        db.session.commit()
        return jsonify(bike.to_dict()), 201

    @app.route('/api/bikes/<int:id>', methods=['PUT'])
    def update_bike(id):
        data = request.get_json()
        bike = Bike.query.get_or_404(id)
        for key, value in data.items():
            setattr(bike, key, value)
        db.session.commit()
        return jsonify(bike.to_dict())

    @app.route('/api/bikes/<int:id>', methods=['DELETE'])
    def delete_bike(id):
        bike = Bike.query.get_or_404(id)
        db.session.delete(bike)
        db.session.commit()
        return '', 204

    # Registering authentication routes
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not all(key in data for key in ['email', 'password']):
            return jsonify({"error": "Missing data"}), 400
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    

    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not all(key in data for key in ['email', 'password']):
            return jsonify({"error": "Missing data"}), 400
        user = User(email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

if __name__ == '__app__':
    app = create_app()
    app.run()
