import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { useTheme } from '../contexts/ThemeContext';
import { EligibilityResult } from '../redux/slices/schemesSlice';

interface Props {
  result: EligibilityResult | null;
  loading: boolean;
}

export const EligibilityResultCard: React.FC<Props> = ({ result, loading }) => {
  const { colors } = useTheme();
  const styles = createStyles(colors);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Checking eligibility...</Text>
      </View>
    );
  }

  if (!result) return null;

  const getResultConfig = () => {
    switch (result.result) {
      case 'likely_eligible':
        return {
          label: 'Likely Eligible',
          emoji: '✅',
          bgColor: '#ECFDF5',
          textColor: '#065F46',
          borderColor: '#A7F3D0',
        };
      case 'possibly_eligible':
        return {
          label: 'Possibly Eligible',
          emoji: '🟡',
          bgColor: '#FFFBEB',
          textColor: '#92400E',
          borderColor: '#FDE68A',
        };
      case 'not_eligible':
        return {
          label: 'Not Eligible',
          emoji: '❌',
          bgColor: '#FEF2F2',
          textColor: '#991B1B',
          borderColor: '#FECACA',
        };
      default:
        return {
          label: 'More Info Needed',
          emoji: 'ℹ️',
          bgColor: '#EFF6FF',
          textColor: '#1E40AF',
          borderColor: '#BFDBFE',
        };
    }
  };

  const config = getResultConfig();

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Result Badge */}
      <View style={[styles.resultBadge, { backgroundColor: config.bgColor, borderColor: config.borderColor }]}>
        <Text style={styles.resultEmoji}>{config.emoji}</Text>
        <Text style={[styles.resultLabel, { color: config.textColor }]}>{config.label}</Text>
      </View>

      {/* Confidence Score */}
      {result.confidence_score > 0 && (
        <View style={styles.scoreContainer}>
          <Text style={styles.scoreLabel}>Confidence</Text>
          <View style={styles.scoreBarBg}>
            <View
              style={[
                styles.scoreBarFill,
                {
                  width: `${result.confidence_score}%`,
                  backgroundColor:
                    result.confidence_score >= 70
                      ? '#10B981'
                      : result.confidence_score >= 40
                      ? '#F59E0B'
                      : '#EF4444',
                },
              ]}
            />
          </View>
          <Text style={styles.scoreValue}>{result.confidence_score}%</Text>
        </View>
      )}

      {/* Explanation */}
      {result.explanation ? (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Summary</Text>
          <Text style={styles.explanationText}>{result.explanation}</Text>
        </View>
      ) : null}

      {/* Matched Conditions */}
      {result.matched_conditions.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>✅ Matched Criteria</Text>
          {result.matched_conditions.map((condition, index) => (
            <View key={index} style={styles.conditionRow}>
              <Text style={[styles.conditionText, { color: '#065F46' }]}>{condition}</Text>
            </View>
          ))}
        </View>
      )}

      {/* Failed Conditions */}
      {result.failed_conditions.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>❌ Not Met</Text>
          {result.failed_conditions.map((condition, index) => (
            <View key={index} style={styles.conditionRow}>
              <Text style={[styles.conditionText, { color: '#991B1B' }]}>{condition}</Text>
            </View>
          ))}
        </View>
      )}

      {/* Missing Conditions */}
      {result.missing_conditions.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>ℹ️ Missing Information</Text>
          {result.missing_conditions.map((condition, index) => (
            <View key={index} style={styles.conditionRow}>
              <Text style={[styles.conditionText, { color: '#1E40AF' }]}>{condition}</Text>
            </View>
          ))}
        </View>
      )}

      {/* Next Steps */}
      {result.result !== 'not_eligible' && (
        <View style={[styles.section, styles.nextStepsSection]}>
          <Text style={styles.sectionTitle}>📋 Next Steps</Text>
          <Text style={styles.nextStepText}>• Visit the official website for application</Text>
          <Text style={styles.nextStepText}>• Gather required documents</Text>
          {result.helpline && (
            <Text style={styles.nextStepText}>• Contact helpline: {result.helpline}</Text>
          )}
        </View>
      )}
    </ScrollView>
  );
};

const createStyles = (colors: any) =>
  StyleSheet.create({
    container: {
      maxHeight: 400,
    },
    loadingContainer: {
      alignItems: 'center',
      paddingVertical: 32,
      gap: 12,
    },
    loadingText: {
      fontSize: 14,
      color: colors.textSecondary,
    },
    resultBadge: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
      paddingVertical: 16,
      paddingHorizontal: 20,
      borderRadius: 16,
      borderWidth: 1,
      marginBottom: 16,
      gap: 10,
    },
    resultEmoji: {
      fontSize: 28,
    },
    resultLabel: {
      fontSize: 20,
      fontWeight: '700',
    },
    scoreContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: 10,
      marginBottom: 16,
    },
    scoreLabel: {
      fontSize: 13,
      color: colors.textSecondary,
      fontWeight: '500',
      width: 80,
    },
    scoreBarBg: {
      flex: 1,
      height: 8,
      backgroundColor: colors.inputBg,
      borderRadius: 4,
      overflow: 'hidden',
    },
    scoreBarFill: {
      height: '100%',
      borderRadius: 4,
    },
    scoreValue: {
      fontSize: 13,
      fontWeight: '700',
      color: colors.textPrimary,
      width: 40,
      textAlign: 'right',
    },
    section: {
      marginBottom: 16,
    },
    sectionTitle: {
      fontSize: 14,
      fontWeight: '700',
      color: colors.textPrimary,
      marginBottom: 8,
    },
    explanationText: {
      fontSize: 14,
      color: colors.textSecondary,
      lineHeight: 20,
    },
    conditionRow: {
      paddingVertical: 4,
      paddingHorizontal: 8,
    },
    conditionText: {
      fontSize: 13,
      lineHeight: 18,
    },
    nextStepsSection: {
      backgroundColor: colors.inputBg,
      padding: 12,
      borderRadius: 12,
    },
    nextStepText: {
      fontSize: 13,
      color: colors.textSecondary,
      lineHeight: 20,
    },
  });
