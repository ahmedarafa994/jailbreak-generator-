from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from models import KnowledgeEntry, JailbreakAttempt, SafetyEvaluation, ResearchPaper, ExtractedTechnique
from easyjailbreak.utils.knowledge_processor import process_knowledge
from easyjailbreak.utils.jailbreak_generator import generate_jailbreak
# Assuming these specific framework integrations are still relevant for other parts or future use.
# If they are only for the very complex /api/test-processing that was removed/simplified, some might be unused.
from easyjailbreak.utils.transferattack_integration import generate_transferattack_framework_jailbreak
from easyjailbreak.utils.igcg_integration import generate_igcg_framework_jailbreak
from easyjailbreak.utils.footindoor_integration import generate_footindoor_framework_jailbreak
from easyjailbreak.utils.knowledge_enhancement_engine import enhance_knowledge_with_ai_prompting
from easyjailbreak.utils.sqlinjection_integration import generate_sqlinjection_framework_jailbreak
from easyjailbreak.utils.hyde_integration import generate_hyde_framework_jailbreak
from easyjailbreak.utils.complete_autodan_strategies import autodan_strategist, get_available_autodan_strategies, get_strategy_categories
from easyjailbreak.utils.overthink_integration import generate_overthink_autodan_jailbreak, overthink_integrator
from easyjailbreak.utils.bot_integration import generate_triple_framework_jailbreak, bot_integrator
from easyjailbreak.utils.flipattack_integration import generate_quad_framework_jailbreak, flipattack_integrator
from easyjailbreak.utils.tap_integration import generate_tap_framework_jailbreak
from easyjailbreak.utils.gptfuzz_integration import generate_gptfuzz_framework_jailbreak
from easyjailbreak.utils.pif_transferable_attacks import generate_pif_transferable_jailbreak
from easyjailbreak.utils.adversarial_triggers import generate_adversarial_trigger_jailbreak
from easyjailbreak.utils.chain_iterative_chaos import generate_chain_iterative_chaos_jailbreak
from easyjailbreak.utils.pathseeker_framework import generate_pathseeker_jailbreak
from easyjailbreak.utils.adversarial_self_replicating import generate_adversarial_self_replicating_jailbreak
from easyjailbreak.utils.jailbreakv_28k_framework import generate_jailbreakv_28k_jailbreak
from easyjailbreak.utils.jailbreakv_mllm_framework import generate_jailbreakv_mllm_jailbreak

import logging
from datetime import datetime # Added missing import

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Supported research domains extracted from comprehensive technique database
SUPPORTED_DOMAINS = [
    # Core AI Security Research Domains
    'AI Safety Research',
    'General AI Security',
    'Machine Learning Security',
    'Adversarial AI',
    'AI Ethics & Alignment',

    # Specialized Attack Research Domains
    'Automated Attack Systems',
    'Context Manipulation',
    'Token Engineering',
    'Mathematical AI Security',
    'AI Reasoning Security',

    # Multi-Modal & Vision Security Domains
    'Computer Vision Security',
    'Multimodal AI Security',
    'Vision-Language Models',
    'Image-Text Adversarial',

    # Advanced Security Technique Domains
    'Cryptographic Security',
    'Human-AI Interaction Security',
    'Security Testing & Evaluation',
    'Defense Development',

    # Implementation & Applied Research Domains
    'Prompt Engineering',
    'Large Language Models',
    'Natural Language Processing',
    'Reinforcement Learning',

    # Emerging Research Areas
    'Jailbreak Generation',
    'Prompt Injection Research',
    'System Prompt Analysis',
    'LLM Vulnerability Assessment',
    'Red Team Methodology',
    'Blue Team Defense Systems'
]

# Target LLMs for safety evaluation
TARGET_LLMS = [
    'GPT-4', 'GPT-3.5-turbo', 'Claude-3', 'Gemini Pro',
    'LLaMA-2', 'PaLM-2', 'Mixtral-8x7B', 'Mistral-7B'
]

@app.route('/')
def index():
    """Home page with overview of the application"""
    recent_jailbreaks = JailbreakAttempt.query.order_by(JailbreakAttempt.created_at.desc()).limit(5).all()
    recent_evaluations = SafetyEvaluation.query.order_by(SafetyEvaluation.created_at.desc()).limit(5).all()

    total_knowledge = KnowledgeEntry.query.count()
    total_jailbreaks = JailbreakAttempt.query.count()
    total_evaluations = SafetyEvaluation.query.count()

    stats = {
        'total_knowledge_entries': total_knowledge,
        'total_jailbreaks': total_jailbreaks,
        'total_evaluations': total_evaluations
    }

    return render_template('index.html',
                           stats=stats,
                           recent_jailbreaks=recent_jailbreaks,
                           recent_evaluations=recent_evaluations,
                           domains=SUPPORTED_DOMAINS)

