import { AskResponse, EligibilityProfile, EligibilityResponse, Policy } from "../types";
import api from "./api";

export async function fetchPolicies(): Promise<Policy[]> {
  const response = await api.get<{ total: number; items: Policy[] }>("/policies");
  return response.data.items;
}

export async function fetchPolicy(id: string): Promise<Policy> {
  const response = await api.get<Policy>(`/policies/${id}`);
  return response.data;
}

export async function checkEligibility(policyId: string, profile: EligibilityProfile): Promise<EligibilityResponse> {
  const response = await api.post<EligibilityResponse>("/policies/check-eligibility", {
    policy_id: policyId,
    profile,
  });
  return response.data;
}

export async function askQuestion(policyId: string, question: string): Promise<AskResponse> {
  const response = await api.post<AskResponse>("/policies/ask", {
    policy_id: policyId,
    question,
  });
  return response.data;
}
