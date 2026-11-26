import { useEffect, useState } from "react";
import { screens } from "./screens";

// Same anchors as the HTML deliverable (#step-N, #step-N-state-<state>), so tickets link both.
function parse(hash: string) {
  const m = /^#step-(\d+)(?:-state-([a-z0-9-]+))?$/.exec(hash);
  const step = screens.find((s) => m !== null && s.step === Number(m[1])) ?? screens[0];
  const state =
    step.states.find((s) => m !== null && s.id === m[2]) ??
    step.states.find((s) => s.id === "success") ??
    step.states[0];
  return { step, state };
}

export default function App() {
  const [hash, setHash] = useState(window.location.hash);
  useEffect(() => {
    const onChange = () => setHash(window.location.hash);
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  const { step, state } = parse(hash);
  const go = (anchor: string) => {
    window.location.hash = anchor;
  };
  const Screen = step.Component;

  return (
    <div className="layout">
      <nav id="state-switcher" aria-label="Steps and states">
        <ol>
          {screens.map((s) => (
            <li key={s.step}>
              <a href={`#step-${s.step}`}>
                Step {s.step}: {s.name}
              </a>
              <ul>
                {s.states.map((st) => (
                  <li key={st.id}>
                    <a
                      href={`#step-${s.step}-state-${st.id}`}
                      aria-current={s === step && st === state ? "true" : undefined}
                    >
                      {st.label}
                    </a>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ol>
      </nav>
      <main>
        <p className="sample-note">Sample data. A reference starter from Ship, not production code.</p>
        <section id={`step-${step.step}`} aria-labelledby="screen-title">
          <h1 id="screen-title">
            Step {step.step}: {step.name}
          </h1>
          <p className="state-label">State: {state.label}</p>
          <Screen state={state.id} go={go} />
        </section>
      </main>
    </div>
  );
}
