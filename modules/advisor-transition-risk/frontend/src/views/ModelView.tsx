import { colors, bandColor, bandTextColor } from '../theme';

const sectionHeader: React.CSSProperties = {
  fontSize: '16px',
  fontWeight: 700,
  margin: '32px 0 4px',
  color: colors.text,
};

const subHeader: React.CSSProperties = {
  fontSize: '13px',
  color: colors.textMuted,
  margin: '0 0 12px',
};

const thStyle: React.CSSProperties = {
  textAlign: 'left',
  padding: '8px 12px',
  borderBottom: `2px solid ${colors.border}`,
  color: colors.textMuted,
  fontWeight: 600,
  fontSize: '11px',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
};

const tdStyle: React.CSSProperties = {
  padding: '8px 12px',
  borderBottom: `1px solid ${colors.border}`,
  fontSize: '13px',
  verticalAlign: 'top',
};

const tdSignal: React.CSSProperties = {
  ...tdStyle,
  fontWeight: 500,
};

interface SignalRow {
  signal: string;
  measures: string;
  brackets: string;
  maxPts: number;
  assumption: string;
}

const ADVISOR_SIGNALS: SignalRow[] = [
  {
    signal: 'Comp ratio',
    measures: 'Advisor comp / peer-segment median',
    brackets: '<0.85 \u2192 20; 0.85\u20130.94 \u2192 14; 0.95\u20131.04 \u2192 4; \u22651.05 \u2192 0',
    maxPts: 20,
    assumption: 'Below-market compensation is the strongest structured predictor of voluntary departure because advisors have high visibility into peer compensation and a liquid labor market.',
  },
  {
    signal: 'Production trend',
    measures: 'Trailing-12mo AUM growth minus firm average',
    brackets: '\u2264-8% \u2192 20; -4% to -8% \u2192 14; -1% to -4% \u2192 8; \u2265-1% \u2192 0',
    maxPts: 20,
    assumption: 'Declining relative production signals either disengagement or client loss, both of which precede departure. An advisor whose book is shrinking relative to peers has less reason to stay and less to lose by leaving.',
  },
  {
    signal: 'Tenure bucket',
    measures: 'Years at firm',
    brackets: '2\u20135 yr \u2192 10; 5\u20138 yr \u2192 6; <2 or >8 \u2192 2',
    maxPts: 10,
    assumption: '2\u20135 years is the peak mobility window: the advisor has a portable book but has not yet accumulated enough deferred compensation, non-compete exposure, or organizational embeddedness to make departure costly.',
  },
  {
    signal: 'Organizational events',
    measures: 'Passed over, manager change, compliance action (binary flags)',
    brackets: 'Each flag adds 5, capped at 15',
    maxPts: 15,
    assumption: 'Discrete organizational shocks loosen attachment. Each is individually ambiguous but they are additive\u2014two concurrent events are meaningfully more predictive than one.',
  },
  {
    signal: 'Engagement decline',
    measures: '% drop in CRM entries + client meetings, trailing 90 days vs. prior period',
    brackets: '\u226540% \u2192 15; 20\u201339% \u2192 10; 10\u201319% \u2192 5; <10% \u2192 0',
    maxPts: 15,
    assumption: 'Behavioral withdrawal\u2014fewer CRM updates, fewer logged meetings\u2014is the closest available leading indicator of imminent departure.',
  },
  {
    signal: 'Free-text sentiment',
    measures: 'Manager/HR notes, keyword/phrase match on curated dictionary',
    brackets: 'Match count and severity mapped to 0\u201320 (see dictionary below)',
    maxPts: 20,
    assumption: 'Manager and HR notes contain signal that structured fields miss, particularly for advisors who are outwardly performing but privately disengaged. Weighted high enough that strong text signal alone can push an otherwise-Stable advisor into Watch.',
  },
];

