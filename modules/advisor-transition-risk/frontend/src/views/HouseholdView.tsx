import { Advisor, Household, View } from '../types';
import { Breadcrumb } from '../components/Breadcrumb';
import { RiskBand } from '../components/RiskBand';
import { FactorList } from '../components/FactorList';
import { SortableTable, Column } from '../components/SortableTable';
import { colors, formatAum } from '../theme';

const FOLLOW_ORDER: Record<string, number> = {
  High: 0, Moderate: 1, Low: 2, 'Insufficient data': 3,
};

interface Props {
  advisor: Advisor;
  households: Household[];
  allAdvisors: Advisor[];
  onNavigate: (view: View) => void;
}

export function HouseholdView({ advisor, households, allAdvisors, onNavigate }: Props) {
  const view: View = { kind: 'household', advisorId: advisor.advisor_id };

  const columns: Column<Household>[] = [
    {
      key: 'name',
      header: 'Household',
      render: h => <span style={{ fontWeight: 500 }}>{h.name}</span>,
      sortValue: h => h.name,
      width: '15%',
    },
    {
      key: 'aum',
      header: 'AUM',
      render: h => formatAum(h.aum),
      sortValue: h => h.aum,
      width: '10%',
    },
    {
      key: 'follow',
      header: 'Follow Likelihood',
      render: h => (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <RiskBand band={h.follow_likelihood_band} size="sm" />
          <FactorList
            factors={h.follow_likelihood_factors}
            missingSignals={h.follow_missing_signals}
          />
        </div>
      ),
      sortValue: h => (FOLLOW_ORDER[h.follow_likelihood_band] ?? 4) * 1e12 - h.aum,
      width: '37%',
    },
    {
      key: 'baseline',
      header: 'Baseline Risk',
      render: h => (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <RiskBand band={h.baseline_risk_band} size="sm" />
          <FactorList
            factors={h.baseline_risk_factors}
            missingSignals={h.baseline_missing_signals}
          />
        </div>
      ),
      sortValue: h => (FOLLOW_ORDER[h.baseline_risk_band] ?? 4) * 1e12 - h.aum,
      width: '37%',
    },
  ];

  return (
    <div>
      <Breadcrumb view={view} advisors={allAdvisors} onNavigate={onNavigate} />

      <p style={{
        fontSize: '15px',
        color: colors.textMuted,
        fontStyle: 'italic',
        margin: '0 0 16px 0',
      }}>
        If {advisor.name} departs, which households need proactive outreach?
      </p>

      <div style={{
        display: 'flex',
        gap: '24px',
        padding: '16px',
        backgroundColor: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: '8px',
        marginBottom: '16px',
        flexWrap: 'wrap',
      }}>
        <div>
          <div style={{ fontSize: '11px', color: colors.textMuted, textTransform: 'uppercase' }}>Advisor</div>
          <div style={{ fontWeight: 600, fontSize: '16px' }}>{advisor.name}</div>
          <RiskBand band={advisor.flight_risk_band} size="sm" />
        </div>
        <div>
          <div style={{ fontSize: '11px', color: colors.textMuted, textTransform: 'uppercase' }}>Book AUM</div>
          <div style={{ fontWeight: 600, fontSize: '16px' }}>{formatAum(advisor.book_aum)}</div>
        </div>
        <div>
          <div style={{ fontSize: '11px', color: colors.textMuted, textTransform: 'uppercase' }}>Exposed AUM</div>
          <div style={{ fontWeight: 600, fontSize: '16px' }}>{formatAum(advisor.exposed_aum)}</div>
        </div>
        <div>
          <div style={{ fontSize: '11px', color: colors.textMuted, textTransform: 'uppercase' }}>Concentration</div>
          <div style={{ fontWeight: 600, fontSize: '16px' }}>{advisor.concentration_pct.toFixed(1)}%</div>
        </div>
        {advisor.has_unscored_households && (
          <div style={{
            fontSize: '12px',
            color: colors.textMuted,
            alignSelf: 'center',
            fontStyle: 'italic',
          }}>
            {advisor.unscored_count} household{advisor.unscored_count > 1 ? 's' : ''} ({formatAum(advisor.unscored_aum)} AUM)
            could not be scored for follow likelihood due to insufficient data.
          </div>
        )}
      </div>

      <div style={{
        fontSize: '12px',
        color: colors.textMuted,
        marginBottom: '12px',
        padding: '10px 14px',
        backgroundColor: '#f1f5f9',
        borderRadius: '6px',
        lineHeight: 1.5,
      }}>
        The two-score model implies different interventions, not just different levels of attention.
        <strong> High follow / Low baseline</strong> calls for building a second firm relationship
        before any departure occurs.
        <strong> Low follow / High baseline</strong> is a fee, performance, or service problem
        that a retention play aimed at the advisor relationship would not address.
      </div>

      <SortableTable
        columns={columns}
        data={households}
        defaultSortKey="follow"
        defaultSortDir="asc"
      />
    </div>
  );
}
