# powerOfCoordinate
Google Developer Student Clubs(GSDC) final project at National Chengchi University, a house price search site using Django and Google API. The site receives an address entered by the user, or the current location of the user, and the range of distances the user wants to query. The site then displays recent home transactions within the required distance and marks them on the displayed map.

## Screenshot
![image](https://user-images.githubusercontent.com/87135678/154725827-67ec0638-9298-4ddc-8fdb-5efd834714de.png)

## Getting Started
To get started, follow the following steps:
- Input the necessary settings in the .env file (you can refer to .env.example for guidance)

Then run the following commands to run your app:
```bash
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py runserver
```


## Tech Used
- Bootstrap
- Django
- SQLite
- HTML, CSS, JavaScript