const BASELINE_SIGNALS: SignalRow[] = [
  {
    signal: 'Fee percentile',
    measures: "Household's effective fee vs. firm median for segment",
    brackets: '\u226580th \u2192 20; 60th\u201379th \u2192 12; 40th\u201359th \u2192 5; <40th \u2192 0',
    maxPts: 20,
    assumption: 'Households paying well above median for their segment are more likely to leave when any additional irritant appears, because fee sensitivity is latent until activated by a triggering event.',
  },
  {
    signal: 'Performance vs. benchmark',
    measures: 'Household portfolio trailing 12mo return vs. benchmark',
    brackets: '\u2264-4% \u2192 25; -2% to -4% \u2192 16; -1% to -2% \u2192 8; \u2265-1% \u2192 0',
    maxPts: 25,
    assumption: 'Underperformance relative to benchmark is the most visible and emotionally salient driver of client dissatisfaction, because clients compare their returns to publicized indices.',
  },
  {
    signal: 'Service complaints',
    measures: 'Count of complaints, trailing 12 months',
    brackets: '\u22653 \u2192 20; 2 \u2192 14; 1 \u2192 7; 0 \u2192 0',
    maxPts: 20,
    assumption: 'Operational failures\u2014errors, delays, unresolved issues\u2014erode trust independently of investment outcomes and compound with each occurrence.',
  },
  {
    signal: 'Net flow trend',
    measures: 'Net withdrawals as % of AUM, trailing 6 months',
    brackets: '\u226515% withdrawal \u2192 20; 8\u201314% \u2192 12; 3\u20137% \u2192 5; <3% \u2192 0',
    maxPts: 20,
    assumption: 'Money leaving the account is the most direct behavioral signal of impending departure\u2014clients withdraw assets before formally closing an account.',
  },
  {
    signal: 'Satisfaction survey',
    measures: 'Last score, 1\u201310 scale',
    brackets: '\u22644 \u2192 15; 5\u20136 \u2192 10; 7\u20138 \u2192 4; \u22659 \u2192 0; missing \u2192 8',
    maxPts: 15,
    assumption: 'Self-reported satisfaction is informative despite known biases. Missing survey is penalized at moderate weight because non-response weakly correlates with disengagement.',
  },
];

const FOLLOW_SIGNALS: SignalRow[] = [
  {
    signal: 'Advisor tenure ratio',
    measures: 'Years with this advisor / years with firm',
    brackets: '\u22650.9 \u2192 25; 0.7\u20130.89 \u2192 18; 0.5\u20130.69 \u2192 10; <0.5 \u2192 3',
    maxPts: 25,
    assumption: 'A ratio near 1.0 means the client has never known another advisor at the firm and equates the advisor relationship with the firm relationship. Weighted highest because it captures relationship concentration directly.',
  },
  {
    signal: 'Acquisition origin',
    measures: "Did the household arrive through the advisor's acquired/recruited book?",
    brackets: 'Yes \u2192 20; No \u2192 0',
    maxPts: 20,
    assumption: 'Clients brought in through an advisor\'s prior practice have already demonstrated willingness to follow that advisor across firms. Binary because the historical fact either applies or it doesn\'t.',
  },
  {
    signal: 'Service breadth',
    measures: 'Count of distinct service lines (investments, planning, banking, insurance, trust)',
    brackets: '1 \u2192 15; 2 \u2192 10; 3 \u2192 5; \u22654 \u2192 0',
    maxPts: 15,
    assumption: 'Each additional service line creates a switching cost and a touchpoint with someone other than the primary advisor.',
  },
  {
    signal: 'Firm contacts',
    measures: 'Firm employees the household has interacted with in last 12 months, excluding primary advisor',
    brackets: '0 \u2192 15; 1 \u2192 10; 2 \u2192 5; \u22653 \u2192 0',
    maxPts: 15,
    assumption: 'Multiple firm touchpoints create an independent relationship with the institution. A household that only knows one person at the firm has no separate reason to stay.',
  },
  {
    signal: 'Digital engagement',
    measures: 'Portal logins per month, trailing 6mo average',
    brackets: '<1 \u2192 10; 1\u20133 \u2192 6; 4\u20138 \u2192 3; >8 \u2192 0',
    maxPts: 10,
    assumption: "Active portal use indicates a relationship with the firm's platform and tools, not just the advisor. Weighted lower because portal usage alone is a weaker signal than direct human relationships.",
  },
  {
    signal: 'Communication exclusivity',
    measures: '% of all firm communications routed solely through primary advisor',
    brackets: '\u226585% \u2192 15; 65\u201384% \u2192 10; 40\u201364% \u2192 5; <40% \u2192 0',
    maxPts: 15,
    assumption: 'If the advisor is the sole communication channel, the firm has no independent relationship with the household. The advisor is the firm, functionally.',
  },
];

