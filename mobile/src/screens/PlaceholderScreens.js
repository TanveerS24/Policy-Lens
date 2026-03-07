// Placeholder screens for mobile app
// These files provide the structure and can be filled with detailed implementation

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../../config/api';

const PlaceholderScreen = ({ screenName }) => (
  <View style={styles.container}>
    <Text style={styles.text}>{screenName}</Text>
  </View>
);

export const PoliciesScreen = () => <PlaceholderScreen screenName="Policies Screen" />;
export const PolicyDetailsScreen = () => <PlaceholderScreen screenName="Policy Details Screen" />;
export const UploadScreen = () => <PlaceholderScreen screenName="Upload Screen" />;
export const MyUploadsScreen = () => <PlaceholderScreen screenName="My Uploads Screen" />;
export const ProfileScreen = () => <PlaceholderScreen screenName="Profile Screen" />;
export const AdminDashboardScreen = () => <PlaceholderScreen screenName="Admin Dashboard Screen" />;
export const AdminPoliciesScreen = () => <PlaceholderScreen screenName="Admin Policies Screen" />;
export const AdminUploadsScreen = () => <PlaceholderScreen screenName="Admin Uploads Screen" />;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  text: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.primary,
  },
});
