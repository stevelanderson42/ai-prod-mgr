export interface Factor {
  signal: string;
  value: string;
  points: number;
  note_excerpt?: string;
}

export interface MissingSignal {
  signal: string;
  reason: string;
}

export interface Advisor {
  advisor_id: string;
  name: string;
  team: string;
  tenure_years: number;
  comp_ratio: number;
  production_trend_pct: number;
  org_events: string[];
  engagement_decline_pct: number;
  free_text_notes: string[];
  book_aum: number;
  household_count: number;
  status: string;
  departure_date: string | null;
  score_as_of_date: string | null;
  flight_risk_score: number;
  flight_risk_band: string;
  flight_risk_factors: Factor[];
  concentration_pct: number;
  exposed_aum: number;
  has_unscored_households: boolean;
  unscored_count: number;
  unscored_aum: number;
}

export interface Household {
  household_id: string;
  name: string;
  advisor_id: string;
  aum: number;
  firm_tenure_years: number;
  advisor_tenure_years: number;
  acquisition_origin: string | null;
  service_lines: string[];
  firm_contacts_count: number | null;
  portal_logins_monthly: number | null;
  communication_exclusivity_pct: number | null;
  fee_percentile: number;
  perf_vs_benchmark_pct: number | null;
  service_complaints_12mo: number;
  net_flow_pct: number | null;
  satisfaction_score: number | null;
  baseline_risk_score: number | null;
  baseline_risk_band: string;
  baseline_risk_factors: Factor[];
  baseline_missing_signals?: MissingSignal[];
  follow_likelihood_score: number | null;
  follow_likelihood_band: string;
  follow_likelihood_factors: Factor[];
  follow_missing_signals?: MissingSignal[];
}

export interface TransitionEntry {
  household_id: string;
  advisor_id: string;
  status: string;
  assigned_to: string;
  last_contact_date: string | null;
  next_action: string;
  follow_likelihood_band: string;
  baseline_risk_band: string;
}

export interface EvaluationCase {
  case_id: string;
  case_type: string;
  label: string;
  description: string;
  expected_band: string;
  actual_band: string;
  actual_score: number | null;
  factors: Factor[];
  missing_signals?: MissingSignal[];
  pass: boolean;
}

export interface AppData {
  metadata: {
    generated: string;
    description: string;
    advisor_count: number;
    household_count: number;
  };
  advisors: Advisor[];
  households: Household[];
  transition_entries: TransitionEntry[];
  evaluation_cases: EvaluationCase[];
}

export type View =
  | { kind: 'advisor-list' }
  | { kind: 'household'; advisorId: string }
  | { kind: 'transition'; advisorId: string }
  | { kind: 'evaluation' };
