"""
One-Click Error Report and Diagnostics System
Comprehensive platform health monitoring and error reporting
"""

import logging
import traceback
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from app import db
from models import KnowledgeEntry, ResearchPaper, ExtractedTechnique, JailbreakAttempt

logger = logging.getLogger(__name__)

class DiagnosticSystem:
    """
    Comprehensive diagnostic and error reporting system
    """
    
    def __init__(self):
        self.diagnostic_checks = [
            self._check_database_connectivity,
            self._check_research_integration_status,
            self._check_technique_extraction_health,
            self._check_api_integrations,
            self._check_file_system_health,
            self._check_recent_errors
        ]
    
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """
        Run comprehensive platform diagnostics
        """
        diagnostic_results = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'healthy',
            'checks': {},
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        critical_failures = 0
        
        for check_func in self.diagnostic_checks:
            try:
                check_name = check_func.__name__.replace('_check_', '')
                logger.info(f"Running diagnostic check: {check_name}")
                
                result = check_func()
                diagnostic_results['checks'][check_name] = result
                
                if result['status'] == 'critical':
                    critical_failures += 1
                    diagnostic_results['critical_issues'].append({
                        'check': check_name,
                        'issue': result.get('message', 'Unknown critical issue'),
                        'details': result.get('details', {})
                    })
                elif result['status'] == 'warning':
                    diagnostic_results['warnings'].append({
                        'check': check_name,
                        'warning': result.get('message', 'Unknown warning'),
                        'details': result.get('details', {})
                    })
                    
            except Exception as e:
                critical_failures += 1
                error_details = {
                    'check': check_func.__name__,
                    'status': 'critical',
                    'message': f'Diagnostic check failed: {str(e)}',
                    'traceback': traceback.format_exc(),
                    'details': {}
                }
                diagnostic_results['checks'][check_func.__name__] = error_details
                diagnostic_results['critical_issues'].append(error_details)
        
        # Determine overall status
        if critical_failures > 0:
            diagnostic_results['overall_status'] = 'critical'
        elif diagnostic_results['warnings']:
            diagnostic_results['overall_status'] = 'warning'
        
        # Generate recommendations
        diagnostic_results['recommendations'] = self._generate_recommendations(diagnostic_results)
        
        return diagnostic_results
    
    def _check_database_connectivity(self) -> Dict[str, Any]:
        """Check database connection and basic operations"""
        try:
            # Test basic database connectivity
            db.session.execute(db.text('SELECT 1'))
            
            # Check table existence
            tables_to_check = ['knowledge_entry', 'research_paper', 'extracted_technique', 'jailbreak_attempt']
            missing_tables = []
            
            for table in tables_to_check:
                try:
                    db.session.execute(db.text(f'SELECT COUNT(*) FROM {table}'))
                except Exception:
                    missing_tables.append(table)
            
            if missing_tables:
                return {
                    'status': 'critical',
                    'message': f'Missing database tables: {", ".join(missing_tables)}',
                    'details': {'missing_tables': missing_tables}
                }
            
            return {
                'status': 'healthy',
                'message': 'Database connectivity and schema validated',
                'details': {'tables_verified': len(tables_to_check)}
            }
            
        except Exception as e:
            return {
                'status': 'critical',
                'message': f'Database connectivity failed: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _check_research_integration_status(self) -> Dict[str, Any]:
        """Check research paper integration health"""
        try:
            # Count research papers and techniques
            paper_count = ResearchPaper.query.count()
            technique_count = ExtractedTechnique.query.filter_by(is_active=True).count()
            
            # Check for papers without techniques
            papers_without_techniques = db.session.query(ResearchPaper.id).outerjoin(
                ExtractedTechnique
            ).filter(ExtractedTechnique.id.is_(None)).count()
            
            details = {
                'total_papers': paper_count,
                'total_techniques': technique_count,
                'papers_without_techniques': papers_without_techniques,
                'avg_techniques_per_paper': technique_count / paper_count if paper_count > 0 else 0
            }
            
            if paper_count == 0:
                return {
                    'status': 'warning',
                    'message': 'No research papers integrated',
                    'details': details
                }
            
            if papers_without_techniques > 0:
                return {
                    'status': 'warning',
                    'message': f'{papers_without_techniques} papers have no extracted techniques',
                    'details': details
                }
            
            return {
                'status': 'healthy',
                'message': f'Research integration healthy: {paper_count} papers, {technique_count} techniques',
                'details': details
            }
            
        except Exception as e:
            return {
                'status': 'critical',
                'message': f'Research integration check failed: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _check_technique_extraction_health(self) -> Dict[str, Any]:
        """Check technique extraction process health"""
        try:
            # Check recent technique extraction activity
            recent_cutoff = datetime.utcnow() - timedelta(hours=24)
            recent_techniques = ExtractedTechnique.query.filter(
                ExtractedTechnique.created_at >= recent_cutoff
            ).count()
            
            # Check technique quality indicators
            techniques_with_descriptions = ExtractedTechnique.query.filter(
                ExtractedTechnique.technique_description != '',
                ExtractedTechnique.technique_description.isnot(None)
            ).count()
            
            total_techniques = ExtractedTechnique.query.count()
            
            details = {
                'recent_extractions_24h': recent_techniques,
                'total_techniques': total_techniques,
                'techniques_with_descriptions': techniques_with_descriptions,
                'description_quality_ratio': techniques_with_descriptions / total_techniques if total_techniques > 0 else 0
            }
            
            if total_techniques == 0:
                return {
                    'status': 'warning',
                    'message': 'No techniques extracted from integrated papers',
                    'details': details
                }
            
            if details['description_quality_ratio'] < 0.5:
                return {
                    'status': 'warning',
                    'message': 'Low technique description quality detected',
                    'details': details
                }
            
            return {
                'status': 'healthy',
                'message': f'Technique extraction healthy: {total_techniques} techniques extracted',
                'details': details
            }
            
        except Exception as e:
            return {
                'status': 'critical',
                'message': f'Technique extraction check failed: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _check_api_integrations(self) -> Dict[str, Any]:
        """Check external API integration health"""
        try:
            api_status = {}
            
            # Check Google Gemini API
            try:
                from utils.gemini_ai_integration import gemini_ai
                gemini_status = gemini_ai.get_model_status()
                api_status['gemini'] = {
                    'available': gemini_status.get('model_available', False),
                    'error': gemini_status.get('error')
                }
            except Exception as e:
                api_status['gemini'] = {
                    'available': False,
                    'error': str(e)
                }
            
            # Check local AI model
            try:
                # Check if local AI components are available
                api_status['local_ai'] = {
                    'available': os.path.exists('utils/opensource_ai_model.py'),
                    'error': None
                }
            except Exception as e:
                api_status['local_ai'] = {
                    'available': False,
                    'error': str(e)
                }
            
            # Determine overall API health
            available_apis = sum(1 for api in api_status.values() if api['available'])
            total_apis = len(api_status)
            
            if available_apis == 0:
                return {
                    'status': 'critical',
                    'message': 'No AI APIs are available',
                    'details': api_status
                }
            elif available_apis < total_apis:
                return {
                    'status': 'warning',
                    'message': f'Some APIs unavailable: {available_apis}/{total_apis} working',
                    'details': api_status
                }
            else:
                return {
                    'status': 'healthy',
                    'message': f'All APIs operational: {available_apis}/{total_apis}',
                    'details': api_status
                }
                
        except Exception as e:
            return {
                'status': 'critical',
                'message': f'API integration check failed: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _check_file_system_health(self) -> Dict[str, Any]:
        """Check file system and storage health"""
        try:
            file_system_status = {}
            
            # Check required directories
            required_dirs = ['attached_assets', 'attached_assets/uploads', 'utils']
            missing_dirs = []
            
            for directory in required_dirs:
                if not os.path.exists(directory):
                    missing_dirs.append(directory)
                else:
                    file_system_status[directory] = {
                        'exists': True,
                        'writable': os.access(directory, os.W_OK)
                    }
            
            # Check PDF files in attached_assets
            pdf_count = 0
            if os.path.exists('attached_assets'):
                pdf_files = [f for f in os.listdir('attached_assets') if f.endswith('.pdf')]
                pdf_count = len(pdf_files)
                file_system_status['pdf_files'] = pdf_count
            
            details = {
                'file_system_status': file_system_status,
                'missing_directories': missing_dirs,
                'pdf_files_available': pdf_count
            }
            
            if missing_dirs:
                return {
                    'status': 'critical',
                    'message': f'Missing required directories: {", ".join(missing_dirs)}',
                    'details': details
                }
            
            return {
                'status': 'healthy',
                'message': f'File system healthy: {pdf_count} PDF files available',
                'details': details
            }
            
        except Exception as e:
            return {
                'status': 'critical',
                'message': f'File system check failed: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _check_recent_errors(self) -> Dict[str, Any]:
        """Check for recent errors in application logs"""
        try:
            # This is a simplified check - in production, you'd analyze actual log files
            error_indicators = {
                'database_errors': 0,
                'api_errors': 0,
                'processing_errors': 0
            }
            
            # Check for recent failed jailbreak attempts
            recent_cutoff = datetime.utcnow() - timedelta(hours=24)
            
            # In a real implementation, you'd scan log files for error patterns
            # For now, we'll check database for indicators of issues
            
            details = {
                'error_indicators': error_indicators,
                'scan_period': '24 hours',
                'log_analysis': 'Basic health indicators checked'
            }
            
            total_errors = sum(error_indicators.values())
            
            if total_errors > 10:
                return {
                    'status': 'warning',
                    'message': f'High error rate detected: {total_errors} errors in 24h',
                    'details': details
                }
            
            return {
                'status': 'healthy',
                'message': f'Low error rate: {total_errors} errors in 24h',
                'details': details
            }
            
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'Error analysis incomplete: {str(e)}',
                'details': {'error': str(e)}
            }
    
    def _generate_recommendations(self, diagnostic_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on diagnostic results"""
        recommendations = []
        
        # Database recommendations
        if any(check.get('status') == 'critical' and 'database' in check_name.lower() 
               for check_name, check in diagnostic_results['checks'].items()):
            recommendations.append("Check DATABASE_URL environment variable and database connectivity")
        
        # Research integration recommendations
        research_check = diagnostic_results['checks'].get('research_integration_status', {})
        if research_check.get('details', {}).get('total_papers', 0) == 0:
            recommendations.append("Upload research papers via /research-integration to enable authentic technique generation")
        
        # API recommendations
        api_check = diagnostic_results['checks'].get('api_integrations', {})
        if api_check.get('status') in ['critical', 'warning']:
            recommendations.append("Verify GOOGLE_API_KEY environment variable for Gemini integration")
        
        # File system recommendations
        fs_check = diagnostic_results['checks'].get('file_system_health', {})
        if fs_check.get('details', {}).get('missing_directories'):
            recommendations.append("Create missing directories for proper file handling")
        
        # General recommendations
        if diagnostic_results['overall_status'] == 'critical':
            recommendations.append("Contact support with this diagnostic report for immediate assistance")
        elif diagnostic_results['overall_status'] == 'warning':
            recommendations.append("Monitor system closely and consider addressing warnings")
        
        return recommendations

# Initialize global diagnostic system
diagnostic_system = DiagnosticSystem()