// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : '/api'; // Will use relative path on production (Vercel will proxy to Railway)

// Global state
let currentPage = 1;
let currentCategory = 'all';
let currentSort = 'created_at';
let searchQuery = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadCategories();
    loadProjects();
    loadSkills();
    loadExperiences();
    loadArticles();
    setupEventListeners();
    setupScrollEffects();
});

// Setup Event Listeners
function setupEventListeners() {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    mobileMenuBtn?.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
    
    // Search
    const searchInput = document.getElementById('search-input');
    searchInput?.addEventListener('input', debounce((e) => {
        searchQuery = e.target.value;
        currentPage = 1;
        loadProjects();
    }, 500));
    
    // Sort
    const sortSelect = document.getElementById('sort-select');
    sortSelect?.addEventListener('change', (e) => {
        currentSort = e.target.value;
        currentPage = 1;
        loadProjects();
    });
    
    // Contact form
    const contactForm = document.getElementById('contact-form');
    contactForm?.addEventListener('submit', handleContactSubmit);
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Close mobile menu if open
                mobileMenu?.classList.add('hidden');
            }
        });
    });
}

// Setup Scroll Effects
function setupScrollEffects() {
    const scrollTopBtn = document.getElementById('scroll-top');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollTopBtn.classList.remove('opacity-0', 'pointer-events-none');
            scrollTopBtn.classList.add('opacity-100');
        } else {
            scrollTopBtn.classList.add('opacity-0', 'pointer-events-none');
            scrollTopBtn.classList.remove('opacity-100');
        }
    });
    
    scrollTopBtn?.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Load Stats
async function loadStats() {
    try {
        const res = await fetch(`${API_BASE_URL}/stats`);
        const data = await res.json();
        
        animateNumber('stat-projects', data.total_projects);
        animateNumber('stat-views', data.total_views);
        animateNumber('stat-likes', data.total_likes);
        animateNumber('stat-articles', data.total_articles);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Animate Number
function animateNumber(id, target) {
    const element = document.getElementById(id);
    if (!element) return;
    
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 30);
}

// Load Categories
async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE_URL}/categories`);
        const categories = await res.json();
        
        const filterContainer = document.getElementById('category-filters');
        filterContainer.innerHTML = categories.map(cat => `
            <button onclick="filterProjects(${cat.id})" 
                    class="filter-btn px-4 py-2 rounded-lg bg-gray-700 hover:bg-purple-600 transition text-white whitespace-nowrap">
                ${cat.icon} ${cat.name}
            </button>
        `).join('');
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Filter Projects
function filterProjects(category) {
    currentCategory = category;
    currentPage = 1;
    loadProjects();
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-purple-600');
        btn.classList.add('bg-gray-700');
    });
    event.target.classList.remove('bg-gray-700');
    event.target.classList.add('bg-purple-600');
}

// Load Projects
async function loadProjects() {
    try {
        let url = `/api/projects?page=${currentPage}&per_page=9&sort=${currentSort}`;
        
        if (currentCategory !== 'all') {
            url += `&category=${currentCategory}`;
        }
        
        if (searchQuery) {
            url += `&search=${encodeURIComponent(searchQuery)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        
        const container = document.getElementById('project-list');
        
        if (data.projects.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-20">
                    <i class="fas fa-folder-open text-6xl text-gray-600 mb-4"></i>
                    <p class="text-gray-400 text-xl">No projects found</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = data.projects.map(project => createProjectCard(project)).join('');
        
        // Update pagination
        updatePagination(data);
    } catch (error) {
        console.error('Error loading projects:', error);
        document.getElementById('project-list').innerHTML = `
            <div class="col-span-full text-center py-20 text-red-500">
                <i class="fas fa-exclamation-triangle text-6xl mb-4"></i>
                <p>Error loading projects</p>
            </div>
        `;
    }
}

