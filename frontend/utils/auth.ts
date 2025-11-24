import AsyncStorage from '@react-native-async-storage/async-storage';

const USERNAME_KEY = '@butterfly_app_username';

export const authUtils = {
  // Save username to AsyncStorage
  async saveUsername(username: string): Promise<void> {
    try {
      await AsyncStorage.setItem(USERNAME_KEY, username);
    } catch (error) {
      console.error('Error saving username:', error);
      throw error;
    }
  },

  // Get username from AsyncStorage
  async getUsername(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(USERNAME_KEY);
    } catch (error) {
      console.error('Error getting username:', error);
      return null;
    }
  },

  // Check if user is logged in (has username)
  async isLoggedIn(): Promise<boolean> {
    const username = await this.getUsername();
    return username !== null && username.trim() !== '';
  },

  // Clear username (logout)
  async clearUsername(): Promise<void> {
    try {
      await AsyncStorage.removeItem(USERNAME_KEY);
    } catch (error) {
      console.error('Error clearing username:', error);
      throw error;
    }
  },
};
