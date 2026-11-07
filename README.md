## Cómo ejecutar

### Ejercicio 1

    python ejercicio_1/sensores.py

### Ejercicio 2

    python ejercicio_2/main.py

Genera `ejercicio_2/catalogo_ecotech.json` con los productos válidos del catálogo.

### Ejercicio 3 (Django)

    cd ejercicio_3
    python -m venv venv
    venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
    pip install -r requirements.txt
    python manage.py test        # corre los tests unitarios (15)
    python manage.py runserver   # panel en http://127.0.0.1:8000/
