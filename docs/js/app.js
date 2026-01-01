/**
 * Talk Like An X - Web Demo Application
 * ======================================
 *
 * Main application logic for the static web demo.
 *
 * License: GPL
 */

class TalkLikeAnXApp {
    constructor() {
        this.filters = [];
        this.currentFilter = null;
        this.filterCache = new Map();
    }

    async init() {
        await this.loadAvailableFilters();
        this.setupUI();
    }

    async loadAvailableFilters() {
        const filterList = [
            { id: 'beatnik_1950s', name: 'Beatnik (1950s)' },
            { id: 'chef', name: 'Chef' },
            { id: 'club_kids_1980s', name: 'Club Kids (1980s)' },
            { id: 'disco', name: 'Disco' },
            { id: 'duck', name: 'Duck' },
            { id: 'flappers_1920s', name: 'Flappers (1920s)' },
            { id: 'fudd', name: 'Fudd' },
            { id: 'german', name: 'German' },
            { id: 'glitch-10', name: 'Glitch (10%)' },
            { id: 'glitch-25', name: 'Glitch (25%)' },
            { id: 'glitch-50', name: 'Glitch (50%)' },
            { id: 'glitch-100', name: 'Glitch (100%)' },
            { id: 'goths_1980s', name: 'Goths (1980s)' },
            { id: 'greasers_1950s', name: 'Greasers (1950s)' },
            { id: 'grunge_musicians_1990s', name: 'Grunge Musicians (1990s)' },
            { id: 'hackers_1990s', name: 'Hackers (1990s)' },
            { id: 'hip_hop_breakers_1980s', name: 'Hip Hop Breakers (1980s)' },
            { id: 'hippies_1960s', name: 'Hippies (1960s)' },
            { id: 'ibm_engineers_1950s', name: 'IBM Engineers (1950s)' },
            { id: 'jethro', name: 'Jethro' },
            { id: 'lolcat', name: 'LOLCAT' },
            { id: 'metalheads_1970s', name: 'Metalheads (1970s)' },
            { id: 'mid_century_modern_1960s', name: 'Mid Century Modern (1960s)' },
            { id: 'mods_1960s', name: 'Mods (1960s)' },
            { id: 'new_romantic_goth_1980s', name: 'New Romantic Goth (1980s)' },
            { id: 'nyc', name: 'NYC' },
            { id: 'outlaw_bikers_1960s', name: 'Outlaw Bikers (1960s)' },
            { id: 'pirate', name: 'Pirate' },
            { id: 'punk_rockers_1970s', name: 'Punk Rockers (1970s)' },
            { id: 'rastafarians_1970s', name: 'Rastafarians (1970s)' },
            { id: 'ravers_1980s', name: 'Ravers (1980s)' },
            { id: 'riot_grrrl_1990s', name: 'Riot Grrrl (1990s)' },
            { id: 'scottish', name: 'Scottish' },
            { id: 'skinheads_1960s', name: 'Skinheads (1960s)' },
            { id: 'slackers_1990s', name: 'Slackers (1990s)' },
            { id: 'studly', name: 'Studly' },
            { id: 'surfers_1960s', name: 'Surfers (1960s)' },
            { id: 'teddy_boys_1950s', name: 'Teddy Boys (1950s)' },
            { id: 'yuppies_1980s', name: 'Yuppies (1980s)' },
            { id: 'zoot_suiters_1940s', name: 'Zoot Suiters (1940s)' }
        ];

        this.filters = filterList;
    }

    setupUI() {
        const filterSelect = document.getElementById('filter-select');
        const transformBtn = document.getElementById('transform-btn');
        const clearBtn = document.getElementById('clear-btn');

        for (const filter of this.filters) {
            const option = document.createElement('option');
            option.value = filter.id;
            option.textContent = filter.name;
            filterSelect.appendChild(option);
        }

        transformBtn.addEventListener('click', () => this.transform());
        clearBtn.addEventListener('click', () => this.clear());

        filterSelect.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.transform();
        });

        document.getElementById('input-text').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) this.transform();
        });
    }

    async loadFilter(filterId) {
        if (this.filterCache.has(filterId)) {
            return this.filterCache.get(filterId);
        }

        const url = `../src/${filterId}.json`;
        const filter = await FilterFactory.fromJsonFile(url);
        this.filterCache.set(filterId, filter);
        return filter;
    }

    async transform() {
        const filterSelect = document.getElementById('filter-select');
        const inputText = document.getElementById('input-text');
        const outputText = document.getElementById('output-text');
        const transformBtn = document.getElementById('transform-btn');
        const errorMessage = document.getElementById('error-message');

        const filterId = filterSelect.value;
        const text = inputText.value.trim();

        if (!filterId) {
            this.showError('Please select a filter');
            return;
        }

        if (!text) {
            this.showError('Please enter some text to transform');
            return;
        }

        this.hideError();
        transformBtn.disabled = true;
        transformBtn.textContent = 'Transforming...';

        try {
            const filter = await this.loadFilter(filterId);
            const result = filter.transform(text);
            outputText.value = result;
        } catch (error) {
            this.showError(`Transformation failed: ${error.message}`);
            console.error(error);
        } finally {
            transformBtn.disabled = false;
            transformBtn.textContent = 'Transform';
        }
    }

    clear() {
        document.getElementById('input-text').value = '';
        document.getElementById('output-text').value = '';
        document.getElementById('filter-select').value = '';
        this.hideError();
    }

    showError(message) {
        const errorElement = document.getElementById('error-message');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        document.getElementById('error-message').style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const app = new TalkLikeAnXApp();
    await app.init();
});
