import streamlit as st

def show_alert(message, image_url=None, alert_type="info"):
    """
    Affiche une alerte personnalisée avec une image et du texte.
    :param message: Texte de l'alerte.
    :param image_url: URL ou chemin de l'image (facultatif).
    :param alert_type: Type d'alerte ('info', 'warning', 'error', 'success').
    """
    colors = {
        "info": "#17a2b8",
        "warning": "#ffc107",
        "error": "#dc3545",
        "success": "#28a745",
    }
    color = colors.get(alert_type, "#17a2b8")  # Couleur par défaut : info

    alert_html = f"""
    <div style="display: flex; align-items: center; background-color: {color}; 
                color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">
        {"<img src='" + image_url + "' style='width: 50px; height: 50px; margin-right: 10px;' />" if image_url else ""}
        <div style="flex: 1; font-size: 16px;">{message}</div>
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)
