"""
PredictiveSense AI — Email Alert System
========================================
Automated email notifications for critical engine health alerts.
Sends email when engine RUL drops below critical threshold (40 cycles).
DRDO Internship 2026 | Vipin Nagar
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ── Sender Configuration ──────────────────────────────────────────
SENDER_EMAIL    = "predictivesense.ai@gmail.com"
SENDER_PASSWORD = "zlqg fhou xgwp wvqc"   # Replace with your 16-char App Password
SMTP_SERVER     = "smtp.gmail.com"
SMTP_PORT       = 587

def send_critical_alert(engine_id, predicted_rul, anomaly_count, receiver_email):
    """
    Send critical alert email when engine RUL is below threshold.
    
    Args:
        engine_id (int)       : Engine unit ID (1-100)
        predicted_rul (float) : Predicted Remaining Useful Life in cycles
        anomaly_count (int)   : Number of anomalies detected for this engine
        receiver_email (str)  : Engineer's email address to send alert to
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # ── Build email ───────────────────────────────────────────
        msg = MIMEMultipart("alternative")
        msg['Subject'] = f"🔴 CRITICAL ALERT — Engine #{engine_id} | PredictiveSense AI"
        msg['From']    = SENDER_EMAIL
        msg['To']      = receiver_email

        timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

        # ── Plain text version ────────────────────────────────────
        text = f"""
CRITICAL ALERT — PredictiveSense AI
=====================================
Engine ID      : #{engine_id}
Predicted RUL  : {predicted_rul:.0f} cycles
Anomalies      : {anomaly_count}
Status         : CRITICAL — Immediate maintenance required!
Timestamp      : {timestamp}

Please take immediate action to inspect Engine #{engine_id}.

— PredictiveSense AI | DRDO Internship 2026 | Vipin Nagar
  github.com/Vipinnagar169/PredictiveSense-AI
        """

        # ── HTML version ──────────────────────────────────────────
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <div style="background-color: #C00000; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0;">🔴 CRITICAL ALERT</h1>
                <p style="color: #FFD0D0; margin: 5px 0 0 0;">PredictiveSense AI — Engine Health Monitor</p>
            </div>
            <div style="background-color: #FFF2F2; padding: 20px; border: 1px solid #C00000;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #FFE0E0;">
                        <td style="padding: 10px; font-weight: bold; color: #C00000;">Engine ID</td>
                        <td style="padding: 10px; font-size: 20px; font-weight: bold;">#{engine_id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; font-weight: bold; color: #C00000;">Predicted RUL</td>
                        <td style="padding: 10px; font-size: 20px; font-weight: bold;">{predicted_rul:.0f} cycles</td>
                    </tr>
                    <tr style="background-color: #FFE0E0;">
                        <td style="padding: 10px; font-weight: bold; color: #C00000;">Anomalies Detected</td>
                        <td style="padding: 10px;">{anomaly_count}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; font-weight: bold; color: #C00000;">Status</td>
                        <td style="padding: 10px; color: #C00000; font-weight: bold;">⚠️ IMMEDIATE MAINTENANCE REQUIRED</td>
                    </tr>
                    <tr style="background-color: #FFE0E0;">
                        <td style="padding: 10px; font-weight: bold; color: #C00000;">Timestamp</td>
                        <td style="padding: 10px;">{timestamp}</td>
                    </tr>
                </table>
            </div>
            <div style="background-color: #1F3864; padding: 15px; border-radius: 0 0 8px 8px; text-align: center;">
                <p style="color: white; margin: 0; font-size: 12px;">
                    PredictiveSense AI | DRDO Internship 2026 | Vipin Nagar<br>
                    <a href="https://predictivesense-ai.streamlit.app" style="color: #AEC6E8;">
                        predictivesense-ai.streamlit.app
                    </a>
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        # ── Send email ────────────────────────────────────────────
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_warning_alert(engine_id, predicted_rul, receiver_email):
    """
    Send warning alert email when engine RUL is between 40-80 cycles.
    
    Args:
        engine_id (int)       : Engine unit ID (1-100)
        predicted_rul (float) : Predicted Remaining Useful Life in cycles
        receiver_email (str)  : Engineer's email address
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = f"🟡 WARNING — Engine #{engine_id} | PredictiveSense AI"
        msg['From']    = SENDER_EMAIL
        msg['To']      = receiver_email

        timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <div style="background-color: #FF8C00; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0;">🟡 WARNING ALERT</h1>
                <p style="color: #FFF0D0; margin: 5px 0 0 0;">PredictiveSense AI — Engine Health Monitor</p>
            </div>
            <div style="background-color: #FFFBF0; padding: 20px; border: 1px solid #FF8C00;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #FFF0D0;">
                        <td style="padding: 10px; font-weight: bold;">Engine ID</td>
                        <td style="padding: 10px; font-size: 20px; font-weight: bold;">#{engine_id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; font-weight: bold;">Predicted RUL</td>
                        <td style="padding: 10px; font-size: 20px; font-weight: bold;">{predicted_rul:.0f} cycles</td>
                    </tr>
                    <tr style="background-color: #FFF0D0;">
                        <td style="padding: 10px; font-weight: bold;">Status</td>
                        <td style="padding: 10px; color: #FF8C00; font-weight: bold;">⚠️ Schedule maintenance soon</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; font-weight: bold;">Timestamp</td>
                        <td style="padding: 10px;">{timestamp}</td>
                    </tr>
                </table>
            </div>
            <div style="background-color: #1F3864; padding: 15px; border-radius: 0 0 8px 8px; text-align: center;">
                <p style="color: white; margin: 0; font-size: 12px;">
                    PredictiveSense AI | DRDO Internship 2026 | Vipin Nagar<br>
                    <a href="https://predictivesense-ai.streamlit.app" style="color: #AEC6E8;">
                        predictivesense-ai.streamlit.app
                    </a>
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False