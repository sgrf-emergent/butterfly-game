import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
} from 'react-native';
import { Image } from 'expo-image';
import { useRouter, useLocalSearchParams } from 'expo-router';
import axios from 'axios';

const { width } = Dimensions.get('window');
const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

interface Butterfly {
  id?: string;
  commonName: string;
  latinName: string;
  imageUrl: string;
  difficulty: number;
}

export default function EditButterflyScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();

  const [isEditMode, setIsEditMode] = useState(false);
  const [butterflyId, setButterflyId] = useState<string | undefined>(undefined);
  const [commonName, setCommonName] = useState('');
  const [latinName, setLatinName] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [difficulty, setDifficulty] = useState(1);
  const [saving, setSaving] = useState(false);
  const [formKey, setFormKey] = useState(0); // Add form key for forcing re-render

  useEffect(() => {
    if (params.butterfly) {
      try {
        const butterfly = JSON.parse(params.butterfly as string);
        setIsEditMode(true);
        setButterflyId(butterfly.id);
        setCommonName(butterfly.commonName);
        setLatinName(butterfly.latinName);
        setImageUrl(butterfly.imageUrl);
        setDifficulty(butterfly.difficulty);
        setFormKey(prev => prev + 1); // Force form re-render with new data
      } catch (error) {
        console.error('Error parsing butterfly data:', error);
      }
    } else {
      // Reset form for add mode
      setIsEditMode(false);
      setButterflyId(undefined);
      setCommonName('');
      setLatinName('');
      setImageUrl('');
      setDifficulty(1);
      setFormKey(prev => prev + 1);
    }
  }, [params.butterfly]);

  const validateForm = () => {
    if (!commonName.trim()) {
      Alert.alert('Validation Error', 'Please enter a common name');
      return false;
    }
    if (!latinName.trim()) {
      Alert.alert('Validation Error', 'Please enter a Latin name');
      return false;
    }
    if (!imageUrl.trim()) {
      Alert.alert('Validation Error', 'Please enter an image URL');
      return false;
    }
    if (!imageUrl.startsWith('http://') && !imageUrl.startsWith('https://')) {
      Alert.alert('Validation Error', 'Image URL must start with http:// or https://');
      return false;
    }
    return true;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      setSaving(true);
      const butterflyData: Butterfly = {
        commonName: commonName.trim(),
        latinName: latinName.trim(),
        imageUrl: imageUrl.trim(),
        difficulty,
      };

      if (isEditMode && butterflyId) {
        // Update existing butterfly
        await axios.put(
          `${EXPO_PUBLIC_BACKEND_URL}/api/admin/butterfly/${butterflyId}`,
          butterflyData
        );
        Alert.alert('Success', 'Butterfly updated successfully');
      } else {
        // Create new butterfly
        await axios.post(`${EXPO_PUBLIC_BACKEND_URL}/api/admin/butterfly`, butterflyData);
        Alert.alert('Success', 'Butterfly created successfully');
      }

      router.back();
    } catch (error) {
      console.error('Error saving butterfly:', error);
      Alert.alert('Error', 'Failed to save butterfly. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={handleCancel} style={styles.backButton}>
            <Text style={styles.backButtonText}>Cancel</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>
            {isEditMode ? 'Edit Butterfly' : 'Add Butterfly'}
          </Text>
          <TouchableOpacity onPress={handleSave} style={styles.saveButton} disabled={saving}>
            <Text style={[styles.saveButtonText, saving && styles.saveButtonTextDisabled]}>
              {saving ? 'Saving...' : 'Save'}
            </Text>
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.formContainer} showsVerticalScrollIndicator={false}>
          {/* Image Preview */}
          {imageUrl.trim() !== '' && (
            <View style={styles.imagePreviewContainer}>
              <Text style={styles.sectionTitle}>Image Preview</Text>
              <Image source={{ uri: imageUrl }} style={styles.imagePreview} contentFit="cover" />
            </View>
          )}

          {/* Common Name */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Common Name *</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g., Monarch"
              placeholderTextColor="#999"
              value={commonName}
              onChangeText={setCommonName}
              editable={!saving}
              autoCapitalize="words"
            />
          </View>

          {/* Latin Name */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Latin Name *</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g., Danaus plexippus"
              placeholderTextColor="#999"
              value={latinName}
              onChangeText={setLatinName}
              editable={!saving}
              autoCapitalize="words"
            />
          </View>

          {/* Image URL */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Image URL *</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="https://example.com/butterfly.jpg"
              placeholderTextColor="#999"
              value={imageUrl}
              onChangeText={setImageUrl}
              editable={!saving}
              autoCapitalize="none"
              autoCorrect={false}
              multiline
              numberOfLines={3}
            />
            <Text style={styles.helperText}>
              Enter a direct image URL (must start with http:// or https://)
            </Text>
          </View>

          {/* Difficulty */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Difficulty Level *</Text>
            <View style={styles.difficultyButtons}>
              <TouchableOpacity
                style={[
                  styles.difficultyButton,
                  difficulty === 1 && styles.difficultyButtonActive,
                  { backgroundColor: difficulty === 1 ? '#4CAF50' : '#E0E0E0' },
                ]}
                onPress={() => setDifficulty(1)}
              >
                <Text
                  style={[
                    styles.difficultyButtonText,
                    difficulty === 1 && styles.difficultyButtonTextActive,
                  ]}
                >
                  Easy
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.difficultyButton,
                  difficulty === 2 && styles.difficultyButtonActive,
                  { backgroundColor: difficulty === 2 ? '#FF9800' : '#E0E0E0' },
                ]}
                onPress={() => setDifficulty(2)}
              >
                <Text
                  style={[
                    styles.difficultyButtonText,
                    difficulty === 2 && styles.difficultyButtonTextActive,
                  ]}
                >
                  Medium
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.difficultyButton,
                  difficulty === 3 && styles.difficultyButtonActive,
                  { backgroundColor: difficulty === 3 ? '#F44336' : '#E0E0E0' },
                ]}
                onPress={() => setDifficulty(3)}
              >
                <Text
                  style={[
                    styles.difficultyButtonText,
                    difficulty === 3 && styles.difficultyButtonTextActive,
                  ]}
                >
                  Hard
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          <View style={styles.bottomPadding} />
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5E9',
  },
  keyboardView: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  backButton: {
    padding: 8,
  },
  backButtonText: {
    fontSize: 16,
    color: '#F44336',
    fontWeight: '600',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  saveButton: {
    padding: 8,
  },
  saveButtonText: {
    fontSize: 16,
    color: '#4CAF50',
    fontWeight: '600',
  },
  saveButtonTextDisabled: {
    color: '#999',
  },
  formContainer: {
    flex: 1,
    padding: 16,
  },
  imagePreviewContainer: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 12,
  },
  imagePreview: {
    width: '100%',
    height: 200,
    borderRadius: 16,
    backgroundColor: '#fff',
  },
  inputGroup: {
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  textArea: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  helperText: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  difficultyButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  difficultyButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  difficultyButtonActive: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  difficultyButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  difficultyButtonTextActive: {
    color: '#fff',
  },
  bottomPadding: {
    height: 40,
  },
});
