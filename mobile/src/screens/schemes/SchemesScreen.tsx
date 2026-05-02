import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { 
  Text, 
  Card, 
  Button, 
  Searchbar, 
  Chip, 
  ActivityIndicator,
  IconButton,
  Menu,
  Divider,
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
import { theme } from '../../theme';

const SCHEME_TYPES = ['All', 'National', 'State', 'Central', 'NGO'];
const CATEGORIES = ['All', 'BPL', 'Women', 'Senior Citizens', 'Children', 'Disabled'];

export const SchemesScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { schemes, isLoading, pagination } = useSelector((state: RootState) => state.schemes);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [showTypeMenu, setShowTypeMenu] = useState(false);
  const [showCategoryMenu, setShowCategoryMenu] = useState(false);

  const loadSchemes = useCallback(async (pageNum: number = 1) => {
    const params: any = { page: pageNum };
    if (searchQuery) params.search = searchQuery;
    if (selectedType !== 'All') params.type = selectedType.toLowerCase();
    if (selectedCategory !== 'All') params.category = selectedCategory;
    
    await dispatch(fetchSchemes(params));
  }, [dispatch, searchQuery, selectedType, selectedCategory]);

  useEffect(() => {
    loadSchemes(1);
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
      <Card.Content>
        <View style={styles.cardHeader}>
          <View style={styles.titleContainer}>
            <Text variant="titleMedium" numberOfLines={2}>
              {scheme.name}
            </Text>
            <Text variant="bodySmall" style={styles.ministryText}>
              {scheme.ministry || scheme.type}
            </Text>
          </View>
          <IconButton
            icon={scheme.is_bookmarked ? 'bookmark' : 'bookmark-outline'}
            size={24}
            iconColor={scheme.is_bookmarked ? theme.colors.primary : theme.colors.onSurfaceVariant}
            onPress={() => handleBookmark(scheme)}
          />
        </View>

        <View style={styles.chipsContainer}>
          <Chip compact style={styles.typeChip}>{scheme.type}</Chip>
          {scheme.target_categories.slice(0, 2).map((cat) => (
            <Chip key={cat} compact style={styles.categoryChip}>{cat}</Chip>
          ))}
        </View>

        <Text variant="bodyMedium" numberOfLines={2} style={styles.description}>
          {scheme.short_description || scheme.description}
        </Text>

        {scheme.coverage_amount && (
          <View style={styles.coverageContainer}>
            <Text variant="bodySmall" style={styles.coverageLabel}>Coverage:</Text>
            <Text variant="bodyMedium" style={styles.coverageAmount}>
              ₹{scheme.coverage_amount.toLocaleString()}
            </Text>
          </View>
        )}

        {scheme.services_covered.length > 0 && (
          <View style={styles.servicesContainer}>
            <Text variant="bodySmall" style={styles.servicesLabel}>Services:</Text>
            <Text variant="bodySmall" style={styles.servicesText}>
              {scheme.services_covered.slice(0, 3).join(', ')}
              {scheme.services_covered.length > 3 && '...'}
            </Text>
          </View>
        )}
      </Card.Content>
      
      <Card.Actions>
        <Button>Check Eligibility</Button>
        <Button mode="contained">View Details</Button>
      </Card.Actions>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text variant="headlineSmall" style={styles.title}>Dental Schemes</Text>
        
        <Searchbar
          placeholder="Search schemes..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchBar}
          onSubmitEditing={() => loadSchemes(1)}
        />

        <View style={styles.filtersContainer}>
          <Menu
            visible={showTypeMenu}
            onDismiss={() => setShowTypeMenu(false)}
            anchor={
              <Chip 
                onPress={() => setShowTypeMenu(true)}
                style={styles.filterChip}
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
              />
            ))}
          </Menu>

          <Menu
            visible={showCategoryMenu}
            onDismiss={() => setShowCategoryMenu(false)}
            anchor={
              <Chip 
                onPress={() => setShowCategoryMenu(true)}
                style={styles.filterChip}
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
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    padding: 16,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.outlineVariant,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 12,
  },
  searchBar: {
    marginBottom: 12,
    elevation: 0,
  },
  filtersContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  filterChip: {
    height: 32,
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
    elevation: 1,
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
    color: theme.colors.onSurfaceVariant,
    marginTop: 2,
  },
  chipsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginBottom: 8,
  },
  typeChip: {
    backgroundColor: theme.colors.primaryContainer,
  },
  categoryChip: {
    backgroundColor: theme.colors.secondaryContainer,
  },
  description: {
    marginTop: 4,
    color: theme.colors.onSurface,
  },
  coverageContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  coverageLabel: {
    color: theme.colors.onSurfaceVariant,
    marginRight: 4,
  },
  coverageAmount: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
  servicesContainer: {
    marginTop: 8,
  },
  servicesLabel: {
    color: theme.colors.onSurfaceVariant,
  },
  servicesText: {
    color: theme.colors.onSurface,
    marginTop: 2,
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
    color: theme.colors.onSurfaceVariant,
    marginTop: 8,
  },
});
