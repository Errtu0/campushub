# Campus Event & Club Management System

A full-featured Django web application for managing university clubs and campus events with Role-Based Access Control (RBAC).

## Features

- **3 User Roles:** Student, Club Manager, Admin
- **Custom User Model** with profile pictures
- **Club Management:** Create, approve, join/leave clubs with logo uploads
- **Event Management:** Create, edit, delete events with participant limits
- **Event Registration:** Register/cancel with duplicate & capacity checks
- **Admin Dashboard:** Approve/reject clubs, manage users and roles
- **Bootstrap 5 UI** — responsive, clean, reusable templates

## Tech Stack

- Python 3 + Django
- SQLite (default)
- Django Templates + Forms
- Django Authentication System
- Bootstrap 5

---

## Setup Instructions

### 1. Clone / unzip the project

```bash
cd campus_event_system
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (Admin)

```bash
python manage.py createsuperuser
```

After creating the superuser, log in and set their role to `admin` via the Django admin panel at `/admin/` or via the Admin > Manage Users page.

**Quick way to make yourself admin via shell:**
```bash
python manage.py shell
>>> from users.models import CustomUser
>>> u = CustomUser.objects.get(username='your_superuser_name')
>>> u.role = 'admin'
>>> u.save()
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## User Roles & Permissions

| Feature | Student | Club Manager | Admin |
|---|---|---|---|
| View clubs/events | ✅ | ✅ | ✅ |
| Join/leave clubs | ✅ | ✅ | ✅ |
| Register for events | ✅ | ✅ | ✅ |
| Create clubs | ❌ | ✅ | ✅ |
| Create events | ❌ | Own clubs only | ✅ |
| Edit clubs | ❌ | Own clubs only | ✅ |
| Edit events | ❌ | Own events only | ✅ |
| Approve clubs | ❌ | ❌ | ✅ |
| Manage users / change roles | ❌ | ❌ | ✅ |

## Pages

| URL | Page |
|---|---|
| `/` | Home |
| `/users/register/` | Register |
| `/users/login/` | Login |
| `/users/profile/` | My Profile |
| `/users/profile/edit/` | Edit Profile |
| `/clubs/` | Club List |
| `/clubs/<id>/` | Club Detail |
| `/clubs/create/` | Create Club (Manager+) |
| `/clubs/dashboard/` | Manager Dashboard |
| `/clubs/admin/approval/` | Admin Approval Dashboard |
| `/events/` | Event List (with search) |
| `/events/<id>/` | Event Detail |
| `/events/create/` | Create Event (Manager+) |
| `/users/admin/users/` | Manage Users (Admin) |

## Authorization Enforcement

- `@login_required` decorator on all protected views
- Role checks at the top of every sensitive view
- `HttpResponseForbidden` returned for unauthorized access
- Queryset filtering (managers only see their own clubs/events)
- Template-level restrictions (buttons only shown to authorized roles)

## Bonus Features Implemented

- Event search/filter
- Pagination (events list)
- Profile picture upload
- Club logo upload
- Participant list for club managers
