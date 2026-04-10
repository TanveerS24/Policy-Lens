export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  otp?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  age: number;
  gender: string;
  state: string;
  income?: number;
}

export interface Policy {
  _id: string;
  title: string;
  short_description?: string;
  summary?: string;
  eligibility_criteria?: string;
  benefits?: string;
  notes?: string;
  category?: string;
  state?: string;
  approved?: boolean;
  created_at?: string;
  published_at?: string;
}

export interface EligibilityProfile {
  age: number;
  gender: string;
  state: string;
  income?: number;
}

export interface EligibilityResponse {
  eligible: boolean;
  reason: string;
  missing_requirements: string[];
}

export interface AskResponse {
  answer: string;
}

export interface UploadItem {
  _id: string;
  filename: string;
  status: string;
}
