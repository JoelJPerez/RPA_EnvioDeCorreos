import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import json
import sys

def cargar_configuracion():
    try:
        if getattr(sys, 'frozen', False):
            # Si es un ejecutable
            config_path = os.path.join(os.path.dirname(sys.executable), 'config.json')
        else:
            # Si es script Python
            config_path = 'config.json'
            
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo config.json")
        input("Presione Enter para salir...")
        sys.exit(1)

def solicitar_datos():
    print("\n=== Registro de Horas Extras para Compensatorio ===\n")
    
    fecha = input("Ingrese la fecha (DD/MM/YYYY): ")
    hora_inicio = input("Ingrese la hora de inicio (HH:MM): ")
    hora_fin = input("Ingrese la hora de fin (HH:MM): ")
    motivo = input("Ingrese el motivo de las horas extras: ")
    
    try:
        # Validar el formato de fecha
        datetime.strptime(fecha, "%d/%m/%Y")
        # Validar el formato de las horas
        datetime.strptime(hora_inicio, "%H:%M")
        datetime.strptime(hora_fin, "%H:%M")
        
        return {
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "motivo": motivo
        }
    except ValueError:
        print("\nError: Formato de fecha u hora incorrecto.")
        input("Presione Enter para salir...")
        sys.exit(1)

def obtener_configuracion_smtp(servicio):
    """Obtiene la configuración SMTP según el servicio de correo"""
    configuraciones = {
        "gmail": {
            "servidor": "smtp.gmail.com",
            "puerto": 587
        },
        "outlook": {
            "servidor": "smtp-mail.outlook.com",
            "puerto": 587
        }
    }
    return configuraciones.get(servicio.lower(), configuraciones["gmail"])

def enviar_correo(config, datos):
    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = config["email_remitente"]
    
    # Manejar múltiples destinatarios
    destinatarios = config["email_destinatario"].replace(" ", "").split(",")
    mensaje["To"] = ", ".join(destinatarios)
    mensaje["Subject"] = "Registro de Horas Extras para Compensatorio"

    # Crear el cuerpo del correo
    cuerpo = f"""
    Registro de Horas Extras para Compensatorio

    Colaborador: {config['nombre_colaborador']}
    Fecha: {datos['fecha']}
    Hora de inicio: {datos['hora_inicio']}
    Hora de fin: {datos['hora_fin']}
    Motivo: {datos['motivo']}

    Este es un correo automático, por favor no responder.
    """

    mensaje.attach(MIMEText(cuerpo, "plain"))

    try:
        # Obtener configuración SMTP según el servicio
        servicio = config.get("servicio_correo", "gmail").lower()
        config_smtp = obtener_configuracion_smtp(servicio)
        
        # Configurar el servidor SMTP
        servidor = smtplib.SMTP(config_smtp["servidor"], config_smtp["puerto"])
        servidor.starttls()
        servidor.login(config["email_remitente"], config["password"])
        
        # Enviar el correo
        texto = mensaje.as_string()
        servidor.sendmail(config["email_remitente"], destinatarios, texto)
        servidor.quit()
        
        print("\nCorreo enviado exitosamente a todos los destinatarios!")
    except Exception as e:
        print(f"\nError al enviar el correo: {str(e)}")
        input("Presione Enter para salir...")
        sys.exit(1)

def main():
    try:
        # Cargar configuración
        config = cargar_configuracion()
        
        # Solicitar datos al usuario
        datos = solicitar_datos()
        
        # Enviar correo
        enviar_correo(config, datos)
        
        input("\nPresione Enter para salir...")
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        input("Presione Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()