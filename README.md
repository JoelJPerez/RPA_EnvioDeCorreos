# Registro de Horas Extras - Aplicación de Consola

Esta aplicación de consola permite registrar horas extras trabajadas y enviar automáticamente un correo electrónico para notificar sobre el tiempo compensatorio.

## Requisitos

- Python 3.6 o superior
- Conexión a Internet
- Cuenta de correo electrónico (Gmail recomendado)

## Configuración

1. Editar el archivo `config.json` con tus datos:
   - `email_remitente`: Tu dirección de correo electrónico
   - `password`: Tu contraseña de aplicación (para Gmail) o contraseña normal (para Outlook)
   - `email_destinatario`: Correos electrónicos de los destinatarios (separados por comas)
   - `servicio_correo`: "gmail" u "outlook" (por defecto: "gmail")
   - `nombre_colaborador`: Tu nombre completo

### Nota para usuarios de Gmail:
Para usar Gmail, necesitarás generar una "Contraseña de aplicación":
1. Ve a tu cuenta de Google
2. Seguridad
3. Verificación en 2 pasos (debe estar activada)
4. Contraseñas de aplicación
5. Genera una nueva contraseña y úsala en el archivo config.json

## Uso

1. Ejecuta el programa
2. Ingresa la fecha (formato: DD/MM/YYYY)
3. Ingresa la hora de inicio (formato: HH:MM)
4. Ingresa la hora de fin (formato: HH:MM)
5. Ingresa el motivo de las horas extras
6. El programa enviará automáticamente un correo con la información

## Generar Ejecutable

Para generar el archivo .exe, sigue estos pasos:

1. Instala PyInstaller:
```
pip install pyinstaller
```

2. Genera el ejecutable:
```
pyinstaller --onefile --add-data "config.json;." main.py
```

El ejecutable se generará en la carpeta `dist`.