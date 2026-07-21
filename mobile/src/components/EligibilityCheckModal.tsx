import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  Modal,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Text, TextInput, ActivityIndicator } from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { checkEligibility, clearEligibilityResult } from '../redux/slices/schemesSlice';
import { useTheme } from '../contexts/ThemeContext';
import { EligibilityResultCard } from './EligibilityResultCard';
import { api } from '../services/api';

interface Props {
  visible: boolean;
  onDismiss: () => void;
  schemeId: number;
  schemeName: string;
}

type Step = 'choice' | 'form' | 'loading' | 'result';

interface FormData {
  age: string;
  gender: string;
  state: string;
  income: string;
  category: string;
  occupation: string;
}

const GENDER_OPTIONS = ['male', 'female', 'other'];
const CATEGORY_OPTIONS = ['General', 'SC', 'ST', 'OBC'];
const INCOME_OPTIONS = ['BPL', 'Low', 'Medium', 'High'];

export const EligibilityCheckModal: React.FC<Props> = ({
  visible,
  onDismiss,
  schemeId,
  schemeName,
}) => {
  const dispatch = useDispatch<AppDispatch>();
  const { colors } = useTheme();
  const styles = createStyles(colors);
  const { eligibilityResult, eligibilityLoading } = useSelector(
    (state: RootState) => state.schemes
  );

  const [step, setStep] = useState<Step>('choice');
  const [formData, setFormData] = useState<FormData>({
    age: '',
    gender: '',
    state: '',
    income: '',
    category: '',
    occupation: '',
  });
  const [fetchingProfile, setFetchingProfile] = useState(false);

  const handleClose = () => {
    setStep('choice');
    setFormData({ age: '', gender: '', state: '', income: '', category: '', occupation: '' });
    dispatch(clearEligibilityResult());
    onDismiss();
  };

  const calculateAge = (dob: string): number => {
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };

  const handleCheckForMyself = async () => {
    setFetchingProfile(true);
    setStep('loading');
    try {
      // Fetch user profile from API
      const response = await api.get('/patients/me');
      const profile = response.data;

      const age = profile.date_of_birth ? calculateAge(profile.date_of_birth) : undefined;

      const checkData: any = {};
      if (age !== undefined) checkData.age = age;
      if (profile.gender) checkData.gender = profile.gender;
      if (profile.address?.state) checkData.state = profile.address.state;

      await dispatch(checkEligibility({ schemeId, data: checkData }));
      setStep('result');
    } catch (error) {
      console.error('Error fetching profile:', error);
      // Fallback: go to form so user can fill manually
      setStep('form');
    } finally {
      setFetchingProfile(false);
    }
  };

  const handleCheckForSomeoneElse = () => {
    setStep('form');
  };

  const handleSubmitForm = async () => {
    setStep('loading');

    const checkData: any = {};
    if (formData.age) checkData.age = parseInt(formData.age, 10);
    if (formData.gender) checkData.gender = formData.gender;
    if (formData.state) checkData.state = formData.state;
    if (formData.income) checkData.income = formData.income;
    if (formData.category) checkData.category = formData.category;
    if (formData.occupation) checkData.occupation = formData.occupation;

    await dispatch(checkEligibility({ schemeId, data: checkData }));
    setStep('result');
  };

  const renderChoice = () => (
    <View style={styles.choiceContainer}>
      <View style={styles.modalHeader}>
        <Text style={styles.modalTitle}>Check Eligibility</Text>
        <Text style={styles.modalSubtitle}>{schemeName}</Text>
      </View>

      <Text style={styles.choiceQuestion}>Who are you checking eligibility for?</Text>

      <TouchableOpacity
        style={[styles.choiceButton, { backgroundColor: colors.primary }]}
        onPress={handleCheckForMyself}
        activeOpacity={0.8}
      >
        <Text style={styles.choiceIcon}>👤</Text>
        <View style={styles.choiceTextContainer}>
          <Text style={styles.choiceButtonText}>For Myself</Text>
          <Text style={styles.choiceButtonDesc}>
            Use my profile data to check eligibility
          </Text>
        </View>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.choiceButton, { backgroundColor: colors.cardBg, borderWidth: 1, borderColor: colors.border }]}
        onPress={handleCheckForSomeoneElse}
        activeOpacity={0.8}
      >
        <Text style={styles.choiceIcon}>👥</Text>
        <View style={styles.choiceTextContainer}>
          <Text style={[styles.choiceButtonText, { color: colors.textPrimary }]}>For Someone Else</Text>
          <Text style={[styles.choiceButtonDesc, { color: colors.textSecondary }]}>
            Enter details manually
          </Text>
        </View>
      </TouchableOpacity>
    </View>
  );

  const renderForm = () => (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Enter Details</Text>
          <Text style={styles.modalSubtitle}>{schemeName}</Text>
        </View>

        <TextInput
          label="Age"
          value={formData.age}
          onChangeText={(text) => setFormData((prev) => ({ ...prev, age: text }))}
          keyboardType="number-pad"
          style={styles.input}
          mode="outlined"
          outlineColor={colors.border}
          activeOutlineColor={colors.primary}
        />

        {/* Gender Selector */}
        <Text style={styles.fieldLabel}>Gender</Text>
        <View style={styles.chipRow}>
          {GENDER_OPTIONS.map((g) => (
            <TouchableOpacity
              key={g}
              style={[
                styles.chip,
                formData.gender === g && { backgroundColor: colors.primary, borderColor: colors.primary },
              ]}
              onPress={() => setFormData((prev) => ({ ...prev, gender: g }))}
            >
              <Text
                style={[
                  styles.chipText,
                  formData.gender === g && { color: '#fff' },
                ]}
              >
                {g.charAt(0).toUpperCase() + g.slice(1)}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <TextInput
          label="State"
          value={formData.state}
          onChangeText={(text) => setFormData((prev) => ({ ...prev, state: text }))}
          style={styles.input}
          mode="outlined"
          outlineColor={colors.border}
          activeOutlineColor={colors.primary}
        />

        {/* Category Selector */}
        <Text style={styles.fieldLabel}>Category</Text>
        <View style={styles.chipRow}>
          {CATEGORY_OPTIONS.map((c) => (
            <TouchableOpacity
              key={c}
              style={[
                styles.chip,
                formData.category === c && { backgroundColor: colors.primary, borderColor: colors.primary },
              ]}
              onPress={() => setFormData((prev) => ({ ...prev, category: c }))}
            >
              <Text
                style={[
                  styles.chipText,
                  formData.category === c && { color: '#fff' },
                ]}
              >
                {c}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Income Selector */}
        <Text style={styles.fieldLabel}>Income Bracket</Text>
        <View style={styles.chipRow}>
          {INCOME_OPTIONS.map((i) => (
            <TouchableOpacity
              key={i}
              style={[
                styles.chip,
                formData.income === i && { backgroundColor: colors.primary, borderColor: colors.primary },
              ]}
              onPress={() => setFormData((prev) => ({ ...prev, income: i }))}
            >
              <Text
                style={[
                  styles.chipText,
                  formData.income === i && { color: '#fff' },
                ]}
              >
                {i}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <TextInput
          label="Occupation (optional)"
          value={formData.occupation}
          onChangeText={(text) => setFormData((prev) => ({ ...prev, occupation: text }))}
          style={styles.input}
          mode="outlined"
          outlineColor={colors.border}
          activeOutlineColor={colors.primary}
        />

        <TouchableOpacity
          style={[styles.submitButton, { backgroundColor: colors.primary }]}
          onPress={handleSubmitForm}
          activeOpacity={0.8}
        >
          <Text style={styles.submitButtonText}>Check Eligibility</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );

  const renderLoading = () => (
    <View style={styles.loadingContainer}>
      <ActivityIndicator size="large" color={colors.primary} />
      <Text style={styles.loadingText}>
        {fetchingProfile ? 'Fetching your profile...' : 'Checking eligibility...'}
      </Text>
    </View>
  );

  const renderResult = () => (
    <View>
      <View style={styles.modalHeader}>
        <Text style={styles.modalTitle}>Eligibility Result</Text>
        <Text style={styles.modalSubtitle}>{schemeName}</Text>
      </View>
      <EligibilityResultCard result={eligibilityResult} loading={eligibilityLoading} />
      <TouchableOpacity
        style={[styles.submitButton, { backgroundColor: colors.primary, marginTop: 16 }]}
        onPress={handleClose}
        activeOpacity={0.8}
      >
        <Text style={styles.submitButtonText}>Done</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent
      onRequestClose={handleClose}
    >
      <View style={styles.overlay}>
        <View style={[styles.modalContainer, { backgroundColor: colors.cardBg }]}>
          {/* Close button */}
          <TouchableOpacity style={styles.closeButton} onPress={handleClose}>
            <Text style={[styles.closeButtonText, { color: colors.textSecondary }]}>✕</Text>
          </TouchableOpacity>

          {step === 'choice' && renderChoice()}
          {step === 'form' && renderForm()}
          {step === 'loading' && renderLoading()}
          {step === 'result' && renderResult()}
        </View>
      </View>
    </Modal>
  );
};

const createStyles = (colors: any) =>
  StyleSheet.create({
    overlay: {
      flex: 1,
      backgroundColor: 'rgba(0,0,0,0.5)',
      justifyContent: 'flex-end',
    },
    modalContainer: {
      borderTopLeftRadius: 28,
      borderTopRightRadius: 28,
      padding: 24,
      paddingBottom: 40,
      maxHeight: '85%',
    },
    closeButton: {
      position: 'absolute',
      right: 16,
      top: 16,
      zIndex: 10,
      width: 32,
      height: 32,
      borderRadius: 16,
      backgroundColor: colors.inputBg,
      alignItems: 'center',
      justifyContent: 'center',
    },
    closeButtonText: {
      fontSize: 16,
      fontWeight: '600',
    },
    modalHeader: {
      marginBottom: 20,
    },
    modalTitle: {
      fontSize: 22,
      fontWeight: '700',
      color: colors.textPrimary,
    },
    modalSubtitle: {
      fontSize: 14,
      color: colors.textSecondary,
      marginTop: 4,
    },
    choiceContainer: {
      gap: 12,
    },
    choiceQuestion: {
      fontSize: 16,
      fontWeight: '500',
      color: colors.textPrimary,
      marginBottom: 8,
    },
    choiceButton: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: 18,
      borderRadius: 16,
      gap: 14,
    },
    choiceIcon: {
      fontSize: 28,
    },
    choiceTextContainer: {
      flex: 1,
    },
    choiceButtonText: {
      fontSize: 16,
      fontWeight: '700',
      color: '#fff',
    },
    choiceButtonDesc: {
      fontSize: 12,
      color: 'rgba(255,255,255,0.8)',
      marginTop: 2,
    },
    input: {
      marginBottom: 12,
      backgroundColor: 'transparent',
    },
    fieldLabel: {
      fontSize: 13,
      fontWeight: '600',
      color: colors.textPrimary,
      marginBottom: 8,
      marginTop: 4,
    },
    chipRow: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      gap: 8,
      marginBottom: 12,
    },
    chip: {
      paddingVertical: 8,
      paddingHorizontal: 16,
      borderRadius: 20,
      borderWidth: 1,
      borderColor: colors.border,
      backgroundColor: colors.inputBg,
    },
    chipText: {
      fontSize: 13,
      fontWeight: '500',
      color: colors.textPrimary,
    },
    submitButton: {
      paddingVertical: 14,
      borderRadius: 14,
      alignItems: 'center',
      marginTop: 8,
    },
    submitButtonText: {
      fontSize: 16,
      fontWeight: '700',
      color: '#fff',
    },
    loadingContainer: {
      alignItems: 'center',
      paddingVertical: 48,
      gap: 16,
    },
    loadingText: {
      fontSize: 15,
      color: colors.textSecondary,
    },
  });