// Create Project Card
function createProjectCard(project) {
    return `
        <div class="bg-gray-900 rounded-2xl overflow-hidden hover:transform hover:scale-105 transition duration-300 shadow-xl group">
            <div class="relative overflow-hidden">
                <img src="${project.image}" alt="${project.title}" 
                     class="w-full h-56 object-cover group-hover:scale-110 transition duration-300">
                ${project.featured ? '<div class="absolute top-4 right-4 px-3 py-1 bg-yellow-500 text-black text-xs font-bold rounded-full">⭐ Featured</div>' : ''}
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition duration-300 flex items-end p-6">
                    <div class="flex gap-2">
                        ${project.demo_url ? `<a href="${project.demo_url}" target="_blank" class="px-4 py-2 bg-purple-600 rounded-lg text-sm font-bold hover:bg-purple-700 transition">
                            <i class="fas fa-external-link-alt mr-1"></i> Demo
                        </a>` : ''}
                        ${project.github_url ? `<a href="${project.github_url}" target="_blank" class="px-4 py-2 bg-gray-700 rounded-lg text-sm font-bold hover:bg-gray-600 transition">
                            <i class="fab fa-github mr-1"></i> Code
                        </a>` : ''}
                    </div>
                </div>
            </div>
            
            <div class="p-6">
                ${project.category ? `<div class="text-purple-400 text-sm mb-2">${project.category.icon} ${project.category.name}</div>` : ''}
                <h3 class="text-xl font-bold mb-2 group-hover:text-purple-400 transition">${project.title}</h3>
                <p class="text-gray-400 text-sm mb-4 line-clamp-2">${project.description}</p>
                
                ${project.tags.length > 0 ? `
                    <div class="flex flex-wrap gap-2 mb-4">
                        ${project.tags.slice(0, 3).map(tag => `
                            <span class="px-2 py-1 bg-gray-800 rounded text-xs">${tag}</span>
                        `).join('')}
                    </div>
                ` : ''}
                
                <div class="flex justify-between items-center text-sm text-gray-500">
                    <div class="flex gap-4">
                        <span><i class="fas fa-eye"></i> ${project.views}</span>
                        <button onclick="likeProject(${project.id})" class="hover:text-red-500 transition">
                            <i class="fas fa-heart"></i> <span id="likes-${project.id}">${project.likes}</span>
                        </button>
                        <span><i class="fas fa-comments"></i> ${project.comments_count}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Like Project
async function likeProject(id) {
    try {
        const res = await fetch(`${API_BASE_URL}/projects/${id}/like`, { method: 'POST' });
        const data = await res.json();
        document.getElementById(`likes-${id}`).textContent = data.likes;
    } catch (error) {
        console.error('Error liking project:', error);
    }
}

// Update Pagination
function updatePagination(data) {
    const pagination = document.getElementById('pagination');
    if (!pagination) return;
    
    if (data.pages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // Previous button
    if (data.has_prev) {
        html += `<button onclick="changePage(${currentPage - 1})" class="px-4 py-2 bg-gray-700 rounded-lg hover:bg-purple-600 transition">
            <i class="fas fa-chevron-left"></i>
        </button>`;
    }
    
    // Page numbers
    for (let i = 1; i <= data.pages; i++) {
        if (i === currentPage) {
            html += `<button class="px-4 py-2 bg-purple-600 rounded-lg font-bold">${i}</button>`;
        } else if (i === 1 || i === data.pages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += `<button onclick="changePage(${i})" class="px-4 py-2 bg-gray-700 rounded-lg hover:bg-purple-600 transition">${i}</button>`;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            html += `<span class="px-2">...</span>`;
        }
    }
    
    // Next button
    if (data.has_next) {
        html += `<button onclick="changePage(${currentPage + 1})" class="px-4 py-2 bg-gray-700 rounded-lg hover:bg-purple-600 transition">
            <i class="fas fa-chevron-right"></i>
        </button>`;
    }
    
    pagination.innerHTML = html;
}

// Change Page
function changePage(page) {
    currentPage = page;
    loadProjects();
    document.getElementById('projects').scrollIntoView({ behavior: 'smooth' });
}

// Load Skills
async function loadSkills() {
    try {
        const res = await fetch(`${API_BASE_URL}/skills`);
        const skills = await res.json();
        
        const container = document.getElementById('skills-container');
        if (skills.length === 0) {
            container.innerHTML = '<p class="col-span-full text-center text-gray-400">No skills added yet</p>';
            return;
        }
        
        container.innerHTML = skills.map(skill => `
            <div class="bg-gray-800 p-6 rounded-xl">
                <div class="flex justify-between items-center mb-3">
                    <span class="font-bold">${skill.icon || '🔧'} ${skill.name}</span>
                    <span class="text-purple-400 font-bold">${skill.level}%</span>
                </div>
                <div class="h-3 bg-gray-700 rounded-full overflow-hidden">
                    <div class="skill-bar h-full bg-gradient-to-r from-purple-500 to-pink-500" 
                         style="width: ${skill.level}%"></div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

// Load Experiences
async function loadExperiences() {
    try {
        const res = await fetch(`${API_BASE_URL}/experiences`);
        const experiences = await res.json();
        
        const container = document.getElementById('experience-timeline');
        if (experiences.length === 0) {
            container.innerHTML = '<p class="text-center text-gray-400">No experience added yet</p>';
            return;
        }
        
        container.innerHTML = experiences.map(exp => `
            <div class="relative pl-8 border-l-2 border-purple-500">
                <div class="absolute -left-3 top-0 w-6 h-6 bg-purple-600 rounded-full border-4 border-gray-900"></div>
                <div class="bg-gray-800 p-6 rounded-xl">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="text-xl font-bold">${exp.title}</h3>
                        ${exp.current ? '<span class="px-3 py-1 bg-green-600 text-xs rounded-full">Current</span>' : ''}
                    </div>
                    <div class="text-purple-400 font-semibold mb-2">${exp.company}</div>
                    <div class="text-sm text-gray-400 mb-3">
                        <i class="fas fa-calendar-alt mr-1"></i> ${exp.start_date} - ${exp.end_date}
                        ${exp.location ? `<span class="ml-4"><i class="fas fa-map-marker-alt mr-1"></i> ${exp.location}</span>` : ''}
                    </div>
                    ${exp.description ? `<p class="text-gray-300">${exp.description}</p>` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading experiences:', error);
    }
}

// Load Articles
async function loadArticles() {
    try {
        const res = await fetch(`${API_BASE_URL}/articles?per_page=6`);
        const data = await res.json();
        
        const container = document.getElementById('blog-list');
        if (data.articles.length === 0) {
            container.innerHTML = '<p class="col-span-full text-center text-gray-400">No articles yet</p>';
            return;
        }
        
        container.innerHTML = data.articles.map(article => `
            <article class="bg-gray-900 rounded-2xl overflow-hidden hover:transform hover:scale-105 transition duration-300 shadow-xl">
                ${article.cover_image ? `
                    <img src="${article.cover_image}" alt="${article.title}" class="w-full h-48 object-cover">
                ` : `
                    <div class="w-full h-48 bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                        <i class="fas fa-newspaper text-6xl text-white/50"></i>
                    </div>
                `}
                <div class="p-6">
                    <div class="text-sm text-gray-400 mb-2">
                        <i class="fas fa-calendar-alt mr-1"></i> ${new Date(article.created_at).toLocaleDateString()}
                        <span class="ml-4"><i class="fas fa-eye mr-1"></i> ${article.views} views</span>
                    </div>
                    <h3 class="text-xl font-bold mb-3 hover:text-purple-400 transition">${article.title}</h3>
                    <p class="text-gray-400 text-sm mb-4 line-clamp-3">${article.excerpt || article.content.substring(0, 150)}...</p>
                    
                    ${article.tags.length > 0 ? `
                        <div class="flex flex-wrap gap-2 mb-4">
                            ${article.tags.slice(0, 3).map(tag => `
                                <span class="px-2 py-1 bg-gray-800 rounded text-xs">#${tag}</span>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    <a href="#" class="text-purple-400 font-semibold hover:text-purple-300 transition">
                        Read More <i class="fas fa-arrow-right ml-1"></i>
                    </a>
                </div>
            </article>
        `).join('');
    } catch (error) {
        console.error('Error loading articles:', error);
    }
}

// Handle Contact Form Submit
async function handleContactSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
        const res = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            alert('✅ Message sent successfully! I will get back to you soon.');
            e.target.reset();
        } else {
            alert('❌ Failed to send message. Please try again.');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('❌ An error occurred. Please try again later.');
    }
}

// Debounce utility
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
