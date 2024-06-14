# TEST SERVER OPEN METHOD

1. Mysql configuration (make osp database)
```bash
mysql -u root -p

CREATE DATABASE osp;
exit
```

2. goto Backend directory
```bash
cd {backend directory}
```

3. modify app/db_init.py
```bash
vi app/db_init.py

(line 18)
engine = create_engine('mysql+pymysql://root:비밀번호@localhost/osp', echo=False)

:wq
```

4. create venv and access
```bash
python3 -m venv venv
source venv/bin/activate
```

5. install requirements
```bash
pip3 install -r requirements.txt
```

6. make .env file
```bash
vi .env

OPENAI_API_KEY	= sk-{your_key}
CLIENT_ID	= 373805319561-p5ff6n7uimubjov3uq51l241qg8u4rs0.apps.googleusercontent.com
CLIENT_SECRET	= {any_long_string}
SECRET_KEY	= {any_long_string}

:wq

```
7. BackEnd Server On
```bash
python3 main.py
```
