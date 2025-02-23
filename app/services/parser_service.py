import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models.analysis import Analysis, AnalysisStatus
from app.core.celery_app import celery_app
from app.services.webhook_service import send_webhook_notification


class ParserService:
    async def create_analysis_request(
        self, db: Session, url: str, settings: dict, user_id: str
    ) -> Analysis:
        """Create initial analysis record"""
        analysis = Analysis(
            url=url,
            analysis_settings=settings,
            created_by=user_id,
            status=AnalysisStatus.PENDING,
            correlation_id=str(uuid4()),
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    async def fetch_and_parse_website(self, analysis_id: str, db: Session):
        """Parse website content and metadata"""
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(analysis.url) as response:
                    html_content = await response.text()

            # Parse HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract metadata
            metadata = {
                "title": soup.title.string if soup.title else None,
                "meta_tags": [tag.attrs for tag in soup.find_all("meta")],
                "links": [link.attrs for link in soup.find_all("link")],
            }

            # Save initial data
            analysis.html_content = html_content
            analysis.metadata = metadata
            analysis.status = AnalysisStatus.PROCESSING
            db.commit()

            # Notify about parsing completion
            await send_webhook_notification(
                analysis_id=analysis_id,
                event_type="parsing_complete",
                data={"metadata": metadata},
            )

            # Schedule analysis tasks
            celery_app.send_task(
                "app.tasks.analysis.start_analysis_tasks", args=[analysis_id]
            )

        except Exception as e:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_details = str(e)
            db.commit()
            raise


parser_service = ParserService()
