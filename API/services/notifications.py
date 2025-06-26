import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.html import strip_tags  # Añade esta importación al inicio del archivo
from api.ficha.models import MatrizCompromiso

def send_telegram_alert(matriz, dias_restantes):
    """Envía alerta a Telegram"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Determinar nivel de urgencia
    if dias_restantes <= 3:
        nivel = "🚨 ALTA URGENCIA 🚨"
    elif dias_restantes <= 7:
        nivel = "⚠️ URGENTE ⚠️"
    else:
        nivel = "⏰ RECORDATORIO"
    
    message = (
        f"<b>{nivel}</b>\n\n"
        f"📋 <b>Matriz de Compromiso</b>\n"
        f"🏥 IPRESS: {matriz.evaluacion.establecimiento}\n"
        f"🔢 Código: {matriz.evaluacion.codigo}\n"
        f"📅 Fecha límite: {matriz.plazo_fin.strftime('%d/%m/%Y')}\n"
        f"⏳ Días restantes: {dias_restantes}\n\n"
        f"👤 Responsables:\n"
        f"- {matriz.responsable_directo}\n"
        f"- {matriz.funcionario_depen_directo}\n"
        f"- {matriz.funcionario_depen_indirecto}\n\n"
        f"📝 Compromisos:\n"
        f"{matriz.medidas_correctivas[:300]}..."
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error enviando a Telegram: {str(e)}")
        return False

def send_email_alert(matriz, user_email, dias_restantes):
    """Envía alerta por correo electrónico"""
    # Determinar nivel de urgencia
    if dias_restantes <= 3:
        nivel = "ALTA URGENCIA"
        color = "#dc3545"
    elif dias_restantes <= 7:
        nivel = "URGENTE"
        color = "#ffc107"
    else:
        nivel = "Recordatorio"
        color = "#17a2b8"
    
    context = {
        'matriz': matriz,
        'dias_restantes': dias_restantes,
        'nivel': nivel,
        'color': color,
        'plazo_fin': matriz.plazo_fin.strftime('%d/%m/%Y')
    }
    
    subject = f"{nivel} - Matriz {matriz.evaluacion.codigo} ({dias_restantes} días restantes)"
    
    html_content = render_to_string('emails/matriz_alert.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
        return False

def send_matriz_alerts():
    """Envía alertas para todas las matrices pendientes"""
    hoy = timezone.now().date()
    matrices = MatrizCompromiso.objects.filter(
        plazo_fin__gte=hoy,
        plazo_inicio__lte=hoy
    ).select_related('evaluacion__usuario')
    
    resultados = {
        'total': 0,
        'exitosas': 0,
        'errores': [],
        'detalle': []
    }
    
    for matriz in matrices:
        dias_restantes = (matriz.plazo_fin - hoy).days
        necesita_alerta = False
        
        # Determinar frecuencia de alerta
        if dias_restantes <= 3 and matriz.ultima_alerta_enviada != hoy:
            necesita_alerta = True
        elif dias_restantes <= 7 and (not matriz.ultima_alerta_enviada or (hoy - matriz.ultima_alerta_enviada).days >= 3):
            necesita_alerta = True
        elif dias_restantes > 7 and (not matriz.ultima_alerta_enviada or (hoy - matriz.ultima_alerta_enviada).days >= 7):
            necesita_alerta = True
        
        if necesita_alerta:
            resultados['total'] += 1
            detalle = {
                'matriz_id': matriz.id,
                'codigo': matriz.evaluacion.codigo,
                'telegram': False,
                'email': False
            }
            
            try:
                # Enviar alertas
                telegram_ok = send_telegram_alert(matriz, dias_restantes)
                email_ok = send_email_alert(matriz, matriz.evaluacion.usuario.email, dias_restantes)
                
                if telegram_ok and email_ok:
                    matriz.ultima_alerta_enviada = hoy
                    matriz.save()
                    resultados['exitosas'] += 1
                    detalle['telegram'] = True
                    detalle['email'] = True
                else:
                    resultados['errores'].append(matriz.id)
                
                resultados['detalle'].append(detalle)
            except Exception as e:
                resultados['errores'].append(matriz.id)
                resultados['detalle'].append({
                    **detalle,
                    'error': str(e)
                })
    
    return resultados