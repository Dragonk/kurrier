import assert from "node:assert/strict";
import { buildCalendarEventAriaLabel } from "../apps/web/lib/calendar-event-accessibility";

assert.equal(
	buildCalendarEventAriaLabel("Team sync", "09:00", "10:30"),
	"Team sync — 09:00–10:30",
);
assert.equal(
	buildCalendarEventAriaLabel("All-day event", "00:00", "23:59"),
	"All-day event — 00:00–23:59",
);

console.log("Calendar event accessibility label checks passed.");
