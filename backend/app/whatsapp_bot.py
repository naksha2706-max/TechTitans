from typing import Dict, Any
from sqlalchemy.orm import Session
from app import rules, upi_detector, normalizers

def process_whatsapp_message(
    sender: str,
    message_text: str,
    db: Session = None
) -> Dict[str, Any]:
    """
    Processes forwarded WhatsApp messages, checks text for scam signals and UPI handles,
    and returns a formatted WhatsApp response payload.
    """
    if not message_text or not message_text.strip():
        return {
            "reply": "🤖 *ScamCheck Bot*\n\nPlease send or forward a job offer message, UPI handle, or offer details to check for scams."
        }

    # Check if message contains a UPI ID
    upi_match = None
    words = message_text.split()
    for word in words:
        cleaned = word.strip(",.()[]{}")
        if "@" in cleaned and len(cleaned) > 5 and not cleaned.endswith(".com"):
            upi_match = cleaned
            break

    if upi_match:
        upi_res = upi_detector.analyze_upi_transaction(upi_id=upi_match, message_text=message_text, db=db)
        band_icon = "🟢" if upi_res["risk_band"] == "low" else "🟠" if upi_res["risk_band"] == "medium" else "🔴"
        
        warnings_str = ""
        for w in upi_res["warnings"]:
            warnings_str += f"\n• ⚠️ *{w['code']}*: {w['label']}"

        reply = (
            f"🤖 *ScamCheck WhatsApp Bot*\n\n"
            f"💳 *UPI Scam Analysis for `{upi_match}`*\n"
            f"Risk Level: {band_icon} *{upi_res['risk_band'].upper()}* ({upi_res['risk_score']}/100)\n"
            f"{warnings_str}\n\n"
            f"💡 *Recommendation*: {upi_res['recommendation']}\n\n"
            f"🔗 _Verified by ScamCheck Platform_"
        )
        return {"reply": reply, "evaluation": upi_res}

    # Evaluate standard message text
    eval_res = rules.evaluate_opportunity(message_text=message_text)
    band_icon = "🟢" if eval_res["risk_band"] == "low" else "🟠" if eval_res["risk_band"] == "medium" else "🔴"

    warnings_str = ""
    for w in eval_res["warnings"]:
        warnings_str += f"\n• ⚠️ *{w['label']}*"

    if not warnings_str:
        warnings_str = "\n• ✅ No immediate red flags detected."

    reply = (
        f"🤖 *ScamCheck WhatsApp Bot*\n\n"
        f"📊 *Opportunity Risk Score*: {band_icon} *{eval_res['risk_band'].upper()}* ({eval_res['risk_score']}/100)\n"
        f"*Warnings Detected*:{warnings_str}\n\n"
        f"💡 *Recommendation*: {eval_res['recommendation']}\n\n"
        f"🔗 _For detailed report & scam search, visit ScamCheck Web App_"
    )

    return {"reply": reply, "evaluation": eval_res}
