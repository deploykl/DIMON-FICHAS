from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Lista de usuarios a crear
usuarios = [
    {"first_name": "Edward dennis", "last_name": "Mandaré durán", "email": "emandared@minsa.gob.pe", "username": "emandared"},
    {"first_name": "Kevin ricardo eli", "last_name": "Garay suarez", "email": "dgos083@minsa.gob.pe", "username": "dgos083"},
    {"first_name": "Guisela santos", "last_name": "Izquierdo morales", "email": "gizquierdo@minsa.gob.pe", "username": "gizquierdo"},
    {"first_name": "Liliana sonia", "last_name": "Monzon rodriguez", "email": "lmonzon@minsa.gob.pe", "username": "lmonzon"},
    {"first_name": "Rocio", "last_name": "Cortijo villacorta", "email": "rcortijo@minsa.gob.pe", "username": "rcortijo"},
    {"first_name": "Juky paola", "last_name": "Vega baldeon", "email": "jvega@minsagob.pe", "username": "jvega"},
    {"first_name": "Carol", "last_name": "Romero sandon", "email": "cromeros@minsa.gob.pe", "username": "cromeros"},
    {"first_name": "Niurka", "last_name": "Coronel lopez", "email": "ncoronel@minsa.gob.pe", "username": "ncoronel"},
    {"first_name": "Doris", "last_name": "De la cruz peñaran", "email": "ddelacruz@minsa.gob.pe", "username": "ddelacruz"},
    {"first_name": "Richard cleofe", "last_name": "Llanca flores", "email": "rllanca@minsa.gob.pe", "username": "rllanca"},
    {"first_name": "Marcos alberto", "last_name": "Cueva pereyra", "email": "mcueva@minsa.gob.pe", "username": "mcueva"},
    {"first_name": "Gladys", "last_name": "Correa bocanegra", "email": "gcorrea@minsa.gob.pe", "username": "gcorrea"},
    {"first_name": "Griselda madelaine", "last_name": "Sanchez velarde", "email": "gsanchez@minsa.gob.pe", "username": "gsanchez"},
    {"first_name": "Larissa", "last_name": "Casanova tovar", "email": "lcasanova@minsa.gob.pe", "username": "lcasanova"},
    {"first_name": "Yadhira", "last_name": "Nieto cisneros", "email": "ynieto@minsa.gob.pe", "username": "ynieto"},
    {"first_name": "Mayela olinda", "last_name": "Leon rivera", "email": "mleonr@minsa.gob.pe", "username": "mleonr"},
    {"first_name": "Jorge luis", "last_name": "Parvina hernandez", "email": "jparvina@minsa.gob.pe", "username": "jparvina"},
    {"first_name": "Marleny", "last_name": "Carrera peze", "email": "mcarrera@minsa.gob.pe", "username": "mcarrera"},
    {"first_name": "Rosa Elizabeth", "last_name": "Garcia encina", "email": "rgarciae@minsa.gob.pe", "username": "rgarciae"},
    {"first_name": "Lupe", "last_name": "Alvarez chavez", "email": "lalvarezc@minsa.gob.pe", "username": "lalvarezc"},
    {"first_name": "Mailin del carmen", "last_name": "Oropesa angel bello", "email": "dgos021@minsa.gob.pe", "username": "dgos021"},
    {"first_name": "Cinthia sineris", "last_name": "Castro barbachan", "email": "dgos022@minsa.gob.pe", "username": "dgos022"},
    {"first_name": "Jose alfredo", "last_name": "Moreyra chavez", "email": "dgos020@minsa.gob.pe", "username": "dgos020"},
    {"first_name": "Alexander", "last_name": "Villafuerte mendoza", "email": "dgos125@minsa.gob.pe", "username": "dgos125"},
    {"first_name": "Nelly sofia", "last_name": "Ccorahua oroe", "email": "dgos031@minsa.gob.pe", "username": "dgos031"},
    {"first_name": "Pilar", "last_name": "Zabarburu cruz", "email": "dgos069@minsa.gob.pe", "username": "dgos069"},
    {"first_name": "Flor itala", "last_name": "Espitia sosa", "email": "dgos137@minsa.gob.pe", "username": "dgos137"}
]

def crear_usuarios():
    for usuario in usuarios:
        # Verificar si el usuario ya existe
        if not User.objects.filter(username=usuario['username']).exists():
            # Crear usuario con contraseña hasheada
            User.objects.create_user(
                username=usuario['username'],
                email=usuario['email'],
                password=usuario['username'],  # La contraseña será igual al username
                first_name=usuario['first_name'],
                last_name=usuario['last_name'],
                is_staff=True,  # O False según necesites
                is_active=True
            )
            print(f"Usuario {usuario['username']} creado exitosamente")
        else:
            print(f"El usuario {usuario['username']} ya existe")

# Ejecutar la función
crear_usuarios()