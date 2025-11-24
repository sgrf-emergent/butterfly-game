import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  Alert,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { authUtils } from '../utils/auth';

export default function SettingsScreen() {
  const router = useRouter();
  const [currentUsername, setCurrentUsername] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUsername();
  }, []);

  const loadUsername = async () => {
    try {
      const username = await authUtils.getUsername();
      if (username) {
        setCurrentUsername(username);
        setNewUsername(username);
      }
    } catch (error) {
      console.error('Error loading username:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    const trimmedUsername = newUsername.trim();
    
    if (!trimmedUsername) {
      Alert.alert('Required', 'Please enter a username');
      return;
    }

    if (trimmedUsername.length < 2) {
      Alert.alert('Too Short', 'Username must be at least 2 characters');
      return;
    }

    if (trimmedUsername.length > 20) {
      Alert.alert('Too Long', 'Username must be 20 characters or less');
      return;
    }

    if (trimmedUsername === currentUsername) {
      Alert.alert('No Changes', 'Username is the same as before');
      return;
    }

    try {
      setSaving(true);
      await authUtils.saveUsername(trimmedUsername);
      setCurrentUsername(trimmedUsername);
      Alert.alert('Success', 'Username updated successfully!');
    } catch (error) {
      Alert.alert('Error', 'Failed to update username. Please try again.');
      console.error('Error updating username:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleBack = () => {
    router.back();
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={styles.content}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>Settings</Text>
            <Text style={styles.subtitle}>Manage your profile</Text>
          </View>

          {/* Current Username */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Current Username</Text>
            <View style={styles.currentUsernameBox}>
              <Text style={styles.currentUsername}>{currentUsername}</Text>
            </View>
          </View>

          {/* Change Username */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Change Username</Text>
            <TextInput
              style={styles.input}
              placeholder="Enter new username"
              placeholderTextColor="#999"
              value={newUsername}
              onChangeText={setNewUsername}
              editable={!saving}
              autoCapitalize="none"
              autoCorrect={false}
              maxLength={20}
            />
            <Text style={styles.helperText}>
              2-20 characters • This will be used for your scores
            </Text>
          </View>

          {/* Buttons */}
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.saveButton, saving && styles.buttonDisabled]}
              onPress={handleSave}
              disabled={saving}
              activeOpacity={0.8}
            >
              {saving ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>Save Changes</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.button, styles.backButton]}
              onPress={handleBack}
              disabled={saving}
              activeOpacity={0.8}
            >
              <Text style={[styles.buttonText, styles.backButtonText]}>Back</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F8E9',
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingVertical: 32,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#4CAF50',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 15,
    color: '#558B2F',
  },
  section: {
    marginBottom: 24,
  },
  sectionLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 8,
  },
  currentUsernameBox: {
    backgroundColor: '#E8F5E9',
    borderWidth: 2,
    borderColor: '#C8E6C9',
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  currentUsername: {
    fontSize: 16,
    color: '#2E7D32',
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#C8E6C9',
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
    fontSize: 16,
    color: '#2E7D32',
  },
  helperText: {
    fontSize: 13,
    color: '#558B2F',
    marginTop: 8,
  },
  buttonContainer: {
    marginTop: 16,
    gap: 12,
  },
  button: {
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  saveButton: {
    backgroundColor: '#4CAF50',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  backButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  backButtonText: {
    color: '#4CAF50',
  },
});
