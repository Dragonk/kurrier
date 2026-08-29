import assert from "node:assert/strict";
import { getCalendarEventInstanceKey } from "../apps/web/lib/calendar-event-identity";

assert.equal(
	getCalendarEventInstanceKey({
		id: "event-1",
		instanceId: "event-1:2026-09-01",
	}),
	"event-1:2026-09-01",
);
assert.equal(getCalendarEventInstanceKey({ id: "event-1" }), "event-1");
assert.equal(getCalendarEventInstanceKey(undefined), "");

console.log("Calendar event identity checks passed.");