@app.route('/knowledge-input', methods=['GET', 'POST'])
def knowledge_input():
    """Interface for inputting domain-specific knowledge"""
    if request.method == 'POST':
        domain = request.form.get('domain')
        knowledge_text = request.form.get('knowledge_text')
        source = request.form.get('source', '')
        objective = request.form.get('objective', '').strip() # Get objective here to use in error re-render

        if not domain or not knowledge_text:
            flash('Domain and knowledge text are required.', 'error')
            return render_template('knowledge_input.html', domains=SUPPORTED_DOMAINS,
                                   current_domain=domain, current_knowledge=knowledge_text,
                                   current_source=source, current_objective=objective)

        if domain not in SUPPORTED_DOMAINS:
            flash('Please select a valid domain.', 'error')
            return render_template('knowledge_input.html', domains=SUPPORTED_DOMAINS,
                                   current_domain=domain, current_knowledge=knowledge_text,
                                   current_source=source, current_objective=objective)

        if not objective:
            flash('Research objective is required', 'error')
            return render_template('knowledge_input.html', domains=SUPPORTED_DOMAINS,
                                   current_domain=domain, current_knowledge=knowledge_text,
                                   current_source=source, current_objective=objective) # Pass objective back

        try:
            processed_knowledge = process_knowledge(knowledge_text, domain)

            knowledge_entry = KnowledgeEntry(
                domain=domain,
                objective=objective,
                knowledge_text=processed_knowledge,
                source=source
            )

            db.session.add(knowledge_entry)
            db.session.commit()
            app.logger.info(f"Knowledge entry created with ID: {knowledge_entry.id}")

            try:
                from easyjailbreak.utils.comprehensive_technique_integration import generate_comprehensive_research_prompt, initialize_comprehensive_integration
                initialize_comprehensive_integration()

                jailbreak_result = generate_comprehensive_research_prompt(
                    knowledge_entry.objective,
                    knowledge_entry.domain,
                    knowledge_entry.knowledge_text
                )

                jailbreak_attempt = JailbreakAttempt(
                    knowledge_entry_id=knowledge_entry.id,
                    generated_jailbreak=jailbreak_result['jailbreak'],
                    relevance_score=jailbreak_result.get('relevance_score'),
                    effectiveness_score=jailbreak_result.get('effectiveness_score')
                )
                db.session.add(jailbreak_attempt)
                db.session.commit()

                flash('Knowledge processed and jailbreak generated successfully!', 'success')
                return render_template('jailbreak_results.html',
                                       knowledge_entry=knowledge_entry,
                                       jailbreak_attempt=jailbreak_attempt,
                                       target_llms=TARGET_LLMS)
            except Exception as jb_error:
                app.logger.error(f"Error generating jailbreak after knowledge input: {str(jb_error)}")
                flash('Knowledge saved but jailbreak generation failed. Please try again or generate manually.', 'warning')
                return redirect(url_for('jailbreak_results', knowledge_id=knowledge_entry.id)) # Redirect to results page for the entry

        except Exception as e:
            app.logger.error(f"Error processing knowledge: {str(e)}")
            flash('Error processing knowledge. Please try again.', 'error')
            return render_template('knowledge_input.html', domains=SUPPORTED_DOMAINS,
                                   current_domain=domain, current_knowledge=knowledge_text,
                                   current_source=source, current_objective=objective)

    return render_template('knowledge_input.html', domains=SUPPORTED_DOMAINS)

@app.route('/generate-jailbreak/<int:knowledge_id>')
def generate_jailbreak_view(knowledge_id):
    """Generate jailbreak from knowledge entry"""
    knowledge_entry = KnowledgeEntry.query.get_or_404(knowledge_id)
    try:
        from easyjailbreak.utils.research_enhanced_generator import research_enhanced_generator
        available_techniques_count = ExtractedTechnique.query.filter_by(is_active=True).count()

        if available_techniques_count > 0:
            jailbreak_result = research_enhanced_generator.generate_research_enhanced_jailbreak(
                knowledge_entry.knowledge_text, knowledge_entry.domain
            )
        else:
            from easyjailbreak.utils.complete_autodan_strategies import generate_autodan_jailbreak
            jailbreak_result = generate_autodan_jailbreak(knowledge_entry.knowledge_text, knowledge_entry.domain)

        jailbreak_attempt = JailbreakAttempt(
            knowledge_entry_id=knowledge_entry.id,
            generated_jailbreak=jailbreak_result['jailbreak'],
            relevance_score=jailbreak_result.get('relevance_score'),
            effectiveness_score=jailbreak_result.get('effectiveness_score')
        )
        db.session.add(jailbreak_attempt)
        db.session.commit()

        return render_template('jailbreak_results.html',
                               knowledge_entry=knowledge_entry,
                               jailbreak_attempt=jailbreak_attempt,
                               target_llms=TARGET_LLMS)
    except Exception as e:
        app.logger.error(f"Error generating jailbreak for knowledge ID {knowledge_id}: {str(e)}")
        flash('Error generating jailbreak. Please try again.', 'error')
        return redirect(url_for('knowledge_input'))

