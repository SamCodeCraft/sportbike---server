from app import db, create_app
from app.models import Bike, User, Login

app = create_app()

with app.app_context():
    db.create_all()

    # Add some sample bikes
    bikes = [
        Bike(make="Yamaha", model="MT-09", year=2024, price=8999.99, description="A great sportbike.", image="https://ultimatemotorcycling.com/wp-content/uploads/2023/10/2024-yamaha-mt-09-first-look-fast-facts-20.webp"),
        Bike(make="BMW", model="R nineT", year=2016, price=11999.99, description="A stylish bike.", image="https://stat.overdrive.in/wp-content/uploads/2016/11/BMW-R-nineT-4.jpg"),
        Bike(make="BMW", model="R1200GS", year=2017, price=15999.99, description="A hybrid bike.", image="https://ridermagazine.com/wp-content/uploads/2017/03/BMW-R1200GS-xDrive-Hybrid-beauty.jpg")
    ]

    db.session.bulk_save_objects(bikes)

    # Add a sample user
    user = User(email="user@example.com")
    user.set_password("password")

    db.session.add(user)

    # Add a sample login
    login = Login(email="login@example.com")
    login.set_password("password")

    db.session.add(login)

    db.session.commit()