function SignalTable({ signals }: { signals: SignalRow[] }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '24px' }}>
        <thead>
          <tr>
            <th style={{ ...thStyle, width: '14%' }}>Signal</th>
            <th style={{ ...thStyle, width: '20%' }}>What It Measures</th>
            <th style={{ ...thStyle, width: '22%' }}>Point Brackets</th>
            <th style={{ ...thStyle, width: '4%' }}>Max</th>
            <th style={{ ...thStyle, width: '40%' }}>Assumption</th>
          </tr>
        </thead>
        <tbody>
          {signals.map(s => (
            <tr key={s.signal}>
              <td style={tdSignal}>{s.signal}</td>
              <td style={tdStyle}>{s.measures}</td>
              <td style={{ ...tdStyle, fontFamily: 'monospace', fontSize: '12px' }}>{s.brackets}</td>
              <td style={{ ...tdStyle, textAlign: 'center' }}>{s.maxPts}</td>
              <td style={{ ...tdStyle, fontSize: '12px', lineHeight: 1.5 }}>{s.assumption}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function BandPill({ band }: { band: string }) {
  return (
    <span style={{
      display: 'inline-block',
      backgroundColor: bandColor(band),
      color: bandTextColor(band),
      padding: '2px 8px',
      borderRadius: '9999px',
      fontSize: '11px',
      fontWeight: 600,
      marginRight: '6px',
    }}>
      {band}
    </span>
  );
}

export function ModelView() {
  return (
    <div>
      {/* Calibration disclaimer */}
      <div style={{
        fontSize: '12px',
        color: colors.textMuted,
        marginBottom: '24px',
        padding: '12px 16px',
        backgroundColor: '#f1f5f9',
        borderRadius: '6px',
        lineHeight: 1.6,
      }}>
        All weights in this model are illustrative. In a production system they would be
        calibrated against observed departure outcomes — historical advisor departures and
        the household-level retention results that followed. That data is unavailable in a
        synthetic demo. The weights here encode assumptions about relative signal importance,
        stated explicitly below.
      </div>

      {/* --- Advisor Flight Risk --- */}
      <h2 style={sectionHeader}>Advisor Flight Risk</h2>
      <p style={subHeader}>
        Which advisors are likely to depart in the next 6–12 months?
        Output is a band assignment, not a decimal score.
        Thresholds: <BandPill band="Elevated" /> {'\u2265'}55
        {' '}<BandPill band="Watch" /> 30–54
        {' '}<BandPill band="Stable" /> {'<'}30
        {' '}(internal 0–100 scale, never shown at the individual level).
      </p>
      <SignalTable signals={ADVISOR_SIGNALS} />

      {/* --- Household Baseline Risk --- */}
      <h2 style={sectionHeader}>Household Baseline Risk</h2>
      <p style={subHeader}>
        How likely is this household to leave the firm regardless of what their advisor does?
        Thresholds: <BandPill band="High" /> {'\u2265'}55
        {' '}<BandPill band="Moderate" /> 25–54
        {' '}<BandPill band="Low" /> {'<'}25.
      </p>
      <SignalTable signals={BASELINE_SIGNALS} />

      {/* --- Household Follow Likelihood --- */}
      <h2 style={sectionHeader}>Household Follow Likelihood</h2>
      <p style={subHeader}>
        If this household's advisor departs, how likely are they to follow the advisor rather
        than stay with the firm?
        Thresholds: <BandPill band="High" /> {'\u2265'}55
        {' '}<BandPill band="Moderate" /> 25–54
        {' '}<BandPill band="Low" /> {'<'}25.
      </p>
      <SignalTable signals={FOLLOW_SIGNALS} />

      {/* --- Free-text Sentiment Dictionary --- */}
      <h2 style={sectionHeader}>Free-Text Sentiment Dictionary</h2>
      <p style={subHeader}>
        Used in advisor flight risk scoring. Curated keyword/phrase matching, not ML.
        Points are additive and capped at 20.
      </p>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '24px' }}>
          <thead>
            <tr>
              <th style={{ ...thStyle, width: '15%' }}>Tier</th>
              <th style={{ ...thStyle, width: '10%' }}>Points Each</th>
              <th style={thStyle}>Phrases</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={tdSignal}>High signal</td>
              <td style={{ ...tdStyle, textAlign: 'center' }}>7</td>
              <td style={tdStyle}>
                "exploring options," "recruiter contact," "not feeling valued," "considering leaving," "unhappy with direction"
              </td>
            </tr>
            <tr>
              <td style={tdSignal}>Medium signal</td>
              <td style={{ ...tdStyle, textAlign: 'center' }}>4</td>
              <td style={tdStyle}>
                "frustrated with," "looking at other," "not sure about future here," "comp discussion"
              </td>
            </tr>
            <tr>
              <td style={tdSignal}>Low signal</td>
              <td style={{ ...tdStyle, textAlign: 'center' }}>2</td>
              <td style={tdStyle}>
                "distracted lately," "less engaged," "skipping team meetings"
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* --- Minimum Data Requirements --- */}
      <h2 style={sectionHeader}>Minimum Data Requirements</h2>
      <p style={{ fontSize: '13px', lineHeight: 1.7, marginBottom: '12px' }}>
        A score is produced only when enough signals have reliable data.
        Signals that cannot contribute normally are classified into two categories:
      </p>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '16px' }}>
          <thead>
            <tr>
              <th style={{ ...thStyle, width: '15%' }}>Category</th>
              <th style={thStyle}>Meaning</th>
              <th style={thStyle}>Examples</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={tdSignal}>Missing</td>
              <td style={tdStyle}>No data exists for this signal.</td>
              <td style={tdStyle}>
                No satisfaction survey on file; acquisition origin unknown.
              </td>
            </tr>
            <tr>
              <td style={tdSignal}>Unreliable</td>
              <td style={tdStyle}>Data exists but the underlying quantity is too thin to trust.</td>
              <td style={tdStyle}>
                Tenure ratio computed from less than 1 year of data;
                portal logins of zero that could mean "never set up" rather than "chooses not to use."
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p style={{ fontSize: '13px', lineHeight: 1.7, marginBottom: '8px' }}>
        Both categories count toward a data-sufficiency threshold.
        If more than 2 of 6 signals (follow likelihood) or more than 2 of 5 signals (baseline risk)
        are missing or unreliable, the system outputs <strong>"Insufficient data"</strong> instead
        of a band, with a list stating which signals are absent, which are present but unreliable,
        and why.
      </p>
      <p style={{ fontSize: '13px', lineHeight: 1.7, marginBottom: '24px' }}>
        For advisors, all structured signals are assumed available from firm systems.
        Free-text is optional and scored as 0 when absent.
      </p>

      {/* --- Band threshold note --- */}
      <div style={{
        fontSize: '12px',
        color: colors.textMuted,
        padding: '12px 16px',
        backgroundColor: '#f1f5f9',
        borderRadius: '6px',
        lineHeight: 1.6,
        marginBottom: '24px',
      }}>
        Band thresholds are internal. Numeric scores are never shown at the individual level
        for advisors. Household scores are shown only in the evaluation view for test-case
        verification.
      </div>
    </div>
  );
}
