// koru-anchor: #step-1
// Replace this example with the first screen from the HTML deliverable. Keep the anchor comment, the
// screen name from scope, and one entry in `states` for every state Harden defined (ids as in the anchors).
import type { ScreenProps } from "../types";
import { sample } from "../data/sample";

export const name = "Example screen";
export const states = [
  { id: "empty", label: "Empty" },
  { id: "loading", label: "Loading" },
  { id: "error", label: "Error" },
  { id: "success", label: "Success" },
] as const;

export default function Step1Example({ state, go }: ScreenProps) {
  if (state === "loading") return <p role="status">Loading items</p>;
  if (state === "error")
    return (
      <div role="alert" className="banner banner-error">
        <p>The items didn't load. Try again.</p>
        <button type="button" className="btn">
          Try again
        </button>
      </div>
    );
  if (state === "empty") return <p>No items yet.</p>;
  return (
    <div>
      <ul>
        {sample.items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
      <button type="button" className="btn btn-primary" onClick={() => go("#step-2")}>
        Continue
      </button>
    </div>
  );
}