@app.route('/jailbreak-results')
def jailbreak_results():
    """View all jailbreak results"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    knowledge_id_filter = request.args.get('knowledge_id', type=int)

    query = JailbreakAttempt.query
    if knowledge_id_filter:
        query = query.filter_by(knowledge_entry_id=knowledge_id_filter)

    jailbreaks_pagination = query.order_by(JailbreakAttempt.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    knowledge_entry_for_display = None
    if knowledge_id_filter:
        knowledge_entry_for_display = KnowledgeEntry.query.get(knowledge_id_filter)

    # If coming from a generation flow for a specific knowledge_id, and there's a jailbreak for it,
    # pass that specific jailbreak_attempt. Otherwise, pass the first of the paginated list.
    specific_jailbreak_attempt = None
    if knowledge_id_filter and jailbreaks_pagination.items:
        # Find the most recent jailbreak for this specific knowledge_id
        specific_jailbreak_attempt = JailbreakAttempt.query.filter_by(knowledge_entry_id=knowledge_id_filter)\
                                                           .order_by(JailbreakAttempt.created_at.desc()).first()

    display_attempt = specific_jailbreak_attempt if specific_jailbreak_attempt else (jailbreaks_pagination.items[0] if jailbreaks_pagination.items else None)

    return render_template('jailbreak_results.html',
                           jailbreaks=jailbreaks_pagination,
                           jailbreak_attempt=display_attempt,
                           knowledge_entry=knowledge_entry_for_display,
                           target_llms=TARGET_LLMS)

@app.route('/safety-evaluation', methods=['GET', 'POST'])
def safety_evaluation():
    """Interface for evaluating jailbreak safety"""
    if request.method == 'POST':
        app.logger.info(f"Safety evaluation form submitted with data: {dict(request.form)}")

        jailbreak_id_str = request.form.get('jailbreak_id')
        target_llm = request.form.get('target_llm')
        llm_response = request.form.get('llm_response', '').strip()
        safety_score_str = request.form.get('safety_score')
        is_harmful = request.form.get('is_harmful') == 'on'

        jailbreak_id = None
        if jailbreak_id_str:
            try:
                jailbreak_id = int(jailbreak_id_str)
            except ValueError:
                flash('Invalid Jailbreak ID format.', 'error')
                return redirect(url_for('safety_evaluation'))


        safety_score = None
        if safety_score_str:
            try:
                safety_score = float(safety_score_str)
            except ValueError:
                flash('Invalid safety score format. Please enter a number.', 'error')
                return redirect(url_for('safety_evaluation', jailbreak_id=jailbreak_id)) # Pass ID back

        app.logger.info(f"Parsed form data: jailbreak_id={jailbreak_id}, target_llm={target_llm}, safety_score={safety_score}, is_harmful={is_harmful}")

        if not jailbreak_id:
            flash('Please select a jailbreak to evaluate.', 'error')
            return redirect(url_for('safety_evaluation'))
        if not target_llm:
            flash('Please select a target LLM.', 'error')
            return redirect(url_for('safety_evaluation', jailbreak_id=jailbreak_id))

        try:
            jailbreak_attempt = JailbreakAttempt.query.get(jailbreak_id)
            if not jailbreak_attempt:
                flash('Jailbreak attempt not found.', 'error')
                return redirect(url_for('safety_evaluation'))

            automated_assessment = None
            if llm_response: # Only run if response is provided
                try:
                    from easyjailbreak.utils.automated_safety_evaluator import automated_evaluator
                    automated_assessment = automated_evaluator.evaluate_jailbreak_response(
                        jailbreak_attempt.generated_jailbreak, llm_response, target_llm
                    )
                    if safety_score is None and automated_assessment and 'safety_score' in automated_assessment:
                        safety_score = automated_assessment.get('safety_score', 50.0)
                    if not request.form.get('is_harmful') and automated_assessment and 'is_harmful' in automated_assessment:
                        is_harmful = automated_assessment.get('is_harmful', False)
                except Exception as e:
                    app.logger.warning(f"Automated evaluation failed: {str(e)}")

            if safety_score is None:
                flash('Safety score is required if not automatically assessed.', 'error')
                return redirect(url_for('safety_evaluation', jailbreak_id=jailbreak_id))

            evaluation = SafetyEvaluation(
                jailbreak_attempt_id=jailbreak_id, target_llm=target_llm,
                llm_response=llm_response, safety_score=safety_score, is_harmful=is_harmful
            )
            db.session.add(evaluation)
            db.session.commit()

            if automated_assessment and automated_assessment.get("risk_level"):
                 flash(f'Safety evaluation saved! AI analysis: Risk Level {automated_assessment.get("risk_level", "N/A").upper()}', 'success')
            else:
                flash('Safety evaluation saved successfully!', 'success')

            return redirect(url_for('safety_evaluation')) # Redirect after successful POST

        except Exception as e:
            app.logger.error(f"Error creating safety evaluation: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Error processing safety evaluation. Please try again.', 'error')
            return redirect(url_for('safety_evaluation', jailbreak_id=jailbreak_id))

    # GET request
    all_jailbreaks = JailbreakAttempt.query.order_by(JailbreakAttempt.created_at.desc()).limit(50).all() # For dropdown
    recent_evaluations = SafetyEvaluation.query.order_by(SafetyEvaluation.created_at.desc()).limit(10).all()
    return render_template('safety_evaluation.html',
                           jailbreaks=all_jailbreaks,
                           recent_evaluations=recent_evaluations, # For display list
                           target_llms=TARGET_LLMS)

@app.route('/simple-test')
def simple_test():
    """Simple test page for emergency processing verification"""
    return render_template('simple_test.html')

@app.route('/api/test-processing', methods=['POST'])
def api_test_processing():
    """API endpoint for advanced AutoDAN + OVERTHINK processing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        objective = data.get('objective', 'Default objective for testing')
        knowledge_text = data.get('knowledge_text', 'Sample knowledge text for testing.')
        frameworks_to_test = data.get('frameworks', ['autodan', 'overthink']) # Default to these two

        results_summary = {}

        if 'autodan' in frameworks_to_test:
            try:
                # Assuming autodan_strategist.create_advanced_strategy exists and takes (objective, knowledge_text)
                autodan_result = autodan_strategist.create_advanced_strategy(objective, knowledge_text)
                results_summary['autodan'] = {
                    'status': 'success',
                    'strategy_name': autodan_result.get('strategy_name', autodan_result.get('strategy', 'Generated AutoDAN Strategy')),
                    'effectiveness_score': autodan_result.get('effectiveness_score', autodan_result.get('effectiveness', 0.75)),
                    'details': autodan_result.get('details', 'No specific details.')
                }
            except Exception as e:
                app.logger.error(f"AutoDAN processing error in API: {str(e)}", exc_info=True)
                results_summary['autodan'] = {'status': 'error', 'error_message': str(e)}

        if 'overthink' in frameworks_to_test:
            try:
                # Assuming overthink_integrator.generate_advanced_prompt exists and takes (objective, knowledge_text)
                overthink_result = overthink_integrator.generate_advanced_prompt(objective, knowledge_text)
                results_summary['overthink'] = {
                    'status': 'success',
                    'generated_prompt_snippet': overthink_result.get('prompt', 'Generated Overthink Prompt')[:100] + "...",
                    'complexity_level': overthink_result.get('complexity_level', overthink_result.get('complexity', 'high')),
                    'reasoning_steps': overthink_result.get('reasoning_steps', 0)
                }
            except Exception as e:
                app.logger.error(f"OVERTHINK processing error in API: {str(e)}", exc_info=True)
                results_summary['overthink'] = {'status': 'error', 'error_message': str(e)}

        return jsonify({
            'status': 'processing_attempted',
            'input_objective': objective,
            'frameworks_tested': frameworks_to_test,
            'results_summary': results_summary,
            'processing_complete_timestamp': datetime.utcnow().isoformat() + "Z"
        })

    except Exception as e:
        app.logger.error(f"API test processing general error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Overall processing failed: {str(e)}'}), 500

@app.route('/api/autodan-strategies')
def api_autodan_strategies():
    """API endpoint to get available AutoDAN strategies"""
    try:
        strategies = get_available_autodan_strategies()
        categories = get_strategy_categories()
        return jsonify({
            'status': 'success',
            'strategies': strategies,
            'categories': categories,
            'total_strategies': len(strategies)
        })
    except Exception as e:
        app.logger.error(f"Error fetching AutoDAN strategies: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/diagnostic')
def diagnostic():
    """Diagnostic page for testing processing functionality"""
    frameworks_status_summary = {}
    try:
        strategies = get_available_autodan_strategies()
        frameworks_status_summary['autodan'] = {
            'status': 'available', 'details': f"{len(strategies)} strategies found."
        }
    except Exception as e:
        frameworks_status_summary['autodan'] = {'status': 'error', 'details': str(e)}

    try:
        from easyjailbreak.utils.overthink_integration import overthink_integrator # Test import
        # Could add a simple test call if overthink_integrator has a status or test method
        frameworks_status_summary['overthink'] = {'status': 'available', 'details': 'Integrator loaded.'}
    except Exception as e:
        frameworks_status_summary['overthink'] = {'status': 'error', 'details': str(e)}

    return render_template('diagnostic.html', frameworks_status=frameworks_status_summary)

@app.route('/about')
def about():
    """About page with research information"""
    return render_template('about.html')

@app.route('/technique-analysis')
def technique_analysis_page(): # Renamed to avoid conflict if there's an import named technique_analysis
    """Advanced technique analysis dashboard"""
    try:
        active_techniques_list = ExtractedTechnique.query.filter_by(is_active=True).order_by(ExtractedTechnique.effectiveness_estimate.desc()).all()
        technique_count_val = len(active_techniques_list)

        technique_types_map = {}
        for tech in active_techniques_list:
            technique_types_map.setdefault(tech.technique_type, []).append(tech)

        recent_papers_list = ResearchPaper.query.order_by(ResearchPaper.created_at.desc()).limit(10).all()

        return render_template('technique_analysis.html',
                               active_techniques=active_techniques_list,
                               technique_count=technique_count_val,
                               technique_types=technique_types_map,
                               recent_papers=recent_papers_list)
    except Exception as e:
        app.logger.error(f"Error in technique analysis page: {str(e)}", exc_info=True)
        flash('Error loading technique analysis page. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/technique-analytics')
def api_technique_analytics():
    """API endpoint for technique analytics and insights"""
    try:
        total_techniques_val = ExtractedTechnique.query.count()
        active_techniques_val = ExtractedTechnique.query.filter_by(is_active=True).count()

        technique_stats_q = db.session.query(
            ExtractedTechnique.technique_type, db.func.count(ExtractedTechnique.id).label('count')
        ).filter_by(is_active=True).group_by(ExtractedTechnique.technique_type).all()

        complexity_stats_q = db.session.query(
            ExtractedTechnique.complexity_level, db.func.count(ExtractedTechnique.id).label('count')
        ).filter_by(is_active=True).group_by(ExtractedTechnique.complexity_level).all()

        return jsonify({
            'status': 'success',
            'total_techniques': total_techniques_val,
            'active_techniques': active_techniques_val,
            'technique_types_distribution': {stat.technique_type: stat.count for stat in technique_stats_q},
            'complexity_levels_distribution': {stat.complexity_level: stat.count for stat in complexity_stats_q}
        })
    except Exception as e:
        app.logger.error(f"Error in API technique analytics: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/technique-detail/<int:technique_id>')
def api_technique_detail(technique_id):
    """API endpoint for detailed technique analysis"""
    try:
        technique = ExtractedTechnique.query.get_or_404(technique_id)
        paper = ResearchPaper.query.get(technique.research_paper_id) if technique.research_paper_id else None

        return jsonify({
            'status': 'success',
            'technique': {
                'id': technique.id,
                'name': technique.technique_name,
                'description': technique.technique_description,
                'type': technique.technique_type,
                'complexity': technique.complexity_level,
                'effectiveness': technique.effectiveness_estimate,
                'priority': technique.implementation_priority,
                'is_active': technique.is_active,
                'created_at': technique.created_at.isoformat() if technique.created_at else None,
                'updated_at': technique.updated_at.isoformat() if technique.updated_at else None,
                'research_paper_id': technique.research_paper_id,
                'paper_title': paper.title if paper else "N/A",
                'paper_arxiv_id': paper.arxiv_id if paper and paper.arxiv_id else "N/A"
            }
        })
    except Exception as e: # Catch specific SQLAlchemy NoResultFound if using get_or_404, or general Exception
        app.logger.error(f"Error getting technique detail for ID {technique_id}: {str(e)}", exc_info=True)
        if "404 Not Found" in str(e): # More specific error for 404 from get_or_404
             return jsonify({'error': f'Technique with ID {technique_id} not found.'}), 404
        return jsonify({'error': str(e)}), 500


@app.route('/integration-demo')
def integration_demo():
    """Demo page showing true integration vs display-only processing"""
    try:
        total_techniques_val = ExtractedTechnique.query.count()
        active_techniques_val = ExtractedTechnique.query.filter_by(is_active=True).count()
        research_papers_val = ResearchPaper.query.count()

        frameworks_status_summary = {}
        try:
            from easyjailbreak.utils.comprehensive_technique_integration import get_integration_status
            frameworks_status_summary['comprehensive'] = get_integration_status()
        except Exception as e:
            frameworks_status_summary['comprehensive'] = {'status': 'error', 'details': str(e)}

        framework_modules_to_test = [
            ('autodan', 'easyjailbreak.utils.complete_autodan_strategies'), ('overthink', 'easyjailbreak.utils.overthink_integration'),
            ('bot', 'easyjailbreak.utils.bot_integration'), ('flipattack', 'easyjailbreak.utils.flipattack_integration')
        ]
        for name, path in framework_modules_to_test:
            try:
                __import__(path)
                frameworks_status_summary[name] = {'status': 'available', 'details': 'Module imported successfully.'}
            except Exception as e:
                frameworks_status_summary[name] = {'status': 'error', 'details': str(e)}

        return render_template('integration_demo.html',
                               total_techniques=total_techniques_val, active_techniques=active_techniques_val,
                               research_papers=research_papers_val, frameworks_status=frameworks_status_summary)
    except Exception as e:
        app.logger.error(f"Error in integration demo page: {str(e)}", exc_info=True)
        flash('Error loading integration demo page. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/knowledge-detail/<int:knowledge_id>') # Corrected route name to match function
def api_knowledge_detail_route(knowledge_id): # Renamed function to avoid conflict
    """API endpoint for knowledge details"""
    try:
        knowledge = KnowledgeEntry.query.get_or_404(knowledge_id)
        return jsonify({
            'status': 'success',
            'knowledge': {
                'id': knowledge.id, 'domain': knowledge.domain, 'objective': knowledge.objective,
                'knowledge_text_snippet': knowledge.knowledge_text[:500] + ('...' if len(knowledge.knowledge_text) > 500 else ''),
                'full_knowledge_text_available': True, # Indicate full text can be fetched if needed by another means or not sent for brevity
                'source': knowledge.source,
                'created_at': knowledge.created_at.isoformat() if knowledge.created_at else None
            }
        })
    except Exception as e:
        app.logger.error(f"Error getting knowledge detail for ID {knowledge_id}: {str(e)}", exc_info=True)
        if "404 Not Found" in str(e):
             return jsonify({'error': f'Knowledge entry with ID {knowledge_id} not found.'}), 404
        return jsonify({'error': str(e)}), 500

@app.route('/api/enhance-knowledge', methods=['POST'])
def api_enhance_knowledge():
    """API endpoint for AI-powered knowledge content enhancement"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        knowledge_text = data.get('knowledge_text', '')
        domain = data.get('domain', 'General AI Security') # Default domain
        # Corrected to match expected signature of enhance_knowledge_with_ai_prompting
        target_audience = data.get('target_audience', 'researcher') # Default audience
        optimization_goals = data.get('optimization_goals', ['clarity', 'depth', 'actionability']) # Default goals

        if not knowledge_text or not domain: # Target audience and goals can be optional with defaults
            return jsonify({'error': 'Knowledge text and domain are required'}), 400

        enhanced_result = enhance_knowledge_with_ai_prompting(
            knowledge_text, domain, target_audience, optimization_goals
        )

        return jsonify({
            'status': 'success',
            'enhanced_knowledge_text': enhanced_result.get('enhanced_text', enhanced_result.get('enhanced_content')), # Check for both keys
            'enhancement_details': enhanced_result.get('enhancement_details', enhanced_result.get('enhancement_metadata', {})),
            'original_length': len(knowledge_text),
            'enhanced_length': len(enhanced_result.get('enhanced_text', enhanced_result.get('enhanced_content',''))),
            'optimization_goals_applied': enhanced_result.get('optimization_goals', optimization_goals) # Reflect what was used
        })
    except Exception as e:
        app.logger.error(f"Error enhancing knowledge: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/integrate-paper', methods=['POST'])
def api_integrate_paper():
    """API endpoint for integrating research paper insights from URL (e.g., arXiv)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        paper_url = data.get('paper_url', '').strip()
        if not paper_url: # Basic validation for URL presence
            return jsonify({'error': 'Paper URL is required'}), 400
        if not (paper_url.startswith('http://') or paper_url.startswith('https://')): # Basic URL check
            return jsonify({'error': 'Invalid Paper URL format'}), 400


        from paper_integration import extract_arxiv_paper_content # Assuming this handles various paper URLs or is specific to arXiv
        paper_content_data = extract_arxiv_paper_content(paper_url) # This should return a dict

        # Create research paper entry
        paper = ResearchPaper(
            title=paper_content_data.get('title', 'Untitled Paper from URL'),
            abstract=paper_content_data.get('abstract', 'Abstract not available or extracted.'),
            arxiv_id=paper_content_data.get('arxiv_id'), # May be None if not arXiv
            source_file=paper_url, # Store the URL as source
            integration_status='integrated_via_url'
        )
        db.session.add(paper)
        db.session.commit() # Commit to get paper.id

        # Placeholder for technique extraction if paper_content_data includes them
        techniques_extracted_count = 0
        if 'techniques' in paper_content_data and isinstance(paper_content_data['techniques'], list):
            for tech_info in paper_content_data['techniques']:
                # Assuming tech_info is a dict with 'name', 'description', etc.
                ExtractedTechnique.create_from_dict(tech_info, research_paper_id=paper.id) # Assumes a helper method in model
                techniques_extracted_count +=1
            db.session.commit()


        return jsonify({
            'status': 'success',
            'paper_id': paper.id,
            'title': paper.title,
            'arxiv_id_found': paper.arxiv_id,
            'techniques_extracted_from_source': techniques_extracted_count, # If applicable
            'integration_status': 'completed_from_url'
        })
    except ImportError:
        app.logger.error(f"Paper integration module not found.", exc_info=True)
        return jsonify({'error': 'Paper integration module (e.g., paper_integration.py) is missing.'}), 501
    except Exception as e:
        app.logger.error(f"Error integrating paper from URL: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/research-integration')
def research_integration_page(): # Renamed function
    """Interface for research paper integration"""
    recent_papers_list = ResearchPaper.query.order_by(ResearchPaper.created_at.desc()).limit(10).all()
    total_techniques_val = ExtractedTechnique.query.count()
    return render_template('research_integration.html',
                           recent_papers=recent_papers_list,
                           total_techniques=total_techniques_val)

@app.route('/api/process-research-paper', methods=['POST'])
def api_process_research_paper_content(): # Renamed to distinguish from URL-based one
    """API endpoint for processing provided research paper content (text)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        paper_text_content = data.get('paper_content', '').strip()
        paper_title_val = data.get('paper_title', 'Untitled Paper (Processed Content)')

        if not paper_text_content:
            return jsonify({'error': 'Paper content (text) is required'}), 400

        from extract_paper_techniques import analyze_techniques # Assumes this utility exists
        extracted_techniques_list = analyze_techniques(paper_text_content) # Expects list of dicts

        paper = ResearchPaper(
            title=paper_title_val,
            abstract=paper_text_content[:500] + ('...' if len(paper_text_content) > 500 else ''), # Snippet as abstract
            integration_status='processed_content'
        )
        db.session.add(paper)
        db.session.commit() # To get paper.id

        technique_entries_count = 0
        for tech_data_dict in extracted_techniques_list:
            if isinstance(tech_data_dict, dict): # Ensure it's a dict
                # Assuming ExtractedTechnique model has a helper or direct constructor
                technique = ExtractedTechnique(
                    research_paper_id=paper.id,
                    technique_name=tech_data_dict.get('name', 'Unnamed Technique from Content'),
                    technique_description=tech_data_dict.get('description', ''),
                    technique_type=tech_data_dict.get('type', 'general'),
                    complexity_level=tech_data_dict.get('complexity', 'medium'),
                    effectiveness_estimate=float(tech_data_dict.get('effectiveness', 0.5)),
                    implementation_priority=tech_data_dict.get('priority', 'medium'),
                    is_active=True # Default to active
                )
                db.session.add(technique)
                technique_entries_count += 1
        db.session.commit()

        return jsonify({
            'status': 'success',
            'paper_id': paper.id,
            'title_processed': paper.title,
            'techniques_extracted_and_stored': technique_entries_count,
            'processing_status': 'completed_text_processing'
        })
    except ImportError:
        app.logger.error(f"Technique extraction module (extract_paper_techniques.py) not found.", exc_info=True)
        return jsonify({'error': 'Technique extraction module is missing.'}), 501
    except Exception as e:
        app.logger.error(f"Error processing research paper content: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/research-techniques-status')
def api_research_techniques_status():
    """API endpoint to check status of integrated research techniques"""
    try:
        total_papers_val = ResearchPaper.query.count()
        total_techniques_val = ExtractedTechnique.query.count()
        active_techniques_val = ExtractedTechnique.query.filter_by(is_active=True).count()

        recent_papers_q = ResearchPaper.query.order_by(ResearchPaper.created_at.desc()).limit(5).all()
        recent_techniques_q = ExtractedTechnique.query.order_by(ExtractedTechnique.created_at.desc()).limit(5).all()

        return jsonify({
            'status': 'success',
            'statistics': {
                'total_research_papers': total_papers_val,
                'total_extracted_techniques': total_techniques_val,
                'active_techniques_count': active_techniques_val,
                'integration_coverage_percentage': (active_techniques_val / total_techniques_val * 100) if total_techniques_val > 0 else 0
            },
            'recent_papers_added': [{'id': p.id, 'title': p.title, 'status': p.integration_status, 'added_at': p.created_at.isoformat() if p.created_at else None} for p in recent_papers_q],
            'recent_techniques_added': [{'id': t.id, 'name': t.technique_name, 'type': t.technique_type, 'active': t.is_active, 'added_at': t.created_at.isoformat() if t.created_at else None} for t in recent_techniques_q]
        })
    except Exception as e:
        app.logger.error(f"Error getting research techniques status: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-research-techniques')
def api_export_research_techniques():
    """API endpoint for exporting research techniques in various formats"""
    try:
        export_format_type = request.args.get('format', 'json').lower()
        active_techniques_list = ExtractedTechnique.query.filter_by(is_active=True).all()

        if not active_techniques_list:
             return jsonify({'status': 'warn', 'message': 'No active techniques to export.'}), 404

        if export_format_type == 'json':
            techniques_data_list = [{
                'id': t.id, 'name': t.technique_name, 'description': t.technique_description,
                'type': t.technique_type, 'complexity': t.complexity_level,
                'effectiveness': t.effectiveness_estimate, 'priority': t.implementation_priority,
                'created_at': t.created_at.isoformat() if t.created_at else None,
                'research_paper_id': t.research_paper_id
            } for t in active_techniques_list]
            return jsonify({
                'status': 'success', 'format': 'json',
                'total_techniques_exported': len(techniques_data_list),
                'techniques': techniques_data_list,
                'export_timestamp': datetime.utcnow().isoformat() + "Z"
            })

        elif export_format_type == 'csv':
            import csv
            import io
            output_io = io.StringIO()
            # Define headers carefully
            headers = ['ID', 'Name', 'Description', 'Type', 'Complexity', 'Effectiveness', 'Priority', 'Created At', 'Paper ID']
            writer = csv.writer(output_io)
            writer.writerow(headers)
            for t in active_techniques_list:
                writer.writerow([
                    t.id, t.technique_name, t.technique_description, t.technique_type,
                    t.complexity_level, t.effectiveness_estimate, t.implementation_priority,
                    t.created_at.isoformat() if t.created_at else None, t.research_paper_id
                ])
            output_io.seek(0)
            csv_response = make_response(output_io.getvalue())
            csv_response.headers['Content-Type'] = 'text/csv'
            csv_response.headers['Content-Disposition'] = f'attachment; filename=research_techniques_export_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
            return csv_response
        else:
            return jsonify({'error': 'Unsupported export format. Use "json" or "csv".'}), 400
    except Exception as e:
        app.logger.error(f"Error exporting research techniques: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-research-paper', methods=['POST'])
def api_upload_research_paper_file(): # Renamed function
    """API endpoint for uploading and processing PDF research papers"""
    try:
        if 'file' not in request.files: # Changed from 'paper_file' to 'file' to match common usage
            return jsonify({'error': 'No file part in the request. Ensure the key is "file".'}), 400

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({'error': 'No file selected for upload.'}), 400
        if not uploaded_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Only PDF files are supported.'}), 400

        import os
        import tempfile
        from pdf_research_extractor import extract_pdf_research_content # Assumed utility

        # Secure filename and create a temporary path
        # Werkzeug's secure_filename is good for this, or a similar custom approach.
        # For simplicity here, using a basic approach.
        base_filename = "".join(c for c in uploaded_file.filename if c.isalnum() or c in ['.', '_', '-']).strip()
        if not base_filename: base_filename = "uploaded_paper.pdf"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, base_filename)
            uploaded_file.save(temp_file_path)

            extracted_data = extract_pdf_research_content(temp_file_path) # Expects dict

            paper = ResearchPaper(
                title=extracted_data.get('title', base_filename),
                abstract=extracted_data.get('abstract', 'Abstract not extracted from PDF.'),
                source_file=base_filename, # Original filename stored
                integration_status='uploaded_pdf'
            )
            db.session.add(paper)
            db.session.commit() # To get paper.id

            techniques_stored_count = 0
            for tech_info_dict in extracted_data.get('techniques', []):
                if isinstance(tech_info_dict, dict):
                     # Assuming ExtractedTechnique.create_from_dict or similar helper
                    ExtractedTechnique.create_from_dict(tech_info_dict, research_paper_id=paper.id)
                    techniques_stored_count += 1
            db.session.commit()

            return jsonify({
                'status': 'success', 'message': f"File '{base_filename}' processed.",
                'paper_id': paper.id, 'title': paper.title,
                'techniques_extracted_and_stored': techniques_stored_count,
                'file_processed': base_filename
            })
    except ImportError:
        app.logger.error(f"PDF extraction module (pdf_research_extractor.py) not found.", exc_info=True)
        return jsonify({'error': 'PDF extraction module is missing.'}), 501
    except Exception as e:
        app.logger.error(f"Error uploading research paper: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/diagnostics-dashboard')
def diagnostics_dashboard_page(): # Renamed function
    """One-Click Error Report and Diagnostics Dashboard page"""
    # This page might fetch data via JS from /api/run-diagnostics or display static info
    return render_template('diagnostics_dashboard.html') # Ensure this template exists

@app.route('/api/run-diagnostics', methods=['POST'])
def api_run_diagnostics_action(): # Renamed function
    """API endpoint for running comprehensive platform diagnostics"""
    try:
        diagnostics_report = {'timestamp': datetime.utcnow().isoformat() + "Z", 'checks': {}}

        # Database Check
        try:
            diagnostics_report['checks']['database'] = {
                'status': 'healthy',
                'counts': {
                    'knowledge': KnowledgeEntry.query.count(), 'jailbreaks': JailbreakAttempt.query.count(),
                    'evaluations': SafetyEvaluation.query.count(), 'papers': ResearchPaper.query.count(),
                    'techniques': ExtractedTechnique.query.count()
                }}
        except Exception as db_err:
            diagnostics_report['checks']['database'] = {'status': 'error', 'detail': str(db_err)}

        # Framework Module Availability Check
        framework_modules = {
            'autodan': 'easyjailbreak.utils.complete_autodan_strategies', 'overthink': 'easyjailbreak.utils.overthink_integration',
            'comprehensive_integration': 'easyjailbreak.utils.comprehensive_technique_integration',
            'automated_safety_evaluator': 'easyjailbreak.utils.automated_safety_evaluator',
            'pdf_extractor': 'pdf_research_extractor', # Example, adjust as needed
            'paper_technique_extractor': 'extract_paper_techniques' # Example
        }
        diagnostics_report['checks']['framework_modules'] = {}
        for name, path in framework_modules.items():
            try:
                __import__(path)
                diagnostics_report['checks']['framework_modules'][name] = {'status': 'available'}
            except ImportError as imp_err:
                diagnostics_report['checks']['framework_modules'][name] = {'status': 'missing', 'detail': str(imp_err)}
            except Exception as gen_err:
                 diagnostics_report['checks']['framework_modules'][name] = {'status': 'error', 'detail': str(gen_err)}

        # Add more checks as needed (e.g., API connectivity to external services, specific util function tests)

        return jsonify({'status': 'success', 'diagnostics_report': diagnostics_report})
    except Exception as e:
        app.logger.error(f"Error running diagnostics API: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-technique-integration', methods=['POST']) # Changed to POST as it's an action
def api_verify_technique_integration_action(): # Renamed function
    """API endpoint to verify authentic research technique integration"""
    try:
        data = request.get_json() if request.is_json else {}
        verification_summary = {'timestamp': datetime.utcnow().isoformat() + "Z", 'steps': {}}

        # 1. Database Verification
        try:
            active_tech_count = ExtractedTechnique.query.filter_by(is_active=True).count()
            papers_count = ResearchPaper.query.count()
            verification_summary['steps']['database_check'] = {
                'status': 'verified', 'active_techniques': active_tech_count, 'research_papers': papers_count,
                'sample_active_technique_types': list(db.session.query(ExtractedTechnique.technique_type)\
                                                    .filter_by(is_active=True).distinct().limit(5).all())
            }
        except Exception as db_err_verify:
            verification_summary['steps']['database_check'] = {'status': 'error', 'detail': str(db_err_verify)}

        # 2. Code-Level Integration (Module/Function Availability)
        try:
            from easyjailbreak.utils.comprehensive_technique_integration import verify_technique_availability # Assumed utility
            code_integ_status = verify_technique_availability() # Expects dict
            verification_summary['steps']['code_module_check'] = code_integ_status
        except ImportError:
             verification_summary['steps']['code_module_check'] = {'status': 'error', 'detail': 'Comprehensive integration module not found.'}
        except Exception as code_err:
            verification_summary['steps']['code_module_check'] = {'status': 'error', 'detail': str(code_err)}

        # 3. Functional Test (Simulated Prompt Generation)
        test_objective_val = data.get('test_objective', 'Default test objective for verification')
        test_domain_val = data.get('test_domain', 'AI Safety Research') # Ensure this is a valid domain
        if test_domain_val not in SUPPORTED_DOMAINS and SUPPORTED_DOMAINS:
            test_domain_val = SUPPORTED_DOMAINS[0]

        try:
            from easyjailbreak.utils.comprehensive_technique_integration import test_technique_integration # Assumed utility
            functional_test_result = test_technique_integration(test_objective_val, test_domain_val) # Expects dict
            verification_summary['steps']['functional_prompt_test'] = functional_test_result
        except ImportError:
            verification_summary['steps']['functional_prompt_test'] = {'status': 'error', 'detail': 'Comprehensive integration test function module not found.'}
        except Exception as func_err:
            verification_summary['steps']['functional_prompt_test'] = {'status': 'error', 'detail': str(func_err)}

        return jsonify({'status': 'success', 'verification_summary': verification_summary})
    except Exception as e:
        app.logger.error(f"Error verifying technique integration: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-domain-template', methods=['POST']) # Changed to POST as it might take specific domain details
def api_get_domain_template_action(): # Renamed function
    """API endpoint to serve authentic research domain templates"""
    try:
        data = request.get_json()
        if not data: return jsonify({'error': 'No JSON data provided'}), 400

        domain_name = data.get('domain', '').strip()
        if not domain_name: return jsonify({'error': 'Domain name is required'}), 400
        if domain_name not in SUPPORTED_DOMAINS: # Validate domain
             return jsonify({'error': f"Domain '{domain_name}' is not supported."}), 400

        # Simplified: Fetch techniques related to the domain by simple keyword matching in description or name
        # A more robust system would use tags or specific domain fields in ExtractedTechnique model
        domain_keywords = domain_name.lower().split()
        relevant_techniques_q = ExtractedTechnique.query.filter(
            ExtractedTechnique.is_active==True,
            db.or_(
                *[ExtractedTechnique.technique_description.ilike(f'%{kw}%') for kw in domain_keywords],
                *[ExtractedTechnique.technique_name.ilike(f'%{kw}%') for kw in domain_keywords],
                ExtractedTechnique.technique_type.ilike(f'%{domain_name}%') # Also check type
            )
        ).limit(10).all() # Limit for brevity

        domain_template_response = {
            'domain_requested': domain_name,
            'relevant_techniques_found_count': len(relevant_techniques_q),
            'sample_relevant_techniques': [{
                'name': t.technique_name, 'type': t.technique_type, 'complexity': t.complexity_level,
                'description_snippet': t.technique_description[:150] + "..." if len(t.technique_description) > 150 else t.technique_description
            } for t in relevant_techniques_q],
            'suggested_research_focus_areas': [ # Example focus areas
                f"Investigating {domain_name} vulnerabilities.",
                f"Developing novel defense mechanisms for {domain_name}.",
                f"Ethical implications of {domain_name} research."
            ],
            'general_integration_guidelines': [
                "Prioritize techniques with high effectiveness and relevance to objective.",
                "Consider multi-framework approaches for complex scenarios.",
                "Always perform safety evaluations on generated jailbreaks."
            ]
        }
        return jsonify({'status': 'success', 'domain_template_data': domain_template_response})
    except Exception as e:
        app.logger.error(f"Error getting domain template for '{data.get('domain', 'N/A')}': {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-diagnostic-report', methods=['GET']) # Changed to GET as it's fetching a report
def api_export_diagnostic_report_action(): # Renamed function
    """Export diagnostic report in various formats"""
    try:
        format_type_req = request.args.get('format', 'json').lower()

        # Reuse the logic from /api/run-diagnostics or a shared utility for consistency
        # For this example, re-implementing a simplified version:
        report_data = {'timestamp': datetime.utcnow().isoformat() + "Z", 'platform_overall_status': 'nominal', 'checks': {}}

        # DB Check
        try:
            report_data['checks']['database_connectivity'] = {'status': 'connected', 'details': f"{KnowledgeEntry.query.count()} knowledge entries."}
        except Exception as db_rep_err:
            report_data['checks']['database_connectivity'] = {'status': 'error', 'details': str(db_rep_err)}

        # Basic Framework Check (example)
        report_data['checks']['autodan_module'] = {'status': 'available' if 'autodan_strategist' in globals() else 'unavailable'}

        if format_type_req == 'json':
            json_response = make_response(jsonify({'status': 'success', 'diagnostic_report_data': report_data}))
            json_response.headers['Content-Disposition'] = f'attachment; filename=diagnostic_report_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.json'
            json_response.headers['Content-Type'] = 'application/json'
            return json_response

        elif format_type_req == 'csv':
            import csv, io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Report Timestamp', report_data['timestamp']])
            writer.writerow(['Overall Status', report_data['platform_overall_status']])
            writer.writerow(['Check Area', 'Status', 'Details'])
            for check_area, check_details in report_data['checks'].items():
                writer.writerow([check_area, check_details.get('status'), check_details.get('details', '')])

            csv_response = make_response(output.getvalue())
            csv_response.headers['Content-Type'] = 'text/csv'
            csv_response.headers['Content-Disposition'] = f'attachment; filename=diagnostic_report_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
            return csv_response
        else:
            return jsonify({'error': 'Unsupported format. Use "json" or "csv".'}), 400

    except Exception as e:
        app.logger.error(f"Error exporting diagnostic report: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def page_not_found_error(e): # Renamed function
    # Log the 404 error with more context if desired
    app.logger.warning(f"404 error at URL: {request.url} - {e}")
    return render_template('errors/404.html'), 404 # Assuming this template exists

@app.errorhandler(500)
def internal_server_error_handler(e): # Renamed function
    # Log the 500 error with stack trace for debugging
    app.logger.error(f"500 Internal Server Error at URL: {request.url}", exc_info=True)
    db.session.rollback() # Good practice to rollback session on 500 if DB was involved
    return render_template('errors/500.html'), 500 # Assuming this template exists
