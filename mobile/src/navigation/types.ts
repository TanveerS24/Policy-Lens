export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
  Otp: undefined;
};

export type AppTabsParamList = {
  Home: undefined;
  Policies: undefined;
  Upload: undefined;
  MyUploads: undefined;
  Profile: undefined;
};

export type MainStackParamList = {
  Tabs: undefined;
  PolicyDetails: { policyId: string };
  Eligibility: { policyId: string };
  AskAi: { policyId: string };
};
