import React, { useEffect } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl, TouchableOpacity, Image } from 'react-native';
import { Text, Card, Avatar, Chip, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import { RootState, AppDispatch } from '../redux/store';
import { fetchSchemes, Scheme } from '../redux/slices/schemesSlice';
import { fetchBookmarks } from '../redux/slices/schemesSlice';
import { fetchNotifications } from '../redux/slices/notificationsSlice';
import { useTheme } from '../contexts/ThemeContext';
import { AppLogo } from '../components/AppLogo';

export const HomeScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation();
  const { user } = useSelector((state: RootState) => state.auth);
  const { schemes, isLoading } = useSelector((state: RootState) => state.schemes);
  const { bookmarks } = useSelector((state: RootState) => state.schemes);
  const { unreadCount } = useSelector((state: RootState) => state.notifications);
  const { colors, isDark } = useTheme();
  const styles = createStyles(colors);
  const [refreshing, setRefreshing] = React.useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    await Promise.all([
      dispatch(fetchSchemes({ page: 1, per_page: 5 })),
      dispatch(fetchBookmarks()),
      dispatch(fetchNotifications({})),
    ]);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const renderQuickActions = () => (
    <View style={styles.quickActions}>
      <TouchableOpacity
        style={[styles.actionCard, { backgroundColor: colors.cardBg }]}
        onPress={() => navigation.navigate('Schemes' as never)}
      >
        <View style={styles.actionContent}>
          <View style={[styles.actionIcon, { backgroundColor: `${colors.primary}20` }]}>
            <Image source={require('../../assets/Search icon.png')} style={styles.actionIconImage} resizeMode="contain" />
          </View>
          <Text style={styles.actionText}>Browse Schemes</Text>
        </View>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.actionCard, { backgroundColor: colors.cardBg }]}
        onPress={() => navigation.navigate('Documents' as never)}
      >
        <View style={styles.actionContent}>
          <View style={[styles.actionIcon, { backgroundColor: `${colors.primary}20` }]}>
            <Image source={require('../../assets/icons8-document-128.png')} style={styles.actionIconImage} resizeMode="contain" />
          </View>
          <Text style={styles.actionText}>Upload Policy</Text>
        </View>
      </TouchableOpacity>
    </View>
  );

  const renderFeaturedSchemes = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Featured Schemes</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Schemes' as never)}>
          <Text style={styles.viewAll}>View All</Text>
        </TouchableOpacity>
      </View>

      {isLoading ? (
        <ActivityIndicator style={styles.loader} color={colors.primary} />
      ) : (
        schemes.slice(0, 3).map((scheme: Scheme) => (
          <TouchableOpacity key={scheme.id} style={styles.schemeCard}>
            <View style={styles.schemeHeader}>
              <View style={styles.schemeInfo}>
                <Text style={styles.schemeName}>{scheme.name}</Text>
                <Text style={styles.ministryText}>
                  {scheme.ministry || scheme.type}
                </Text>
              </View>
              <View style={[styles.typeBadge, { backgroundColor: `${colors.primary}20` }]}>
                <Text style={[styles.typeText, { color: colors.primary }]}>
                  {scheme.type}
                </Text>
              </View>
            </View>

            <Text style={styles.description} numberOfLines={2}>
              {scheme.short_description || scheme.description}
            </Text>

            {scheme.coverage_amount && (
              <Text style={[styles.coverage, { color: colors.primary }]}>
                Coverage: ₹{scheme.coverage_amount.toLocaleString()}
              </Text>
            )}

            <View style={styles.cardActions}>
              <TouchableOpacity style={styles.secondaryButton}>
                <Text style={[styles.secondaryButtonText, { color: colors.textSecondary }]}>
                  Check Eligibility
                </Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.primaryButton, { backgroundColor: colors.primary }]}>
                <Text style={styles.primaryButtonText}>View Details</Text>
              </TouchableOpacity>
            </View>
          </TouchableOpacity>
        ))
      )}
    </View>
  );

  const renderBookmarkedSchemes = () => {
    if (bookmarks.length === 0) return null;

    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Your Bookmarks</Text>

        {bookmarks.slice(0, 2).map((scheme: Scheme) => (
          <TouchableOpacity key={scheme.id} style={styles.bookmarkCard}>
            <View style={styles.bookmarkContent}>
              <Text style={styles.schemeName}>{scheme.name}</Text>
              <Text style={styles.ministryText}>
                {scheme.ministry || scheme.type}
              </Text>
            </View>
            <Text style={[styles.bookmarkIcon, { color: colors.primary }]}>🔖</Text>
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.primary}
            colors={[colors.primary]}
          />
        }
      >
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <AppLogo size="small" showSparkle={false} />
            <View style={styles.headerText}>
              <Text style={styles.greeting}>
                Hello, {user?.name?.split(' ')[0] || 'User'}
              </Text>
              <Text style={styles.subtitle}>
                Find dental health schemes
              </Text>
            </View>
          </View>

          <TouchableOpacity 
            style={styles.notificationBadge}
            onPress={() => navigation.navigate('Notifications' as never)}
          >
            <View style={[styles.notificationIcon, { backgroundColor: colors.cardBg }]}>
              <Image 
                source={require('../../assets/icons8-notification-50.png')} 
                style={styles.notificationIconImage} 
                resizeMode="contain"
              />
            </View>
            {unreadCount > 0 && (
              <View style={[styles.badge, { backgroundColor: colors.primary }]}>
                <Text style={styles.badgeText}>{unreadCount}</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>

        {renderQuickActions()}
        {renderFeaturedSchemes()}
        {renderBookmarkedSchemes()}
      </ScrollView>
    </SafeAreaView>
  );
};

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 28,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  headerText: {
    justifyContent: 'center',
  },
  greeting: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  subtitle: {
    fontSize: 13,
    color: colors.textSecondary,
    marginTop: 2,
  },
  notificationBadge: {
    position: 'relative',
  },
  notificationIcon: {
    width: 48,
    height: 48,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  notificationIconImage: {
    width: 24,
    height: 24,
  },
  badge: {
    position: 'absolute',
    top: -4,
    right: -4,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badgeText: {
    color: colors.cardBg,
    fontSize: 11,
    fontWeight: 'bold',
  },
  quickActions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 28,
  },
  actionCard: {
    flex: 1,
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
    borderColor: colors.border,
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 4,
  },
  actionContent: {
    alignItems: 'center',
    gap: 10,
  },
  actionIcon: {
    width: 48,
    height: 48,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionIconText: {
    fontSize: 24,
  },
  actionIconImage: {
    width: 28,
    height: 28,
  },
  actionText: {
    fontSize: 13,
    fontWeight: '600',
    color: colors.textPrimary,
    textAlign: 'center',
  },
  section: {
    marginBottom: 28,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  viewAll: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.primary,
  },
  loader: {
    marginVertical: 24,
  },
  schemeCard: {
    backgroundColor: colors.cardBg,
    borderRadius: 20,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: colors.border,
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 4,
  },
  schemeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  schemeInfo: {
    flex: 1,
    marginRight: 8,
  },
  schemeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 4,
  },
  typeBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  typeText: {
    fontSize: 11,
    fontWeight: '600',
  },
  ministryText: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  description: {
    fontSize: 14,
    color: colors.textSecondary,
    lineHeight: 20,
    marginBottom: 12,
  },
  coverage: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 16,
  },
  cardActions: {
    flexDirection: 'row',
    gap: 8,
  },
  secondaryButton: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 12,
    backgroundColor: colors.inputBg,
    alignItems: 'center',
  },
  secondaryButtonText: {
    fontSize: 13,
    fontWeight: '600',
  },
  primaryButton: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: colors.cardBg,
  },
  bookmarkCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.cardBg,
    borderRadius: 16,
    padding: 16,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: colors.border,
  },
  bookmarkContent: {
    flex: 1,
  },
  bookmarkIcon: {
    fontSize: 20,
  },
});
