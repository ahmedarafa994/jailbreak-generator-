// Main JavaScript functionality for Knowledge-to-Jailbreak platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializeProgressBars();
    initializeTooltips();
    initializeLoadingStates();
    initializeCharacterCounters();
    initializeSafetyWarnings();
    initializeAutoDanProcessing();
});

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showValidationErrors(form);
            } else {
                showLoadingState(form);
            }
            form.classList.add('was-validated');
        });
    });
}

// AutoDAN + OVERTHINK + BoT Processing Integration
function initializeAutoDanProcessing() {
    const processBtn = document.getElementById('processBtn');
    const knowledgeForm = document.getElementById('knowledgeForm');
    const overthinkCheckbox = document.getElementById('use_overthink');
    const overthinkOptions = document.getElementById('overthink_options');
    const botCheckbox = document.getElementById('use_bot');
    const botOptions = document.getElementById('bot_options');
    const flipattackCheckbox = document.getElementById('use_flipattack');
    const flipattackOptions = document.getElementById('flipattack_options');
    const tapCheckbox = document.getElementById('use_tap');
    const tapOptions = document.getElementById('tap_options');
    
    if (processBtn && knowledgeForm) {
        processBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const domain = document.getElementById('domain').value;
            const knowledgeText = document.getElementById('knowledge_text').value;
            const strategy = document.getElementById('autodan_strategy').value;
            const useOverthink = document.getElementById('use_overthink').checked;
            const overthinkComplexity = document.getElementById('overthink_complexity').value;
            const useBot = document.getElementById('use_bot').checked;
            const botComplexity = document.getElementById('bot_complexity').value;
            const useFlipattack = document.getElementById('use_flipattack').checked;
            const flipIntensity = document.getElementById('flip_intensity').value;
            const useTap = document.getElementById('use_tap').checked;
            const tapIntensity = document.getElementById('tap_intensity').value;
            const useGptfuzz = document.getElementById('use_gptfuzz').checked;
            const gptfuzzIntensity = document.getElementById('gptfuzz_intensity').value;
            const useSqlinjection = document.getElementById('use_sqlinjection').checked;
            const injectionIntensity = document.getElementById('injection_intensity').value;
            
            if (!domain || !knowledgeText) {
                showAlert('Please fill in domain and knowledge content fields.', 'danger');
                return;
            }
            
            // Framework requirements are now optional - each can work independently
            // Only show warnings for optimal combinations, but allow individual use
            
            processWithAdvancedFrameworks(domain, knowledgeText, strategy, useOverthink, overthinkComplexity, useBot, botComplexity, useFlipattack, flipIntensity, useTap, tapIntensity, useGptfuzz, gptfuzzIntensity, useSqlinjection, injectionIntensity);
        });
    }
    
    // Show/hide OVERTHINK options based on checkbox
    if (overthinkCheckbox && overthinkOptions) {
        overthinkCheckbox.addEventListener('change', function() {
            overthinkOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide BoT options based on checkbox
    if (botCheckbox && botOptions) {
        botCheckbox.addEventListener('change', function() {
            botOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide FlipAttack options based on checkbox
    if (flipattackCheckbox && flipattackOptions) {
        flipattackCheckbox.addEventListener('change', function() {
            flipattackOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide TAP options based on checkbox
    if (tapCheckbox && tapOptions) {
        tapCheckbox.addEventListener('change', function() {
            tapOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide GPTFuzz options based on checkbox
    const gptfuzzCheckbox = document.getElementById('use_gptfuzz');
    const gptfuzzOptions = document.getElementById('gptfuzz_options');
    if (gptfuzzCheckbox && gptfuzzOptions) {
        gptfuzzCheckbox.addEventListener('change', function() {
            gptfuzzOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide SQL Injection Jailbreak options based on checkbox
    const sqlinjectionCheckbox = document.getElementById('use_sqlinjection');
    const sqlinjectionOptions = document.getElementById('sqlinjection_options');
    if (sqlinjectionCheckbox && sqlinjectionOptions) {
        sqlinjectionCheckbox.addEventListener('change', function() {
            sqlinjectionOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide TransferAttack options based on checkbox
    const transferattackCheckbox = document.getElementById('use_transferattack');
    const transferattackOptions = document.getElementById('transferattack_options');
    if (transferattackCheckbox && transferattackOptions) {
        transferattackCheckbox.addEventListener('change', function() {
            transferattackOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide I-GCG options based on checkbox
    const igcgCheckbox = document.getElementById('use_igcg');
    const igcgOptions = document.getElementById('igcg_options');
    if (igcgCheckbox && igcgOptions) {
        igcgCheckbox.addEventListener('change', function() {
            igcgOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide Foot-in-the-door options based on checkbox
    const footindoorCheckbox = document.getElementById('use_footindoor');
    const footindoorOptions = document.getElementById('footindoor_options');
    if (footindoorCheckbox && footindoorOptions) {
        footindoorCheckbox.addEventListener('change', function() {
            footindoorOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide PiF options based on checkbox
    const pifCheckbox = document.getElementById('use_pif');
    const pifOptions = document.getElementById('pif_options');
    if (pifCheckbox && pifOptions) {
        pifCheckbox.addEventListener('change', function() {
            pifOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide Adversarial Triggers options based on checkbox
    const triggersCheckbox = document.getElementById('use_triggers');
    const triggerOptions = document.getElementById('trigger_options');
    if (triggersCheckbox && triggerOptions) {
        triggersCheckbox.addEventListener('change', function() {
            triggerOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide Chain of Iterative Chaos options based on checkbox
    const chaosCheckbox = document.getElementById('use_chaos');
    const chaosOptions = document.getElementById('chaos_options');
    if (chaosCheckbox && chaosOptions) {
        chaosCheckbox.addEventListener('change', function() {
            chaosOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
    
    // Show/hide HyDE options based on checkbox
    const hydeCheckbox = document.getElementById('use_hyde');
    const hydeOptions = document.getElementById('hyde_options');
    if (hydeCheckbox && hydeOptions) {
        hydeCheckbox.addEventListener('change', function() {
            hydeOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
}

// Process knowledge using advanced frameworks (Eleven Complete Frameworks)
async function processWithAdvancedFrameworks(domain, knowledgeText, strategy, useOverthink, overthinkComplexity, useBot, botComplexity, useFlipattack, flipIntensity, useTap, tapIntensity, useGptfuzz, gptfuzzIntensity, useSqlinjection, injectionIntensity, useTransferattack, optimizationIntensity, useIgcg, igcgComplexity, useFootindoor, persuasionIntensity, useHyde, generationStrategy) {
    const processBtn = document.getElementById('processBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsContent = document.getElementById('resultsContent');
    
    // Show loading state with appropriate framework indicators
    processBtn.disabled = true;
    let frameworkText = 'AutoDAN';
    
    // Build framework text based on selected options
    let frameworks = [];
    if (useOverthink) frameworks.push('OVERTHINK');
    if (useBot) frameworks.push('BoT');
    if (useFlipattack) frameworks.push('FlipAttack');
    if (useTap) frameworks.push('TAP');
    if (useGptfuzz) frameworks.push('GPTFuzz');
    if (useSqlinjection) frameworks.push('SQL Injection');
    if (useTransferattack) frameworks.push('TransferAttack');
    if (useIgcg) frameworks.push('I-GCG');
    if (useFootindoor) frameworks.push('Foot-in-the-door');
    if (useHyde) frameworks.push('HyDE');
    
    if (frameworks.length > 0) {
        frameworkText = 'AutoDAN + ' + frameworks.join(' + ');
    } else if (!useOverthink && !useBot && !useFlipattack && !useTap && !useGptfuzz && !useSqlinjection && !useTransferattack && !useIgcg && !useFootindoor && !useHyde) {
        frameworkText = 'AutoDAN';
    }
    
    processBtn.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>Processing with ${frameworkText}...`;
    
    try {
        const response = await fetch('/api/test-processing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                domain: domain,
                knowledge_text: knowledgeText,
                strategy: strategy,
                use_autodan: true,
                use_overthink: useOverthink,
                overthink_complexity: overthinkComplexity,
                use_bot: useBot || false,
                bot_complexity: botComplexity || 'high',
                use_flipattack: useFlipattack || false,
                flip_intensity: flipIntensity || 'high',
                use_tap: useTap || false,
                tap_intensity: tapIntensity || 'high',
                use_gptfuzz: useGptfuzz || false,
                gptfuzz_intensity: gptfuzzIntensity || 'high',
                use_sqlinjection: useSqlinjection || false,
                injection_intensity: injectionIntensity || 'high',
                use_transferattack: useTransferattack || false,
                optimization_intensity: optimizationIntensity || 'aggressive',
                use_igcg: useIgcg || false,
                igcg_complexity: igcgComplexity || 'advanced',
                use_footindoor: useFootindoor || false,
                persuasion_intensity: persuasionIntensity || 'intensive',
                use_hyde: useHyde || false,
                generation_strategy: generationStrategy || 'multi_perspective'
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayAdvancedResults(result);
            resultsContainer.style.display = 'block';
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        } else {
            showAlert('Error processing knowledge: ' + result.error, 'danger');
        }
        
    } catch (error) {
        showAlert('Network error occurred. Please try again.', 'danger');
        console.error('Processing error:', error);
    } finally {
        // Reset button
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-arrow-right me-2"></i>Process Knowledge & Generate Jailbreak';
    }
}

// Display advanced processing results (AutoDAN + OVERTHINK)
function displayAdvancedResults(result) {
    const resultsContent = document.getElementById('resultsContent');
    
    // Store current result for copy functions
    currentResult = result;
    
    // Determine which frameworks are active
    const isOverthink = result.overthink_framework || false;
    const isAutodan = result.autodan_framework || false;
    const isBot = result.bot_framework || false;
    const isFlipattack = result.flipattack_framework || false;
    const isTap = result.tap_framework || false;
    const isGptfuzz = result.gptfuzz_framework || false;
    
    let frameworkBadges = '';
    if (isAutodan) frameworkBadges += '<span class="badge bg-primary me-2"><i class="fas fa-robot me-1"></i>AutoDAN</span>';
    if (isOverthink) frameworkBadges += '<span class="badge bg-warning me-2"><i class="fas fa-brain me-1"></i>OVERTHINK</span>';
    if (isBot) frameworkBadges += '<span class="badge bg-danger me-2"><i class="fas fa-bolt me-1"></i>BoT</span>';
    if (isFlipattack) frameworkBadges += '<span class="badge bg-info me-2"><i class="fas fa-exchange-alt me-1"></i>FlipAttack</span>';
    if (isTap) frameworkBadges += '<span class="badge bg-success me-2"><i class="fas fa-tree me-1"></i>TAP</span>';
    if (isGptfuzz) frameworkBadges += '<span class="badge bg-dark me-2"><i class="fas fa-flask me-1"></i>GPTFuzz</span>';
    
    let overthinkMetrics = '';
    if (isOverthink) {
        overthinkMetrics = `
            <div class="col-md-6">
                <h6 class="text-warning mb-3">
                    <i class="fas fa-brain me-2"></i>OVERTHINK Metrics
                </h6>
                
                <div class="mb-2">
                    <strong>MDP Template:</strong> ${result.mdp_template_used || 'N/A'}
                </div>
                <div class="mb-2">
                    <strong>Complexity Level:</strong> 
                    <span class="badge bg-secondary">${result.complexity_level || 'N/A'}</span>
                </div>
                <div class="mb-2">
                    <strong>Reasoning Tokens:</strong> ${result.reasoning_tokens_estimated || 'N/A'}
                </div>
                <div class="mb-2">
                    <strong>Slowdown Factor:</strong> ${result.slowdown_factor || 'N/A'}x
                </div>
            </div>
        `;
    }
    
    let botMetrics = '';
    if (isBot) {
        botMetrics = `
            <div class="col-md-6">
                <h6 class="text-danger mb-3">
                    <i class="fas fa-bolt me-2"></i>BoT Metrics
                </h6>
                
                <div class="mb-2">
                    <strong>Reasoning Bypass Score:</strong> 
                    <span class="badge bg-danger">${(result.reasoning_bypass_score * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Vulnerability Level:</strong> 
                    <span class="badge bg-secondary">${result.unthinking_vulnerability_level || 'N/A'}</span>
                </div>
                <div class="mb-2">
                    <strong>BoT Complexity:</strong> ${result.bot_complexity || 'N/A'}
                </div>
                <div class="mb-2">
                    <strong>Combined Effectiveness:</strong> ${(result.effectiveness_score * 100).toFixed(1)}%
                </div>
            </div>
        `;
    }
    
    let flipattackMetrics = '';
    if (isFlipattack) {
        flipattackMetrics = `
            <div class="col-md-6">
                <h6 class="text-info mb-3">
                    <i class="fas fa-exchange-alt me-2"></i>FlipAttack Metrics
                </h6>
                
                <div class="mb-2">
                    <strong>Adversarial Score:</strong> 
                    <span class="badge bg-info">${(result.adversarial_score * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Semantic Inversion:</strong> 
                    <span class="badge bg-secondary">${result.semantic_inversion_level || 'N/A'}</span>
                </div>
                <div class="mb-2">
                    <strong>Attack Sophistication:</strong> ${(result.attack_sophistication * 100).toFixed(1)}%
                </div>
                <div class="mb-2">
                    <strong>Flip Intensity:</strong> ${result.flip_intensity || 'N/A'}
                </div>
            </div>
        `;
    }
    
    let gptfuzzMetrics = '';
    if (isGptfuzz) {
        gptfuzzMetrics = `
            <div class="col-md-6">
                <h6 class="text-dark mb-3">
                    <i class="fas fa-flask me-2"></i>GPTFuzz Metrics
                </h6>
                
                <div class="mb-2">
                    <strong>Generation Diversity:</strong> 
                    <span class="badge bg-dark">${(result.generation_diversity * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Evolutionary Fitness:</strong> 
                    <span class="badge bg-secondary">${(result.evolutionary_fitness * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Red Teaming Score:</strong> ${(result.red_teaming_score * 100).toFixed(1)}%
                </div>
                <div class="mb-2">
                    <strong>Fuzzing Effectiveness:</strong> ${(result.fuzzing_effectiveness * 100).toFixed(1)}%
                </div>
                <div class="mb-2">
                    <strong>Mutation Rounds:</strong> ${result.mutation_rounds || 'N/A'}
                </div>
                <div class="mb-2">
                    <strong>Population Size:</strong> ${result.population_size || 'N/A'}
                </div>
            </div>
        `;
    }
    
    let tapMetrics = '';
    if (isTap) {
        tapMetrics = `
            <div class="col-md-6">
                <h6 class="text-success mb-3">
                    <i class="fas fa-tree me-2"></i>TAP Metrics
                </h6>
                
                <div class="mb-2">
                    <strong>Query Efficiency:</strong> 
                    <span class="badge bg-success">${(result.query_efficiency * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Tree Optimization:</strong> 
                    <span class="badge bg-secondary">${(result.tree_optimization_score * 100).toFixed(1)}%</span>
                </div>
                <div class="mb-2">
                    <strong>Pruning Effectiveness:</strong> ${(result.pruning_effectiveness * 100).toFixed(1)}%
                </div>
                <div class="mb-2">
                    <strong>Tree Depth:</strong> ${result.tree_depth || 'N/A'}
                </div>
                <div class="mb-2">
                    <strong>Branching Factor:</strong> ${result.branching_factor || 'N/A'}
                </div>
            </div>
        `;
    }
    
    resultsContent.innerHTML = `
        <div class="mb-3">
            ${frameworkBadges}
        </div>
        
        <div class="row">
            <div class="col-md-8">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="text-primary mb-0">
                        <i class="fas fa-code me-2"></i>Generated Jailbreak
                    </h6>
                    <button type="button" class="btn btn-outline-primary btn-sm" id="copyJailbreakBtn" 
                            onclick="copyJailbreakText()">
                        <i class="fas fa-copy me-2"></i>Copy
                    </button>
                </div>
                <div class="bg-light p-3 rounded mb-3" style="position: relative;">
                    <pre class="mb-0" style="white-space: pre-wrap;" id="jailbreakContent"></pre>
                </div>
                
                <h6 class="text-info mb-2">Strategy Information</h6>
                <p><strong>Strategy Used:</strong> ${result.strategy_used}</p>
                <p><strong>Risk Level:</strong> 
                    <span class="badge bg-${getRiskBadgeColor(result.risk_level)}">${result.risk_level}</span>
                </p>
            </div>
            
            <div class="col-md-4">
                <h6 class="text-success mb-3">
                    <i class="fas fa-chart-bar me-2"></i>Performance Metrics
                </h6>
                
                <div class="mb-3">
                    <label class="form-label">Relevance Score</label>
                    <div class="progress mb-1">
                        <div class="progress-bar bg-info" style="width: ${result.relevance_score * 100}%"></div>
                    </div>
                    <small class="text-muted">${(result.relevance_score * 100).toFixed(1)}%</small>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Effectiveness Score</label>
                    <div class="progress mb-1">
                        <div class="progress-bar bg-success" style="width: ${result.effectiveness_score * 100}%"></div>
                    </div>
                    <small class="text-muted">${(result.effectiveness_score * 100).toFixed(1)}%</small>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            ${overthinkMetrics}
            ${botMetrics}
            ${flipattackMetrics}
            ${tapMetrics}
            ${gptfuzzMetrics}
        </div>
        
        ${result.strategy_definition ? `
        <div class="mt-4">
            <details class="mb-3">
                <summary class="btn btn-outline-secondary btn-sm">
                    <i class="fas fa-info-circle me-2"></i>Strategy Definition
                </summary>
                <div class="mt-2 p-3 bg-light rounded">
                    <p class="mb-0">${result.strategy_definition}</p>
                </div>
            </details>
        </div>
        ` : ''}
        
        <div class="mt-4">
            <div class="d-flex gap-2 flex-wrap">
                <button type="button" class="btn btn-success btn-sm" id="copyFullResultBtn" 
                        onclick="copyFullResult()">
                    <i class="fas fa-download me-2"></i>Copy Full Analysis
                </button>
                <button type="button" class="btn btn-info btn-sm" id="copyMetricsBtn" 
                        onclick="copyMetrics()">
                    <i class="fas fa-chart-line me-2"></i>Copy Metrics
                </button>
            </div>
        </div>
    `;
    
    // Safely set the jailbreak content to avoid template literal issues
    const jailbreakContent = document.getElementById('jailbreakContent');
    if (jailbreakContent && result.jailbreak) {
        jailbreakContent.textContent = result.jailbreak;
    }
}

// Copy jailbreak text specifically
function copyJailbreakText() {
    if (!currentResult || !currentResult.jailbreak) {
        showAlert('No jailbreak text available to copy', 'danger');
        return;
    }
    
    const button = document.getElementById('copyJailbreakBtn');
    const originalText = button.innerHTML;
    
    navigator.clipboard.writeText(currentResult.jailbreak).then(function() {
        button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-success');
        
        setTimeout(function() {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-primary');
        }, 2000);
    }).catch(function(err) {
        console.error('Copy error:', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

// Display AutoDAN processing results (legacy support)
function displayAutodanResults(result) {
    displayAdvancedResults(result);
}

// Global variable to store current result for copy functions
let currentResult = null;

// Copy functionality for jailbreak content
function copyToClipboard(text, buttonId) {
    navigator.clipboard.writeText(text).then(function() {
        const button = document.getElementById(buttonId);
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-success');
        
        setTimeout(function() {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-primary');
        }, 2000);
    }).catch(function(err) {
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

// Copy full analysis results
function copyFullResult() {
    if (!currentResult) {
        showAlert('No result data available to copy', 'danger');
        return;
    }
    
    const frameworks = [];
    if (currentResult.autodan_framework) frameworks.push('AutoDAN');
    if (currentResult.overthink_framework) frameworks.push('OVERTHINK');
    
    let fullText = `=== Knowledge-to-Jailbreak Analysis ===
Frameworks: ${frameworks.join(' + ')}
Strategy: ${currentResult.strategy_used}
Risk Level: ${currentResult.risk_level}
Relevance Score: ${(currentResult.relevance_score * 100).toFixed(1)}%
Effectiveness Score: ${(currentResult.effectiveness_score * 100).toFixed(1)}%`;

    if (currentResult.overthink_framework) {
        fullText += `
OVERTHINK Metrics:
- MDP Template: ${currentResult.mdp_template_used || 'N/A'}
- Complexity Level: ${currentResult.complexity_level || 'N/A'}
- Reasoning Tokens: ${currentResult.reasoning_tokens_estimated || 'N/A'}
- Slowdown Factor: ${currentResult.slowdown_factor || 'N/A'}x`;
    }

    fullText += `

=== Generated Jailbreak ===
${currentResult.jailbreak}

=== End Analysis ===`;

    copyToClipboard(fullText, 'copyFullResultBtn');
}

// Copy metrics only
function copyMetrics() {
    if (!currentResult) {
        showAlert('No result data available to copy', 'danger');
        return;
    }
    
    let metricsText = `Performance Metrics:
- Relevance Score: ${(currentResult.relevance_score * 100).toFixed(1)}%
- Effectiveness Score: ${(currentResult.effectiveness_score * 100).toFixed(1)}%
- Risk Level: ${currentResult.risk_level}
- Strategy Used: ${currentResult.strategy_used}`;

    if (currentResult.overthink_framework) {
        metricsText += `
- Reasoning Tokens: ${currentResult.reasoning_tokens_estimated || 'N/A'}
- Slowdown Factor: ${currentResult.slowdown_factor || 'N/A'}x
- MDP Template: ${currentResult.mdp_template_used || 'N/A'}`;
    }

    copyToClipboard(metricsText, 'copyMetricsBtn');
}

// Get appropriate badge color for risk level
function getRiskBadgeColor(riskLevel) {
    switch(riskLevel) {
        case 'minimal': return 'success';
        case 'low': return 'info';
        case 'medium': return 'warning';
        case 'high': return 'danger';
        default: return 'secondary';
    }
}

// Show validation errors with better UX
function showValidationErrors(form) {
    const invalidFields = form.querySelectorAll(':invalid');
    
    if (invalidFields.length > 0) {
        const firstInvalidField = invalidFields[0];
        firstInvalidField.focus();
        
        // Show custom error message
        const fieldName = firstInvalidField.labels?.[0]?.textContent?.replace('*', '').trim() || 'Field';
        showAlert(`Please check the ${fieldName} field and try again.`, 'danger');
    }
}

// Loading states for forms
function initializeLoadingStates() {
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = button.closest('form');
            if (form && form.checkValidity()) {
                showLoadingState(form);
            }
        });
    });
}

function showLoadingState(element) {
    element.classList.add('loading');
    
    const submitButton = element.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Store original text for potential restoration
        submitButton.dataset.originalText = originalText;
        
        // Add timeout to prevent permanent stuck state
        const timeoutId = setTimeout(() => {
            hideLoadingState(element);
            showAlert('Processing is taking longer than expected. Please try again.', 'warning');
        }, 30000); // 30 second timeout
        
        // Store timeout ID for cleanup
        submitButton.dataset.timeoutId = timeoutId;
    }
}

function hideLoadingState(element) {
    element.classList.remove('loading');
    
    const submitButton = element.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = false;
        if (submitButton.dataset.originalText) {
            submitButton.innerHTML = submitButton.dataset.originalText;
        }
        
        // Clear timeout if it exists
        if (submitButton.dataset.timeoutId) {
            clearTimeout(parseInt(submitButton.dataset.timeoutId));
            delete submitButton.dataset.timeoutId;
        }
    }
}

// Progress bar animations
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
                
                observer.unobserve(progressBar);
            }
        });
    });
    
    progressBars.forEach(bar => observer.observe(bar));
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Character and word counters
function initializeCharacterCounters() {
    const textareas = document.querySelectorAll('textarea[data-max-length], textarea#knowledge_text');
    
    textareas.forEach(textarea => {
        const maxLength = textarea.dataset.maxLength || 10000;
        updateCounter(textarea);
        
        textarea.addEventListener('input', () => updateCounter(textarea));
    });
}

function updateCounter(textarea) {
    const charCount = document.getElementById('charCount');
    const wordCount = document.getElementById('wordCount');
    
    if (charCount || wordCount) {
        const text = textarea.value;
        const chars = text.length;
        const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        
        if (charCount) {
            charCount.textContent = chars;
        }
        
        if (wordCount) {
            wordCount.textContent = words;
        }
    }
}

// Safety warnings and confirmations
function initializeSafetyWarnings() {
    const dangerousActions = document.querySelectorAll('[data-danger="true"], .btn-danger');
    
    dangerousActions.forEach(element => {
        element.addEventListener('click', function(event) {
            const confirmed = confirm(
                'This action involves safety-critical operations. ' +
                'Please confirm that you understand this is for research purposes only.'
            );
            
            if (!confirmed) {
                event.preventDefault();
                return false;
            }
        });
    });
}

// Alert system
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the container
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    }
}

// Knowledge preview functionality
function previewKnowledge(knowledgeId) {
    fetch(`/api/knowledge/${knowledgeId}`)
        .then(response => response.json())
        .then(data => {
            const modalBody = document.getElementById('knowledgePreviewBody');
            if (modalBody) {
                modalBody.innerHTML = `
                    <div class="mb-3">
                        <span class="badge bg-primary">${data.domain}</span>
                        ${data.source ? `<small class="text-muted ms-2">Source: ${data.source}</small>` : ''}
                    </div>
                    <p>${data.knowledge_text}</p>
                    <small class="text-muted">Created: ${new Date(data.created_at).toLocaleDateString()}</small>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching knowledge details:', error);
            showAlert('Error loading knowledge details', 'danger');
        });
}

// Copy to clipboard functionality
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (navigator.clipboard && window.isSecureContext) {
        // Use modern clipboard API
        navigator.clipboard.writeText(text).then(() => {
            showAlert(successMessage, 'success', 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            fallbackCopyToClipboard(text, successMessage);
        });
    } else {
        // Fallback for older browsers
        fallbackCopyToClipboard(text, successMessage);
    }
}

function fallbackCopyToClipboard(text, successMessage) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert(successMessage, 'success', 2000);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showAlert('Failed to copy to clipboard', 'danger');
    }
    
    document.body.removeChild(textArea);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to submit forms
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const activeForm = document.activeElement?.closest('form');
        if (activeForm) {
            const submitButton = activeForm.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.click();
            }
        }
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Auto-save functionality for forms (optional)
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave="true"]');
    
    forms.forEach(form => {
        const formData = new FormData(form);
        const savedData = localStorage.getItem(`autosave_${form.id}`);
        
        if (savedData) {
            try {
                const parsed = JSON.parse(savedData);
                Object.keys(parsed).forEach(key => {
                    const field = form.querySelector(`[name="${key}"]`);
                    if (field) {
                        field.value = parsed[key];
                    }
                });
            } catch (e) {
                console.error('Error loading autosaved data:', e);
            }
        }
        
        // Save on input
        form.addEventListener('input', debounce(() => {
            const currentData = new FormData(form);
            const dataObj = {};
            for (let [key, value] of currentData.entries()) {
                dataObj[key] = value;
            }
            localStorage.setItem(`autosave_${form.id}`, JSON.stringify(dataObj));
        }, 1000));
        
        // Clear on successful submit
        form.addEventListener('submit', () => {
            localStorage.removeItem(`autosave_${form.id}`);
        });
    });
}

// Utility function: debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Dark mode toggle (if needed)
function toggleDarkMode() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme from localStorage
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// Call theme initialization
initializeTheme();

// Export functions for global use
window.Knowledge2Jailbreak = {
    showAlert,
    copyToClipboard,
    previewKnowledge,
    showLoadingState,
    hideLoadingState,
    toggleDarkMode
};
