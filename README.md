

# Django Vercel Deployment

This guide explains how to deploy a Django project on Vercel, including explanations for the various configurations.

## Prerequisites

- Python 3.12+
- Django
- Vercel account

## Deployment Steps

### 1. Modify `wsgi.py`

In the file `./project/wsgi.py`, ensure you have the following code:

```python
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

app = get_wsgi_application()  # Add this line
```

**Reason:** The line `app = get_wsgi_application()` is added to ensure that Vercel can correctly interact with your Django application.

### 2. Configure `settings.py`

- **Allow Hosts**

  Update `ALLOWED_HOSTS` in the file `./project/settings.py`:

```python
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]
```

  **Reason:** `ALLOWED_HOSTS` specifies which domains are allowed to access your site. Adding `.vercel.app` allows Vercel to access your project.

- **Comment Out `DATABASES`**

  Comment out the `DATABASES` configuration:

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

  **Reason:** Vercel uses a different database setup. Commenting out the SQLite configuration prevents potential issues related to the database setup in the deployment environment.

- **Static Files Configuration**

  Configure static files settings:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [Path.joinpath(BASE_DIR, 'static')]
STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles_build', 'static')
```

  **Reason:** These settings help Django locate where static files (such as CSS, JavaScript, images) are stored. Vercel will collect and serve these static files.

- **Template Configuration**

  Set up template configuration:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

  **Reason:** This configuration allows Django to find and use template files located in the `templates` directory of your project.

### 3. Create `build_files.sh`

Create a file named `build_files.sh` with the following content:

```sh
echo "Building the project..."
python3.12 -m pip install -r requirements.txt

echo "Collect Static..."
python3.12 manage.py collectstatic --noinput --clear
```

**Reason:** This script installs necessary dependencies and collects all static files before deployment.

### 4. Create `vercel.json`

Create a file named `vercel.json` with the following content. Replace `<project_name>` with your Django project name:

```json
{
    "version": 2,
    "builds": [
    {
        "src": "<project_name>/wsgi.py",
        "use": "@vercel/python"
    },
    {
        "src": "build_files.sh",
        "use": "@vercel/static-build",
        "config": {
        "distDir": "staticfiles_build"
        }
    }
    ],
    "routes": [
    {
        "src": "/static/(.*)",
        "dest": "/static/$1"
    },
    {
        "src": "/(.*)",
        "dest": "<project_name>/wsgi.py"
    }
    ]
}
```

**Reason:** This file specifies how Vercel will build and serve your project, including handling routes for static files and your Django application.

### 5. Create `requirements.txt`

Create a file named `requirements.txt` with the following content:

```txt
Django
```

**Reason:** The `requirements.txt` file lists the dependencies required by your project, allowing Vercel to install them during deployment.

1. **Deployment**

   - Push your changes to your Git repository.
   - Connect your repository to Vercel.
   - Vercel will automatically build and deploy your Django project.

## Troubleshooting

- Ensure you are using the correct Python and Django versions.
- Check Vercel logs for deployment errors.
- Verify the configuration in `vercel.json` and `settings.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


# Deploy Django บน Vercel

คู่มือนี้อธิบายขั้นตอนการปรับใช้โปรเจกต์ Django บน Vercel พร้อมอธิบายเหตุผลในการตั้งค่าต่าง ๆ

## ข้อกำหนดเบื้องต้น

- Python 3.12+
- Django
- บัญชี Vercel

## ขั้นตอนการปรับใช้

### 1. แก้ไข `wsgi.py`

ในไฟล์ `./project/wsgi.py` ให้แน่ใจว่าคุณมีโค้ดดังต่อไปนี้:

```python
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

app = get_wsgi_application()  # เพิ่มบรรทัดนี้
```

**เหตุผล:** บรรทัด `app = get_wsgi_application()` ถูกเพิ่มเข้ามาเพื่อให้แน่ใจว่า Vercel สามารถเรียกใช้งานแอปพลิเคชัน Django ของคุณได้อย่างถูกต้อง

### 2. กำหนดค่า `settings.py`

- **Allow Hosts**

  อัปเดต `ALLOWED_HOSTS` ในไฟล์ `./project/settings.py`:

