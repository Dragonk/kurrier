export function buildCalendarEventAriaLabel(
	title: string,
	startTime: string,
	endTime: string,
) {
	return `${title} — ${startTime}–${endTime}`;
}
