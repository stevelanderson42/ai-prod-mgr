import { Advisor, View } from '../types';
import { RiskBand } from '../components/RiskBand';
import { FactorList } from '../components/FactorList';
import { SortableTable, Column } from '../components/SortableTable';
import { colors, formatAum, bandColor } from '../theme';

const BAND_ORDER: Record<string, number> = { Elevated: 0, Watch: 1, Stable: 2 };

interface Props {
  advisors: Advisor[];
  onNavigate: (view: View) => void;
}

export function AdvisorListView({ advisors, onNavigate }: Props) {
  // Scale concentration bar to observed max so the contrast is visible
  const maxConcentration = Math.max(...advisors.map(a => a.concentration_pct), 1);

  const columns: Column<Advisor>[] = [
    {
      key: 'name',
      header: 'Advisor',
      render: a => (
        <div>
          <div style={{ fontWeight: 500 }}>{a.name}</div>
          <div style={{ fontSize: '11px', color: colors.textMuted }}>{a.team}</div>
        </div>
      ),
      sortValue: a => a.name,
      width: '14%',
    },
    {
      key: 'band',
      header: 'Risk Band',
      render: a => <RiskBand band={a.flight_risk_band} />,
      sortValue: a => BAND_ORDER[a.flight_risk_band] ?? 3,
      width: '9%',
    },
    {
      key: 'factors',
      header: 'Top Factors',
      render: a => (
        <FactorList
          factors={a.flight_risk_factors}
          showNoteDisclaimer={true}
        />
      ),
      width: '28%',
    },
    {
      key: 'book_aum',
      header: 'Book AUM',
      tooltip: 'Total AUM across all assigned households.',
      render: a => formatAum(a.book_aum),
      sortValue: a => a.book_aum,
      width: '9%',
    },
    {
      key: 'exposed_aum',
      header: 'Exposed AUM',
      tooltip: 'AUM in households scored High follow likelihood.',
      render: a => formatAum(a.exposed_aum),
      sortValue: a => a.exposed_aum,
      width: '10%',
    },
    {
      key: 'concentration',
      header: 'Concentration',
      tooltip: 'Share of book AUM in households scored High follow likelihood. Unscored households are excluded from the numerator but included in the denominator.',
      render: a => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '60px',
            height: '8px',
            backgroundColor: colors.border,
            borderRadius: '4px',
            overflow: 'hidden',
          }}>
            <div style={{
              width: `${(a.concentration_pct / maxConcentration) * 100}%`,
              height: '100%',
              backgroundColor: bandColor(a.flight_risk_band),
              borderRadius: '4px',
            }} />
          </div>
          <span style={{ fontSize: '12px', fontWeight: 500 }}>
            {a.concentration_pct.toFixed(1)}%
          </span>
        </div>
      ),
      sortValue: a => a.concentration_pct,
      width: '12%',
    },
    {
      key: 'households',
      header: 'Households',
      render: a => {
        return (
          <div>
            <div>{a.household_count}</div>
            {a.has_unscored_households && (
              <div style={{ fontSize: '11px', color: colors.textMuted }}>
                {a.unscored_count} unscored
              </div>
            )}
          </div>
        );
      },
      sortValue: a => a.household_count,
      width: '6%',
    },
    {
      key: 'status',
      header: 'Status',
      render: a => (
        <div>
          <div style={{ fontSize: '12px' }}>
            {a.status === 'departed' ? 'Departed' : 'Active'}
          </div>
          {a.score_as_of_date && (
            <div style={{ fontSize: '11px', color: colors.textMuted }}>
              Score as of {a.score_as_of_date}
            </div>
          )}
        </div>
      ),
      sortValue: a => a.status === 'departed' ? 0 : 1,
      width: '12%',
    },
  ];

  const handleClick = (a: Advisor) => {
    if (a.status === 'departed') {
      onNavigate({ kind: 'transition', advisorId: a.advisor_id });
    } else {
      onNavigate({ kind: 'household', advisorId: a.advisor_id });
    }
  };

  return (
    <div>
      <p style={{
        fontSize: '15px',
        color: colors.textMuted,
        fontStyle: 'italic',
        margin: '0 0 16px 0',
      }}>
        Which advisor departures would create the largest client exposure?
      </p>
      <SortableTable
        columns={columns}
        data={advisors}
        defaultSortKey="band"
        defaultSortDir="asc"
        onRowClick={handleClick}
      />
    </div>
  );
}