```python
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]
```

  **เหตุผล:** `ALLOWED_HOSTS` กำหนดว่าเว็บไซต์ของคุณสามารถเข้าถึงได้จากที่ไหนบ้าง การเพิ่ม `.vercel.app` ช่วยให้ Vercel สามารถเข้าถึงโปรเจกต์ของคุณได้

- **คอมเมนต์ `DATABASES`**

  คอมเมนต์การกำหนดค่าของ `DATABASES`:

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

  **เหตุผล:** เนื่องจาก Vercel ใช้ฐานข้อมูลที่ต่างออกไป การคอมเมนต์การตั้งค่าของฐานข้อมูล SQLite จะช่วยหลีกเลี่ยงข้อผิดพลาดที่อาจเกิดขึ้นจากการตั้งค่าในสภาพแวดล้อมการปรับใช้

- **การกำหนดค่าไฟล์สแตติก**

  กำหนดค่าไฟล์สแตติก:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [Path.joinpath(BASE_DIR, 'static')]
STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles_build', 'static')
```

  **เหตุผล:** การกำหนดค่าเหล่านี้ช่วยให้ Django รู้จักตำแหน่งที่จัดเก็บไฟล์สแตติก (เช่น CSS, JavaScript, รูปภาพ) ซึ่งจะถูกรวบรวมและบริการโดย Vercel

- **การตั้งค่า Template**

  กำหนดค่า templates:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

  **เหตุผล:** การตั้งค่า template ช่วยให้ Django สามารถค้นหาและใช้ไฟล์ template ที่อยู่ในไดเรกทอรี `templates` ของโปรเจกต์ของคุณ

### 3. สร้าง `build_files.sh`

สร้างไฟล์ที่ชื่อว่า `build_files.sh` พร้อมเนื้อหาดังนี้:

```sh
echo "Building the project..."
python3.12 -m pip install -r requirements.txt

echo "Collect Static..."
python3.12 manage.py collectstatic --noinput --clear
```

**เหตุผล:** สคริปต์นี้จะติดตั้ง dependencies ที่จำเป็นและรวบรวมไฟล์สแตติกทั้งหมดก่อนการปรับใช้

### 4. สร้าง `vercel.json`

สร้างไฟล์ที่ชื่อว่า `vercel.json` ด้วยเนื้อหาดังนี้ เปลี่ยน `<project_name>` เป็นชื่อโปรเจกต์ Django ของคุณ:

```json
{
    "version": 2,
    "builds": [
    {
        "src": "<project_name>/wsgi.py",
        "use": "@vercel/python"
    },
    {
        "src": "build_files.sh",
        "use": "@vercel/static-build",
        "config": {
        "distDir": "staticfiles_build"
        }
    }
    ],
    "routes": [
    {
        "src": "/static/(.*)",
        "dest": "/static/$1"
    },
    {
        "src": "/(.*)",
        "dest": "<project_name>/wsgi.py"
    }
    ]
}
```

**เหตุผล:** ไฟล์นี้กำหนดวิธีการที่ Vercel จะสร้างและบริการโปรเจกต์ของคุณ รวมถึงการจัดการเส้นทางสำหรับไฟล์สแตติกและแอปพลิเคชัน Django ของคุณ

### 5. สร้าง `requirements.txt`

สร้างไฟล์ที่ชื่อว่า `requirements.txt` ด้วยเนื้อหาดังนี้:

```txt
Django
```

**เหตุผล:** `requirements.txt` เป็นไฟล์ที่ใช้ในการติดตั้ง dependencies ที่โปรเจกต์ของคุณต้องการ

1. **การปรับใช้**

   - ดันการเปลี่ยนแปลงของคุณไปยังรีโพซิทอรี Git ของคุณ
   - เชื่อมต่อรีโพซิทอรีของคุณกับ Vercel
   - Vercel จะทำการสร้างและปรับใช้โปรเจกต์ Django ของคุณโดยอัตโนมัติ

## การแก้ปัญหา

- ตรวจสอบให้แน่ใจว่าคุณใช้เวอร์ชันของ Python และ Django ที่ถูกต้อง
- ตรวจสอบบันทึกของ Vercel สำหรับข้อผิดพลาดในการปรับใช้
- ตรวจสอบการกำหนดค่าใน `vercel.json` และ `settings.py`

## ใบอนุญาต

โปรเจกต์นี้ได้รับอนุญาตภายใต้ใบอนุญาต MIT - ดูรายละเอียดในไฟล์ [LICENSE](LICENSE)

