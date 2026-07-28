import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, TouchableOpacity } from 'react-native';
import { 
  Text, 
  Card, 
  Button, 
  Searchbar, 
  Chip, 
  ActivityIndicator,
  IconButton,
  Menu,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../../redux/store';
import { 
  fetchSchemes, 
  Scheme, 
  bookmarkScheme, 
  removeBookmark,
} from '../../redux/slices/schemesSlice';
import { useTheme } from '../../contexts/ThemeContext';
import { EligibilityCheckModal } from '../../components/EligibilityCheckModal';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';

const SCHEME_TYPES = ['All', 'National', 'State', 'Central', 'NGO'];
const CATEGORIES = ['All', 'BPL', 'Women', 'Senior Citizens', 'Children', 'Disabled'];

export const SchemesScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { colors } = useTheme();
  const styles = createStyles(colors);
  const navigation = useNavigation<StackNavigationProp<RootStackParamList>>();
  const { schemes, isLoading, pagination } = useSelector((state: RootState) => state.schemes);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [showTypeMenu, setShowTypeMenu] = useState(false);
  const [showCategoryMenu, setShowCategoryMenu] = useState(false);
  const [eligibilityModalVisible, setEligibilityModalVisible] = useState(false);
  const [selectedScheme, setSelectedScheme] = useState<Scheme | null>(null);

  const loadSchemes = useCallback(async (pageNum: number = 1) => {
    const params: any = { page: pageNum };
    if (searchQuery) params.search = searchQuery;
    if (selectedType !== 'All') params.type = selectedType.toLowerCase();
    if (selectedCategory !== 'All') params.category = selectedCategory;
    
    await dispatch(fetchSchemes(params));
  }, [dispatch, searchQuery, selectedType, selectedCategory]);

  useEffect(() => {
    loadSchemes(1);
    const interval = setInterval(() => {
      loadSchemes(1);
    }, 10000);
    return () => clearInterval(interval);
  }, [loadSchemes]);

  const onRefresh = async () => {
    setRefreshing(true);
    setPage(1);
    await loadSchemes(1);
    setRefreshing(false);
  };

  const loadMore = async () => {
    if (page < pagination.totalPages && !isLoading) {
      const nextPage = page + 1;
      setPage(nextPage);
      await loadSchemes(nextPage);
    }
  };

  const handleBookmark = async (scheme: Scheme) => {
    if (scheme.is_bookmarked) {
      await dispatch(removeBookmark(scheme.id));
    } else {
      await dispatch(bookmarkScheme(scheme.id));
    }
  };

  const renderSchemeCard = ({ item: scheme }: { item: Scheme }) => (
    <Card style={styles.card}>
      <Card.Content style={styles.cardContent}>
        <View style={styles.cardHeader}>
          <View style={styles.titleContainer}>
            <Text 
              variant="titleMedium" 
              numberOfLines={2}
              style={{ 
                color: colors.textPrimary,
                fontWeight: 'bold',
                lineHeight: 22,
              }}
            >
              {scheme.name}
            </Text>
            <Text 
              variant="bodySmall" 
              style={[styles.ministryText, { color: colors.textSecondary, marginTop: 2 }]}
            >
              {scheme.ministry || scheme.type}
            </Text>
          </View>
          <IconButton
            icon={scheme.is_bookmarked ? 'bookmark' : 'bookmark-outline'}
            size={22}
            iconColor={scheme.is_bookmarked ? colors.primary : colors.textSecondary}
            onPress={() => handleBookmark(scheme)}
            style={{ margin: 0 }}
          />
        </View>

        <View style={styles.chipsContainer}>
          <Chip 
            compact 
            style={styles.typeChip}
            textStyle={{ fontSize: 11, fontWeight: '600', color: colors.primary }}
          >
            {scheme.type}
          </Chip>
          {scheme.target_categories.slice(0, 2).map((cat) => (
            <Chip 
              key={cat} 
              compact 
              style={styles.categoryChip}
              textStyle={{ fontSize: 11, fontWeight: '500', color: colors.textSecondary }}
            >
              {cat}
            </Chip>
          ))}
        </View>

        <Text 
          variant="bodySmall" 
          numberOfLines={2} 
          style={[styles.description, { color: colors.textSecondary, lineHeight: 18, marginBottom: 8 }]}
        >
          {scheme.short_description || scheme.description}
        </Text>

        {scheme.coverage_amount && (
          <View style={styles.coverageStrip}>
            <Text style={styles.coverageLabel}>Coverage:</Text>
            <Text style={styles.coverageAmount}>
              ₹{scheme.coverage_amount.toLocaleString()}
            </Text>
          </View>
        )}

        <View style={styles.cardActionsRow}>
          <TouchableOpacity
            style={styles.secondaryCardButton}
            onPress={() => {
              setSelectedScheme(scheme);
              setEligibilityModalVisible(true);
            }}
            activeOpacity={0.7}
          >
            <Text style={[styles.secondaryCardButtonText, { color: colors.primary }]}>
              Check Eligibility
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.primaryCardButton, { backgroundColor: colors.primary }]}
            onPress={() => navigation.navigate('SchemeDetail', { schemeId: scheme.id })}
            activeOpacity={0.7}
          >
            <Text style={styles.primaryCardButtonText}>
              View Details
            </Text>
          </TouchableOpacity>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text variant="headlineSmall" style={[styles.title, { color: colors.textPrimary }]}>Dental Schemes</Text>
        
        <Searchbar
          placeholder="Search schemes..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchBar}
          onSubmitEditing={() => loadSchemes(1)}
          inputStyle={{ color: colors.textPrimary }}
          iconColor={colors.textSecondary}
          placeholderTextColor={colors.textSecondary}
        />

        <View style={styles.filtersContainer}>
          <Menu
            visible={showTypeMenu}
            onDismiss={() => setShowTypeMenu(false)}
            anchor={
              <Chip 
                compact
                onPress={() => setShowTypeMenu(true)}
                style={[styles.filterChip, { backgroundColor: selectedType !== 'All' ? `${colors.primary}20` : colors.inputBg }]}
                textStyle={{ color: selectedType !== 'All' ? colors.primary : colors.textPrimary, fontSize: 12, marginHorizontal: 0 }}
                selected={selectedType !== 'All'}
              >
                Type: {selectedType}
              </Chip>
            }
          >
            {SCHEME_TYPES.map((type) => (
              <Menu.Item
                key={type}
                onPress={() => {
                  setSelectedType(type);
                  setShowTypeMenu(false);
                  loadSchemes(1);
                }}
                title={type}
                titleStyle={{ 
                  color: colors.textPrimary,
                  fontSize: 14,
                  fontWeight: '500'
                }}
              />
            ))}
          </Menu>

          <Menu
            visible={showCategoryMenu}
            onDismiss={() => setShowCategoryMenu(false)}
            anchor={
              <Chip 
                compact
                onPress={() => setShowCategoryMenu(true)}
                style={[styles.filterChip, { backgroundColor: selectedCategory !== 'All' ? `${colors.primary}20` : colors.inputBg }]}
                textStyle={{ color: selectedCategory !== 'All' ? colors.primary : colors.textPrimary, fontSize: 12, marginHorizontal: 0 }}
                selected={selectedCategory !== 'All'}
              >
                Category: {selectedCategory}
              </Chip>
            }
          >
            {CATEGORIES.map((cat) => (
              <Menu.Item
                key={cat}
                onPress={() => {
                  setSelectedCategory(cat);
                  setShowCategoryMenu(false);
                  loadSchemes(1);
                }}
                title={cat}
                titleStyle={{ 
                  color: colors.textPrimary,
                  fontSize: 14,
                  fontWeight: '500'
                }}
              />
            ))}
          </Menu>
        </View>
      </View>

      {isLoading && schemes.length === 0 ? (
        <ActivityIndicator style={styles.loader} size="large" />
      ) : (
        <FlatList
          data={schemes}
          renderItem={renderSchemeCard}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContent}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
          ListFooterComponent={
            isLoading && schemes.length > 0 ? (
              <ActivityIndicator style={styles.loadMoreIndicator} />
            ) : null
          }
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text variant="bodyLarge">No schemes found</Text>
              <Text variant="bodyMedium" style={styles.emptySubtext}>
                Try adjusting your filters
              </Text>
            </View>
          }
        />
      )}

      {/* Eligibility Check Modal */}
      {selectedScheme && (
        <EligibilityCheckModal
          visible={eligibilityModalVisible}
          onDismiss={() => {
            setEligibilityModalVisible(false);
            setSelectedScheme(null);
          }}
          schemeId={selectedScheme.id}
          schemeName={selectedScheme.name}
        />
      )}
    </SafeAreaView>
  );
};

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: 16,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 12,
  },
  searchBar: {
    marginBottom: 12,
    backgroundColor: colors.inputBg,
    elevation: 0,
  },
  filtersContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  filterChip: {
    height: 32,
    backgroundColor: colors.inputBg,
    borderColor: colors.border,
  },
  listContent: {
    padding: 16,
  },
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  card: {
    marginBottom: 12,
    backgroundColor: colors.cardBg,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    elevation: 2,
    overflow: 'hidden',
  },
  cardContent: {
    padding: 14,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  titleContainer: {
    flex: 1,
    marginRight: 8,
  },
  ministryText: {
    color: colors.textSecondary,
    fontSize: 12,
  },
  chipsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginBottom: 8,
  },
  typeChip: {
    backgroundColor: `${colors.primary}15`,
  },
  categoryChip: {
    backgroundColor: `${colors.secondary}15`,
  },
  description: {
    color: colors.textSecondary,
  },
  coverageStrip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${colors.primary}10`,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  coverageLabel: {
    fontSize: 12,
    fontWeight: '500',
    color: colors.textSecondary,
    marginRight: 4,
  },
  coverageAmount: {
    fontSize: 13,
    fontWeight: '700',
    color: colors.primary,
  },
  cardActionsRow: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 4,
    width: '100%',
  },
  secondaryCardButton: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 8,
    borderRadius: 10,
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  secondaryCardButtonText: {
    fontSize: 12,
    fontWeight: '600',
    textAlign: 'center',
  },
  primaryCardButton: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 8,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  primaryCardButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#FFFFFF',
    textAlign: 'center',
  },
  loadMoreIndicator: {
    marginVertical: 16,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 48,
  },
  emptySubtext: {
    color: colors.textSecondary,
    marginTop: 8,
  },
});
