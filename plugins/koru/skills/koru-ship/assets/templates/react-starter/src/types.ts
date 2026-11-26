import type { ComponentType } from "react";

/** One state Harden defined for a screen. id is the anchor slug: #step-N-state-<id>. */
export type StateDef = { id: string; label: string };

/** Props every screen gets: the state to show, and go() to move to another anchor. */
export type ScreenProps = { state: string; go: (anchor: string) => void };

export type ScreenDef = { step: number; name: string; states: readonly StateDef[]; Component: ComponentType<ScreenProps> };
