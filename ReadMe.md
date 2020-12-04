# README for Sabra and Melissa's Group Implementation Project

## 1. Authentication
This sample requires you to have authentication setup. Refer to the [Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started) for instructions on setting up credentials for applications.

Place a JSON file that contains your key in the main directory. The file name should be `aikey.json`.

## 2. Create Python Virtual Environment
```
python -m venv .
```
or
```
virtualenv .
```

## 3. Activate Virtual Enviromment
Linux
```
source bin/activate
```

Windows
```
source Scripts/activate
```

## 4. Install Dependencies 
```
pip install -r requirements.txt
```

## 5. Run the App  
```
flask run
```
Check http://localhost:5000/


## 6. Quit the App
Press CTRL+C


## 7. Deactivate Virtual Environment
```
deactivate
```