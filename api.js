const API_BASE = window.AGERINFO_API_URL || 'http://127.0.0.1:8000/api';

const API = {
    _token: sessionStorage.getItem('agerinfo_token') || null,
    _cache: {},
    _cacheTTL: 30000,

    async init() {},

    _headers() {
        const h = { 'Content-Type': 'application/json' };
        if (this._token) h['Authorization'] = 'Token ' + this._token;
        return h;
    },

    async _fetchWithTimeout(url, options = {}, timeoutMs = 15000) {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs);
        try {
            const res = await fetch(url, { ...options, signal: controller.signal });
            clearTimeout(timer);
            return res;
        } catch (e) {
            clearTimeout(timer);
            if (e.name === 'AbortError') throw new Error('Request timed out');
            throw e;
        }
    },

    _getCache(key) {
        const entry = this._cache[key];
        if (entry && Date.now() - entry.ts < this._cacheTTL) return entry.data;
        return null;
    },

    _setCache(key, data) {
        this._cache[key] = { data, ts: Date.now() };
    },

    _clearCache(collection) {
        const keys = Object.keys(this._cache);
        keys.forEach(k => { if (k.startsWith(collection)) delete this._cache[k]; });
    },

    async _handleError(res) {
        let msg = 'Request failed (' + res.status + ')';
        try {
            const data = await res.json();
            if (data.detail) msg = data.detail;
            else if (data.error) msg = data.error;
            else if (typeof data === 'object') {
                const first = Object.entries(data)[0];
                if (first) msg = first[0] + ': ' + (Array.isArray(first[1]) ? first[1].join(', ') : first[1]);
            }
        } catch (e) {}
        throw new Error(msg);
    },

    async getData(collection) {
        const endpoints = {
            news: '/news/',
            gallery: '/gallery/',
            slider: '/slider/',
            topics: '/topics/'
        };
        const cacheKey = collection;
        const cached = this._getCache(cacheKey);
        if (cached) return cached;

        const res = await this._fetchWithTimeout(API_BASE + endpoints[collection], {
            headers: this._headers()
        });
        if (!res.ok) await this._handleError(res);
        const data = await res.json();
        this._setCache(cacheKey, data);
        return data;
    },

    async addItem(collection, item) {
        const endpoints = {
            news: '/news/create/',
            gallery: '/gallery/create/',
            slider: '/slider/create/',
            topics: '/topics/create/'
        };
        this._clearCache(collection);
        const res = await this._fetchWithTimeout(API_BASE + endpoints[collection], {
            method: 'POST',
            headers: this._headers(),
            body: JSON.stringify(item)
        }, 20000);
        if (!res.ok) await this._handleError(res);
        return await res.json();
    },

    async updateItem(collection, id, updates) {
        const endpoints = {
            news: `/news/${id}/update/`,
            gallery: `/gallery/${id}/update/`,
            slider: `/slider/${id}/update/`,
            topics: `/topics/${id}/update/`
        };
        this._clearCache(collection);
        const res = await this._fetchWithTimeout(API_BASE + endpoints[collection], {
            method: 'PATCH',
            headers: this._headers(),
            body: JSON.stringify(updates)
        }, 20000);
        if (!res.ok) await this._handleError(res);
        return await res.json();
    },

    async deleteItem(collection, id) {
        const endpoints = {
            news: `/news/${id}/delete/`,
            gallery: `/gallery/${id}/delete/`,
            slider: `/slider/${id}/delete/`,
            topics: `/topics/${id}/delete/`
        };
        this._clearCache(collection);
        const res = await this._fetchWithTimeout(API_BASE + endpoints[collection], {
            method: 'DELETE',
            headers: this._headers()
        }, 15000);
        if (!res.ok) await this._handleError(res);
    },

    async getCounts() {
        const cached = this._getCache('counts');
        if (cached) return cached;
        const res = await this._fetchWithTimeout(API_BASE + '/counts/', {
            headers: this._headers()
        });
        if (!res.ok) await this._handleError(res);
        const data = await res.json();
        this._setCache('counts', data);
        return data;
    },

    _compressImage(file, maxWidth = 1200, quality = 0.8) {
        return new Promise((resolve) => {
            if (file.size < 200 * 1024) { resolve(file); return; }
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let w = img.width, h = img.height;
                    if (w > maxWidth) { h = (maxWidth / w) * h; w = maxWidth; }
                    canvas.width = w;
                    canvas.height = h;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, w, h);
                    canvas.toBlob((blob) => {
                        if (blob && blob.size < file.size) {
                            resolve(new File([blob], file.name, { type: 'image/jpeg' }));
                        } else {
                            resolve(file);
                        }
                    }, 'image/jpeg', quality);
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    },

    async uploadImage(file) {
        const apiKey = window.AGERINFO_IMGBB_KEY || '';
        if (!apiKey) throw new Error('ImgBB API key not configured');
        const compressed = await this._compressImage(file);
        const base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(compressed);
        });
        const formData = new FormData();
        formData.append('key', apiKey);
        formData.append('image', base64);
        const res = await this._fetchWithTimeout('https://api.imgbb.com/1/upload', {
            method: 'POST',
            body: formData
        }, 30000);
        if (!res.ok) throw new Error('Image upload failed');
        const result = await res.json();
        return result.data.url;
    },

    async login(email, password) {
        const res = await this._fetchWithTimeout(API_BASE + '/auth/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        }, 15000);
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.error || 'Login failed');
        }
        const data = await res.json();
        this._token = data.token;
        sessionStorage.setItem('agerinfo_token', data.token);
        sessionStorage.setItem('agerinfo_user', data.email);
        return data;
    },

    logout() {
        this._token = null;
        this._cache = {};
        sessionStorage.removeItem('agerinfo_token');
        sessionStorage.removeItem('agerinfo_user');
    },

    isLoggedIn() {
        return !!this._token;
    },

    getUser() {
        return sessionStorage.getItem('agerinfo_user') || '';
    }
};
