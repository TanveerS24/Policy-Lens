import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Text, TextInput, Snackbar, Menu, Button } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useDispatch, useSelector } from 'react-redux';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { RootState, AppDispatch } from '../../redux/store';
import { requestOTP, clearError } from '../../redux/slices/authSlice';
import { theme, currentColors } from '../../theme';
import { useToast } from 'react-native-toast-notifications';

type RegisterScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Register'>;

const renderStepIndicator = (currentStep: number) => (
  <View style={styles.stepIndicator}>
    {[1, 2].map((step) => (
      <View key={step} style={styles.stepRow}>
        <View
          style={[
            styles.stepDot,
            currentStep >= step && styles.stepDotActive,
          ]}
        >
          <Text
            style={[
              styles.stepNumber,
              currentStep >= step && styles.stepNumberActive,
            ]}
          >
            {step}
          </Text>
        </View>
        {step < 2 && (
          <View
            style={[
              styles.stepLine,
              currentStep > step && styles.stepLineActive,
            ]}
          />
        )}
      </View>
    ))}
  </View>
);

const INDIAN_STATES = [
  'Andhra Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
  'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Odisha', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telangana',
  'Uttar Pradesh', 'West Bengal', 'Delhi',
];

const STATE_DISTRICTS: Record<string, string[]> = {
  'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Kadapa', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari'],
  'Assam': ['Barpeta', 'Bongaigaon', 'Cachar', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Goalpara', 'Golaghat', 'Hailakandi', 'Jorhat', 'Kamrup', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Marigaon', 'Nagaon', 'Nalbari', 'North Cachar Hills', 'Sivasagar', 'Sonitpur', 'Tinsukia'],
  'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
  'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja'],
  'Goa': ['North Goa', 'South Goa'],
  'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
  'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Mewat', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
  'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una'],
  'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahibganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum'],
  'Karnataka': ['Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar', 'Chamarajanagar', 'Chikballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir'],
  'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
  'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha'],
  'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
  'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh'],
  'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Muktsar', 'Nawanshahr', 'Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'Tarn Taran'],
  'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Sri Ganganagar', 'Tonk', 'Udaipur'],
  'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kancheepuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
  'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Komaram Bheem', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak', 'Medchal Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Rangareddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal Rural', 'Warangal Urban', 'Yadadri Bhuvanagiri'],
  'Uttar Pradesh': ['Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Rae Bareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
  'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur'],
  'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi'],
};

const GENDERS = ['male', 'female', 'other'];

