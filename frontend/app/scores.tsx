import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { useRouter } from 'expo-router';
import axios from 'axios';
import { authUtils } from '../utils/auth';

const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;
const { width } = Dimensions.get('window');

interface PersonalBests {
  easy: number | null;
  medium: number | null;
  hard: number | null;
}

interface RecentGame {
  id: string;
  score: number;
  total: number;
  difficulty: number;
  percentage: number;
  date: string;
}

interface ScoresData {
  personalBests: PersonalBests;
  recentGames: RecentGame[];
  totalGames: number;
}

export default function ScoresScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [scoresData, setScoresData] = useState<ScoresData | null>(null);

  useEffect(() => {
    loadScores();
  }, []);

  const loadScores = async () => {
    try {
      const savedUsername = await authUtils.getUsername();
      if (!savedUsername) {
        router.replace('/setup');
        return;
      }
      
      setUsername(savedUsername);

      const response = await axios.get(`${EXPO_PUBLIC_BACKEND_URL}/api/scores/${savedUsername}`);
      setScoresData(response.data);
    } catch (error) {
      console.error('Error loading scores:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyLabel = (difficulty: number) => {
    switch (difficulty) {
      case 1:
        return 'Easy';
      case 2:
        return 'Medium';
      case 3:
        return 'Hard';
      default:
        return 'Unknown';
    }
  };

  const getDifficultyColor = (difficulty: number) => {
    switch (difficulty) {
      case 1:
        return '#4CAF50';
      case 2:
        return '#FF9800';
      case 3:
        return '#F44336';
      default:
        return '#999';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const handleBack = () => {
    router.back();
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>Loading your scores...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>My Scores</Text>
          <Text style={styles.subtitle}>Player: {username}</Text>
        </View>

        {/* Total Games */}
        <View style={styles.totalGamesCard}>
          <Text style={styles.totalGamesNumber}>{scoresData?.totalGames || 0}</Text>
          <Text style={styles.totalGamesLabel}>Total Games Played</Text>
        </View>

        {/* Personal Bests */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Personal Best Scores</Text>
          
          <View style={styles.personalBestsContainer}>
            {/* Easy */}
            <View style={[styles.bestCard, { borderColor: '#4CAF50' }]}>
              <Text style={styles.bestLabel}>Easy</Text>
              <Text style={[styles.bestScore, { color: '#4CAF50' }]}>
                {scoresData?.personalBests.easy !== null ? `${scoresData?.personalBests.easy}%` : '-'}
              </Text>
            </View>

            {/* Medium */}
            <View style={[styles.bestCard, { borderColor: '#FF9800' }]}>
              <Text style={styles.bestLabel}>Medium</Text>
              <Text style={[styles.bestScore, { color: '#FF9800' }]}>
                {scoresData?.personalBests.medium !== null ? `${scoresData?.personalBests.medium}%` : '-'}
              </Text>
            </View>

            {/* Hard */}
            <View style={[styles.bestCard, { borderColor: '#F44336' }]}>
              <Text style={styles.bestLabel}>Hard</Text>
              <Text style={[styles.bestScore, { color: '#F44336' }]}>
                {scoresData?.personalBests.hard !== null ? `${scoresData?.personalBests.hard}%` : '-'}
              </Text>
            </View>
          </View>
        </View>

        {/* Recent Games */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recent Games</Text>
          
          {scoresData && scoresData.recentGames.length > 0 ? (
            scoresData.recentGames.map((game, index) => (
              <View key={game.id} style={styles.gameCard}>
                <View style={styles.gameCardLeft}>
                  <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(game.difficulty) }]}>
                    <Text style={styles.difficultyBadgeText}>{getDifficultyLabel(game.difficulty)}</Text>
                  </View>
                  <View style={styles.gameInfo}>
                    <Text style={styles.gameScore}>{game.score}/{game.total}</Text>
                    <Text style={styles.gameDate}>{formatDate(game.date)}</Text>
                  </View>
                </View>
                <Text style={styles.gamePercentage}>{game.percentage}%</Text>
              </View>
            ))
          ) : (
            <View style={styles.noGamesContainer}>
              <Text style={styles.noGamesText}>No games played yet</Text>
              <Text style={styles.noGamesSubtext}>Start playing to see your history!</Text>
            </View>
          )}
        </View>

        {/* Back Button */}
        <TouchableOpacity
          style={styles.backButton}
          onPress={handleBack}
          activeOpacity={0.8}
        >
          <Text style={styles.backButtonText}>Back to Home</Text>
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
    paddingVertical: 24,
    paddingHorizontal: 20,
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
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#558B2F',
  },
  totalGamesCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 2,
    borderColor: '#C8E6C9',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  totalGamesNumber: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 4,
  },
  totalGamesLabel: {
    fontSize: 16,
    color: '#558B2F',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 12,
  },
  personalBestsContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  bestCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    borderWidth: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  bestLabel: {
    fontSize: 14,
    color: '#558B2F',
    marginBottom: 8,
    fontWeight: '600',
  },
  bestScore: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  gameCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E8F5E9',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  gameCardLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  difficultyBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  difficultyBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  gameInfo: {
    gap: 2,
  },
  gameScore: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  gameDate: {
    fontSize: 13,
    color: '#558B2F',
  },
  gamePercentage: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  noGamesContainer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 32,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E8F5E9',
  },
  noGamesText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 4,
  },
  noGamesSubtext: {
    fontSize: 14,
    color: '#558B2F',
  },
  backButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
