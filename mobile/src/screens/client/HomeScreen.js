import React, { useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPolicies } from '../../store/policiesSlice';
import { Card, Loading, EmptyState, Badge } from '../../components/ui';
import { COLORS } from '../../config/api';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const HomeScreen = ({ navigation }) => {
  const dispatch = useDispatch();
  const { list: policies, loading } = useSelector((state) => state.policies);
  const [refreshing, setRefreshing] = React.useState(false);

  useEffect(() => {
    loadPolicies();
  }, []);

  const loadPolicies = async () => {
    await dispatch(fetchPolicies({ limit: 10 }));
  };

  const onRefresh = React.useCallback(async () => {
    setRefreshing(true);
    await loadPolicies();
    setRefreshing(false);
  }, []);

  const renderPolicyCard = ({ item }) => (
    <TouchableOpacity
      onPress={() => navigation.navigate('PolicyDetails', { policyId: item._id })}
      activeOpacity={0.7}
    >
      <Card style={styles.policyCard}>
        <View style={styles.cardHeader}>
          <Text style={styles.policyTitle} numberOfLines={2}>
            {item.title}
          </Text>
          <Badge label="Category" value={item.category} />
        </View>
        <Text style={styles.policyDescription} numberOfLines={3}>
          {item.short_description}
        </Text>
        <View style={styles.cardFooter}>
          {item.state && <Badge label="State" value={item.state} />}
          <View style={styles.spacer} />
          <Icon name="chevron-right" size={24} color={COLORS.primary} />
        </View>
      </Card>
    </TouchableOpacity>
  );

  if (loading && !policies.length) return <Loading />;

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.headerSection}>
        <Text style={styles.sectionTitle}>Welcome</Text>
        <Text style={styles.sectionSubtitle}>
          Discover healthcare policies suited for you
        </Text>
      </View>

      <View style={styles.statsContainer}>
        <Card style={styles.statCard}>
          <Icon name="file-document-multiple" size={32} color={COLORS.primary} />
          <Text style={styles.statNumber}>{policies.length}</Text>
          <Text style={styles.statLabel}>Policies Available</Text>
        </Card>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Latest Policies</Text>
          <TouchableOpacity
            onPress={() => navigation.navigate('Policies')}
          >
            <Text style={styles.viewAllLink}>View All</Text>
          </TouchableOpacity>
        </View>

        {policies.length === 0 ? (
          <EmptyState message="No policies available" />
        ) : (
          <FlatList
            data={policies.slice(0, 5)}
            renderItem={renderPolicyCard}
            keyExtractor={(item) => item._id}
            scrollEnabled={false}
          />
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Upload')}
        >
          <Icon name="cloud-upload" size={32} color={COLORS.primary} />
          <Text style={styles.actionButtonText}>Upload Policy</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  headerSection: {
    padding: 16,
    backgroundColor: COLORS.primary,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  sectionSubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 16,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.primary,
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  section: {
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  viewAllLink: {
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600',
  },
  policyCard: {
    marginBottom: 12,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  policyTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  policyDescription: {
    fontSize: 13,
    color: COLORS.textSecondary,
    lineHeight: 18,
    marginBottom: 8,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  spacer: {
    flex: 1,
  },
  actionButton: {
    backgroundColor: COLORS.card,
    borderWidth: 2,
    borderColor: COLORS.primary,
    borderRadius: 12,
    padding: 24,
    alignItems: 'center',
    marginTop: 8,
  },
  actionButtonText: {
    color: COLORS.primary,
    fontSize: 16,
    fontWeight: '600',
    marginTop: 8,
  },
});

export default HomeScreen;
