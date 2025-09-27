import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  TextInput,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

const HomeScreen = ({ navigation }: any) => {
  const [isLinked, setIsLinked] = useState(false);
  const [partnerName, setPartnerName] = useState('');
  const [showLinkForm, setShowLinkForm] = useState(false);

  const handleLinkWithPartner = () => {
    if (partnerName.trim()) {
      setIsLinked(true);
      setShowLinkForm(false);
      Alert.alert(
        'Successfully Linked! 🎉',
        `You're now connected with ${partnerName}. AI will help plan your perfect dates!`,
        [{ text: 'Awesome!', style: 'default' }]
      );
    }
  };

  const handleUnlink = () => {
    Alert.alert(
      'Unlink Partner',
      'Are you sure you want to unlink from your partner?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Unlink', 
          style: 'destructive',
          onPress: () => {
            setIsLinked(false);
            setPartnerName('');
          }
        }
      ]
    );
  };

  const renderLinkSection = () => {
    if (isLinked) {
      return (
        <View style={styles.linkedContainer}>
          <View style={styles.linkedHeader}>
            <Text style={styles.linkedTitle}>You're Linked! 💕</Text>
            <Text style={styles.linkedSubtitle}>
              Connected with {partnerName}
            </Text>
          </View>
          
          <View style={styles.statusCard}>
            <Text style={styles.statusTitle}>AI Date Planning Active</Text>
            <Text style={styles.statusDescription}>
              Our AI is analyzing your schedules and interests to suggest perfect date ideas.
            </Text>
            <View style={styles.statusIndicator}>
              <View style={styles.statusDot} />
              <Text style={styles.statusText}>Planning in progress...</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.unlinkButton} onPress={handleUnlink}>
            <Text style={styles.unlinkButtonText}>Unlink Partner</Text>
          </TouchableOpacity>
        </View>
      );
    }

    if (showLinkForm) {
      return (
        <View style={styles.linkFormContainer}>
          <Text style={styles.formTitle}>Link with Your Partner</Text>
          <Text style={styles.formSubtitle}>
            Enter your partner's name to start planning amazing dates together
          </Text>
          
          <TextInput
            style={styles.nameInput}
            placeholder="Partner's name"
            placeholderTextColor="#999"
            value={partnerName}
            onChangeText={setPartnerName}
            autoCapitalize="words"
          />
          
          <View style={styles.formButtons}>
            <TouchableOpacity 
              style={styles.cancelButton} 
              onPress={() => setShowLinkForm(false)}
            >
              <Text style={styles.cancelButtonText}>Cancel</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.linkButton, !partnerName.trim() && styles.linkButtonDisabled]}
              onPress={handleLinkWithPartner}
              disabled={!partnerName.trim()}
            >
              <Text style={styles.linkButtonText}>Link Now</Text>
            </TouchableOpacity>
          </View>
        </View>
      );
    }

    return (
      <View style={styles.unlinkedContainer}>
        <View style={styles.unlinkedHeader}>
          <Text style={styles.unlinkedTitle}>Ready to Link? 💫</Text>
          <Text style={styles.unlinkedSubtitle}>
            Connect with your partner and let AI plan your perfect dates
          </Text>
        </View>
        
        <TouchableOpacity 
          style={styles.linkButton} 
          onPress={() => setShowLinkForm(true)}
        >
          <Text style={styles.linkButtonText}>Link with Partner</Text>
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.gradient}
      >
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          <View style={styles.header}>
            <Text style={styles.appTitle}>Let's Link</Text>
            <Text style={styles.appSubtitle}>AI-Powered Date Planning</Text>
          </View>

          {renderLinkSection()}

          <View style={styles.featuresContainer}>
            <Text style={styles.featuresTitle}>Coming Soon</Text>
            <View style={styles.featureCard}>
              <Text style={styles.featureEmoji}>📅</Text>
              <Text style={styles.featureTitle}>Schedule Import</Text>
              <Text style={styles.featureDescription}>
                Import your calendar to find the perfect time for dates
              </Text>
            </View>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureEmoji}>🤖</Text>
              <Text style={styles.featureTitle}>AI Date Suggestions</Text>
              <Text style={styles.featureDescription}>
                Get personalized date ideas based on your interests and location
              </Text>
            </View>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureEmoji}>📍</Text>
              <Text style={styles.featureTitle}>Location-Based Planning</Text>
              <Text style={styles.featureDescription}>
                Discover amazing places and activities near you
              </Text>
            </View>
          </View>
        </ScrollView>
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
  scrollView: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 30,
    alignItems: 'center',
  },
  appTitle: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  appSubtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  unlinkedContainer: {
    marginHorizontal: 24,
    marginBottom: 30,
  },
  unlinkedHeader: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 20,
    padding: 24,
    marginBottom: 20,
    alignItems: 'center',
  },
  unlinkedTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  unlinkedSubtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
    opacity: 0.9,
    lineHeight: 22,
  },
  linkFormContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 20,
    padding: 24,
    marginHorizontal: 24,
    marginBottom: 30,
  },
  formTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 8,
  },
  formSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    textAlign: 'center',
    opacity: 0.9,
    marginBottom: 24,
    lineHeight: 20,
  },
  nameInput: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    marginBottom: 20,
    color: '#333',
  },
  formButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  cancelButton: {
    flex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 12,
    paddingVertical: 14,
    marginRight: 8,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  linkButton: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingVertical: 14,
    marginLeft: 8,
    alignItems: 'center',
  },
  linkButtonDisabled: {
    opacity: 0.5,
  },
  linkButtonText: {
    color: '#667eea',
    fontSize: 16,
    fontWeight: 'bold',
  },
  linkedContainer: {
    marginHorizontal: 24,
    marginBottom: 30,
  },
  linkedHeader: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 20,
    padding: 24,
    marginBottom: 20,
    alignItems: 'center',
  },
  linkedTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  linkedSubtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  statusCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
  },
  statusTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  statusDescription: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    lineHeight: 20,
    marginBottom: 16,
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#4CAF50',
    marginRight: 8,
  },
  statusText: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  unlinkButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: 'center',
  },
  unlinkButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  featuresContainer: {
    marginHorizontal: 24,
    marginBottom: 30,
  },
  featuresTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 20,
    textAlign: 'center',
  },
  featureCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureEmoji: {
    fontSize: 32,
    marginRight: 16,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
    flex: 1,
  },
  featureDescription: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.8,
    flex: 1,
    lineHeight: 18,
  },
});

export default HomeScreen;
