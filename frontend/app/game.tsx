import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  SafeAreaView,
  Dimensions,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import axios from 'axios';

const { width, height } = Dimensions.get('window');
const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

interface Butterfly {
  id: string;
  commonName: string;
  latinName: string;
  imageUrl: string;
}

interface QuizQuestion {
  correctAnswer: Butterfly;
  options: Butterfly[];
}

export default function GameScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState<QuizQuestion | null>(null);
  const [currentRound, setCurrentRound] = useState(1);
  const [score, setScore] = useState(0);
  const [showOptions, setShowOptions] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [timeLeft, setTimeLeft] = useState(10);
  const [isAnswered, setIsAnswered] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    loadQuestion();
  }, []);

  useEffect(() => {
    if (showOptions && !isAnswered) {
      // Start 10 second timer
      setTimeLeft(10);
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleTimeout();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [showOptions, isAnswered]);

  const loadQuestion = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${EXPO_PUBLIC_BACKEND_URL}/api/quiz/question`);
      setQuestion(response.data);
      setShowOptions(false);
      setSelectedAnswer(null);
      setShowFeedback(false);
      setIsAnswered(false);
      
      // Show image for 5 seconds, then show options
      setTimeout(() => {
        setShowOptions(true);
      }, 5000);
    } catch (error) {
      console.error('Error loading question:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTimeout = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setIsAnswered(true);
    setIsCorrect(false);
    setShowFeedback(true);
  };

  const handleAnswer = (butterfly: Butterfly) => {
    if (isAnswered || !question) return;

    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    setIsAnswered(true);
    setSelectedAnswer(butterfly.id);
    const correct = butterfly.id === question.correctAnswer.id;
    setIsCorrect(correct);
    
    if (correct) {
      setScore(score + 1);
    }
    
    setShowFeedback(true);
  };

  const handleNext = () => {
    if (currentRound >= 10) {
      // Game over
      router.push({
        pathname: '/results',
        params: { score, total: 10 },
      });
    } else {
      setCurrentRound(currentRound + 1);
      loadQuestion();
    }
  };

  if (loading || !question) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.roundText}>Round {currentRound}/10</Text>
          <Text style={styles.scoreText}>Score: {score}/{currentRound - 1}</Text>
        </View>

        {/* Butterfly Image */}
        <View style={styles.imageContainer}>
          <Image
            source={{ uri: question.correctAnswer.imageUrl }}
            style={styles.butterflyImage}
            resizeMode="cover"
          />
          {!showOptions && (
            <View style={styles.overlay}>
              <ActivityIndicator size="large" color="#fff" />
              <Text style={styles.overlayText}>Get Ready...</Text>
            </View>
          )}
        </View>

        {/* Timer */}
        {showOptions && !isAnswered && (
          <View style={styles.timerContainer}>
            <Text style={styles.timerText}>Time Left: {timeLeft}s</Text>
          </View>
        )}

        {/* Options */}
        {showOptions && (
          <View style={styles.optionsContainer}>
            <Text style={styles.questionText}>Which butterfly is this?</Text>
            {question.options.map((butterfly) => {
              const isSelected = selectedAnswer === butterfly.id;
              const isCorrectAnswer = butterfly.id === question.correctAnswer.id;
              const showCorrect = showFeedback && isCorrectAnswer;
              const showWrong = showFeedback && isSelected && !isCorrect;

              return (
                <TouchableOpacity
                  key={butterfly.id}
                  style={[
                    styles.optionButton,
                    showCorrect && styles.correctOption,
                    showWrong && styles.wrongOption,
                  ]}
                  onPress={() => handleAnswer(butterfly)}
                  disabled={isAnswered}
                  activeOpacity={0.7}
                >
                  <Text style={styles.commonName}>{butterfly.commonName}</Text>
                  <Text style={styles.latinName}>{butterfly.latinName}</Text>
                </TouchableOpacity>
              );
            })}
          </View>
        )}

        {/* Feedback */}
        {showFeedback && (
          <View style={styles.feedbackContainer}>
            <Text style={[styles.feedbackText, isCorrect ? styles.correctText : styles.wrongText]}>
              {isCorrect ? '✓ Correct!' : '✗ Wrong!'}
            </Text>
            {!isCorrect && (
              <Text style={styles.correctAnswerText}>
                Correct answer: {question.correctAnswer.commonName}
              </Text>
            )}
            <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
              <Text style={styles.nextButtonText}>
                {currentRound >= 10 ? 'View Results' : 'Next'}
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5E9',
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#C8E6C9',
  },
  roundText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  scoreText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  imageContainer: {
    width: width,
    height: height * 0.4,
    position: 'relative',
  },
  butterflyImage: {
    width: '100%',
    height: '100%',
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  overlayText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 16,
  },
  timerContainer: {
    padding: 16,
    alignItems: 'center',
  },
  timerText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: timeLeft => (timeLeft <= 3 ? '#F44336' : '#4CAF50'),
  },
  optionsContainer: {
    padding: 16,
  },
  questionText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    textAlign: 'center',
    marginBottom: 16,
  },
  optionButton: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 2,
    borderColor: '#A5D6A7',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  correctOption: {
    backgroundColor: '#C8E6C9',
    borderColor: '#4CAF50',
  },
  wrongOption: {
    backgroundColor: '#FFCDD2',
    borderColor: '#F44336',
  },
  commonName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  latinName: {
    fontSize: 14,
    fontStyle: 'italic',
    color: '#558B2F',
    marginTop: 4,
  },
  feedbackContainer: {
    padding: 24,
    alignItems: 'center',
  },
  feedbackText: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  correctText: {
    color: '#4CAF50',
  },
  wrongText: {
    color: '#F44336',
  },
  correctAnswerText: {
    fontSize: 16,
    color: '#2E7D32',
    marginBottom: 24,
    textAlign: 'center',
  },
  nextButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 48,
    paddingVertical: 16,
    borderRadius: 24,
    minWidth: 200,
    alignItems: 'center',
  },
  nextButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
