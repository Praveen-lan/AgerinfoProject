# AGERinfo

Agriculture Information Hub for Indian farmers. Provides farming tips, news, photo galleries, and educational topics about crop management, irrigation, weed control, and more.

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: Django 5+ with Django REST Framework
- **Database**: MySQL
- **Image Hosting**: ImgBB API

## Setup

### 1. Clone and install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 3. Setup database

Create a MySQL database and run migrations:

```bash
python manage.py migrate
```

### 4. Create admin user

```bash
python manage.py create_admin --email admin@agerinfo.com --password yourpassword
```

### 5. Run the server

```bash
python manage.py runserver
```

### 6. Open frontend

Open `index.html` in your browser (use Live Server in VS Code).

Open `admin.html` for the admin panel.

## Project Structure

```
Agriinfo/
  index.html          # Public website
  admin.html          # Admin CMS panel
  api.js              # Frontend API client
  api-config.js       # API configuration
  backend/
    manage.py
    requirements.txt
    agerinfo_backend/  # Django project
    api/               # REST API app
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/counts/` | No | Dashboard counts |
| POST | `/api/auth/login/` | No | Login, get token |
| POST | `/api/auth/logout/` | Yes | Logout |
| GET | `/api/news/` | No | List news |
| POST | `/api/news/create/` | Yes | Create news |
| PATCH | `/api/news/{id}/update/` | Yes | Update news |
| DELETE | `/api/news/{id}/delete/` | Yes | Delete news |
| GET | `/api/gallery/` | No | List gallery |
| POST | `/api/gallery/create/` | Yes | Create gallery item |
| PATCH | `/api/gallery/{id}/update/` | Yes | Update gallery item |
| DELETE | `/api/gallery/{id}/delete/` | Yes | Delete gallery item |
| GET | `/api/slider/` | No | List slider images |
| POST | `/api/slider/create/` | Yes | Create slider image |
| PATCH | `/api/slider/{id}/update/` | Yes | Update slider image |
| DELETE | `/api/slider/{id}/delete/` | Yes | Delete slider image |
| GET | `/api/topics/` | No | List topics |
| POST | `/api/topics/create/` | Yes | Create topic |
| PATCH | `/api/topics/{id}/update/` | Yes | Update topic |
| DELETE | `/api/topics/{id}/delete/` | Yes | Delete topic |

## Running Tests

```bash
cd backend
python manage.py test api
```
