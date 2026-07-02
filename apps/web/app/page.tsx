"use client";

import { useEffect, useState } from 'react';
import { appConfig } from '@/app/config';
import { getBackendHealth, getBackendVersion } from '@/lib/api';

type StatusState = {
  state: 'loading' | 'success' | 'error';
  detail?: string;
};

function StatusBadge({ status }: { status: StatusState }) {
  const label = status.state === 'loading' ? 'Loading' : status.state === 'success' ? 'Healthy' : 'Error';
  return <span className={`badge ${status.state}`}>{label}</span>;
}

export default function HomePage() {
  const [health, setHealth] = useState<StatusState>({ state: 'loading' });
  const [version, setVersion] = useState<StatusState>({ state: 'loading' });

  useEffect(() => {
    let active = true;

    async function loadStatus() {
      try {
        const healthResponse = await getBackendHealth(appConfig.backendBaseUrl);
        if (!active) return;
        setHealth({ state: 'success', detail: healthResponse.status });
      } catch (error) {
        if (!active) return;
        setHealth({ state: 'error', detail: error instanceof Error ? error.message : 'Unknown error' });
      }

      try {
        const versionResponse = await getBackendVersion(appConfig.backendBaseUrl);
        if (!active) return;
        setVersion({ state: 'success', detail: versionResponse.version });
      } catch (error) {
        if (!active) return;
        setVersion({ state: 'error', detail: error instanceof Error ? error.message : 'Unknown error' });
      }
    }

    loadStatus();
    return () => {
      active = false;
    };
  }, []);

  return (
    <main>
      <section className="card">
        <h1>Garuda OS</h1>
        <p>The first frontend shell for Garuda.</p>
      </section>

      <section className="grid">
        <div className="card">
          <h2>Application</h2>
          <p>Version: {appConfig.appVersion}</p>
          <p>Environment: {appConfig.environment}</p>
        </div>

        <div className="card">
          <h2>Backend</h2>
          <p>Health: <StatusBadge status={health} /></p>
          {health.detail ? <p>{health.detail}</p> : null}
          <p>Version: <StatusBadge status={version} /></p>
          {version.detail ? <p>{version.detail}</p> : null}
          <p>Connected backend: {appConfig.backendBaseUrl}</p>
        </div>

        <div className="card">
          <h2>Architecture</h2>
          <p>Architecture version: {appConfig.architectureVersion}</p>
          <p>Sprint version: {appConfig.sprintVersion}</p>
        </div>
      </section>
    </main>
  );
}
