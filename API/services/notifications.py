import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from api.ficha.models import MatrizCompromiso

def send_telegram_message(message):
    """Envía mensaje al grupo de Telegram configurado"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")
        return False

def send_email_notification(subject, message, recipient_list, matriz=None):
    """Envía correo con HTML y opcionalmente PDF adjunto"""
    html_content = render_to_string('emails/matriz_alert.html', {
        'matriz': matriz,
        'message': message,
        'subject': subject
    })
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,  # Versión texto plano
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

def check_and_send_alerts():
    """Verifica matrices próximas a vencer y envía alertas"""
    
    hoy = timezone.now().date()
    umbral_alerta = hoy + timedelta(days=7)  # Alertar 7 días antes
    
    matrices = MatrizCompromiso.objects.filter(
        plazo_fin__gte=hoy,
        plazo_fin__lte=umbral_alerta,
        alertas_enviadas=False  # Campo nuevo que debes añadir al modelo
    ).select_related('evaluacion', 'evaluacion__usuario')
    
    for matriz in matrices:
        dias_restantes = (matriz.plazo_fin - hoy).days
        
        # Mensaje común
        subject = f"⏰ Alerta: Matriz {matriz.evaluacion.codigo} vence en {dias_restantes} días"
        message = (
            f"⚠️ <b>Alerta de Matriz de Compromiso</b>\n\n"
            f"🏥 <b>Establecimiento:</b> {matriz.evaluacion.establecimiento}\n"
            f"🔢 <b>Código:</b> {matriz.evaluacion.codigo}\n"
            f"📅 <b>Fecha fin:</b> {matriz.plazo_fin.strftime('%d/%m/%Y')}\n"
            f"⏳ <b>Días restantes:</b> {dias_restantes}\n\n"
            f"📝 <b>Compromisos:</b>\n{matriz.medidas_correctivas[:150]}...\n\n"
            f"🔗 <b>Acceso:</b> {settings.FRONTEND_URL}/matrices/{matriz.id}"
        )
        
        # Enviar notificaciones
        telegram_ok = send_telegram_message(message)
        email_ok = send_email_notification(
            subject, 
            message, 
            [matriz.evaluacion.usuario.email],
            matriz
        )
        
        # Marcar como alertada si se envió correctamente
        if telegram_ok and email_ok:
            matriz.alertas_enviadas = True
            matriz.save()
    
    return f"Procesadas {matrices.count()} matrices"