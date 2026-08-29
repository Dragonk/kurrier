type CalendarEventIdentity = {
	id: string;
	instanceId?: string | null;
};

export function getCalendarEventInstanceKey(
	event: CalendarEventIdentity | undefined,
) {
	return event?.instanceId ?? event?.id ?? "";
}
