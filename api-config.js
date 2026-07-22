// AGERinfo - API Configuration
// ============================================
// ImgBB API key for image uploads
// Get yours at: https://api.imgbb.com (Sign up > Get API key)
// ============================================

const CONFIG = {
    imgbb: {
        apiKey: '2af218f2172198fd7349714f99f23f27'
    }
};

// Set backend API URL (change for production)
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
window.AGERINFO_API_URL = isLocal ? 'http://127.0.0.1:8000/api' : 'https://agerinfo.onrender.com/api';
window.AGERINFO_IMGBB_KEY = CONFIG.imgbb.apiKey;
