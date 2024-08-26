## SafePass

SafePass là ứng dụng quản lí mật khẩu toàn diện, giúp bạn:
- Lưu trữ mật khẩu an toàn.
- Tạo mật khẩu an toàn.
- Tạo các workspace khác nhau để phân loại mật khẩu.

## Table of Contents
* **[Installation](#installation)**
* **[License](#license)**
----

## 📖 Hướng dẫn cài đặt

Bạn clone dự án theo đường dẫn bên dưới và di chuyển vào thư mục dự án.
```
$ git clone https://github.com/devhungthinh/SafePass
$ cd SafePass
```

Tiếp theo, bạn cài đặt môi trường ảo cho python.
```
# Windows
$ python -m venv .venv
$ Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
$ .venv\Scripts\Activate.ps1

# macOS
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Bạn cài đặt các dependency và khởi động SafePass.
```
(.venv) $ pip install -r requirements.txt
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py runserver
```

Truy cập vào đường dẫn [tại đây](http://127.0.0.1:8000) để sử dụng ứng dụng.

## License

[The MIT License](LICENSE)
