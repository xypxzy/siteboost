from celery import chain
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.services import parser_service, analyzer_service, recommender_service


@celery_app.task
def start_analysis_pipeline(analysis_id: str):
    """Start the complete analysis pipeline"""
    db = SessionLocal()
    try:
        # Create chain of tasks
        analysis_chain = chain(
            parse_website.s(analysis_id), run_analysis.s(), generate_recommendations.s()
        )

        # Execute chain
        analysis_chain.apply_async()
    finally:
        db.close()


@celery_app.task
def parse_website(analysis_id: str):
    """Parse website content"""
    db = SessionLocal()
    try:
        parser_service.fetch_and_parse_website(analysis_id, db)
        return analysis_id
    finally:
        db.close()


@celery_app.task
def run_analysis(analysis_id: str):
    """Run all analysis tasks"""
    db = SessionLocal()
    try:
        analyzer_service.run_parallel_analysis(analysis_id, db)
        return analysis_id
    finally:
        db.close()


@celery_app.task
def generate_recommendations(analysis_id: str):
    """Generate recommendations"""
    db = SessionLocal()
    try:
        recommender_service.generate_recommendations(analysis_id, db)
        return analysis_id
    finally:
        db.close()
