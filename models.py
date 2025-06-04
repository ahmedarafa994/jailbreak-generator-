from app import db
from datetime import datetime
from sqlalchemy import Text, Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

class KnowledgeEntry(db.Model):
    """Model for storing knowledge entries and their metadata"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    knowledge_text: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<KnowledgeEntry {self.id}: {self.domain}>'

class JailbreakAttempt(db.Model):
    """Model for storing jailbreak generation attempts and results"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    knowledge_entry_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('knowledge_entry.id'), nullable=False)
    generated_jailbreak: Mapped[str] = mapped_column(Text, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=True)
    effectiveness_score: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    knowledge_entry = db.relationship('KnowledgeEntry', backref='jailbreak_attempts')
    
    def __repr__(self):
        return f'<JailbreakAttempt {self.id}>'

class SafetyEvaluation(db.Model):
    """Model for storing safety evaluation results"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jailbreak_attempt_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('jailbreak_attempt.id'), nullable=False)
    target_llm: Mapped[str] = mapped_column(String(100), nullable=False)
    llm_response: Mapped[str] = mapped_column(Text, nullable=True)
    safety_score: Mapped[float] = mapped_column(Float, nullable=True)
    is_harmful: Mapped[bool] = mapped_column(db.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    jailbreak_attempt = db.relationship('JailbreakAttempt', backref='safety_evaluations')
    
    def __repr__(self):
        return f'<SafetyEvaluation {self.id}: {self.target_llm}>'

class ResearchPaper(db.Model):
    """Model for storing integrated research papers"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=True)
    arxiv_id: Mapped[str] = mapped_column(String(50), nullable=True)
    source_file: Mapped[str] = mapped_column(String(200), nullable=True)
    integration_status: Mapped[str] = mapped_column(String(50), default='processed')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResearchPaper {self.id}: {self.title[:50]}...>'

class ExtractedTechnique(db.Model):
    """Model for storing techniques extracted from research papers"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    research_paper_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('research_paper.id'), nullable=False)
    technique_name: Mapped[str] = mapped_column(String(200), nullable=False)
    technique_description: Mapped[str] = mapped_column(Text, nullable=False)
    technique_type: Mapped[str] = mapped_column(String(100), nullable=False)  # 'attack', 'defense', 'evaluation'
    complexity_level: Mapped[str] = mapped_column(String(50), nullable=True)
    effectiveness_estimate: Mapped[float] = mapped_column(Float, nullable=True)
    implementation_priority: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    research_paper = db.relationship('ResearchPaper', backref='extracted_techniques')
    
    def __repr__(self):
        return f'<ExtractedTechnique {self.id}: {self.technique_name}>'
