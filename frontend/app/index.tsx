import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { Image } from 'expo-image';
import { useRouter } from 'expo-router';
import axios from 'axios';

const { width, height } = Dimensions.get('window');
const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

export default function HomeScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);
  const [selectedDifficulty, setSelectedDifficulty] = useState<number>(1); // 1=Easy, 2=Medium, 3=Hard

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Initialize butterflies in database
      await axios.post(`${EXPO_PUBLIC_BACKEND_URL}/api/init-butterflies`);
      setInitialized(true);
    } catch (error) {
      console.error('Error initializing app:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartGame = () => {
    router.push({
      pathname: '/game',
      params: { difficulty: selectedDifficulty }
    });
  };

  const handleAdminPanel = () => {
    router.push('/admin');
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* HM Logo */}
        <View style={styles.logoContainer}>
          <Image
            source={{
              uri: 'https://customer-assets.emergentagent.com/job_4b17dfa0-2069-4af0-b587-cffef1721d1d/artifacts/w6x2g86q_HM%20logo.png',
            }}
            style={styles.logo}
            contentFit="contain"
          />
        </View>

        {/* Title */}
        <Text style={styles.title}>Butterfly Identification</Text>
        <Text style={styles.subtitle}>Test Your Knowledge</Text>

        {/* Decorative Butterfly Image */}
        <View style={styles.butterflyContainer}>
          <Image
            source={{
              uri: 'https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85',
            }}
            style={styles.butterflyImage}
            contentFit="cover"
          />
        </View>

        {/* Difficulty Selection */}
        <View style={styles.difficultyContainer}>
          <Text style={styles.difficultyLabel}>Select Difficulty</Text>
          <View style={styles.difficultyButtons}>
            <TouchableOpacity
              style={[
                styles.difficultyButton,
                selectedDifficulty === 1 && [styles.difficultyButtonActive, { backgroundColor: '#4CAF50' }],
              ]}
              onPress={() => setSelectedDifficulty(1)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.difficultyButtonText,
                  selectedDifficulty === 1 && styles.difficultyButtonTextActive,
                ]}
              >
                Easy
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.difficultyButton,
                selectedDifficulty === 2 && [styles.difficultyButtonActive, { backgroundColor: '#FF9800' }],
              ]}
              onPress={() => setSelectedDifficulty(2)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.difficultyButtonText,
                  selectedDifficulty === 2 && styles.difficultyButtonTextActive,
                ]}
              >
                Medium
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.difficultyButton,
                selectedDifficulty === 3 && [styles.difficultyButtonActive, { backgroundColor: '#F44336' }],
              ]}
              onPress={() => setSelectedDifficulty(3)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.difficultyButtonText,
                  selectedDifficulty === 3 && styles.difficultyButtonTextActive,
                ]}
              >
                Hard
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Start Button */}
        <TouchableOpacity
          style={styles.startButton}
          onPress={handleStartGame}
          activeOpacity={0.8}
        >
          <Text style={styles.startButtonText}>START GAME</Text>
        </TouchableOpacity>

        {/* Info Text */}
        <Text style={styles.infoText}>10 rounds • Selected difficulty: {selectedDifficulty === 1 ? 'Easy' : selectedDifficulty === 2 ? 'Medium' : 'Hard'}</Text>

        {/* Admin Button */}
        <TouchableOpacity
          style={styles.adminButton}
          onPress={handleAdminPanel}
          activeOpacity={0.8}
        >
          <Text style={styles.adminButtonText}>Admin Panel</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F8E9',
  },
  scrollContent: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 32,
    paddingHorizontal: 20,
  },
  logoContainer: {
    marginBottom: 12,
  },
  logo: {
    width: 100,
    height: 100,
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 15,
    color: '#558B2F',
    marginBottom: 20,
    textAlign: 'center',
  },
  butterflyContainer: {
    width: width * 0.5,
    height: width * 0.5,
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  butterflyImage: {
    width: '100%',
    height: '100%',
  },
  difficultyContainer: {
    width: '100%',
    alignItems: 'center',
    marginBottom: 24,
  },
  difficultyLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 12,
  },
  difficultyButtons: {
    flexDirection: 'row',
    gap: 10,
    width: '100%',
    justifyContent: 'center',
  },
  difficultyButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
    backgroundColor: '#E8F5E9',
    borderWidth: 2,
    borderColor: '#C8E6C9',
  },
  difficultyButtonActive: {
    borderColor: 'transparent',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 3,
  },
  difficultyButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E7D32',
  },
  difficultyButtonTextActive: {
    color: '#fff',
  },
  startButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 14,
    paddingHorizontal: 40,
    borderRadius: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
    marginBottom: 12,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  infoText: {
    fontSize: 13,
    color: '#558B2F',
    textAlign: 'center',
    marginBottom: 20,
  },
  adminButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  adminButtonText: {
    color: '#2E7D32',
    fontSize: 15,
    fontWeight: '600',
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
});
