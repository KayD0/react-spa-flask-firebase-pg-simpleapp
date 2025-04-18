import { getAuth } from 'firebase/auth';

// Environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

/**
 * Get the current user's ID token
 * 
 * @returns {Promise<string|null>} ID token, or null if not authenticated
 */
export const getIdToken = async () => {
  const auth = getAuth();
  const currentUser = auth.currentUser;
  
  if (!currentUser) {
    console.warn('No user is currently signed in');
    return null;
  }
  
  try {
    // Get a new token (default is force refresh = false)
    const token = await currentUser.getIdToken();
    return token;
  } catch (error) {
    console.error('Error getting ID token:', error);
    return null;
  }
};

/**
 * Make an authenticated API request
 * 
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} - Fetch response
 */
export const authenticatedFetch = async (endpoint, options = {}) => {
  // Get ID token
  const token = await getIdToken();
  
  if (!token) {
    throw new Error('Authentication required');
  }
  
  // Add token to Authorization header
  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`
  };
  
  // Make request with token
  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers
  });
};

/**
 * Verify authentication token with backend
 * 
 * @returns {Promise<Object>} - User info from verified token
 */
export const verifyAuth = async () => {
  try {
    const response = await authenticatedFetch('/api/auth/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Auth verification error:', error);
    throw error;
  }
};

/**
 * Get user profile
 * 
 * @returns {Promise<Object>} - Profile information
 */
export const getProfile = async () => {
  try {
    const response = await authenticatedFetch('/api/profile', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Profile fetch error:', error);
    throw error;
  }
};

/**
 * Update user profile
 * 
 * @param {Object} profileData - Profile data to update
 * @param {string} profileData.display_name - Display name (optional)
 * @param {string} profileData.bio - Bio (optional)
 * @param {string} profileData.location - Location (optional)
 * @param {string} profileData.website - Website (optional)
 * @returns {Promise<Object>} - Updated profile information
 */
export const updateProfile = async (profileData) => {
  try {
    const response = await authenticatedFetch('/api/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Profile update error:', error);
    throw error;
  }
};

/**
 * Search YouTube videos (authenticated version)
 * 
 * @param {Object} params - Search parameters
 * @param {string} params.q - Search query
 * @param {string} params.published_after - Filter videos published after this date (ISO 8601 format)
 * @param {number} params.max_results - Maximum number of results to return
 * @param {string} params.channel_id - Filter by channel ID (optional)
 * @returns {Promise<Object>} - Search results
 */
export const searchVideos = async (params) => {
  try {
    const response = await authenticatedFetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Video search error:', error);
    throw error;
  }
};

/**
 * Generate YouTube video summary (authenticated version)
 * 
 * @param {string} videoId - YouTube video ID
 * @param {string} formatType - Summary format ("json" or "markdown")
 * @returns {Promise<Object>} - Summary data
 */
export const generateVideoSummary = async (videoId, formatType = 'json') => {
  try {
    const response = await authenticatedFetch('/api/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        video_id: videoId,
        format_type: formatType
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Video summary generation error:', error);
    throw error;
  }
};
