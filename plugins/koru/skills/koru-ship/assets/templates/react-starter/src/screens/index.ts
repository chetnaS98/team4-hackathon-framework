import type { ScreenDef } from "../types";
import Step1, { name as name1, states as states1 } from "./Step1Example";

// One entry per screen in journey order, one component file per screen (Step<N><Name>.tsx).
export const screens: ScreenDef[] = [{ step: 1, name: name1, states: states1, Component: Step1 }];
