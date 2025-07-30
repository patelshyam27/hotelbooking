from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from urllib.parse import quote

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cricket-connect-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crickconnect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    area = db.Column(db.String(50))
    cricket_role = db.Column(db.String(50))  # batsman, bowler, all-rounder, wicket-keeper
    availability = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    bio = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)
    admin_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')
    profile_views = db.relationship('ProfileView', backref='viewed_user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(f)

    def unfollow(self, user):
        f = self.following.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProfileView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    viewed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    viewer = db.relationship('User', foreign_keys=[viewer_id])

class Coaching(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    coach_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    area = db.Column(db.String(50))
    price = db.Column(db.Float)
    discount_percentage = db.Column(db.Integer, default=0)
    coupon_code = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    contact_whatsapp = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class LiveMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    team1 = db.Column(db.String(100))
    team2 = db.Column(db.String(100))
    description = db.Column(db.Text)
    youtube_url = db.Column(db.String(500))
    is_live = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StoreProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # bat, ball, gloves, pads, helmet, etc.
    price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    affiliate_link = db.Column(db.String(500))
    in_stock = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    live_matches = LiveMatch.query.filter_by(is_live=True).limit(3).all()
    coaching_ads = Coaching.query.filter_by(is_active=True).limit(3).all()
    return render_template('index.html', recent_users=recent_users, live_matches=live_matches, coaching_ads=coaching_ads)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        age = request.form.get('age', type=int)
        gender = request.form['gender']
        state = request.form['state']
        city = request.form['city']
        area = request.form['area']
        cricket_role = request.form['cricket_role']
        availability = request.form['availability']
        phone = request.form['phone']
        whatsapp = request.form['whatsapp']
        bio = request.form['bio']

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email, full_name=full_name, age=age, gender=gender,
                   state=state, city=city, area=area, cricket_role=cricket_role, availability=availability,
                   phone=phone, whatsapp=whatsapp, bio=bio)
        user.set_password(password)
        
        # First user becomes owner
        if User.query.count() == 0:
            user.is_owner = True
            user.is_admin = True
            user.admin_approved = True
        
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    following_count = current_user.get_following_count()
    followers_count = current_user.get_followers_count()
    profile_views = current_user.profile_views.count()
    
    # Recent activity
    recent_followers = User.query.join(Follow, User.id == Follow.follower_id)\
                          .filter(Follow.followed_id == current_user.id)\
                          .order_by(Follow.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', following_count=following_count, 
                         followers_count=followers_count, profile_views=profile_views,
                         recent_followers=recent_followers)

@app.route('/players')
def players():
    page = request.args.get('page', 1, type=int)
    state = request.args.get('state', '')
    city = request.args.get('city', '')
    area = request.args.get('area', '')
    role = request.args.get('role', '')
    gender = request.args.get('gender', '')
    search = request.args.get('search', '')

    query = User.query

    if state:
        query = query.filter(User.state.ilike(f'%{state}%'))
    if city:
        query = query.filter(User.city.ilike(f'%{city}%'))
    if area:
        query = query.filter(User.area.ilike(f'%{area}%'))
    if role:
        query = query.filter(User.cricket_role == role)
    if gender:
        query = query.filter(User.gender == gender)
    if search:
        query = query.filter(User.full_name.ilike(f'%{search}%') | 
                           User.username.ilike(f'%{search}%'))

    players = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)

    return render_template('players.html', players=players, 
                         state=state, city=city, area=area, role=role, gender=gender, search=search)

@app.route('/player/<int:user_id>')
def player_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    # Track profile view
    if current_user.is_authenticated and current_user.id != user.id:
        existing_view = ProfileView.query.filter_by(viewer_id=current_user.id, viewed_id=user.id).first()
        if not existing_view:
            view = ProfileView(viewer_id=current_user.id, viewed_id=user.id)
            db.session.add(view)
            db.session.commit()
    
    is_following = current_user.is_following(user) if current_user.is_authenticated else False
    followers_count = user.get_followers_count()
    following_count = user.get_following_count()
    
    return render_template('player_profile.html', user=user, is_following=is_following,
                         followers_count=followers_count, following_count=following_count)

@app.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('player_profile', user_id=user_id))
    
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.full_name}!')
    return redirect(url_for('player_profile', user_id=user_id))

@app.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {user.full_name}!')
    return redirect(url_for('player_profile', user_id=user_id))

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form['full_name']
        current_user.age = request.form.get('age', type=int)
        current_user.gender = request.form['gender']
        current_user.state = request.form['state']
        current_user.city = request.form['city']
        current_user.area = request.form['area']
        current_user.cricket_role = request.form['cricket_role']
        current_user.availability = request.form['availability']
        current_user.phone = request.form['phone']
        current_user.whatsapp = request.form['whatsapp']
        current_user.bio = request.form['bio']
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('player_profile', user_id=current_user.id))
    
    return render_template('edit_profile.html')

