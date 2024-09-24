# django-lrnd

`django-lrnd` adalah middleware Django untuk validasi LRND (License/Registration Number Data). Middleware ini memeriksa validitas kunci LRND yang disimpan di database dan mengarahkan pengguna ke halaman validasi jika kunci tidak valid atau telah kedaluwarsa.

## Fitur

- Middleware untuk memeriksa validitas kunci LRND.
- Halaman validasi untuk memasukkan kunci LRND.
- Penyimpanan kunci LRND di database.

## Instalasi

1. Install package `django-lrnd` menggunakan pip:

    ```sh
    pip install django-lrnd
    ```

2. Tambahkan `django-lrnd` ke `INSTALLED_APPS` di `settings.py`:

    ```python
    INSTALLED_APPS = [
        ...
        'djangoLrnd',
    ]
    ```

3. Tambahkan `LRNDMiddleware` ke `MIDDLEWARE` di `settings.py`:

    ```python
    MIDDLEWARE = [
        ...
        'djangoLrnd.middleware.LRNDMiddleware',
    ]
    ```

4. Tambahkan URL untuk halaman validasi di `urls.py`:

    ```python
    from django.urls import path
    from djangoLrnd.views import validate_view

    urlpatterns = [
        ...
        path('validate/', validate_view, name='lrnd_validate'),
    ]
    ```

5. Jalankan migrasi untuk membuat tabel `LRNDKey` di database:

    ```sh
    python manage.py migrate
    ```

## Konfigurasi

Tambahkan konfigurasi berikut di `settings.py`:

- `LRND_VALIDATION_ENDPOINT`: URL endpoint untuk validasi kunci LRND.
- `LRND_ENCRYPTION_PASSWORD`: Password untuk enkripsi dan dekripsi kunci LRND.
- `LRND_EXEMPT_PATHS`: Daftar path yang dikecualikan dari validasi kunci LRND.
- `LRND_KEY_MODEL`: Model yang digunakan untuk menyimpan kunci LRND.
- `LRND_SUCCESS_REDIRECT_URL`: URL untuk redirect setelah kunci berhasil divalidasi.

Contoh konfigurasi:

    ```python
    LRND_VALIDATION_ENDPOINT = 'http://127.0.0.1:8000/validate/'
    LRND_ENCRYPTION_PASSWORD = 'YourEncryptionPassword'
    LRND_EXEMPT_PATHS = ['/validate/']
    LRND_KEY_MODEL = 'djangoLrnd.LRNDKey'
    LRND_SUCCESS_REDIRECT_URL = 'home'
    ```

## Penggunaan

1. Middleware akan secara otomatis memeriksa validitas kunci LRND setiap kali ada request.
2. Jika kunci tidak valid atau telah kedaluwarsa, pengguna akan diarahkan ke halaman validasi.
3. Pengguna dapat memasukkan kunci LRND di halaman validasi.
4. Jika kunci valid, pengguna akan diarahkan ke URL yang ditentukan di `LRND_SUCCESS_REDIRECT_URL`.

## Contoh

Berikut adalah contoh bagaimana middleware ini bekerja:

1. Pengguna mengakses halaman yang tidak dikecualikan dari validasi.
2. Middleware memeriksa validitas kunci LRND.
3. Jika kunci tidak valid, pengguna diarahkan ke halaman validasi.
4. Pengguna memasukkan kunci LRND di halaman validasi.
5. Middleware memvalidasi kunci dengan endpoint yang ditentukan.
6. Jika kunci valid, pengguna diarahkan ke halaman yang ditentukan di `LRND_SUCCESS_REDIRECT_URL`.

## Lisensi

`django-lrnd` dilisensikan di bawah lisensi MIT. Lihat file LICENSE untuk informasi lebih lanjut.