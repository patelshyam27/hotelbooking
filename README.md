# CrickConnect - Cricket Community Platform 🏏

CrickConnect is a comprehensive web-based platform designed to unite cricket enthusiasts by providing tools for player discovery, community building, coaching services, live match streaming, and cricket equipment shopping. Built with Flask and modern web technologies, it serves as a one-stop solution for the cricket community.

## 🌟 Features

### 🏏 Player Discovery & Networking
- **Location-Based Search**: Find cricket players by state, city, and area
- **Role-Based Filtering**: Search by cricket roles (batsman, bowler, all-rounder, wicket-keeper)
- **Social Networking**: Follow/unfollow system for building connections
- **Direct Communication**: WhatsApp integration for instant player contact
- **Privacy Controls**: Profile view tracking with search-based access

### 👥 User Management System
- **User Registration**: Comprehensive profile creation with cricket-specific details
- **Authentication**: Secure login/logout with session management
- **Profile Management**: Editable profiles with age, location, availability, and contact info
- **Gender Diversity**: Inclusive gender options and filtering

### 🎯 Admin & Content Management
- **Dual Admin System**: Owner dashboard and approved admin management
- **Content Creation**: Tools for managing coaching ads, live matches, and store products
- **User Administration**: Complete user management with search, filtering, and status control
- **Analytics Dashboard**: Statistics and platform insights

### 🏆 Coaching Services
- **Coaching Advertisements**: Create and browse coaching opportunities
- **Location-Based Coaching**: Find coaching services in specific areas
- **Discount System**: Coupon codes and discount percentages
- **Contact Integration**: Direct contact with coaches via WhatsApp

### 📺 Live Match Streaming
- **YouTube Integration**: Embed live cricket matches
- **Match Management**: Add, edit, and delete live match streams
- **Team Information**: Display team details and match descriptions
- **Live Status**: Toggle live/offline status for matches

### 🛒 Cricket Store
- **Product Catalog**: Browse cricket equipment and accessories
- **Category Filtering**: Organize products by type (bat, ball, gloves, etc.)
- **Search Functionality**: Find products by name and description
- **Affiliate Links**: Support for external product links
- **Stock Management**: Track product availability

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CrickConnect
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The first registered user automatically becomes the platform owner

## 🏗️ Technical Architecture

### Backend Stack
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy ORM with SQLite (PostgreSQL compatible)
- **Authentication**: Flask-Login for session management
- **Security**: Werkzeug password hashing and security utilities

### Frontend Technologies
- **Template Engine**: Jinja2
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JS with Bootstrap components
- **Responsive Design**: Mobile-first approach

### Database Models
- **User**: Player profiles with location hierarchy and cricket details
- **Follow**: Many-to-many relationships for social networking
- **ProfileView**: Track profile visits for privacy and analytics
- **Coaching**: Coaching service advertisements with location and pricing
- **LiveMatch**: Live cricket match streaming with YouTube integration
- **StoreProduct**: Cricket equipment catalog with affiliate links

## 👥 User Roles & Permissions

### 🏏 Regular Users
- Create and manage personal cricket profiles
- Search and connect with local players
- Follow/unfollow other players
- View coaching services and store products
- Contact players via WhatsApp

### 👨‍💼 Admins (Approved)
- Manage coaching advertisements
- Create and manage live match streams
- Add and manage store products
- View content analytics

### 🔑 Owner (Super Admin)
- All admin capabilities
- User management and moderation
- Admin approval and management
- Platform-wide analytics and control
- Full system administration

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///crickconnect.db
# For production, use PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/crickconnect
```

### Database Setup
The application automatically creates the database and tables on first run. For production deployment:

1. **SQLite** (Default): No additional setup required
2. **PostgreSQL**: Update the `DATABASE_URL` in your environment variables

## 📱 Key Features Walkthrough

### Player Registration
1. Comprehensive profile creation with cricket-specific fields
2. Location hierarchy (State → City → Area)
3. Cricket role selection and availability settings
4. Contact information with WhatsApp integration

### Player Discovery
1. Advanced search with multiple filters
2. Location-based player matching
3. Role and gender-based filtering
4. Follow/unfollow social features

### Admin Dashboard
1. Platform statistics and analytics
2. Content management tools
3. User administration (Owner only)
4. Quick action buttons for content creation

### Coaching Services
1. Create detailed coaching advertisements
2. Location-based coaching discovery
3. Pricing with discount system
4. Direct coach contact via WhatsApp

### Live Streaming
1. YouTube video embedding
2. Team vs team match display
3. Live status management
4. Auto-refresh for new matches

### Cricket Store
1. Product catalog with categories
2. Image and description support
3. Affiliate link integration
4. Stock status management

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Environment Setup for Production
- Set `SECRET_KEY` to a secure random string
- Use PostgreSQL for the database
- Configure proper HTTPS/SSL
- Set up proper logging and monitoring

## 🔒 Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask-Login secure sessions
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Built-in Flask security features
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📊 Analytics & Insights

The platform provides various analytics:
- Total user count and growth
- Content statistics (coaching, matches, products)
- Profile view tracking
- Follow/follower relationships
- Admin activity monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

## 🚀 Future Enhancements

- Mobile app development (React Native/Flutter)
- Advanced match scheduling and tournament management
- Payment gateway integration for coaching services
- Video coaching platform integration
- AI-powered player recommendations
- Team formation algorithms
- Rating and review systems
- Real-time chat and messaging
- Push notifications
- Advanced analytics and reporting

---

**CrickConnect - Bringing the cricket community together, one connection at a time!** 🏏

Built with ❤️ for cricket enthusiasts worldwide.
