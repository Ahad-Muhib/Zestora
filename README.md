# 🍳 Zestora - Recipe Sharing Platform

A modern, feature-rich recipe sharing platform built with Django that brings food enthusiasts together to discover, share, and discuss culinary creations.

![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 User Management
- **User Registration & Authentication** - Secure signup/login system
- **User Profiles** - Customizable profiles with bio, location, and profile pictures
- **Social Authentication** - Google OAuth integration
- **Profile Statistics** - Track recipes, comments, likes, and activity

### 🍽️ Recipe Management
- **Recipe Creation** - Rich text editor with image uploads
- **Recipe Categories** - Organized categorization system
- **Recipe Search** - Find recipes by title, ingredients, or category
- **Recipe Editing** - Full CRUD operations for recipe authors
- **PDF Export** - Download recipes as beautifully formatted PDFs

### 💬 Social Features
- **Comments System** - Threaded discussions on recipes
- **Like/Dislike System** - Rate recipes with thumbs up/down
- **Recipe Bookmarking** - Save favorite recipes for later
- **Recipe Sharing** - Share recipes via direct links
- **Community Engagement** - Interactive discussions and feedback

### 👨‍🍳 Community Features
- **Chef Profiles** - Dedicated pages for cooking enthusiasts
- **Member Directory** - Browse community members
- **Activity Tracking** - Monitor user engagement and contributions
- **Recipe Collections** - Curated lists of related recipes

### 🎨 User Experience
- **Responsive Design** - Mobile-first, works on all devices
- **Modern UI** - Clean, intuitive interface with Bootstrap 5
- **Real-time Updates** - AJAX-powered interactions
- **Image Optimization** - Efficient media handling
- **Fast Loading** - Optimized performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- pip (Python package manager)
- Virtual environment support

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ahad-Muhib/Zestora.git
   cd Zestora
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Linux/macOS (bash/zsh):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
   **Linux/macOS (fish shell):**
   ```bash
   python -m venv venv
   source venv/bin/activate.fish
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 🏗️ Project Structure

```
Zestora/
├── community/          # Community features and member management
├── recipes/            # Core recipe functionality
│   ├── models.py      # Recipe, Comment, Like models
│   ├── views.py       # Recipe views and API endpoints
│   ├── forms.py       # Recipe and comment forms
│   └── migrations/    # Database migrations
├── userprofile/        # User profile management
├── tips/              # Cooking tips and guides
├── templates/         # HTML templates
│   ├── recipes/       # Recipe-specific templates
│   ├── userprofile/   # Profile templates
│   └── community/     # Community templates
├── static/            # CSS, JavaScript, images
├── media/             # User-uploaded content
├── zestora/           # Main project settings
└── requirements.txt   # Python dependencies
```

## 🛠️ Technology Stack

- **Backend:** Django 5.2.6, Python 3.x
- **Frontend:** Bootstrap 5.3.0, JavaScript (ES6+), HTML5, CSS3
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Authentication:** Django Auth + Google OAuth
- **File Storage:** Django file handling with WhiteNoise
- **PDF Generation:** WeasyPrint
- **Image Processing:** Pillow
- **Deployment:** Render, Gunicorn, WhiteNoise

## 📱 Key Functionalities

### Recipe Management
- Create recipes with ingredients, instructions, and images
- Categorize recipes for easy discovery
- Edit and delete your own recipes
- Search and filter recipes

### Social Interactions
- Comment on recipes with threaded discussions
- Like or dislike recipes
- Save recipes to personal collection
- Share recipes with others

### User Profiles
- Customize profile with photo and bio
- View personal statistics (recipes, comments, likes)
- Track cooking activity and engagement
- Manage saved recipes

### Content Organization
- Browse recipes by categories
- Discover featured recipes
- Access cooking tips and guides
- Explore community members

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add credentials to Django admin under Social Applications

## 🚢 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static file serving
5. Set environment variables
6. Run `python manage.py collectstatic`

### Render Deployment
The project includes `build.sh` for easy Render deployment:
1. Connect repository to Render
2. Set build command: `./build.sh`
3. Set start command: `gunicorn zestora.wsgi:application`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Ahad Muhib** - [@Ahad-Muhib](https://github.com/Ahad-Muhib)
- **Minazur Rahman** - [@Minazur-Rahman](https://github.com/MinazurRahman)


## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- All contributors and testers who helped improve the platform

## 📧 Support

For support, email [muhibalahad@gmail.com] or open an issue on GitHub.

## 🔗 Links

- [Live Demo](https://zestora-1.onrender.com/)
- [Documentation](https://github.com/Ahad-Muhib/Zestora/wiki)
- [Issues](https://github.com/Ahad-Muhib/Zestora/issues)

---

Made with ❤️ by food enthusiasts, for food enthusiasts.