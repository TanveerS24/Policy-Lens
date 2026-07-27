import React, { useEffect, useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
  Platform,
} from 'react-native';
import { Text, ActivityIndicator, Chip, IconButton } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { RootState, AppDispatch } from '../../redux/store';
import {
  fetchSchemeById,
  bookmarkScheme,
  removeBookmark,
  Scheme,
} from '../../redux/slices/schemesSlice';
import { useTheme } from '../../contexts/ThemeContext';
import { EligibilityCheckModal } from '../../components/EligibilityCheckModal';

type SchemeDetailRouteParams = {
  SchemeDetail: { schemeId: number };
};

export const SchemeDetailScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation();
  const route = useRoute<RouteProp<SchemeDetailRouteParams, 'SchemeDetail'>>();
  const { schemeId } = route.params;
  const { colors } = useTheme();
  const styles = createStyles(colors);

  const { currentScheme, isLoading } = useSelector(
    (state: RootState) => state.schemes
  );
  const [eligibilityModalVisible, setEligibilityModalVisible] = useState(false);

  useEffect(() => {
    dispatch(fetchSchemeById(schemeId));
  }, [dispatch, schemeId]);

  const scheme = currentScheme;

  const handleBookmark = async () => {
    if (!scheme) return;
    if (scheme.is_bookmarked) {
      await dispatch(removeBookmark(scheme.id));
    } else {
      await dispatch(bookmarkScheme(scheme.id));
    }
    dispatch(fetchSchemeById(schemeId));
  };

  const handleViewDocument = () => {
    if (!scheme) return;
    const API_URL = __DEV__
      ? 'http://localhost:8000/api/v1'
      : process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    const docUrl = `${API_URL}/schemes/${scheme.id}/document`;
    Linking.openURL(docUrl);
  };

  if (isLoading || !scheme) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Text style={[styles.backIcon, { color: colors.textPrimary }]}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle} numberOfLines={1}>
          Scheme Details
        </Text>
        <IconButton
          icon={scheme.is_bookmarked ? 'bookmark' : 'bookmark-outline'}
          size={24}
          iconColor={scheme.is_bookmarked ? colors.primary : colors.textSecondary}
          onPress={handleBookmark}
        />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Name & Type Badge */}
        <Text style={styles.schemeName}>{scheme.name}</Text>
        <View style={styles.badgeRow}>
          <Chip style={[styles.typeBadge, { backgroundColor: `${colors.primary}20` }]}>
            <Text style={{ color: colors.primary, fontWeight: '600', fontSize: 12 }}>
              {scheme.type?.toUpperCase()}
            </Text>
          </Chip>
          {scheme.ministry && (
            <Text style={styles.ministryText}>{scheme.ministry}</Text>
          )}
        </View>

        {/* Description */}
        {scheme.description && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>About</Text>
            <Text style={styles.descriptionText}>{scheme.description}</Text>
          </View>
        )}

        {/* Coverage */}
        {scheme.coverage_amount && (
          <View style={[styles.highlightCard, { backgroundColor: `${colors.primary}10` }]}>
            <Text style={styles.highlightLabel}>Coverage Amount</Text>
            <Text style={[styles.highlightValue, { color: colors.primary }]}>
              ₹{scheme.coverage_amount.toLocaleString()}
            </Text>
          </View>
        )}

        {/* Services Covered */}
        {scheme.services_covered && scheme.services_covered.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Services Covered</Text>
            <View style={styles.chipRow}>
              {scheme.services_covered.map((service, index) => (
                <Chip key={index} style={styles.serviceChip} compact>
                  {service}
                </Chip>
              ))}
            </View>
          </View>
        )}

        {/* Target Categories */}
        {scheme.target_categories && scheme.target_categories.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Target Categories</Text>
            <View style={styles.chipRow}>
              {scheme.target_categories.map((cat, index) => (
                <Chip key={index} style={styles.categoryChip} compact>
                  {cat}
                </Chip>
              ))}
            </View>
          </View>
        )}

        {/* Age Requirements */}
        {(scheme.min_age || scheme.max_age) && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Age Requirements</Text>
            <View style={styles.infoRow}>
              {scheme.min_age && (
                <View style={styles.infoItem}>
                  <Text style={styles.infoLabel}>Minimum Age</Text>
                  <Text style={styles.infoValue}>{scheme.min_age} years</Text>
                </View>
              )}
              {scheme.max_age && (
                <View style={styles.infoItem}>
                  <Text style={styles.infoLabel}>Maximum Age</Text>
                  <Text style={styles.infoValue}>{scheme.max_age} years</Text>
                </View>
              )}
            </View>
          </View>
        )}

        {/* Required Documents */}
        {scheme.required_documents && scheme.required_documents.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Required Documents</Text>
            {scheme.required_documents.map((doc, index) => (
              <View key={index} style={styles.docRow}>
                <Text style={styles.docBullet}>📄</Text>
                <Text style={styles.docText}>{doc}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Application Process */}
        {scheme.application_process && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Application Process</Text>
            <Text style={styles.descriptionText}>{scheme.application_process}</Text>
          </View>
        )}

        {/* Contact Info */}
        {(scheme.website || scheme.helpline) && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Contact Information</Text>
            {scheme.website && (
              <TouchableOpacity onPress={() => Linking.openURL(scheme.website!)}>
                <View style={styles.contactRow}>
                  <Text style={styles.contactIcon}>🌐</Text>
                  <Text style={[styles.contactText, { color: colors.primary }]}>
                    {scheme.website}
                  </Text>
                </View>
              </TouchableOpacity>
            )}
            {scheme.helpline && (
              <TouchableOpacity onPress={() => Linking.openURL(`tel:${scheme.helpline}`)}>
                <View style={styles.contactRow}>
                  <Text style={styles.contactIcon}>📞</Text>
                  <Text style={[styles.contactText, { color: colors.primary }]}>
                    {scheme.helpline}
                  </Text>
                </View>
              </TouchableOpacity>
            )}
          </View>
        )}

        {/* Full Document Text */}
        {scheme.full_document_text && (
          <View style={styles.section}>
            <View style={styles.documentTextHeader}>
              <Text style={styles.sectionTitle}>📄 Full Document</Text>
              <Text style={styles.documentTextHint}>Complete extracted text from the official document</Text>
            </View>
            <View style={[styles.documentTextContainer, { backgroundColor: colors.inputBg, borderColor: colors.border }]}>
              <Text style={styles.documentTextContent}>
                {scheme.full_document_text}
              </Text>
            </View>
          </View>
        )}

        {/* View Original Document (PDF) */}
        {scheme.has_original_document && (
          <TouchableOpacity
            style={[styles.documentButton, { borderColor: colors.primary }]}
            onPress={handleViewDocument}
            activeOpacity={0.7}
          >
            <Text style={styles.documentIcon}>📋</Text>
            <Text style={[styles.documentButtonText, { color: colors.primary }]}>
              Download Original PDF
            </Text>
          </TouchableOpacity>
        )}

        {/* Action Buttons */}
        <View style={styles.actionsContainer}>
          <TouchableOpacity
            style={[styles.primaryActionButton, { backgroundColor: colors.primary }]}
            onPress={() => setEligibilityModalVisible(true)}
            activeOpacity={0.8}
          >
            <Text style={styles.primaryActionText}>Check Eligibility</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* Eligibility Modal */}
      <EligibilityCheckModal
        visible={eligibilityModalVisible}
        onDismiss={() => setEligibilityModalVisible(false)}
        schemeId={scheme.id}
        schemeName={scheme.name}
      />
    </SafeAreaView>
  );
};

