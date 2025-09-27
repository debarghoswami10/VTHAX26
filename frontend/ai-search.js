// ai-search.js - AI-powered search integration for the woke platform

class AISearch {
    constructor(apiBaseUrl = 'http://localhost:3001') {
        this.apiBaseUrl = apiBaseUrl;
        this.currentAnswers = {};
        this.selectedService = null;
    }

    async classifyRequest(text) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/bot/classify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Classification error:', error);
            // Fallback to basic keyword matching
            return this.fallbackClassification(text);
        }
    }

    async getFollowups(serviceId, answers = {}) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/bot/followups`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ service_id: serviceId, answers })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Followups error:', error);
            return { next: [], ready: true, estimate_hours: [1, 2] };
        }
    }

    async matchProviders(serviceId, spec = {}, location = null) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/match`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ service_id: serviceId, spec, location })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Matching error:', error);
            return { providers: [] };
        }
    }

    fallbackClassification(text) {
        const lowerText = text.toLowerCase();
        const services = [
            { id: 'beauty_massage', label: 'Massage Therapy', keywords: ['massage', 'therapy', 'relax', 'spa'] },
            { id: 'home_cleaning', label: 'Home Cleaning', keywords: ['clean', 'cleaning', 'house', 'home'] },
            { id: 'car_wash', label: 'Car Wash', keywords: ['car', 'wash', 'vehicle', 'auto'] },
            { id: 'appliance_repair', label: 'Appliance Repair', keywords: ['repair', 'fix', 'appliance', 'broken'] },
            { id: 'beauty_facial', label: 'Facial Treatment', keywords: ['facial', 'skin', 'beauty', 'glow'] }
        ];

        const matches = services.filter(service => 
            service.keywords.some(keyword => lowerText.includes(keyword))
        );

        return {
            candidates: matches.slice(0, 3).map(service => ({
                service_id: service.id,
                label: service.label,
                reason: `Keyword match: ${service.label}`,
                confidence: 0.5
            }))
        };
    }

    // UI Integration Methods
    async handleSearchInput(searchText) {
        if (!searchText.trim()) return;

        console.log('🔍 AI Search:', searchText);
        
        // Show loading state
        this.showLoadingState();
        
        try {
            // Step 1: Classify the request
            const classification = await this.classifyRequest(searchText);
            this.displayServiceCandidates(classification.candidates);
        } catch (error) {
            console.error('Search failed:', error);
            this.showErrorState('Search failed. Please try again.');
        }
    }

    displayServiceCandidates(candidates) {
        const container = document.getElementById('ai-search-results');
        if (!container) return;

        container.innerHTML = '';
        
        if (candidates.length === 0) {
            container.innerHTML = '<p class="text-gray-500">No services found. Try a different search term.</p>';
            return;
        }

        const title = document.createElement('h3');
        title.className = 'text-lg font-semibold text-gray-900 mb-4';
        title.textContent = 'What service do you need?';
        container.appendChild(title);

        candidates.forEach((candidate, index) => {
            const card = document.createElement('div');
            card.className = 'bg-white border border-gray-200 rounded-lg p-4 mb-3 cursor-pointer hover:border-teal-500 hover:shadow-md transition-all';
            card.innerHTML = `
                <div class="flex items-center justify-between">
                    <div>
                        <h4 class="font-medium text-gray-900">${candidate.label}</h4>
                        <p class="text-sm text-gray-600">${candidate.reason}</p>
                        <span class="text-xs text-teal-600">Confidence: ${Math.round(candidate.confidence * 100)}%</span>
                    </div>
                    <button class="bg-teal-600 text-white px-4 py-2 rounded-md text-sm hover:bg-teal-700">
                        Select
                    </button>
                </div>
            `;
            
            card.addEventListener('click', () => this.selectService(candidate));
            container.appendChild(card);
        });
    }

    async selectService(service) {
        this.selectedService = service;
        this.currentAnswers = {};
        
        console.log('🎯 Selected service:', service.label);
        
        // Get followup questions
        const followups = await this.getFollowups(service.service_id);
        this.displayFollowupQuestions(followups);
    }

    displayFollowupQuestions(followups) {
        const container = document.getElementById('ai-search-results');
        if (!container) return;

        container.innerHTML = `
            <div class="bg-teal-50 border border-teal-200 rounded-lg p-4 mb-4">
                <h3 class="text-lg font-semibold text-teal-900 mb-2">${this.selectedService.label}</h3>
                <p class="text-sm text-teal-700">Estimated time: ${followups.estimate_hours[0]}-${followups.estimate_hours[1]} hours</p>
            </div>
        `;

        if (followups.next.length === 0) {
            // No more questions, show provider matching
            this.showProviderMatching();
            return;
        }

        const questionsContainer = document.createElement('div');
        questionsContainer.className = 'space-y-4';
        
        followups.next.forEach(question => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'bg-white border border-gray-200 rounded-lg p-4';
            
            let inputHtml = '';
            if (question.type === 'select') {
                inputHtml = `
                    <select class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500" 
                            data-question-id="${question.id}">
                        <option value="">Select an option</option>
                        ${question.options.map(option => `<option value="${option}">${option}</option>`).join('')}
                    </select>
                `;
            } else {
                inputHtml = `
                    <input type="text" 
                           class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500" 
                           placeholder="${question.q}"
                           data-question-id="${question.id}">
                `;
            }
            
            questionDiv.innerHTML = `
                <label class="block text-sm font-medium text-gray-700 mb-2">${question.q}</label>
                ${inputHtml}
            `;
            
            questionsContainer.appendChild(questionDiv);
        });

        const submitButton = document.createElement('button');
        submitButton.className = 'w-full bg-teal-600 text-white py-2 px-4 rounded-md hover:bg-teal-700 mt-4';
        submitButton.textContent = 'Continue';
        submitButton.addEventListener('click', () => this.submitAnswers(followups));
        
        questionsContainer.appendChild(submitButton);
        container.appendChild(questionsContainer);
    }

    async submitAnswers(followups) {
        // Collect answers from form
        const answers = {};
        const inputs = document.querySelectorAll('[data-question-id]');
        inputs.forEach(input => {
            const questionId = input.getAttribute('data-question-id');
            answers[questionId] = input.value;
        });

        this.currentAnswers = { ...this.currentAnswers, ...answers };
        
        // Get next set of questions
        const nextFollowups = await this.getFollowups(this.selectedService.service_id, this.currentAnswers);
        this.displayFollowupQuestions(nextFollowups);
    }

    async showProviderMatching() {
        const container = document.getElementById('ai-search-results');
        if (!container) return;

        container.innerHTML += '<div class="mt-4"><h3 class="text-lg font-semibold text-gray-900 mb-4">Finding the best providers for you...</h3></div>';
        
        // Get provider matches
        const matches = await this.matchProviders(this.selectedService.service_id, this.currentAnswers);
        this.displayProviders(matches.providers);
    }

    displayProviders(providers) {
        const container = document.getElementById('ai-search-results');
        if (!container) return;

        if (providers.length === 0) {
            container.innerHTML += '<p class="text-gray-500">No providers available at the moment.</p>';
            return;
        }

        const providersContainer = document.createElement('div');
        providersContainer.className = 'space-y-4';
        
        providers.forEach(provider => {
            const providerCard = document.createElement('div');
            providerCard.className = 'bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all';
            providerCard.innerHTML = `
                <div class="flex items-start justify-between mb-3">
                    <div>
                        <h4 class="font-semibold text-gray-900">${provider.name}</h4>
                        <div class="flex items-center space-x-2 mt-1">
                            <div class="flex items-center text-yellow-500">
                                <span class="text-sm">★</span>
                                <span class="ml-1 text-sm font-medium">${provider.avg_rating}</span>
                            </div>
                            <span class="text-sm text-gray-500">•</span>
                            <span class="text-sm text-gray-500">${provider.eta_min} min away</span>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-lg font-bold text-teal-600">₹${provider.rate_hour}/hr</div>
                    </div>
                </div>
                <p class="text-sm text-gray-600 mb-3">${provider.reason_line}</p>
                <button class="w-full bg-teal-600 text-white py-2 px-4 rounded-md hover:bg-teal-700">
                    Book Now
                </button>
            `;
            
            providersContainer.appendChild(providerCard);
        });
        
        container.appendChild(providersContainer);
    }

    showLoadingState() {
        const container = document.getElementById('ai-search-results');
        if (!container) return;
        
        container.innerHTML = `
            <div class="flex items-center justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
                <span class="ml-3 text-gray-600">Finding the perfect service for you...</span>
            </div>
        `;
    }

    showErrorState(message) {
        const container = document.getElementById('ai-search-results');
        if (!container) return;
        
        container.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-700">${message}</p>
            </div>
        `;
    }
}

// Initialize AI Search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const aiSearch = new AISearch();
    
    // Add AI search results container to the page
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        const resultsContainer = document.createElement('div');
        resultsContainer.id = 'ai-search-results';
        resultsContainer.className = 'mt-6 max-w-4xl mx-auto';
        searchForm.parentNode.insertBefore(resultsContainer, searchForm.nextSibling);
        
        // Override the search form submission
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchText = document.getElementById('searchQuery').value;
            if (searchText.trim()) {
                aiSearch.handleSearchInput(searchText);
            }
        });
    }
});
