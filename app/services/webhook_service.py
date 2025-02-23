import aiohttp
from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.models.webhook import WebhookConfig, WebhookDelivery
from app.models.webhook import AnalysisEvent


async def send_webhook_notification(
    analysis_id: str, event_type: str, data: dict, db: Session = None
):
    """Send webhook notification to all configured endpoints"""
    if db is None:
        db = SessionLocal()

    try:
        # Create event record
        event = AnalysisEvent(
            analysis_id=analysis_id, event_type=event_type, event_data=data
        )
        db.add(event)
        db.commit()

        # Get webhook configs
        webhook_configs = (
            db.query(WebhookConfig)
            .join(Analysis)
            .filter(Analysis.id == analysis_id)
            .filter(WebhookConfig.is_active == True)
            .all()
        )

        # Send notifications
        async with aiohttp.ClientSession() as session:
            for config in webhook_configs:
                try:
                    async with session.post(
                        config.url,
                        json={
                            "event": event_type,
                            "analysisId": analysis_id,
                            "data": data,
                        },
                        headers={"X-Webhook-Secret": config.secret},
                    ) as response:
                        # Record delivery
                        delivery = WebhookDelivery(
                            webhook_config_id=config.id,
                            analysis_event_id=event.id,
                            status="success" if response.status == 200 else "failed",
                            response_details={
                                "status": response.status,
                                "body": await response.text(),
                            },
                        )
                        db.add(delivery)

                except Exception as e:
                    # Record failed delivery
                    delivery = WebhookDelivery(
                        webhook_config_id=config.id,
                        analysis_event_id=event.id,
                        status="failed",
                        error_details=str(e),
                    )
                    db.add(delivery)

        db.commit()

    finally:
        if db:
            db.close()