const createStyles = (colors: any) =>
  StyleSheet.create({
    container: {
      flex: 1,
    },
    loadingContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingHorizontal: 8,
      paddingVertical: 8,
      borderBottomWidth: 1,
      borderBottomColor: colors.border,
    },
    backButton: {
      padding: 8,
    },
    backIcon: {
      fontSize: 22,
      fontWeight: '600',
    },
    headerTitle: {
      flex: 1,
      fontSize: 18,
      fontWeight: '600',
      color: colors.textPrimary,
      marginLeft: 4,
    },
    scrollContent: {
      paddingHorizontal: 16,
      paddingVertical: 16,
      paddingBottom: 40,
    },
    schemeName: {
      fontSize: 24,
      fontWeight: '800',
      color: colors.textPrimary,
      lineHeight: 32,
      marginBottom: 12,
    },
    badgeRow: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: 10,
      marginBottom: 20,
    },
    typeBadge: {
      borderRadius: 8,
    },
    ministryText: {
      fontSize: 14,
      color: colors.textSecondary,
      fontWeight: '500',
    },
    section: {
      marginBottom: 20,
    },
    sectionTitle: {
      fontSize: 16,
      fontWeight: '700',
      color: colors.textPrimary,
      marginBottom: 10,
    },
    descriptionText: {
      fontSize: 14,
      color: colors.textSecondary,
      lineHeight: 22,
    },
    highlightCard: {
      borderRadius: 16,
      padding: 16,
      marginBottom: 20,
      alignItems: 'center',
    },
    highlightLabel: {
      fontSize: 13,
      color: colors.textSecondary,
      fontWeight: '500',
      marginBottom: 4,
    },
    highlightValue: {
      fontSize: 28,
      fontWeight: '800',
    },
    chipRow: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      gap: 8,
    },
    serviceChip: {
      backgroundColor: colors.inputBg,
    },
    categoryChip: {
      backgroundColor: `${colors.secondary}20`,
    },
    infoRow: {
      flexDirection: 'row',
      gap: 16,
    },
    infoItem: {
      flex: 1,
      backgroundColor: colors.inputBg,
      borderRadius: 12,
      padding: 12,
      alignItems: 'center',
    },
    infoLabel: {
      fontSize: 12,
      color: colors.textSecondary,
      marginBottom: 4,
    },
    infoValue: {
      fontSize: 18,
      fontWeight: '700',
      color: colors.textPrimary,
    },
    docRow: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: 8,
      paddingVertical: 6,
    },
    docBullet: {
      fontSize: 14,
    },
    docText: {
      fontSize: 14,
      color: colors.textPrimary,
      flex: 1,
    },
    contactRow: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: 8,
      paddingVertical: 6,
    },
    contactIcon: {
      fontSize: 16,
    },
    contactText: {
      fontSize: 14,
      fontWeight: '500',
    },
    documentButton: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 14,
      borderRadius: 14,
      borderWidth: 2,
      gap: 8,
      marginBottom: 20,
    },
    documentIcon: {
      fontSize: 18,
    },
    documentButtonText: {
      fontSize: 15,
      fontWeight: '700',
    },
    documentTextHeader: {
      marginBottom: 10,
    },
    documentTextHint: {
      fontSize: 12,
      color: colors.textSecondary,
      marginTop: 4,
      fontStyle: 'italic',
    },
    documentTextContainer: {
      borderRadius: 14,
      borderWidth: 1,
      padding: 16,
      maxHeight: 400,
    },
    documentTextContent: {
      fontSize: 13,
      color: colors.textPrimary,
      lineHeight: 22,
      fontFamily: undefined, // use system default
    },
    actionsContainer: {
      marginTop: 4,
    },
    primaryActionButton: {
      paddingVertical: 16,
      borderRadius: 14,
      alignItems: 'center',
    },
    primaryActionText: {
      fontSize: 16,
      fontWeight: '700',
      color: '#fff',
    },
  });
