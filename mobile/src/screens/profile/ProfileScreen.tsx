import React from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { 
  Text, 
  Card, 
  Button, 
  Avatar, 
  List,
  Divider,
  Dialog,
  Portal,
  TextInput,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import { RootState, AppDispatch } from '../../redux/store';
import { logout } from '../../redux/slices/authSlice';
import { useTheme } from '../../contexts/ThemeContext';

export const ProfileScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation();
  const { user } = useSelector((state: RootState) => state.auth);
  const { theme: currentTheme, setTheme, isDark, colors } = useTheme();
  const styles = createStyles(colors);
  const [logoutDialogVisible, setLogoutDialogVisible] = React.useState(false);
  const [deleteDialogVisible, setDeleteDialogVisible] = React.useState(false);

  const handleLogout = () => {
    setLogoutDialogVisible(true);
  };

  const confirmLogout = async () => {
    setLogoutDialogVisible(false);
    await dispatch(logout());
  };

  const handleDeleteAccount = () => {
    setDeleteDialogVisible(true);
  };

  const confirmDelete = () => {
    setDeleteDialogVisible(false);
    // TODO: Implement account deletion
    Alert.alert('Info', 'Account deletion request has been submitted.');
  };

  const menuItems = [
    {
      icon: 'account-edit',
      title: 'Edit Profile',
      onPress: () => {},
    },
    {
      icon: 'bookmark-outline',
      title: 'My Bookmarks',
      onPress: () => navigation.navigate('Schemes' as never),
    },
    {
      icon: 'file-document-outline',
      title: 'My Documents',
      onPress: () => navigation.navigate('Documents' as never),
    },
    {
      icon: 'bell-outline',
      title: 'Notifications',
      onPress: () => {},
    },
    {
      icon: 'lock-outline',
      title: 'Change Password',
      onPress: () => {},
    },
  ];

  const legalItems = [
    {
      icon: 'download-outline',
      title: 'Download My Data',
      onPress: () => {},
    },
    {
      icon: 'shield-check-outline',
      title: 'Privacy Policy',
      onPress: () => {},
    },
    {
      icon: 'file-document-outline',
      title: 'Terms of Service',
      onPress: () => {},
    },
    {
      icon: 'help-circle-outline',
      title: 'Help & Support',
      onPress: () => {},
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Avatar.Icon 
            size={80} 
            icon="account" 
            style={styles.avatar}
            color={colors.primary}
          />
          <Text variant="headlineSmall" style={styles.name}>
            {user?.name || 'User'}
          </Text>
          <Text variant="bodyMedium" style={styles.mobile}>
            {user?.mobile || ''}
          </Text>
          {user?.email && (
            <Text variant="bodySmall" style={styles.email}>
              {user.email}
            </Text>
          )}
        </View>

        <Card style={[styles.infoCard, { backgroundColor: colors.cardBg }]}>
          <Card.Content>
            <View style={styles.infoRow}>
              <Text variant="bodyMedium" style={styles.infoLabel}>Member Since</Text>
              <Text variant="bodyMedium">{new Date().toLocaleDateString('en-IN')}</Text>
            </View>
            <Divider style={styles.divider} />
            <View style={styles.infoRow}>
              <Text variant="bodyMedium" style={styles.infoLabel}>Account Status</Text>
              <Text variant="bodyMedium" style={styles.activeStatus}>Active</Text>
            </View>
          </Card.Content>
        </Card>

        <Card style={[styles.themeCard, { backgroundColor: colors.cardBg }]}>
          <Card.Content>
            <Text variant="titleMedium" style={[styles.themeTitle, { color: colors.textPrimary }]}>
              Appearance
            </Text>
            <Text variant="bodySmall" style={[styles.themeSubtitle, { color: colors.textSecondary }]}>
              Choose your preferred theme
            </Text>
            
            <View style={styles.themeOptions}>
              <Card
                style={[
                  styles.themeOption,
                  currentTheme === 'light' && styles.themeOptionActive,
                  { borderColor: currentTheme === 'light' ? colors.primary : colors.border }
                ]}
                onPress={() => setTheme('light')}
              >
                <Card.Content style={styles.themeOptionContent}>
                  <View style={[styles.themePreview, { backgroundColor: '#F8F9FA' }]}>
                    <View style={[styles.themePreviewDot, { backgroundColor: '#4A90E2' }]} />
                    <View style={[styles.themePreviewDot, { backgroundColor: '#F4A261' }]} />
                  </View>
                  <Text style={[styles.themeOptionText, { color: colors.textPrimary }]}>Light</Text>
                  <Text style={[styles.themeOptionSubtext, { color: colors.textMuted }]}>Silver & Peach Blue</Text>
                  {currentTheme === 'light' && (
                    <View style={[styles.checkmark, { backgroundColor: colors.primary }]}>
                      <Text style={styles.checkmarkText}>✓</Text>
                    </View>
                  )}
                </Card.Content>
              </Card>

              <Card
                style={[
                  styles.themeOption,
                  currentTheme === 'dark' && styles.themeOptionActive,
                  { borderColor: currentTheme === 'dark' ? colors.primary : colors.border }
                ]}
                onPress={() => setTheme('dark')}
              >
                <Card.Content style={styles.themeOptionContent}>
                  <View style={[styles.themePreview, { backgroundColor: '#272822' }]}>
                    <View style={[styles.themePreviewDot, { backgroundColor: '#66D9EF' }]} />
                    <View style={[styles.themePreviewDot, { backgroundColor: '#FD971F' }]} />
                  </View>
                  <Text style={[styles.themeOptionText, { color: colors.textPrimary }]}>Dark</Text>
                  <Text style={[styles.themeOptionSubtext, { color: colors.textMuted }]}>Monokai Theme</Text>
                  {currentTheme === 'dark' && (
                    <View style={[styles.checkmark, { backgroundColor: colors.primary }]}>
                      <Text style={styles.checkmarkText}>✓</Text>
                    </View>
                  )}
                </Card.Content>
              </Card>
            </View>
          </Card.Content>
        </Card>

        <View style={[styles.listSection, { backgroundColor: colors.cardBg }]}>
          <List.Section>
            <List.Subheader style={{ color: colors.textPrimary }}>Settings</List.Subheader>
            {menuItems.map((item, index) => (
              <List.Item
                key={index}
                title={item.title}
                titleStyle={{ color: colors.textPrimary }}
                left={(props) => <List.Icon {...props} icon={item.icon} color={colors.textSecondary} />}
                right={(props) => <List.Icon {...props} icon="chevron-right" color={colors.textMuted} />}
                onPress={item.onPress}
              />
            ))}
          </List.Section>
        </View>

        <View style={[styles.listSection, { backgroundColor: colors.cardBg }]}>
          <List.Section>
            <List.Subheader style={{ color: colors.textPrimary }}>Legal & Support</List.Subheader>
            {legalItems.map((item, index) => (
              <List.Item
                key={index}
                title={item.title}
                titleStyle={{ color: colors.textPrimary }}
                left={(props) => <List.Icon {...props} icon={item.icon} color={colors.textSecondary} />}
                right={(props) => <List.Icon {...props} icon="chevron-right" color={colors.textMuted} />}
                onPress={item.onPress}
              />
            ))}
          </List.Section>
        </View>

        <View style={styles.actionButtons}>
          <Button 
            mode="outlined" 
            onPress={handleLogout}
            style={styles.logoutButton}
            icon="logout"
          >
            Log Out
          </Button>

          <Button 
            mode="text" 
            onPress={handleDeleteAccount}
            textColor={colors.error}
            style={styles.deleteButton}
            icon="delete-forever"
          >
            Delete Account
          </Button>
        </View>

        <Text variant="bodySmall" style={styles.version}>
          Version 1.0.0
        </Text>
      </ScrollView>

      <Portal>
        <Dialog visible={logoutDialogVisible} onDismiss={() => setLogoutDialogVisible(false)}>
          <Dialog.Title>Log Out</Dialog.Title>
          <Dialog.Content>
            <Text variant="bodyMedium">Are you sure you want to log out?</Text>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setLogoutDialogVisible(false)}>Cancel</Button>
            <Button onPress={confirmLogout}>Log Out</Button>
          </Dialog.Actions>
        </Dialog>

        <Dialog visible={deleteDialogVisible} onDismiss={() => setDeleteDialogVisible(false)}>
          <Dialog.Title>Delete Account</Dialog.Title>
          <Dialog.Content>
            <Text variant="bodyMedium">
              This action cannot be undone. All your data will be permanently deleted.
            </Text>
            <TextInput
              label="Type DELETE to confirm"
              style={styles.confirmInput}
            />
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setDeleteDialogVisible(false)}>Cancel</Button>
            <Button onPress={confirmDelete} textColor={colors.error}>
              Delete
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </SafeAreaView>
  );
};

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    paddingBottom: 24,
  },
  header: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  avatar: {
    backgroundColor: colors.secondary,
    marginBottom: 16,
  },
  name: {
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  mobile: {
    color: colors.textSecondary,
    marginTop: 4,
  },
  email: {
    color: colors.textSecondary,
    marginTop: 2,
  },
  infoCard: {
    margin: 16,
    elevation: 1,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  infoLabel: {
    color: colors.textSecondary,
  },
  activeStatus: {
    color: colors.success,
    fontWeight: '600',
  },
  divider: {
    marginVertical: 8,
  },
  actionButtons: {
    padding: 16,
    gap: 12,
  },
  logoutButton: {
    borderColor: colors.border,
  },
  deleteButton: {
    marginTop: 8,
  },
  version: {
    textAlign: 'center',
    color: colors.textSecondary,
    marginTop: 16,
  },
  confirmInput: {
    marginTop: 12,
  },
  listSection: {
    margin: 16,
    marginTop: 8,
    borderRadius: 12,
    overflow: 'hidden',
  },
  themeCard: {
    margin: 16,
    marginTop: 8,
    elevation: 1,
  },
  themeTitle: {
    fontWeight: 'bold',
  },
  themeSubtitle: {
    marginTop: 4,
    marginBottom: 16,
  },
  themeOptions: {
    flexDirection: 'row',
    gap: 12,
  },
  themeOption: {
    flex: 1,
    borderWidth: 2,
    borderRadius: 12,
  },
  themeOptionActive: {
    borderWidth: 2,
  },
  themeOptionContent: {
    alignItems: 'center',
    padding: 12,
  },
  themePreview: {
    width: 48,
    height: 48,
    borderRadius: 24,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 4,
    marginBottom: 8,
  },
  themePreviewDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  themeOptionText: {
    fontSize: 14,
    fontWeight: '600',
  },
  themeOptionSubtext: {
    fontSize: 11,
    marginTop: 2,
  },
  checkmark: {
    position: 'absolute',
    top: 8,
    right: 8,
    width: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmarkText: {
    color: colors.cardBg,
    fontSize: 12,
    fontWeight: 'bold',
  },
});
