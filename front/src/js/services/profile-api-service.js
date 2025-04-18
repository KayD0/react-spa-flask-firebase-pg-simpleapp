/**
 * プロフィールAPIサービス
 * 
 * このサービスはユーザープロフィールの取得と更新を処理します。
 */

import { authenticatedFetch } from './auth-api-service.js';

/**
 * ユーザープロフィールを取得
 * 
 * @returns {Promise<Object>} - プロフィール情報
 */
export async function getProfile() {
  try {
    const response = await authenticatedFetch('/api/profile', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `APIエラー: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('プロフィール取得エラー:', error);
    throw error;
  }
}

/**
 * ユーザープロフィールを更新
 * 
 * @param {Object} profileData - 更新するプロフィールデータ
 * @param {string} profileData.display_name - 表示名（オプション）
 * @param {string} profileData.bio - 自己紹介（オプション）
 * @param {string} profileData.location - 場所（オプション）
 * @param {string} profileData.website - ウェブサイト（オプション）
 * @returns {Promise<Object>} - 更新されたプロフィール情報
 */
export async function updateProfile(profileData) {
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
      throw new Error(errorData.error || `APIエラー: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('プロフィール更新エラー:', error);
    throw error;
  }
}

export default {
  getProfile,
  updateProfile
};