export const RegisterScreen: React.FC = () => {
  const navigation = useNavigation<RegisterScreenNavigationProp>();
  const dispatch = useDispatch<AppDispatch>();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  const toast = useToast();
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    mobile: '',
    dateOfBirth: '',
    gender: '',
    state: '',
    district: '',
    pinCode: '',
    password: '',
    confirmPassword: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showStateMenu, setShowStateMenu] = useState(false);
  const [showDistrictMenu, setShowDistrictMenu] = useState(false);
  const [showGenderMenu, setShowGenderMenu] = useState(false);
  const [snackbarVisible, setSnackbarVisible] = useState(false);

  const availableDistricts = formData.state ? STATE_DISTRICTS[formData.state] || [] : [];

  const handleStateSelect = (state: string) => {
    updateForm('state', state);
    updateForm('district', ''); // Reset district when state changes
    setShowStateMenu(false);
  };

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      return 'Passwords do not match';
    }
    if (formData.mobile.length !== 10) {
      return 'Mobile number must be 10 digits';
    }
    if (formData.pinCode.length !== 6) {
      return 'PIN code must be 6 digits';
    }
    if (formData.password.length < 8) {
      return 'Password must be at least 8 characters long';
    }
    if (!/[A-Z]/.test(formData.password)) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!/[a-z]/.test(formData.password)) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!/\d/.test(formData.password)) {
      return 'Password must contain at least one digit';
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(formData.password)) {
      return 'Password must contain at least one special character';
    }
    return null;
  };

  const handleNext = () => {
    setStep(2);
  };

  const handlePrevious = () => {
    setStep(1);
  };

  const handleRegister = async () => {
    console.log('Register button clicked');
    console.log('Form data:', formData);
    
    const error = validateForm();
    console.log('Validation error:', error);
    
    if (error) {
      console.log('Validation failed:', error);
      dispatch(clearError());
      toast.show(error, {
        type: 'danger',
        placement: 'top',
      });
      return;
    }

    console.log('Validation passed, requesting OTP...');
    
    // Request OTP
    try {
      const result = await dispatch(requestOTP({ mobile: formData.mobile, purpose: 'registration' })).unwrap();
      console.log('OTP requested successfully:', result);
      
      toast.show('OTP sent to your mobile number', {
        type: 'success',
        placement: 'top',
      });
      
      navigation.navigate('OTPVerification', {
        mobile: formData.mobile,
        purpose: 'registration',
        nextScreen: 'Main',
        userData: formData,
      });
    } catch (err: any) {
      console.error('OTP request failed:', err);
      
      // Handle specific user exists error
      if (err?.response?.status === 400 && err?.response?.data?.detail?.includes('already exists')) {
        toast.show('User already exists. Please login instead.', {
          type: 'warning',
          placement: 'top',
          duration: 5000,
        });
        // Navigate to login after delay
        setTimeout(() => {
          navigation.navigate('Login');
        }, 3000);
      } else {
        toast.show(err?.response?.data?.detail || err?.message || 'Failed to send OTP. Please try again.', {
          type: 'danger',
          placement: 'top',
        });
      }
    }
  };

  const handleLogin = () => {
    navigation.navigate('Login');
  };

  return (
    <View style={styles.gradient}>
      <SafeAreaView style={styles.container}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <ScrollView
            style={styles.scrollView}
            contentContainerStyle={styles.scrollContent}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={true}
          >
            {/* Header */}
            <View style={styles.header}>
              <Text style={styles.title}>Create Account</Text>
              <Text style={styles.subtitle}>
                Sign up to explore dental health schemes
              </Text>
            </View>

            {/* Step Indicator */}
            {renderStepIndicator(step)}

            {/* Glassmorphism Card */}
            <View style={styles.card}>
              <View style={styles.form}>
                {step === 1 && (
                  <>
            <TextInput
              label="Full Name *"
              value={formData.name}
              onChangeText={(text) => updateForm('name', text)}
              mode="outlined"
              style={styles.input}
            />

            <TextInput
              label="Mobile Number *"
              value={formData.mobile}
              onChangeText={(text) => updateForm('mobile', text.replace(/[^0-9]/g, '').slice(0, 10))}
              mode="outlined"
              keyboardType="phone-pad"
              style={styles.input}
            />

            <TextInput
              label="Email (optional)"
              value={formData.email}
              onChangeText={(text) => updateForm('email', text)}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
            />

            <TextInput
              label="Date of Birth (DD-MM-YYYY) *"
              value={formData.dateOfBirth}
              onChangeText={(text) => updateForm('dateOfBirth', text)}
              mode="outlined"
              placeholder="01-01-1990"
              style={styles.input}
            />

            <View style={styles.dropdownContainer}>
              <TouchableOpacity onPress={() => setShowGenderMenu(!showGenderMenu)} activeOpacity={0.7}>
                <TextInput
                  label="Gender *"
                  value={formData.gender ? formData.gender.charAt(0).toUpperCase() + formData.gender.slice(1) : ''}
                  editable={false}
                  mode="outlined"
                  style={styles.input}
                  right={<TextInput.Icon icon={showGenderMenu ? "menu-up" : "menu-down"} />}
                  pointerEvents="none"
                />
              </TouchableOpacity>
              {showGenderMenu && (
                <View style={styles.customDropdown}>
                  <ScrollView style={styles.dropdownScrollContent} nestedScrollEnabled={true}>
                    {GENDERS.map((gender) => (
                      <TouchableOpacity
                        key={gender}
                        style={styles.dropdownItem}
                        onPress={() => {
                          updateForm('gender', gender);
                          setShowGenderMenu(false);
                        }}
                      >
                        <Text style={styles.dropdownItemText}>{gender.charAt(0).toUpperCase() + gender.slice(1)}</Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>
              )}
            </View>

            <TouchableOpacity
              style={[
                styles.continueButton,
                styles.buttonGradient,
                (!formData.name || !formData.mobile || !formData.dateOfBirth || !formData.gender) && styles.continueButtonDisabled,
              ]}
              onPress={handleNext}
              disabled={!formData.name || !formData.mobile || !formData.dateOfBirth || !formData.gender}
            >
              <Text style={styles.buttonText}>Next</Text>
            </TouchableOpacity>
                  </>
                )}

                {step === 2 && (
                  <>
            <View style={styles.dropdownContainer}>
              <TouchableOpacity onPress={() => setShowStateMenu(!showStateMenu)} activeOpacity={0.7}>
                <TextInput
                  label="State *"
                  value={formData.state}
                  editable={false}
                  mode="outlined"
                  style={styles.input}
                  right={<TextInput.Icon icon={showStateMenu ? "menu-up" : "menu-down"} />}
                  pointerEvents="none"
                />
              </TouchableOpacity>
              {showStateMenu && (
                <View style={styles.customDropdown}>
                  <ScrollView style={styles.dropdownScrollContent} nestedScrollEnabled={true}>
                    {INDIAN_STATES.map((state) => (
                      <TouchableOpacity
                        key={state}
                        style={styles.dropdownItem}
                        onPress={() => {
                          handleStateSelect(state);
                          setShowStateMenu(false);
                        }}
                      >
                        <Text style={styles.dropdownItemText}>{state}</Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>
              )}
            </View>

            <View style={styles.dropdownContainer}>
              <TouchableOpacity 
                onPress={() => formData.state && setShowDistrictMenu(!showDistrictMenu)} 
                activeOpacity={0.7}
                disabled={!formData.state}
              >
                <TextInput
                  label="District *"
                  value={formData.district}
                  editable={false}
                  mode="outlined"
                  style={[styles.input, !formData.state && styles.inputDisabled]}
                  right={<TextInput.Icon icon={formData.state ? (showDistrictMenu ? "menu-up" : "menu-down") : "lock"} />}
                  pointerEvents="none"
                />
              </TouchableOpacity>
              {showDistrictMenu && formData.state && (
                <View style={styles.customDropdown}>
                  <ScrollView style={styles.dropdownScrollContent} nestedScrollEnabled={true}>
                    {availableDistricts.map((district) => (
                      <TouchableOpacity
                        key={district}
                        style={styles.dropdownItem}
                        onPress={() => {
                          updateForm('district', district);
                          setShowDistrictMenu(false);
                        }}
                      >
                        <Text style={styles.dropdownItemText}>{district}</Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>
              )}
            </View>

            <TextInput
              label="PIN Code *"
              value={formData.pinCode}
              onChangeText={(text) => updateForm('pinCode', text.replace(/[^0-9]/g, '').slice(0, 6))}
              mode="outlined"
              keyboardType="number-pad"
              style={styles.input}
            />

            <TextInput
              label="Password * (min 8 chars)"
              value={formData.password}
              onChangeText={(text) => updateForm('password', text)}
              mode="outlined"
              secureTextEntry={!showPassword}
              right={
                <TextInput.Icon
                  icon={showPassword ? 'eye-off' : 'eye'}
                  onPress={() => setShowPassword(!showPassword)}
                />
              }
              style={styles.input}
            />

            <TextInput
              label="Confirm Password *"
              value={formData.confirmPassword}
              onChangeText={(text) => updateForm('confirmPassword', text)}
              mode="outlined"
              secureTextEntry={!showConfirmPassword}
              right={
                <TextInput.Icon
                  icon={showConfirmPassword ? 'eye-off' : 'eye'}
                  onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                />
              }
              style={styles.input}
            />

            <TouchableOpacity
              style={[
                styles.continueButton,
                styles.buttonGradient,
              ]}
              onPress={handlePrevious}
            >
              <Text style={styles.buttonText}>Previous</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.continueButton,
                styles.buttonGradient,
                isLoading && styles.continueButtonDisabled,
              ]}
              onPress={handleRegister}
              disabled={isLoading}
            >
              <Text style={styles.buttonText}>
                {isLoading ? 'Please wait...' : 'Register'}
              </Text>
            </TouchableOpacity>
                  </>
                )}

            <View style={styles.loginContainer}>
              <Text style={styles.loginText}>Already have an account?</Text>
              <TouchableOpacity onPress={handleLogin}>
                <Text style={styles.loginLink}>Sign In</Text>
              </TouchableOpacity>
            </View>
          </View>
            </View>
          </ScrollView>
        </KeyboardAvoidingView>

        <Snackbar
          visible={snackbarVisible || !!error}
          onDismiss={() => {
            setSnackbarVisible(false);
            dispatch(clearError());
          }}
          duration={3000}
          style={styles.snackbar}
        >
          {error || validateForm() || 'Registration failed. Please try again.'}
        </Snackbar>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
    backgroundColor: currentColors.background,
  },
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 100,
    minHeight: 800,
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: currentColors.textPrimary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: currentColors.textSecondary,
    textAlign: 'center',
  },
  stepIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  stepDot: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: currentColors.inputBg,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: currentColors.border,
  },
  stepDotActive: {
    backgroundColor: currentColors.primary,
    borderColor: currentColors.primary,
  },
  stepNumber: {
    fontSize: 14,
    fontWeight: '600',
    color: currentColors.textSecondary,
  },
  stepNumberActive: {
    color: '#FFFFFF',
  },
  stepLine: {
    width: 40,
    height: 2,
    backgroundColor: currentColors.border,
    marginHorizontal: 8,
  },
  stepLineActive: {
    backgroundColor: currentColors.primary,
  },
  card: {
    backgroundColor: currentColors.cardBg,
    borderRadius: 24,
    padding: 24,
    borderWidth: 1,
    borderColor: currentColors.border,
    shadowColor: currentColors.shadow,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.5,
    shadowRadius: 24,
    elevation: 10,
  },
  form: {
    gap: 12,
    paddingBottom: 24,
  },
  input: {
    backgroundColor: currentColors.inputBg,
  },
  inputDisabled: {
    opacity: 0.5,
  },
  continueButton: {
    marginTop: 16,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: currentColors.buttonShadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 6,
  },
  continueButtonDisabled: {
    opacity: 0.6,
  },
  previousButton: {
    flex: 1,
    marginRight: 8,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: currentColors.buttonShadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 6,
  },
  buttonRow: {
    flexDirection: 'row',
    marginTop: 16,
    gap: 12,
  },
  dropdownMenu: {
    maxHeight: 200,
  },
  dropdownContent: {
    maxHeight: 180,
  },
  menuContent: {
    maxHeight: 180,
  },
  dropdownContainer: {
    position: 'relative',
    zIndex: 1000,
  },
  customDropdown: {
    position: 'absolute',
    top: '100%',
    left: 0,
    right: 0,
    backgroundColor: currentColors.cardBg,
    borderWidth: 1,
    borderColor: currentColors.border,
    borderRadius: 8,
    maxHeight: 180,
    elevation: 8,
    shadowColor: currentColors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    zIndex: 1001,
  },
  dropdownScrollContent: {
    maxHeight: 180,
  },
  dropdownItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: currentColors.border,
  },
  dropdownItemText: {
    fontSize: 16,
    color: currentColors.textPrimary,
  },
  buttonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
    backgroundColor: currentColors.primary,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  loginContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 24,
    gap: 4,
  },
  loginText: {
    color: currentColors.textSecondary,
    fontSize: 14,
  },
  loginLink: {
    color: currentColors.primary,
    fontSize: 14,
    fontWeight: '600',
  },
  snackbar: {
    backgroundColor: currentColors.cardBg,
    borderRadius: 12,
  },
});
