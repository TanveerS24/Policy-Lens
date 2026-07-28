import React, { useEffect } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Text, IconButton, Divider, Badge } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../../redux/store';
import {
  fetchNotifications,
  markAsRead,
  markAllAsRead,
  Notification,
} from '../../redux/slices/notificationsSlice';
import { useTheme } from '../../contexts/ThemeContext';
import { formatDistanceToNow } from '../../utils/dateUtils';

export const NotificationsScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation();
  const { colors } = useTheme();
  const { notifications, unreadCount, isLoading } = useSelector(
    (state: RootState) => state.notifications
  );

  const styles = createStyles(colors);

  useEffect(() => {
    loadNotifications();
    const interval = setInterval(() => {
      loadNotifications();
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const loadNotifications = async () => {
    await dispatch(fetchNotifications({}));
  };

  const handleMarkAsRead = async (id: number) => {
    await dispatch(markAsRead(id));
  };

  const handleMarkAllAsRead = async () => {
    await dispatch(markAllAsRead());
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'SCHEME_UPDATE':
        return 'file-document';
      case 'ELIGIBILITY_UPDATE':
        return 'check-circle';
      case 'ADMIN_BROADCAST':
        return 'bullhorn';
      case 'DOCUMENT_PROCESSED':
        return 'file-check';
      default:
        return 'bell';
    }
  };

  const renderNotificationItem = ({ item }: { item: Notification }) => (
    <TouchableOpacity
      style={[
        styles.notificationItem,
        { backgroundColor: item.is_read ? colors.cardBg : `${colors.primary}10` },
      ]}
      onPress={() => !item.is_read && handleMarkAsRead(item.id)}
    >
      <View style={styles.notificationContent}>
        <View style={styles.iconContainer}>
          <IconButton
            icon={getNotificationIcon(item.notification_type)}
            size={24}
            iconColor={item.is_read ? colors.textSecondary : colors.primary}
          />
        </View>
        <View style={styles.textContainer}>
          <Text
            variant="titleSmall"
            style={[
              styles.title,
              { color: colors.textPrimary },
              !item.is_read && styles.unreadTitle,
            ]}
          >
            {item.title}
          </Text>
          <Text
            variant="bodySmall"
            style={[styles.message, { color: colors.textSecondary }]}
            numberOfLines={2}
          >
            {item.message}
          </Text>
          <Text
            variant="bodySmall"
            style={[styles.timestamp, { color: colors.textMuted }]}
          >
            {formatDistanceToNow(item.created_at)}
          </Text>
        </View>
        {!item.is_read && (
          <View style={[styles.unreadDot, { backgroundColor: colors.primary }]} />
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <IconButton
          icon="arrow-left"
          size={24}
          iconColor={colors.textPrimary}
          onPress={() => navigation.goBack()}
        />
        <Text variant="titleLarge" style={[styles.headerTitle, { color: colors.textPrimary }]}>
          Notifications
        </Text>
        {unreadCount > 0 && (
          <TouchableOpacity onPress={handleMarkAllAsRead}>
            <Text style={[styles.markAllText, { color: colors.primary }]}>
              Mark all read
            </Text>
          </TouchableOpacity>
        )}
      </View>

      <FlatList
        data={notifications}
        renderItem={renderNotificationItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={isLoading}
            onRefresh={loadNotifications}
            tintColor={colors.primary}
          />
        }
        ItemSeparatorComponent={() => <Divider style={styles.divider} />}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <IconButton icon="bell-off" size={64} iconColor={colors.textMuted} />
            <Text variant="titleMedium" style={[styles.emptyTitle, { color: colors.textSecondary }]}>
              No notifications
            </Text>
            <Text variant="bodyMedium" style={[styles.emptySubtitle, { color: colors.textMuted }]}>
              You don't have any notifications yet
            </Text>
          </View>
        }
      />
    </SafeAreaView>
  );
};

const createStyles = (colors: any) =>
  StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: colors.background,
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingHorizontal: 8,
      paddingVertical: 8,
      borderBottomWidth: 1,
      borderBottomColor: colors.border,
    },
    headerTitle: {
      flex: 1,
      fontWeight: 'bold',
    },
    markAllText: {
      fontSize: 14,
      fontWeight: '600',
      marginRight: 8,
    },
    listContent: {
      padding: 16,
    },
    notificationItem: {
      borderRadius: 12,
      marginBottom: 8,
      padding: 12,
    },
    notificationContent: {
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    iconContainer: {
      marginRight: 8,
    },
    textContainer: {
      flex: 1,
    },
    title: {
      fontWeight: '600',
      marginBottom: 4,
    },
    unreadTitle: {
      fontWeight: 'bold',
    },
    message: {
      marginBottom: 4,
    },
    timestamp: {
      fontSize: 12,
    },
    unreadDot: {
      width: 8,
      height: 8,
      borderRadius: 4,
      marginLeft: 8,
      marginTop: 8,
    },
    divider: {
      backgroundColor: colors.border,
      height: 1,
    },
    emptyContainer: {
      alignItems: 'center',
      justifyContent: 'center',
      paddingTop: 64,
    },
    emptyTitle: {
      marginTop: 16,
      fontWeight: '600',
    },
    emptySubtitle: {
      marginTop: 8,
      textAlign: 'center',
    },
  });
