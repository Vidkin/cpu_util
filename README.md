# cpu_util
CPU utilization service

## REQUIREMENTS
Tested on python3.7.3(3.6.8)
```
All package requirements listed in requirements.txt
```

## QUICK START
```
$ cd <cpu_util path>                    (Linux)
cd <cpu_util path>                      (Windows)

$ python3 ./app.py                      (Linux)
python app.py                           (Windows)
```

## CONFIG
Default config.json:
```
{
  "rabbit-host": "127.0.0.1",
  "rabbit-port": 5672,
  "rabbit-login": "guest",
  "rabbit-psw": "guest",
  "cpu-load-limit": 60
}
```
