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
import { RootState } from '../../redux/store';
import { logout } from '../../redux/slices/authSlice';
import { theme } from '../../theme';

export const ProfileScreen: React.FC = () => {
  const dispatch = useDispatch();
  const navigation = useNavigation();
  const { user } = useSelector((state: RootState) => state.auth);
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
            color={theme.colors.primary}
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

        <Card style={styles.infoCard}>
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

        <List.Section>
          <List.Subheader>Settings</List.Subheader>
          {menuItems.slice(0, 5).map((item, index) => (
            <List.Item
              key={index}
              title={item.title}
              left={(props) => <List.Icon {...props} icon={item.icon} />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={item.onPress}
            />
          ))}
        </List.Section>

        <List.Section>
          <List.Subheader>Legal & Support</List.Subheader>
          {menuItems.slice(5).map((item, index) => (
            <List.Item
              key={index}
              title={item.title}
              left={(props) => <List.Icon {...props} icon={item.icon} />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={item.onPress}
            />
          ))}
        </List.Section>

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
            textColor={theme.colors.error}
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
            <Button onPress={confirmDelete} textColor={theme.colors.error}>
              Delete
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  scrollContent: {
    paddingBottom: 24,
  },
  header: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.outlineVariant,
  },
  avatar: {
    backgroundColor: theme.colors.primaryContainer,
    marginBottom: 16,
  },
  name: {
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  mobile: {
    color: theme.colors.onSurfaceVariant,
    marginTop: 4,
  },
  email: {
    color: theme.colors.onSurfaceVariant,
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
    color: theme.colors.onSurfaceVariant,
  },
  activeStatus: {
    color: theme.colors.success,
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
    borderColor: theme.colors.outline,
  },
  deleteButton: {
    marginTop: 8,
  },
  version: {
    textAlign: 'center',
    color: theme.colors.onSurfaceVariant,
    marginTop: 16,
  },
  confirmInput: {
    marginTop: 12,
  },
});
