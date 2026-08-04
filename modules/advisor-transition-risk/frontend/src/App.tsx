import { useState, useEffect } from 'react';
import { AppData, View } from './types';
import { colors } from './theme';
import { SyntheticBanner } from './components/SyntheticBanner';
import { AdvisorListView } from './views/AdvisorListView';
import { HouseholdView } from './views/HouseholdView';
import { TransitionView } from './views/TransitionView';
import { EvaluationView } from './views/EvaluationView';
import { ModelView } from './views/ModelView';

export function App() {
  const [data, setData] = useState<AppData | null>(null);
  const [view, setView] = useState<View>({ kind: 'advisor-list' });
  const [activeTab, setActiveTab] = useState<'cascade' | 'model' | 'evaluation'>('cascade');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(import.meta.env.BASE_URL + 'data.json')
      .then(r => {
        if (!r.ok) throw new Error(`Failed to load data: ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch(e => setError(e.message));
  }, []);

  if (error) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#991b1b' }}>
        {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: colors.textMuted }}>
        Loading...
      </div>
    );
  }

  const handleNavigate = (v: View) => {
    setView(v);
    setActiveTab('cascade');
  };

  const renderView = () => {
    if (activeTab === 'model') {
      return <ModelView />;
    }

    if (activeTab === 'evaluation') {
      return <EvaluationView cases={data.evaluation_cases} />;
    }

    switch (view.kind) {
      case 'advisor-list':
        return (
          <AdvisorListView
            advisors={data.advisors}
            onNavigate={handleNavigate}
          />
        );

      case 'household': {
        const advisor = data.advisors.find(a => a.advisor_id === view.advisorId);
        if (!advisor) return <div>Advisor not found</div>;
        const households = data.households.filter(
          h => h.advisor_id === view.advisorId
        );
        return (
          <HouseholdView
            advisor={advisor}
            households={households}
            allAdvisors={data.advisors}
            onNavigate={handleNavigate}
          />
        );
      }

      case 'transition': {
        const advisor = data.advisors.find(a => a.advisor_id === view.advisorId);
        if (!advisor) return <div>Advisor not found</div>;
        const entries = data.transition_entries.filter(
          e => e.advisor_id === view.advisorId
        );
        const households = data.households.filter(
          h => h.advisor_id === view.advisorId
        );
        return (
          <TransitionView
            advisor={advisor}
            entries={entries}
            households={households}
            allAdvisors={data.advisors}
            onNavigate={handleNavigate}
          />
        );
      }

      default:
        return null;
    }
  };

  return (
    <div style={{
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      color: colors.text,
      backgroundColor: colors.bg,
      minHeight: '100vh',
    }}>
      <SyntheticBanner />

      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '0 24px',
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          alignItems: 'baseline',
          justifyContent: 'space-between',
          padding: '20px 0 12px',
          borderBottom: `1px solid ${colors.border}`,
          marginBottom: '20px',
        }}>
          <h1 style={{
            fontSize: '20px',
            fontWeight: 700,
            margin: 0,
            color: colors.text,
          }}>
            Advisor Transition Risk
          </h1>

          <div style={{ display: 'flex', gap: '4px' }}>
            <button
              onClick={() => {
                setActiveTab('cascade');
                setView({ kind: 'advisor-list' });
              }}
              style={{
                padding: '6px 16px',
                border: `1px solid ${colors.border}`,
                borderRadius: '6px',
                backgroundColor: activeTab === 'cascade' ? colors.elevated : colors.surface,
                color: activeTab === 'cascade' ? '#ffffff' : colors.text,
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: 500,
              }}
            >
              Cascade
            </button>
            <button
              onClick={() => setActiveTab('model')}
              style={{
                padding: '6px 16px',
                border: `1px solid ${colors.border}`,
                borderRadius: '6px',
                backgroundColor: activeTab === 'model' ? colors.elevated : colors.surface,
                color: activeTab === 'model' ? '#ffffff' : colors.text,
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: 500,
              }}
            >
              Model / Definitions
            </button>
            <button
              onClick={() => setActiveTab('evaluation')}
              style={{
                padding: '6px 16px',
                border: `1px solid ${colors.border}`,
                borderRadius: '6px',
                backgroundColor: activeTab === 'evaluation' ? colors.elevated : colors.surface,
                color: activeTab === 'evaluation' ? '#ffffff' : colors.text,
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: 500,
              }}
            >
              Test Results
            </button>
          </div>
        </div>

        {activeTab === 'cascade' && (
          <p style={{
            fontSize: '15px',
            fontWeight: 500,
            color: colors.text,
            margin: '0 0 16px 0',
            lineHeight: 1.5,
          }}>
            When an advisor leaves, some clients leave too. This traces that
            cascade — from advisor risk, to the households exposed, to what the
            transition recovered.
          </p>
        )}

        {renderView()}

        {/* Footer */}
        <div style={{
          padding: '24px 0',
          marginTop: '40px',
          borderTop: `1px solid ${colors.border}`,
          fontSize: '11px',
          color: colors.textMuted,
          textAlign: 'center',
        }}>
          Synthetic data generated {data.metadata.generated} &mdash;{' '}
          {data.metadata.advisor_count} advisors, {data.metadata.household_count} households
        </div>
      </div>
    </div>
  );
}
