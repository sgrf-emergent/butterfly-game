import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

const { width, height } = Dimensions.get('window');

export default function ResultsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const score = parseInt(params.score as string) || 0;
  const total = parseInt(params.total as string) || 10;
  const difficulty = parseInt(params.difficulty as string) || 1;
  const percentage = Math.round((score / total) * 100);

  const getMessage = () => {
    if (percentage >= 90) return 'Outstanding! 🦋';
    if (percentage >= 70) return 'Great Job! 🌟';
    if (percentage >= 50) return 'Good Effort! 👍';
    return 'Keep Practicing! 💪';
  };

  const getDifficultyLabel = () => {
    switch(difficulty) {
      case 1: return 'Easy';
      case 2: return 'Medium';
      case 3: return 'Hard';
      default: return 'Easy';
    }
  };

  const getDifficultyColor = () => {
    switch(difficulty) {
      case 1: return '#4CAF50';
      case 2: return '#FF9800';
      case 3: return '#F44336';
      default: return '#4CAF50';
    }
  };

  const handlePlayAgain = () => {
    router.replace({
      pathname: '/game',
      params: { difficulty }
    });
  };

  const handleHome = () => {
    router.replace('/');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Title */}
        <Text style={styles.title}>Game Over!</Text>

        {/* Difficulty Badge */}
        <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor() }]}>
          <Text style={styles.difficultyText}>{getDifficultyLabel()}</Text>
        </View>

        {/* Score Circle */}
        <View style={styles.scoreCircle}>
          <Text style={styles.scoreNumber}>{score}</Text>
          <Text style={styles.scoreDivider}>/</Text>
          <Text style={styles.totalNumber}>{total}</Text>
        </View>

        {/* Percentage */}
        <Text style={styles.percentage}>{percentage}%</Text>

        {/* Message */}
        <Text style={styles.message}>{getMessage()}</Text>

        {/* Stats */}
        <View style={styles.statsContainer}>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{score}</Text>
            <Text style={styles.statLabel}>Correct</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{total - score}</Text>
            <Text style={styles.statLabel}>Wrong</Text>
          </View>
        </View>

        {/* Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.playAgainButton}
            onPress={handlePlayAgain}
            activeOpacity={0.8}
          >
            <Text style={styles.playAgainButtonText}>Play Again</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.homeButton}
            onPress={handleHome}
            activeOpacity={0.8}
          >
            <Text style={styles.homeButtonText}>Home</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5E9',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 32,
  },
  scoreCircle: {
    width: 200,
    height: 200,
    borderRadius: 100,
    backgroundColor: '#fff',
    borderWidth: 8,
    borderColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
    marginBottom: 24,
  },
  scoreNumber: {
    fontSize: 56,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  scoreDivider: {
    fontSize: 40,
    fontWeight: 'bold',
    color: '#81C784',
    marginHorizontal: 4,
  },
  totalNumber: {
    fontSize: 40,
    fontWeight: 'bold',
    color: '#81C784',
  },
  percentage: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 16,
  },
  message: {
    fontSize: 24,
    fontWeight: '600',
    color: '#558B2F',
    marginBottom: 32,
  },
  statsContainer: {
    flexDirection: 'row',
    gap: 24,
    marginBottom: 48,
  },
  statBox: {
    backgroundColor: '#fff',
    padding: 24,
    borderRadius: 16,
    minWidth: 120,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  statNumber: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 8,
  },
  statLabel: {
    fontSize: 16,
    color: '#558B2F',
  },
  buttonContainer: {
    width: '100%',
    gap: 16,
  },
  playAgainButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 18,
    borderRadius: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  playAgainButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  homeButton: {
    backgroundColor: '#fff',
    paddingVertical: 18,
    borderRadius: 24,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  homeButtonText: {
    color: '#4CAF50',
    fontSize: 20,
    fontWeight: 'bold',
  },
});
