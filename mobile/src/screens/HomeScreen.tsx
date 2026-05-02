import React, { useEffect } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Text, Card, Button, Avatar, Chip, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import { RootState, AppDispatch } from '../redux/store';
import { fetchSchemes, Scheme } from '../redux/slices/schemesSlice';
import { fetchBookmarks } from '../redux/slices/schemesSlice';
import { fetchNotifications } from '../redux/slices/notificationsSlice';
import { theme, colors } from '../theme';

export const HomeScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation();
  const { user } = useSelector((state: RootState) => state.auth);
  const { schemes, isLoading } = useSelector((state: RootState) => state.schemes);
  const { bookmarks } = useSelector((state: RootState) => state.schemes);
  const { unreadCount } = useSelector((state: RootState) => state.notifications);
  const [refreshing, setRefreshing] = React.useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    await Promise.all([
      dispatch(fetchSchemes({ page: 1, per_page: 5 })),
      dispatch(fetchBookmarks()),
      dispatch(fetchNotifications()),
    ]);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const renderQuickActions = () => (
    <View style={styles.quickActions}>
      <Card style={styles.actionCard} onPress={() => navigation.navigate('Schemes' as never)}>
        <Card.Content style={styles.actionContent}>
          <Avatar.Icon size={40} icon="tooth" style={{ backgroundColor: theme.colors.primaryContainer }} />
          <Text variant="bodyMedium" style={styles.actionText}>Browse Schemes</Text>
        </Card.Content>
      </Card>
      
      <Card style={styles.actionCard} onPress={() => navigation.navigate('Documents' as never)}>
        <Card.Content style={styles.actionContent}>
          <Avatar.Icon size={40} icon="file-upload" style={{ backgroundColor: theme.colors.secondaryContainer }} />
          <Text variant="bodyMedium" style={styles.actionText}>Upload Policy</Text>
        </Card.Content>
      </Card>
    </View>
  );

  const renderFeaturedSchemes = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text variant="titleLarge" style={styles.sectionTitle}>Featured Schemes</Text>
        <Button mode="text" onPress={() => navigation.navigate('Schemes' as never)}>
          View All
        </Button>
      </View>

      {isLoading ? (
        <ActivityIndicator style={styles.loader} />
      ) : (
        schemes.slice(0, 3).map((scheme: Scheme) => (
          <Card key={scheme.id} style={styles.schemeCard}>
            <Card.Content>
              <View style={styles.schemeHeader}>
                <View>
                  <Text variant="titleMedium">{scheme.name}</Text>
                  <Text variant="bodySmall" style={styles.ministryText}>
                    {scheme.ministry || scheme.type}
                  </Text>
                </View>
                <Chip compact>{scheme.type}</Chip>
              </View>
              
              <Text variant="bodyMedium" style={styles.description} numberOfLines={2}>
                {scheme.short_description || scheme.description}
              </Text>

              {scheme.coverage_amount && (
                <Text variant="bodySmall" style={styles.coverage}>
                  Coverage: ₹{scheme.coverage_amount.toLocaleString()}
                </Text>
              )}
            </Card.Content>
            <Card.Actions>
              <Button onPress={() => {}}>Check Eligibility</Button>
              <Button mode="contained">View Details</Button>
            </Card.Actions>
          </Card>
        ))
      )}
    </View>
  );

  const renderBookmarkedSchemes = () => {
    if (bookmarks.length === 0) return null;

    return (
      <View style={styles.section}>
        <Text variant="titleLarge" style={styles.sectionTitle}>Your Bookmarks</Text>
        
        {bookmarks.slice(0, 2).map((scheme: Scheme) => (
          <Card key={scheme.id} style={styles.schemeCard}>
            <Card.Content>
              <Text variant="titleMedium">{scheme.name}</Text>
              <Text variant="bodySmall" style={styles.ministryText}>
                {scheme.ministry || scheme.type}
              </Text>
            </Card.Content>
          </Card>
        ))}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <View style={styles.header}>
          <View>
            <Text variant="headlineSmall" style={styles.greeting}>
              Hello, {user?.name?.split(' ')[0] || 'User'}
            </Text>
            <Text variant="bodyMedium" style={styles.subtitle}>
              Find dental health schemes available for you
            </Text>
          </View>
          
          <View style={styles.notificationBadge}>
            <Avatar.Icon size={40} icon="bell" style={{ backgroundColor: theme.colors.surfaceVariant }} />
            {unreadCount > 0 && (
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{unreadCount}</Text>
              </View>
            )}
          </View>
        </View>

        {renderQuickActions()}
        {renderFeaturedSchemes()}
        {renderBookmarkedSchemes()}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  scrollContent: {
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  greeting: {
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  subtitle: {
    color: theme.colors.onSurfaceVariant,
    marginTop: 4,
  },
  notificationBadge: {
    position: 'relative',
  },
  badge: {
    position: 'absolute',
    top: -4,
    right: -4,
    backgroundColor: theme.colors.error,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badgeText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  quickActions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  actionCard: {
    flex: 1,
    elevation: 2,
  },
  actionContent: {
    alignItems: 'center',
    gap: 8,
  },
  actionText: {
    textAlign: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  loader: {
    marginVertical: 24,
  },
  schemeCard: {
    marginBottom: 12,
    elevation: 1,
  },
  schemeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  ministryText: {
    color: theme.colors.onSurfaceVariant,
  },
  description: {
    marginTop: 8,
    color: theme.colors.onSurface,
  },
  coverage: {
    marginTop: 8,
    color: theme.colors.primary,
    fontWeight: '600',
  },
});
