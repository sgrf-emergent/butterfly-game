import React, { useState } from 'react';
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
} from 'react-native';
import { useRouter } from 'expo-router';
import { authUtils } from '../utils/auth';

export default function SetupScreen() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    const trimmedUsername = username.trim();
    
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

    try {
      setSaving(true);
      await authUtils.saveUsername(trimmedUsername);
      // Navigate to home screen
      router.replace('/');
    } catch (error) {
      Alert.alert('Error', 'Failed to save username. Please try again.');
      console.error('Error saving username:', error);
    } finally {
      setSaving(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={styles.content}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.inner}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.emoji}>🦋</Text>
            <Text style={styles.title}>Welcome!</Text>
            <Text style={styles.subtitle}>
              Let's start by creating your player profile
            </Text>
          </View>

          {/* Input Section */}
          <View style={styles.inputSection}>
            <Text style={styles.label}>Enter Your Username</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g., ButterflyLover"
              placeholderTextColor="#999"
              value={username}
              onChangeText={setUsername}
              editable={!saving}
              autoCapitalize="none"
              autoCorrect={false}
              maxLength={20}
            />
            <Text style={styles.helperText}>
              This name will be used to track your scores
            </Text>
          </View>

          {/* Continue Button */}
          <TouchableOpacity
            style={[styles.button, saving && styles.buttonDisabled]}
            onPress={handleSave}
            disabled={saving}
            activeOpacity={0.8}
          >
            {saving ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Continue</Text>
            )}
          </TouchableOpacity>
        </View>
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
  inner: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  header: {
    alignItems: 'center',
    marginBottom: 48,
  },
  emoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#558B2F',
    textAlign: 'center',
    lineHeight: 22,
  },
  inputSection: {
    marginBottom: 32,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 8,
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
  button: {
    backgroundColor: '#4CAF50',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
