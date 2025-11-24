import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  ActivityIndicator,
  Alert,
  Dimensions,
} from 'react-native';
import { Image } from 'expo-image';
import { useRouter, useFocusEffect } from 'expo-router';
import axios from 'axios';

const { width } = Dimensions.get('window');
const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

interface Butterfly {
  id: string;
  commonName: string;
  latinName: string;
  imageUrl: string;
  difficulty: number;
}

export default function AdminHomeScreen() {
  const router = useRouter();
  const [butterflies, setButterflies] = useState<Butterfly[]>([]);
  const [filteredButterflies, setFilteredButterflies] = useState<Butterfly[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  // Reload butterflies when screen comes into focus (after returning from edit screen)
  useFocusEffect(
    React.useCallback(() => {
      loadButterflies();
    }, [])
  );

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredButterflies(butterflies);
    } else {
      const filtered = butterflies.filter(
        (b) =>
          b.commonName.toLowerCase().includes(searchQuery.toLowerCase()) ||
          b.latinName.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredButterflies(filtered);
    }
  }, [searchQuery, butterflies]);

  const loadButterflies = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${EXPO_PUBLIC_BACKEND_URL}/api/admin/butterflies`);
      setButterflies(response.data);
      setFilteredButterflies(response.data);
    } catch (error) {
      console.error('Error loading butterflies:', error);
      Alert.alert('Error', 'Failed to load butterflies');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string, name: string) => {
    Alert.alert(
      'Delete Butterfly',
      `Are you sure you want to delete "${name}"?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await axios.delete(`${EXPO_PUBLIC_BACKEND_URL}/api/admin/butterfly/${id}`);
              Alert.alert('Success', 'Butterfly deleted successfully');
              loadButterflies();
            } catch (error) {
              console.error('Error deleting butterfly:', error);
              Alert.alert('Error', 'Failed to delete butterfly');
            }
          },
        },
      ]
    );
  };

  const handleEdit = (butterfly: Butterfly) => {
    router.push({
      pathname: '/admin/edit',
      params: { butterfly: JSON.stringify(butterfly) },
    });
  };

  const handleAddNew = () => {
    router.push('/admin/edit');
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
        return '#9E9E9E';
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading butterflies...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Admin Panel</Text>
        <View style={styles.placeholder} />
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search butterflies..."
          placeholderTextColor="#999"
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>

      {/* Add New Button */}
      <TouchableOpacity style={styles.addButton} onPress={handleAddNew}>
        <Text style={styles.addButtonText}>+ Add New Butterfly</Text>
      </TouchableOpacity>

      {/* Butterfly Count */}
      <Text style={styles.countText}>
        {filteredButterflies.length} {filteredButterflies.length === 1 ? 'butterfly' : 'butterflies'}
      </Text>

      {/* Butterfly List */}
      <ScrollView style={styles.listContainer} showsVerticalScrollIndicator={false}>
        {filteredButterflies.map((butterfly) => (
          <View key={butterfly.id} style={styles.card}>
            <Image source={{ uri: butterfly.imageUrl }} style={styles.cardImage} contentFit="cover" />
            <View style={styles.cardContent}>
              <Text style={styles.cardTitle}>{butterfly.commonName}</Text>
              <Text style={styles.cardSubtitle}>{butterfly.latinName}</Text>
              <View style={styles.cardFooter}>
                <View
                  style={[
                    styles.difficultyBadge,
                    { backgroundColor: getDifficultyColor(butterfly.difficulty) },
                  ]}
                >
                  <Text style={styles.difficultyText}>{getDifficultyLabel(butterfly.difficulty)}</Text>
                </View>
                <View style={styles.cardActions}>
                  <TouchableOpacity
                    style={[styles.actionButton, styles.editButton]}
                    onPress={() => handleEdit(butterfly)}
                  >
                    <Text style={styles.actionButtonText}>Edit</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.actionButton, styles.deleteButton]}
                    onPress={() => handleDelete(butterfly.id, butterfly.commonName)}
                  >
                    <Text style={styles.actionButtonText}>Delete</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5E9',
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
    color: '#4CAF50',
    fontWeight: '600',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  placeholder: {
    width: 60,
  },
  searchContainer: {
    padding: 16,
  },
  searchInput: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  addButton: {
    backgroundColor: '#4CAF50',
    marginHorizontal: 16,
    marginBottom: 8,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  countText: {
    fontSize: 14,
    color: '#666',
    marginHorizontal: 16,
    marginBottom: 8,
  },
  listContainer: {
    flex: 1,
    paddingHorizontal: 16,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    marginBottom: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardImage: {
    width: '100%',
    height: 200,
  },
  cardContent: {
    padding: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
  },
  cardSubtitle: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
    marginBottom: 12,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  difficultyBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  difficultyText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  cardActions: {
    flexDirection: 'row',
    gap: 8,
  },
  actionButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  editButton: {
    backgroundColor: '#2196F3',
  },
  deleteButton: {
    backgroundColor: '#F44336',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#4CAF50',
    textAlign: 'center',
  },
});