@app.route('/coaching')
def coaching():
    page = request.args.get('page', 1, type=int)
    state = request.args.get('state', '')
    city = request.args.get('city', '')
    search = request.args.get('search', '')

    query = Coaching.query.filter_by(is_active=True)

    if state:
        query = query.filter(Coaching.state.ilike(f'%{state}%'))
    if city:
        query = query.filter(Coaching.city.ilike(f'%{city}%'))
    if search:
        query = query.filter(Coaching.title.ilike(f'%{search}%') | 
                           Coaching.description.ilike(f'%{search}%'))

    coaching_ads = query.order_by(Coaching.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False)

    return render_template('coaching.html', coaching_ads=coaching_ads,
                         state=state, city=city, search=search)

@app.route('/live-matches')
def live_matches():
    matches = LiveMatch.query.filter_by(is_live=True).order_by(LiveMatch.created_at.desc()).all()
    return render_template('live_matches.html', matches=matches)

@app.route('/store')
def store():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    query = StoreProduct.query.filter_by(in_stock=True)

    if category:
        query = query.filter(StoreProduct.category == category)
    if search:
        query = query.filter(StoreProduct.name.ilike(f'%{search}%') | 
                           StoreProduct.description.ilike(f'%{search}%'))

    products = query.order_by(StoreProduct.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)

    categories = ['bat', 'ball', 'gloves', 'pads', 'helmet', 'shoes', 'kit', 'accessories']

    return render_template('store.html', products=products, categories=categories,
                         category=category, search=search)

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not (current_user.is_admin and current_user.admin_approved) and not current_user.is_owner:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_coaching = Coaching.query.count()
    total_matches = LiveMatch.query.count()
    total_products = StoreProduct.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', total_users=total_users,
                         total_coaching=total_coaching, total_matches=total_matches,
                         total_products=total_products, recent_users=recent_users)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_owner:
        flash('Access denied. Owner privileges required.')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(User.full_name.ilike(f'%{search}%') | 
                           User.username.ilike(f'%{search}%') |
                           User.email.ilike(f'%{search}%'))
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users, search=search)

@app.route('/admin/approve-admin/<int:user_id>')
@login_required
def approve_admin(user_id):
    if not current_user.is_owner:
        flash('Access denied. Owner privileges required.')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    user.admin_approved = True
    db.session.commit()
    flash(f'{user.full_name} has been approved as admin!')
    return redirect(url_for('admin_users'))

@app.route('/admin/coaching/add', methods=['GET', 'POST'])
@login_required
def add_coaching():
    if not (current_user.is_admin and current_user.admin_approved) and not current_user.is_owner:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        coaching = Coaching(
            title=request.form['title'],
            description=request.form['description'],
            coach_name=request.form['coach_name'],
            location=request.form['location'],
            state=request.form['state'],
            city=request.form['city'],
            area=request.form['area'],
            price=float(request.form['price']) if request.form['price'] else None,
            discount_percentage=int(request.form['discount_percentage']) if request.form['discount_percentage'] else 0,
            coupon_code=request.form['coupon_code'],
            contact_phone=request.form['contact_phone'],
            contact_whatsapp=request.form['contact_whatsapp'],
            created_by=current_user.id
        )
        db.session.add(coaching)
        db.session.commit()
        flash('Coaching ad added successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_coaching.html')

@app.route('/admin/match/add', methods=['GET', 'POST'])
@login_required
def add_match():
    if not (current_user.is_admin and current_user.admin_approved) and not current_user.is_owner:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        match = LiveMatch(
            title=request.form['title'],
            team1=request.form['team1'],
            team2=request.form['team2'],
            description=request.form['description'],
            youtube_url=request.form['youtube_url'],
            is_live=bool(request.form.get('is_live')),
            created_by=current_user.id
        )
        db.session.add(match)
        db.session.commit()
        flash('Live match added successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_match.html')

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not (current_user.is_admin and current_user.admin_approved) and not current_user.is_owner:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        product = StoreProduct(
            name=request.form['name'],
            description=request.form['description'],
            category=request.form['category'],
            price=float(request.form['price']) if request.form['price'] else None,
            image_url=request.form['image_url'],
            affiliate_link=request.form['affiliate_link'],
            in_stock=bool(request.form.get('in_stock')),
            created_by=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_product.html')

# Helper function for WhatsApp links
@app.template_filter('whatsapp_link')
def whatsapp_link(phone, message="Hi! I found your profile on CrickConnect."):
    if phone:
        clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
        encoded_message = quote(message)
        return f"https://wa.me/{clean_phone}?text={encoded_message}"
    return "#"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)