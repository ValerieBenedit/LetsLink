import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
  SafeAreaView,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

const { width, height } = Dimensions.get('window');

const interests = [
  { id: 1, name: 'Dining Out', emoji: '🍽️' },
  { id: 2, name: 'Movies', emoji: '🎬' },
  { id: 3, name: 'Art & Museums', emoji: '🎨' },
  { id: 4, name: 'Music & Concerts', emoji: '🎵' },
  { id: 5, name: 'Sports & Fitness', emoji: '⚽' },
  { id: 6, name: 'Nature & Hiking', emoji: '🌲' },
  { id: 7, name: 'Travel & Adventure', emoji: '✈️' },
  { id: 8, name: 'Gaming', emoji: '🎮' },
  { id: 9, name: 'Reading & Books', emoji: '📚' },
  { id: 10, name: 'Photography', emoji: '📸' },
  { id: 11, name: 'Cooking', emoji: '👨‍🍳' },
  { id: 12, name: 'Dancing', emoji: '💃' },
];

const OnboardingScreen = ({ navigation }: any) => {
  const [selectedInterests, setSelectedInterests] = useState<number[]>([]);
  const [currentStep, setCurrentStep] = useState(0);

  const handleInterestToggle = (interestId: number) => {
    setSelectedInterests(prev => 
      prev.includes(interestId) 
        ? prev.filter(id => id !== interestId)
        : [...prev, interestId]
    );
  };

  const handleNext = () => {
    if (currentStep === 0) {
      setCurrentStep(1);
    } else {
      // Navigate to home screen
      navigation.replace('Home');
    }
  };

  const renderWelcomeStep = () => (
    <View style={styles.stepContainer}>
      <View style={styles.welcomeContent}>
        <Text style={styles.welcomeTitle}>Welcome to Let's Link</Text>
        <Text style={styles.welcomeSubtitle}>
          Discover amazing dates and connect with your partner through AI-powered planning
        </Text>
        <View style={styles.illustrationContainer}>
          <Text style={styles.illustrationEmoji}>💕</Text>
        </View>
      </View>
    </View>
  );

  const renderInterestsStep = () => (
    <View style={styles.stepContainer}>
      <View style={styles.interestsHeader}>
        <Text style={styles.stepTitle}>What interests you?</Text>
        <Text style={styles.stepSubtitle}>
          Select your favorite activities to help us plan perfect dates
        </Text>
      </View>
      
      <ScrollView 
        style={styles.interestsContainer}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.interestsGrid}>
          {interests.map((interest) => (
            <TouchableOpacity
              key={interest.id}
              style={[
                styles.interestCard,
                selectedInterests.includes(interest.id) && styles.interestCardSelected
              ]}
              onPress={() => handleInterestToggle(interest.id)}
            >
              <Text style={styles.interestEmoji}>{interest.emoji}</Text>
              <Text style={[
                styles.interestName,
                selectedInterests.includes(interest.id) && styles.interestNameSelected
              ]}>
                {interest.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#FF6B9D', '#C44569']}
        style={styles.gradient}
      >
        {currentStep === 0 ? renderWelcomeStep() : renderInterestsStep()}
        
        <View style={styles.bottomContainer}>
          <View style={styles.stepIndicator}>
            <View style={[styles.stepDot, currentStep === 0 && styles.stepDotActive]} />
            <View style={[styles.stepDot, currentStep === 1 && styles.stepDotActive]} />
          </View>
          
          <TouchableOpacity
            style={[
              styles.nextButton,
              currentStep === 1 && selectedInterests.length === 0 && styles.nextButtonDisabled
            ]}
            onPress={handleNext}
            disabled={currentStep === 1 && selectedInterests.length === 0}
          >
            <Text style={styles.nextButtonText}>
              {currentStep === 0 ? 'Get Started' : 'Continue'}
            </Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  stepContainer: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
  },
  welcomeContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcomeTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 16,
  },
  welcomeSubtitle: {
    fontSize: 18,
    color: '#FFFFFF',
    textAlign: 'center',
    lineHeight: 24,
    opacity: 0.9,
    marginBottom: 40,
  },
  illustrationContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  illustrationEmoji: {
    fontSize: 60,
  },
  interestsHeader: {
    marginBottom: 30,
  },
  stepTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 12,
  },
  stepSubtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
    opacity: 0.9,
    lineHeight: 22,
  },
  interestsContainer: {
    flex: 1,
  },
  interestsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  interestCard: {
    width: (width - 72) / 2,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  interestCardSelected: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderColor: '#FFFFFF',
  },
  interestEmoji: {
    fontSize: 32,
    marginBottom: 8,
  },
  interestName: {
    fontSize: 14,
    color: '#FFFFFF',
    textAlign: 'center',
    fontWeight: '600',
  },
  interestNameSelected: {
    fontWeight: 'bold',
  },
  bottomContainer: {
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  stepIndicator: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 30,
  },
  stepDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
    marginHorizontal: 4,
  },
  stepDotActive: {
    backgroundColor: '#FFFFFF',
  },
  nextButton: {
    backgroundColor: '#FFFFFF',
    borderRadius: 25,
    paddingVertical: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  nextButtonDisabled: {
    opacity: 0.5,
  },
  nextButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#C44569',
  },
});

export default OnboardingScreen;
